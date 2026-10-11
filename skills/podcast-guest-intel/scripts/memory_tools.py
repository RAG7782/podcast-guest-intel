#!/usr/bin/env python3
"""Memória / centro de comando do show (F6, task *memoria). Roda local: os dados ficam no computador do usuário.

Arquivos = fonte da verdade; índice SQLite FTS5 = cache (`reindex` reconstrói). A mesma lógica
(memory_store/index/ops/privacy/md) é a que o MCP remoto/SaaS vai expor depois.

  init       WS --show-ref ID [--retention-days N]
  new        WS EP [--title T] [--status S] [--series S] [--theme T]... [--guest G]...
  add        WS EP --type intake|dossier|pauta|script|research|decision ARQ.json
  add        WS EP --type recording|transcript|edit --ref CAMINHO_OU_URL [--duration-s N] [--platform P]
  status     WS EP [--to STATUS] [--gate APPROVE|REQUEST_CHANGES|HOLD] [--by QUEM] [--decision ARQ.json]
  lessons    WS EP [--lesson TEXTO]... [--metric k=v]... [--clip-url URL --clip-platform P
             [--clip-posted-at ISO] [--clip-metric k=v]... [--clip-duration-s N] [--clip-title T]]
  search     WS CONSULTA [--type K] [--guest G] [--theme T] [--since AAAA-MM-DD] [--until ...] [--limit N] [--json]
  catalog    WS [-o SAIDA.json] [--include-archived]     formato que pauta_tools --catalog lê
  import-catalog WS ARQ.json                              lista {id, titulo, serie, temas, data, convidados, ...}
  suggest    WS [--today AAAA-MM-DD] [--json]
  forget     WS --subject ID [--name NOME]... [--confirm ID --decided-by QUEM]   sem --confirm = relatório
  retention  WS (--dry-run | --apply) [--today AAAA-MM-DD]
  export-md  WS --out DIR [--episode EP]...
  import-md  WS --vault DIR --opt-in
  reindex    WS

`add` de artefato JSON, `status --decision` e `import-catalog` validam contra references/contracts/ (jsonschema
+ pyyaml): uv run --no-project -q --with jsonschema --with pyyaml python scripts/memory_tools.py ...
search/catalog/suggest/export-md/import-md/forget/retention/reindex são stdlib.

Plano pago (capacidade memoria-centro-de-comando): os comandos conferem a chave de licença
(scripts/licenca.py). forget, retention e export-md ficam livres: apagar a pedido do titular, cumprir a
retenção prometida e levar os próprios dados embora não dependem de assinatura (LGPD arts. 16 e 18).
"""
import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import memory_index as mi  # noqa: E402
import memory_md as md  # noqa: E402
import memory_ops as ops  # noqa: E402
import memory_privacy as priv  # noqa: E402
import memory_store as ms  # noqa: E402
import licenca  # noqa: E402


def emit(obj, as_json=True):
    print(json.dumps(obj, ensure_ascii=False, indent=2) if as_json else obj)


def kv_pairs(items):
    out = {}
    for item in items or []:
        key, sep, value = item.partition("=")
        try:
            if not sep or not key.strip():
                raise ValueError(item)
            out[key.strip()] = float(value) if "." in value else int(value)
        except ValueError:
            raise ms.MemoryError_(f"métrica={item!r} | esperado: chave=número (ex.: views=120)")
    return out


def as_day(text):
    return date.fromisoformat(text) if text else None


# ── comandos ─────────────────────────────────────────────────────────────

def cmd_init(a):
    emit(ms.init_workspace(a.ws, a.show_ref, a.retention_days))


def cmd_new(a):
    rec = ms.new_record(a.ws, a.episode, a.title or "", a.status, series_ref=a.series,
                        themes=a.theme, guest_refs=a.guest)
    mi.rebuild(a.ws)
    emit({"criado": rec["episode_id"], "status": rec["status"]})


def cmd_add(a):
    if a.type in ms.MEDIA:
        if not a.ref:
            raise ms.MemoryError_(f"--type {a.type} sem --ref | esperado: caminho ou URL da mídia")
        rec = ms.add_media(a.ws, a.episode, a.type, ms.media_ref(a.ref, a.duration_s, a.platform))
        ref = a.ref
    else:
        if not a.file:
            raise ms.MemoryError_(f"--type {a.type} sem ARQ.json | esperado: caminho do artefato")
        rec, ref = ms.add_artifact(a.ws, a.episode, a.type, ms.read_json(a.file))
    mi.rebuild(a.ws)
    emit({"episodio": rec["episode_id"], "tipo": a.type, "ref": ref, "artifacts": sorted(rec["artifacts"])})


