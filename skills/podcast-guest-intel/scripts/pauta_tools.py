#!/usr/bin/env python3
"""Ferramentas determinísticas da pauta (task *pauta): 3 troncos no repo e no servidor; editorial no pacote local.

Subcomandos:
  build  --dossier --host-profile --show-profile --catalog --trends --episode-ref --pauta-id
         --approach-mode --format [--intake] [--max-items N] [-o SAIDA.json]
         monta o ESQUELETO do envelope {pauta, fontes_usadas, confianca, removidos}: candidatos
         ancorados por tronco, score por sobreposição de termos, tetos de confiança, filtro de
         off_limits. A curadoria final (cortar, reescrever título, perguntas) é do agente.
  check  ARQ [--dossier --catalog --trends --show-profile --host-profile --intake]
         schema + regras cruzadas; sai 1 se houver violação. Regra sem a entrada que ela
         precisa é PULADA e contada no denominador.
  render ARQ [-o SAIDA.md]   envelope -> markdown para o host.

`build` e `render` são stdlib; `check` reusa scripts/validate-contracts.py (jsonschema + pyyaml).
Catálogo: lista de episode-records ({episode_id, title, series_ref}) ou de entradas de catálogo
({id, titulo, serie, temas}); os dois formatos são aceitos.
"""
import argparse
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dossier_tools import load_json, load_validator, split_envelope as split_dossier  # noqa: E402

import paths  # noqa: E402
TRUNKS = ("trend", "continuity", "editorial")
DEFAULT_MAX = 5
DEGRADED_CAP = 0.7   # item com claim_ids quando o dossiê veio degradado
DRAFT_CAP = 0.8      # item do tronco editorial quando o host-profile é draft
ENVELOPE_KEYS = ["pauta", "fontes_usadas", "confianca", "removidos"]
STOP = {"para", "como", "mais", "sobre", "entre", "pela", "pelo", "pelos", "pelas", "esse", "essa",
        "isso", "este", "esta", "ainda", "quem", "onde", "quando", "porque", "pode", "podem", "fazer",
        "episodio", "podcast", "parte", "real", "voce", "precisa", "saber", "nova", "novo", "forma"}


# ── texto ─────────────────────────────────────────────────────────────────

def norm(text):
    raw = unicodedata.normalize("NFKD", str(text or "")).encode("ascii", "ignore").decode()
    return raw.lower()


def tokens(*texts):
    """Termos de >=4 letras, sem acento, sem stopwords."""
    words = re.findall(r"[a-z0-9]+", norm(" ".join(str(t) for t in texts)))
    return {w for w in words if len(w) >= 4 and w not in STOP}


def short_title(title):
    return str(title or "").split(" | ")[0].strip()


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ── entradas normalizadas ─────────────────────────────────────────────────

def episodes_of(catalog):
    items = catalog.get("episodes", []) if isinstance(catalog, dict) else catalog or []
    return [{"id": e.get("episode_id") or e.get("id"), "title": e.get("title") or e.get("titulo") or "",
             "series": e.get("series_ref") or e.get("serie") or "", "themes": e.get("temas") or []}
            for e in items if isinstance(e, dict)]


def usable_claims(dossier):
    """Claims que podem ancorar item: dado sensível nunca vira gancho (manifesto, proibição 6)."""
    return [c for c in dossier.get("claims") or [] if isinstance(c, dict) and not c.get("sensitive")]


def profile_terms(show, host):
    return tokens(show.get("editorial_line"), *(show.get("pillars") or []), *(show.get("covers") or []),
                  *(host.get("recurring_themes") or []), *(host.get("open_gaps") or []))


def off_limits(show, intake):
    return [t for t in (show.get("does_not_cover") or []) + ((intake or {}).get("off_limits_topics") or [])
            if str(t).strip()]


def resolve_max(arg, show):
    value = arg or show.get("pauta_max_items_per_trunk") or DEFAULT_MAX
    if not 1 <= int(value) <= 10:
        raise SystemExit(f"max_items_per_trunk={value} | esperado: inteiro de 1 a 10 (default 5)")
    return int(value)


# ── candidatos ────────────────────────────────────────────────────────────

def claim_hits(text_terms, claims, min_overlap=2):
    """Claims que dividem >=2 termos com o texto (1 termo genérico, tipo 'direito', não ancora)."""
    return [c["id"] for c in claims if len(text_terms & tokens(c.get("text"))) >= min_overlap]


def candidate(title, rationale, score, **anchors):
    item = {"title": title, "rationale": rationale, "score": round(min(score, 1.0), 2)}
    item.update({k: v for k, v in anchors.items() if v})
    return item


