#!/usr/bin/env python3
"""Métricas de produto (F11, research/02 §2.3): eventos locais, opt-in, sem telemetria externa.

Nada sai da máquina: os eventos ficam em <DIR>/events.jsonl e só são gravados depois de
`enable DIR` (cria <DIR>/OPT_IN). Sem opt-in, `record`/`from-artifacts` recusam (exit 2).

  enable  DIR | disable DIR
  record  DIR EP EVENTO [--at ISO] [--minutes N] [--score 1-5] [--used N --total N]
                        [--correct N] [--what TEXTO] [--ref ID]
  from-artifacts DIR EP [--dossier ARQ] [--pauta ARQ] [--script ARQ]... [--decision ARQ]...
  report  DIR [--episode EP] [-o SAIDA.md]

Eventos: invite_sent, intake_received, dossier_generated, pauta_generated, script_generated,
interaction (obrigatória do host; --what), human_accept (--ref), help_requested, active_minutes
(--minutes), host_rating (--score, Q3), questions_used (--used/--total, Q4), sample_audit
(--correct/--total, Q2).

Métricas: T1 min do intake à 1ª pauta · T2 minutos ativos informados · Q1 % de claims
`verificado` com URL http(s) (sintática; não testa se resolve) · Q2 auditoria manual · Q3 nota
do host · Q4 % perguntas usadas · F1 interações obrigatórias até a 1ª pauta · F2 chegou ao
roteiro sem pedir ajuda. Toda métrica sem dado sai "n/d" com o motivo, nunca 0.
Stdlib pura: python3 scripts/metrics_tools.py ...
"""
import argparse
import json
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

EVENTS = ("invite_sent", "intake_received", "dossier_generated", "pauta_generated", "script_generated",
          "interaction", "human_accept", "help_requested", "active_minutes", "host_rating", "questions_used",
          "sample_audit")
TARGETS = {"T1": "≤ 15 min", "T2": "≤ 20 min", "Q1": "100%", "Q2": "≥ 95%", "Q3": "≥ 4", "Q4": "≥ 50%",
           "F1": "≤ 5", "F2": "≥ 80%"}
NAMES = {"T1": "tempo até a 1ª pauta", "T2": "minutos ativos do host", "Q1": "% claims FATO com fonte",
         "Q2": "precisão de amostra (auditoria)", "Q3": "nota do host à pauta", "Q4": "% perguntas usadas",
         "F1": "interações obrigatórias", "F2": "conclusão sem ajuda"}


class MetricsError(Exception):
    """Erro de uso: mensagem com o valor ofensor e o formato esperado."""


# ── armazenamento ─────────────────────────────────────────────────────────

def metrics_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_event_ts(value):
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        raise MetricsError(f"timestamp={value!r} | esperado: ISO 8601, ex. 2026-10-09T16:10:00Z") from None


def opted_in(d):
    return (Path(d) / "OPT_IN").is_file()