def cmd_status(a):
    out = {}
    if a.gate:
        out["gate"] = ops.set_gate(a.ws, a.episode, a.gate, a.by)["gate"]
    if a.to:
        decision = ms.read_json(a.decision) if a.decision else None
        rec, alerts = ops.change_status(a.ws, a.episode, a.to, a.by, decision)
        out.update({"status": rec["status"], "alertas_aceitos": [x["code"] for x in alerts]})
    if not out:
        rec = ms.load_record(a.ws, a.episode)
        out = {"status": rec["status"], "gate": rec.get("gate"), "history": rec.get("history", [])}
    mi.rebuild(a.ws)
    emit(out)


def clip_of(a):
    if not a.clip_url:
        return None
    if not a.clip_platform:
        raise ms.MemoryError_(f"--clip-url {a.clip_url!r} sem --clip-platform | esperado: plataforma do corte")
    clip = {"platform": a.clip_platform, "url": a.clip_url, "posted_at": a.clip_posted_at,
            "metrics": kv_pairs(a.clip_metric) or None, "duration_s": a.clip_duration_s, "title": a.clip_title}
    return {k: v for k, v in clip.items() if v is not None}


def cmd_lessons(a):
    rec = ops.add_lessons(a.ws, a.episode, a.lesson or [], kv_pairs(a.metric), clip_of(a))
    mi.rebuild(a.ws)
    emit({"lessons": rec.get("lessons", []), "metrics": rec.get("metrics", {}),
          "clips": len(rec["artifacts"].get("clips", []))})


def cmd_search(a):
    hits = mi.search(a.ws, a.query, a.limit, kind=a.type, guest=a.guest, theme=a.theme, since=a.since, until=a.until)
    if a.json:
        return emit(hits)
    print(f"{len(hits)} resultado(s) para {a.query!r}")
    for h in hits:
        print(f"- [{h['kind']}] {h['episode_id'] or '(nota)'} {h['date']} · {h['title'][:70]}\n    {h['snippet']}")


def cmd_catalog(a):
    rows = ops.catalog(a.ws, a.include_archived)
    if a.output:
        ms.write_json(a.output, rows)
        print(f"{len(rows)} episódio(s) -> {a.output}")
    else:
        emit(rows)


def cmd_import_catalog(a):
    doc = ms.read_json(a.file)
    entries = doc.get("episodes", doc) if isinstance(doc, dict) else doc
    ids = ops.import_catalog(a.ws, entries)
    emit({"importados": len(ids), "documentos_indexados": mi.rebuild(a.ws)})


def cmd_suggest(a):
    out = ops.suggest(a.ws, as_day(a.today))
    if a.json:
        return emit(out)
    for group, items in out.items():
        print(f"## {group} ({len(items)})")
        for s in items:
            print(f"- {s['title']}\n    regra {s['rule']}: {s['why']}\n    evidência: {', '.join(s['evidence'])}")


def cmd_forget(a):
    report = priv.forget(a.ws, a.subject, a.name or [], a.confirm, a.decided_by)
    emit(report)
    if not report["aplicado"]:
        print("DRY-RUN: nada foi apagado. Para aplicar: --confirm <subject> --decided-by <quem decidiu>",
              file=sys.stderr)
    res = report.get("residuo") or {}
    return 1 if res.get("busca_hits") or res.get("arquivos_com_mencao") else 0


def cmd_retention(a):
    out = priv.retention(a.ws, as_day(a.today), apply=a.apply)
    emit({"aplicado": a.apply, "episodios": out})


def cmd_export_md(a):
    files = md.export_md(a.ws, a.out, a.episode)
    print(f"{len(files)} nota(s) em {a.out}")


def cmd_import_md(a):
    out = md.import_md(a.ws, a.vault, a.opt_in)
    out["documentos_indexados"] = mi.rebuild(a.ws)
    emit(out)


def cmd_reindex(a):
    print(f"índice reconstruído: {mi.rebuild(a.ws)} documento(s) em {mi.index_path(a.ws)}")


# ── parser ───────────────────────────────────────────────────────────────