def editorial_candidates(host, episodes, claims, removed):
    out = []
    for gap in host.get("open_gaps") or []:
        terms = tokens(gap)
        refs = [e["id"] for e in episodes if terms & tokens(e["title"], e["series"], *e["themes"])][:3]
        hits = claim_hits(terms, claims)
        if not refs and not hits:
            removed.append({"titulo": gap, "regra": "sem âncora (nenhum episódio ou claim sustenta)"})
            continue
        score = 0.4 + 0.1 * len(refs) + 0.1 * len(hits)
        out.append(candidate(gap, "lacuna declarada no host-profile (open_gaps); padrão no catálogo"
                             f" em {len(refs)} episódio(s)", score, episode_refs=refs, claim_ids=hits))
    return out


# ── tetos, filtros, ranking ───────────────────────────────────────────────

def apply_caps(item, trunk, degraded, draft, inferencias):
    notes = []
    infer = [c for c in item.get("claim_ids") or [] if c in inferencias]
    if infer:
        notes.append(f"claim {', '.join(infer)} é inferência: hipótese a confirmar com o convidado")
    if degraded and item.get("claim_ids"):
        item["score"] = min(item["score"], DEGRADED_CAP)
        notes.append("[confiança rebaixada: dossiê degradado]")
    if draft and trunk == "editorial":
        item["score"] = min(item["score"], DRAFT_CAP)
        notes.append("[confiança rebaixada: host-profile em draft]")
    if notes:
        item["rationale"] += "; " + "; ".join(notes)
    return item


def violates(item, topics):
    text, terms = norm(item["title"] + " " + item["rationale"]), tokens(item["title"], item["rationale"])
    return next((t for t in topics if norm(t) in text or (tokens(t) and tokens(t) <= terms)), None)


def finalize(trunk, cands, ctx, removed):
    kept = []
    for item in cands:
        topic = violates(item, ctx["topics"])
        if topic:
            removed.append({"titulo": item["title"], "regra": f"off_limits/does_not_cover: {topic}"})
        else:
            kept.append(apply_caps(item, trunk, ctx["degraded"], ctx["draft"], ctx["inferencias"]))
    kept.sort(key=lambda i: -i["score"])
    return [dict(id=f"{trunk[0]}{n}", rank=n, **item) for n, item in enumerate(kept[:ctx["max"]], 1)]


def confianca(degraded, host_status, dossier, extra=None):
    motivos = [extra] if extra else []
    if degraded:
        gaps = ", ".join((dossier.get("coverage") or {}).get("gaps") or [])
        motivos.append(f"dossiê degradado (lacunas: {gaps}); itens com claim_ids limitados a {DEGRADED_CAP}")
    if host_status != "confirmed":
        motivos.append(f"host-profile em {host_status}; tronco editorial limitado a {DRAFT_CAP}")
    return {"dossie": "rebaixada" if degraded else "normal", "host_profile": host_status,
            "motivo": "; ".join(motivos) or "entradas completas"}


PAUTA_PAGA = ("troncos tendência e continuidade são do plano pago (tool pauta_completa do MCP do PodFácil);"
              " este pacote monta só o tronco editorial")


def paid_candidates(inp, show, host, claims, episodes):
    """Troncos tendência e continuidade (pauta-3-troncos, plano pago). pauta_troncos.py fica no repositório e no
    servidor (tool pauta_completa) e não vai para o pacote local: lá só o editorial sai, e a confiança diz por quê."""
    try:
        import pauta_troncos as pp
    except ImportError:
        return {"trend": [], "continuity": []}, PAUTA_PAGA
    return {"trend": pp.trend_candidates(inp["trends"], profile_terms(show, host), claims),
            "continuity": pp.continuity_candidates(episodes, host, claims)}, None


def build_pauta(inp, meta):
    """inp: dossier, host, show, catalog, trends, intake. meta: ids + max_items + generated_at."""
    dossier, host, show = inp["dossier"], inp["host"], inp["show"]
    claims, episodes, removed = usable_claims(dossier), episodes_of(inp["catalog"]), []
    degraded = bool(dossier.get("degraded"))
    ctx = {"topics": off_limits(show, inp.get("intake")), "degraded": degraded,
           "draft": host.get("status") != "confirmed", "max": resolve_max(meta.get("max_items"), show),
           "inferencias": {c["id"] for c in claims if c.get("status") == "inferencia"}}
    raw, paid_note = paid_candidates(inp, show, host, claims, episodes)
    raw["editorial"] = editorial_candidates(host, episodes, claims, removed)
    trunks = {t: finalize(t, raw[t], ctx, removed) for t in TRUNKS}
    pauta = {"pauta_id": meta["pauta_id"], "episode_ref": meta["episode_ref"], "show_ref": show.get("show_id"),
             "host_profile_ref": host.get("host_id"), "dossier_ref": dossier.get("dossier_id"),
             "approach_mode": meta["approach_mode"], "format": meta["format"], "dossier_degraded": degraded,
             "max_items_per_trunk": ctx["max"], "locale": show.get("locale", "pt-BR"), "trunks": trunks,
             "generated_at": meta.get("generated_at") or now_iso()}
    return {"pauta": {k: v for k, v in pauta.items() if v is not None},
            "fontes_usadas": inp["trends"].get("sources_used") or [],
            "confianca": confianca(degraded, host.get("status", "draft"), dossier, paid_note), "removidos": removed}