def append_event(d, episode, event, at=None, **fields):
    if not opted_in(d):
        raise MetricsError(f"{d}: métricas desligadas | esperado: rodar `enable {d}` (opt-in) antes")
    if event not in EVENTS:
        raise MetricsError(f"evento={event!r} | esperado: um de {EVENTS}")
    parse_event_ts(at or metrics_now())
    rec = {"ts": at or metrics_now(), "episode": episode, "event": event,
           **{k: v for k, v in fields.items() if v is not None}}
    with open(Path(d) / "events.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def load_events(d):
    path = Path(d) / "events.jsonl"
    if not path.is_file():
        return []
    out = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                out.append(json.loads(line))
            except ValueError as exc:
                raise MetricsError(f"{path}:{n} JSON inválido ({exc}) | esperado: 1 objeto por linha") from None
    return sorted(out, key=lambda e: parse_event_ts(e["ts"]))


# ── extração de artefatos existentes ──────────────────────────────────────

def claim_counts(dossier_doc):
    claims = (dossier_doc.get("dossier") or dossier_doc).get("claims") or []
    facts = [c for c in claims if c.get("status") == "verificado"]
    sourced = [c for c in facts if any(str(s.get("url", "")).startswith(("http://", "https://"))
                                       for s in c.get("sources") or [])]
    return {"claims_total": len(claims), "claims_fact": len(facts), "claims_fact_with_source": len(sourced)}


def generated_at(doc, *paths):
    for path in paths:
        node = doc
        for part in path:
            node = node.get(part) if isinstance(node, dict) else None
        if node:
            return node
    raise MetricsError(f"generated_at ausente (procurado em {paths}) | esperado: artefato do pipeline")


def from_artifacts(d, episode, dossier=None, pauta=None, scripts=(), decisions=()):
    read = lambda p: json.loads(Path(p).read_text(encoding="utf-8"))  # noqa: E731
    recs = []
    if dossier:
        doc = read(dossier)
        recs.append(append_event(d, episode, "dossier_generated", generated_at(doc, ("dossier", "generated_at"),
                                 ("generated_at",)), ref=Path(dossier).name, **claim_counts(doc)))
    if pauta:
        doc = read(pauta)
        recs.append(append_event(d, episode, "pauta_generated", generated_at(doc, ("pauta", "generated_at"),
                                 ("generated_at",)), ref=Path(pauta).name))
    for s in scripts:
        doc = read(s)
        recs.append(append_event(d, episode, "script_generated", generated_at(doc, ("meta", "generated_at"),
                                 ("generated_at",)), ref=Path(s).name))
    for dec in decisions:
        doc = read(dec)
        recs.append(append_event(d, episode, "human_accept", doc["decided_at"], ref=doc.get("subject_ref"),
                                 what=doc.get("decision")))
    return recs


# ── cálculo ───────────────────────────────────────────────────────────────

def first_event(evs, name):
    return next((e for e in evs if e["event"] == name), None)


def nd(reason):
    return {"value": None, "why": reason}


def val(v, fmt, extra=""):
    return {"value": v, "text": fmt.format(v) + extra}


def t1(evs):
    intake, pauta = first_event(evs, "intake_received"), first_event(evs, "pauta_generated")
    if not intake or not pauta:
        return nd("sem evento " + ("intake_received" if not intake else "pauta_generated"))
    minutes = (parse_event_ts(pauta["ts"]) - parse_event_ts(intake["ts"])).total_seconds() / 60
    return nd("pauta registrada antes do intake (relógio inconsistente)") if minutes < 0 else val(minutes, "{:.1f} min")


def t2(evs):
    mins = [e["minutes"] for e in evs if e["event"] == "active_minutes"]
    return val(sum(mins), "{:.0f} min", f" ({len(mins)} registro(s))") if mins else nd("minutos ativos não informados")


def q1(evs):
    dos = [e for e in evs if e["event"] == "dossier_generated" and "claims_fact" in e]
    if not dos:
        return nd("sem dossiê registrado")
    last = dos[-1]
    if not last["claims_fact"]:
        return nd("dossiê sem claims verificado")
    pct = 100 * last["claims_fact_with_source"] / last["claims_fact"]
    return val(pct, "{:.0f}%", f" ({last['claims_fact_with_source']}/{last['claims_fact']}; "
                               f"{last['claims_total']} claims no total)")


def ratio_metric(evs, name, num, label):
    rows = [e for e in evs if e["event"] == name]
    if not rows:
        return nd(f"{label} não informado (entrada manual)")
    last = rows[-1]
    return val(100 * last[num] / last["total"], "{:.0f}%", f" ({last[num]}/{last['total']})")


def q3(evs):
    scores = [e["score"] for e in evs if e["event"] == "host_rating"]
    return val(statistics.mean(scores), "{:.1f}", f" (n={len(scores)})") if scores else nd("nota do host não informada")


def f1(evs):
    start = first_event(evs, "intake_received") or first_event(evs, "invite_sent")
    pauta = first_event(evs, "pauta_generated")
    if not start or not pauta:
        return nd("sem janela convite/intake → pauta registrada")
    lo, hi = parse_event_ts(start["ts"]), parse_event_ts(pauta["ts"])
    n = sum(1 for e in evs if e["event"] == "interaction" and lo <= parse_event_ts(e["ts"]) <= hi)
    return val(n, "{}", " (interações registradas)")


def f2(evs):
    script = first_event(evs, "script_generated")
    if not script:
        return nd("roteiro não gerado")
    if not (first_event(evs, "intake_received") or first_event(evs, "invite_sent")):
        return nd("sessão não acompanhada desde o convite/intake (pedido de ajuda não teria sido registrado)")
    helped = any(e["event"] == "help_requested" and parse_event_ts(e["ts"]) <= parse_event_ts(script["ts"]) for e in evs)
    return val(0.0 if helped else 100.0, "{}", "") | {"text": "não (pediu ajuda)" if helped else "sim"}


def episode_metrics(evs):
    return {"T1": t1(evs), "T2": t2(evs), "Q1": q1(evs),
            "Q2": ratio_metric(evs, "sample_audit", "correct", "auditoria de amostra"), "Q3": q3(evs),
            "Q4": ratio_metric(evs, "questions_used", "used", "uso de perguntas"), "F1": f1(evs), "F2": f2(evs)}


def aggregate(per_episode):
    out = {}
    for m in TARGETS:
        vals = [r[m]["value"] for r in per_episode.values() if r[m]["value"] is not None]
        if not vals:
            out[m] = nd("nenhum episódio com dado")
            continue
        agg = statistics.median(vals) if m in ("T1", "F1") else statistics.mean(vals)
        unit = {"T1": " min", "T2": " min", "Q3": ""}.get(m, "" if m == "F1" else "%")
        out[m] = val(agg, "{:.1f}" + unit, f" ({'mediana' if m in ('T1', 'F1') else 'média'}; "
                                            f"n={len(vals)}/{len(per_episode)})")
    return out


# ── relatório ─────────────────────────────────────────────────────────────

def table(metrics):
    lines = ["| Métrica | Valor | Meta (research/02) |", "|---|---|---|"]
    for m, r in metrics.items():
        shown = r.get("text") if r["value"] is not None else f"n/d: {r['why']}"
        lines.append(f"| {m} {NAMES[m]} | {shown} | {TARGETS[m]} |")
    return lines


def report(d, episode=None):
    evs = load_events(d)
    episodes = sorted({e["episode"] for e in evs if not episode or e["episode"] == episode})
    per = {ep: episode_metrics([e for e in evs if e["episode"] == ep]) for ep in episodes}
    out = ["# Relatório de métricas de produto", "",
           f"Gerado em {metrics_now()} a partir de `{Path(d).name}/events.jsonl` (local, opt-in). "
           f"Eventos examinados: {len(evs)}. Episódios: {len(episodes)}.", ""]
    for ep, metrics in per.items():
        accepts = sum(1 for e in evs if e["episode"] == ep and e["event"] == "human_accept")
        out += [f"## Episódio `{ep}`", "", *table(metrics), "", f"Aceites humanos registrados: {accepts}.", ""]
    if len(per) > 1:
        out += ["## Agregado", "", *table(aggregate(per)), ""]
    measured = sum(1 for m in per.values() for r in m.values() if r["value"] is not None)
    out += [f"Denominador: {measured} de {len(per) * len(TARGETS)} métricas medidas; o resto é n/d com motivo."]
    return "\n".join(out) + "\n"


# ── CLI ───────────────────────────────────────────────────────────────────

def metrics_parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("enable", "disable"):
        sub.add_parser(name).add_argument("dir")
    r = sub.add_parser("record")
    for a in ("dir", "episode", "event"):
        r.add_argument(a)
    r.add_argument("--at")
    r.add_argument("--minutes", type=float)
    r.add_argument("--score", type=int, choices=range(1, 6))
    for a in ("--used", "--total", "--correct"):
        r.add_argument(a, type=int)
    r.add_argument("--what")
    r.add_argument("--ref")
    f = sub.add_parser("from-artifacts")
    f.add_argument("dir")
    f.add_argument("episode")
    f.add_argument("--dossier")
    f.add_argument("--pauta")
    f.add_argument("--script", action="append", default=[])
    f.add_argument("--decision", action="append", default=[])
    g = sub.add_parser("report")
    g.add_argument("dir")
    g.add_argument("--episode")
    g.add_argument("-o", "--out")
    return p


def check_record_args(a):
    needs = {"active_minutes": ("minutes",), "host_rating": ("score",), "questions_used": ("used", "total"),
             "sample_audit": ("correct", "total")}.get(a.event, ())
    missing = [n for n in needs if getattr(a, n) is None]
    if missing:
        raise MetricsError(f"evento {a.event} sem {missing} | esperado: --{' --'.join(missing)}")
    if "total" in needs and a.total <= 0:
        raise MetricsError(f"--total={a.total} | esperado: > 0")


def metrics_main(argv=None):
    a = metrics_parser().parse_args(argv)
    try:
        if a.cmd == "enable":
            Path(a.dir).mkdir(parents=True, exist_ok=True)
            (Path(a.dir) / "OPT_IN").write_text(f"opt-in local em {metrics_now()}; nada é enviado para fora.\n")
        elif a.cmd == "disable":
            (Path(a.dir) / "OPT_IN").unlink(missing_ok=True)
        elif a.cmd == "record":
            check_record_args(a)
            append_event(a.dir, a.episode, a.event, a.at, minutes=a.minutes, score=a.score, used=a.used,
                         total=a.total, correct=a.correct, what=a.what, ref=a.ref)
        elif a.cmd == "from-artifacts":
            print(f"eventos gravados: {len(from_artifacts(a.dir, a.episode, a.dossier, a.pauta, a.script, a.decision))}")
        else:
            text = report(a.dir, a.episode)
            Path(a.out).write_text(text, encoding="utf-8") if a.out else sys.stdout.write(text)
    except MetricsError as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(metrics_main())