def subcmd(sub, name):
    """Subcomando com o workspace como 1º posicional e a função cmd_<nome> ligada."""
    p = sub.add_parser(name)
    p.add_argument("ws", help="pasta do workspace da memória")
    p.set_defaults(func=globals()["cmd_" + name.replace("-", "_")])
    return p


def add_episode_cmds(sub):
    p = subcmd(sub, "init")
    p.add_argument("--show-ref", required=True)
    p.add_argument("--retention-days", type=int)
    p = subcmd(sub, "new")
    p.add_argument("episode")
    p.add_argument("--title")
    p.add_argument("--status", default="idea", choices=ms.STATUSES)
    p.add_argument("--series")
    p.add_argument("--theme", action="append")
    p.add_argument("--guest", action="append")
    p = subcmd(sub, "add")
    p.add_argument("episode")
    p.add_argument("file", nargs="?")
    p.add_argument("--type", required=True, choices=sorted(ms.TYPES) + sorted(ms.MEDIA))
    p.add_argument("--ref")
    p.add_argument("--duration-s", type=float)
    p.add_argument("--platform")
    p = subcmd(sub, "status")
    p.add_argument("episode")
    p.add_argument("--to", choices=ms.STATUSES)
    p.add_argument("--gate", choices=ops.GATE_VERDICTS)
    p.add_argument("--by")
    p.add_argument("--decision")


def add_lessons_cmd(sub):
    p = subcmd(sub, "lessons")
    p.add_argument("episode")
    p.add_argument("--lesson", action="append")
    p.add_argument("--metric", action="append")
    for opt in ("--clip-url", "--clip-platform", "--clip-posted-at", "--clip-title"):
        p.add_argument(opt)
    p.add_argument("--clip-metric", action="append")
    p.add_argument("--clip-duration-s", type=float)


def add_query_cmds(sub):
    p = subcmd(sub, "search")
    p.add_argument("query")
    for opt in ("--type", "--guest", "--theme", "--since", "--until"):
        p.add_argument(opt)
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--json", action="store_true")
    p = subcmd(sub, "catalog")
    p.add_argument("-o", "--output")
    p.add_argument("--include-archived", action="store_true")
    p = subcmd(sub, "import-catalog")
    p.add_argument("file")
    p = subcmd(sub, "suggest")
    p.add_argument("--today")
    p.add_argument("--json", action="store_true")


def add_privacy_cmds(sub):
    p = subcmd(sub, "forget")
    p.add_argument("--subject", required=True)
    p.add_argument("--name", action="append", help="forma extra; nome, nome de tratamento e @ do intake já entram")
    p.add_argument("--confirm")
    p.add_argument("--decided-by")
    p = subcmd(sub, "retention")
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    p.add_argument("--today")
    p = subcmd(sub, "export-md")
    p.add_argument("--out", required=True)
    p.add_argument("--episode", action="append")
    p = subcmd(sub, "import-md")
    p.add_argument("--vault", required=True)
    p.add_argument("--opt-in", action="store_true")
    subcmd(sub, "reindex")


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    for add in (add_episode_cmds, add_lessons_cmd, add_query_cmds, add_privacy_cmds):
        add(sub)
    return parser


AUTO_RETENTION_SKIP = ("init", "retention", "forget")
LICENSE_FREE = ("forget", "retention", "export-md")   # dever legal e portabilidade: nunca atrás da licença


def auto_retention(args):
    """Retenção prometida ao convidado ligada por padrão (ALQERA PRV-001): todo comando num workspace
    aplica o que venceu. memory.json com auto_retention=false desliga e passa a só avisar."""
    ws = getattr(args, "ws", None)
    if args.cmd in AUTO_RETENTION_SKIP or not ws or not (Path(ws) / ms.CONFIG).is_file():
        return
    on = ms.config(ws).get("auto_retention", True) is not False
    due = priv.retention(ws, apply=on)
    if due and on:
        print(f"retenção automática: {len(due)} episódio(s) vencido(s) aplicados {[d['episode_id'] for d in due]}",
              file=sys.stderr)
    elif due:
        print(f"AVISO: {len(due)} episódio(s) com retenção vencida e auto_retention=false: rode"
              " `retention --apply`", file=sys.stderr)


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        auto_retention(args)   # antes do gate: a retenção prometida roda mesmo sem licença
        if args.cmd not in LICENSE_FREE:
            licenca.exigir("memoria-centro-de-comando")
        return args.func(args) or 0
    except ms.MemoryError_ as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