# ── check ─────────────────────────────────────────────────────────────────

def split_pauta(doc):
    if isinstance(doc, dict) and isinstance(doc.get("pauta"), dict):
        return doc["pauta"], doc
    if isinstance(doc, dict):
        return doc, None
    raise SystemExit(f"raiz é {type(doc).__name__} | esperado: pauta ou envelope {{pauta, ...}}")


def all_items(pauta):
    for trunk in TRUNKS:
        for i, item in enumerate((pauta.get("trunks") or {}).get(trunk) or []):
            if isinstance(item, dict):
                yield f"trunks/{trunk}/{i}", trunk, item


def rule_anchor(pauta):
    return [f"R-PAUTA-ANCORA @{where}: item {item.get('title')!r} sem âncora"
            " | esperado: >=1 de claim_ids, episode_refs, trend_refs"
            for where, _t, item in all_items(pauta)
            if not (item.get("claim_ids") or item.get("episode_refs") or item.get("trend_refs"))]


def rule_refs(pauta, key, known, rule):
    errs = []
    for where, _t, item in all_items(pauta):
        refs = [r.get("source_id") if isinstance(r, dict) else r for r in item.get(key) or []]
        missing = [r for r in refs if r not in known]
        if missing:
            errs.append(f"{rule} @{where}/{key}: {missing} não existe(m) na entrada"
                        f" | esperado: um de {sorted(known)[:8]}{'…' if len(known) > 8 else ''}")
    return errs


def rule_caps(pauta, env):
    errs, draft = [], (env or {}).get("confianca", {}).get("host_profile", "confirmed") != "confirmed"
    for where, trunk, item in all_items(pauta):
        score = item.get("score", 0)
        if pauta.get("dossier_degraded") and item.get("claim_ids") and score > DEGRADED_CAP:
            errs.append(f"R-PAUTA-CONFIANCA @{where}/score: {score} com dossiê degradado"
                        f" | esperado: <= {DEGRADED_CAP}")
        if draft and trunk == "editorial" and score > DRAFT_CAP:
            errs.append(f"R-PAUTA-CONFIANCA @{where}/score: {score} com host-profile draft"
                        f" | esperado: <= {DRAFT_CAP}")
    return errs


def rule_inferencia(pauta, dossier):
    infer = {c.get("id") for c in dossier.get("claims") or [] if c.get("status") == "inferencia"}
    return [f"R-PAUTA-INFERENCIA @{where}: cita inferência {sorted(set(item['claim_ids']) & infer)}"
            " sem ressalva | esperado: 'hipótese' no rationale"
            for where, _t, item in all_items(pauta)
            if set(item.get("claim_ids") or []) & infer and "hipotese" not in norm(item.get("rationale"))]


def rule_degraded(pauta, env, dossier):
    want = bool(dossier.get("degraded"))
    errs = [] if pauta.get("dossier_degraded") is want else [
        f"R-PAUTA-DEGRADED @dossier_degraded: {pauta.get('dossier_degraded')!r} | esperado: {want}"
        " (copia guest-dossier.degraded)"]
    got = (env or {}).get("confianca", {}).get("dossie")
    if env is not None and got != ("rebaixada" if want else "normal"):
        errs.append(f"R-PAUTA-DEGRADED @confianca/dossie: {got!r} | esperado:"
                    f" {'rebaixada' if want else 'normal'}")
    return errs


def rule_off_limits(pauta, topics):
    return [f"R-PAUTA-OFF-LIMITS @{where}: {item.get('title')!r} toca {hit!r}"
            " | esperado: nenhum item sobre does_not_cover/off_limits_topics"
            for where, _t, item in all_items(pauta)
            for hit in [violates({"title": item.get("title", ""), "rationale": item.get("rationale", "")}, topics)]
            if hit]


def rule_envelope(env, host, validator):
    errs = []
    if list(env) != ENVELOPE_KEYS:
        errs.append(f"R-PAUTA-ENVELOPE @<raiz>: chaves {list(env)} | esperado: {ENVELOPE_KEYS} nesta ordem")
    for i, src in enumerate(env.get("fontes_usadas") or []):
        if src.get("kind") == "byok" and src.get("status") != "valid":
            errs.append(f"R-PAUTA-BYOK @fontes_usadas/{i}: {src.get('source_id')} status={src.get('status')!r}"
                        " | esperado: só BYOK com credential.status=valid")
    if host is not None and env.get("confianca", {}).get("host_profile") != host.get("status"):
        errs.append(f"R-PAUTA-HOST-STATUS @confianca/host_profile: {env.get('confianca', {}).get('host_profile')!r}"
                    f" | esperado: {host.get('status')!r}")
    return errs + rule_no_secret(env, validator)


def rule_no_secret(env, validator):
    pattern = validator.SECRET_RE
    return [f"R-PAUTA-NO-SECRET @{path}: string com forma de credencial (len={len(text)})"
            " | esperado: nenhum valor de chave na saída"
            for path, text in validator.walk_strings(env)
            if not path.endswith("url") and pattern.search(text)]


def rule_registries(pauta):
    modes, formats = paths.load_yaml(paths.MODES), paths.load_yaml(paths.FORMATS)
    mode_ids = {m.get("id") for m in modes.get("modes") or []}
    errs = [] if pauta.get("approach_mode") in mode_ids else [
        f"R-PAUTA-MODE @approach_mode: {pauta.get('approach_mode')!r} | esperado: um de {sorted(mode_ids)}"]
    if pauta.get("format") not in formats:
        errs.append(f"R-PAUTA-FORMAT @format: {pauta.get('format')!r} | esperado: id em assets/config/formats.yaml")
    return errs


def check_pauta(doc, refs=None, validator=None):
    """(violações, regras puladas). refs: dossier, catalog, trends, show, host, intake (opcionais)."""
    refs, validator = refs or {}, validator or load_validator()
    pauta, env = split_pauta(doc)
    schemas, registry = validator.load_schemas()
    errs = validator.check("pauta", pauta, schemas, registry) + rule_anchor(pauta)
    errs += rule_caps(pauta, env) + rule_registries(pauta)
    skipped = []
    for name, fn in cross_rules(pauta, env, refs, validator).items():
        if fn is None:
            skipped.append(name)
        else:
            errs += fn()
    return errs, skipped


def cross_rules(pauta, env, refs, validator):
    """{regra: função | None}. None = entrada ausente => regra pulada (entra no denominador)."""
    d, c, t, s, i = (refs.get(k) for k in ("dossier", "catalog", "trends", "show", "intake"))
    claim_ids = {x.get("id") for x in (d or {}).get("claims") or []}
    trend_ids = {x.get("source_id") for x in (t or {}).get("sources_used") or []}
    rules = {
        "R-PAUTA-REF-CLAIM": (d, lambda: rule_refs(pauta, "claim_ids", claim_ids, "R-PAUTA-REF-CLAIM")),
        "R-PAUTA-INFERENCIA": (d, lambda: rule_inferencia(pauta, d)),
        "R-PAUTA-DEGRADED": (d, lambda: rule_degraded(pauta, env, d)),
        "R-PAUTA-REF-EPISODE": (c, lambda: rule_refs(pauta, "episode_refs", {e["id"] for e in episodes_of(c)},
                                                     "R-PAUTA-REF-EPISODE")),
        "R-PAUTA-REF-TREND": (t, lambda: rule_refs(pauta, "trend_refs", trend_ids, "R-PAUTA-REF-TREND")),
        "R-PAUTA-OFF-LIMITS": (s or i, lambda: rule_off_limits(pauta, off_limits(s or {}, i))),
        "R-PAUTA-ENVELOPE": (env, lambda: rule_envelope(env, refs.get("host"), validator)),
    }
    return {name: (fn if src is not None else None) for name, (src, fn) in rules.items()}


# ── render ────────────────────────────────────────────────────────────────

TRUNK_TITLE = {"trend": "Tendência × perfil", "continuity": "Continuidade (catálogo)",
               "editorial": "Linha editorial do host"}


def render_anchors(item):
    parts = []
    if item.get("claim_ids"):
        parts.append("claims " + ", ".join(f"`{c}`" for c in item["claim_ids"]))
    if item.get("episode_refs"):
        parts.append("episódios " + ", ".join(f"`{e}`" for e in item["episode_refs"]))
    for ref in item.get("trend_refs") or []:
        label = f"{ref['source_id']} {ref['observed_at'][:10]}"
        parts.append(f"[{label}]({ref['url']})" if ref.get("url") else label)
    return "; ".join(parts)


def render_item(item):
    score = f" · score {item['score']}" if "score" in item else ""
    lines = [f"{item['rank']}. **{item['title']}**{score}", f"   - Por quê: {item['rationale']}",
             f"   - Âncoras: {render_anchors(item)}"]
    lines += [f"   - Pergunta: {q}" for q in item.get("questions") or []]
    return lines


def render_pauta(doc):
    pauta, env = split_pauta(doc)
    env = env or {}
    conf = env.get("confianca") or {}
    lines = [f"# Pauta — {pauta.get('episode_ref')}", "",
             f"- Modo `{pauta.get('approach_mode')}` · formato `{pauta.get('format')}` · até"
             f" {pauta.get('max_items_per_trunk', DEFAULT_MAX)} itens por tronco · gerada em {pauta.get('generated_at')}",
             f"- Confiança: dossiê {conf.get('dossie', '?')} · host-profile {conf.get('host_profile', '?')}"]
    if pauta.get("dossier_degraded"):
        lines += ["", f"> **Confiança rebaixada** — {conf.get('motivo', '')}"]
    for trunk in TRUNKS:
        items = (pauta.get("trunks") or {}).get(trunk) or []
        lines += ["", f"## {TRUNK_TITLE[trunk]} — {len(items)}", ""]
        lines += [ln for item in items for ln in render_item(item)] or ["_Sem itens ancorados._"]
    fontes = ", ".join(f"{f['source_id']} ({f['kind']})" for f in env.get("fontes_usadas") or []) or "—"
    lines += ["", "## Fontes e cortes", "", f"- Fontes consultadas: {fontes}"]
    lines += [f"- Removido: {r['titulo']} — {r['regra']}" for r in env.get("removidos") or []]
    return "\n".join(lines) + "\n"


# ── CLI ───────────────────────────────────────────────────────────────────

def opt_json(path):
    return load_json(path) if path else None


def cmd_build(args):
    inp = {"dossier": split_dossier(load_json(args.dossier))[0], "host": load_json(args.host_profile),
           "show": load_json(args.show_profile), "catalog": load_json(args.catalog),
           "trends": load_json(args.trends), "intake": opt_json(args.intake)}
    meta = {k: getattr(args, k) for k in ("pauta_id", "episode_ref", "approach_mode", "format", "max_items")}
    text = json.dumps(build_pauta(inp, meta), ensure_ascii=False, indent=2) + "\n"
    Path(args.output).write_text(text, encoding="utf-8") if args.output else sys.stdout.write(text)
    return 0


def cmd_check_pauta(args):
    dossier = opt_json(args.dossier)
    refs = {"dossier": split_dossier(dossier)[0] if dossier else None, "catalog": opt_json(args.catalog),
            "trends": opt_json(args.trends), "show": opt_json(args.show_profile),
            "host": opt_json(args.host_profile), "intake": opt_json(args.intake)}
    errs, skipped = check_pauta(load_json(args.arquivo), refs)
    for err in errs:
        print(f"FALHA  {err}")
    items = sum(1 for _ in all_items(split_pauta(load_json(args.arquivo))[0]))
    print(f"check {args.arquivo}: itens examinados={items} · violações={len(errs)}"
          f" · regras puladas={len(skipped)} {skipped if skipped else ''}".rstrip())
    return 1 if errs else 0


def cmd_render_pauta(args):
    text = render_pauta(load_json(args.arquivo))
    Path(args.output).write_text(text, encoding="utf-8") if args.output else sys.stdout.write(text)
    return 0


def add_refs(parser, required):
    for name in ("--dossier", "--host-profile", "--show-profile", "--catalog", "--trends"):
        parser.add_argument(name, required=required)
    parser.add_argument("--intake")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    bld = sub.add_parser("build")
    add_refs(bld, required=True)
    for name in ("--pauta-id", "--episode-ref", "--approach-mode", "--format"):
        bld.add_argument(name, required=True)
    bld.add_argument("--max-items", type=int)
    bld.add_argument("-o", "--output")
    chk = sub.add_parser("check")
    chk.add_argument("arquivo")
    add_refs(chk, required=False)
    ren = sub.add_parser("render")
    ren.add_argument("arquivo")
    ren.add_argument("-o", "--output")
    args = parser.parse_args(argv)
    return {"build": cmd_build, "check": cmd_check_pauta, "render": cmd_render_pauta}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
