#!/usr/bin/env python3
"""Operações da memória do show (F6): status, lições/cortes, catálogo e surfacing.

status:   transição no ciclo do references/contracts/episode-record.schema.json. O plugin RECOMENDA:
          avançar para gravação sem roteiro pronto (R-MEMORIA-ROTEIRO-PENDENTE) ou para
          publicação sem gate APPROVE (R-PUBLICACAO-GATE) só passa com human-decision
          `seguir_contra` que cite os alertas (references/principios.md: a decisão é sempre humana).
catalog:  episode-records no formato que pauta_tools já lê ({id, titulo, serie, temas}).
suggest:  regras simples e explicáveis (cada sugestão diz a regra e a evidência).
"""
import re
import statistics
import sys
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import memory_store as ms  # noqa: E402

RECORDING_AT = ms.STATUSES.index("ready_to_record")
PUBLISH = ("ready_to_publish", "publishing", "published")
GATE_VERDICTS = ("APPROVE", "REQUEST_CHANGES", "HOLD")
BLOCKING = {"atencao", "alta"}
FOLLOWUP_DAYS = 60
PROMISE_RE = re.compile(r"\b(parte \d+|pr[oó]ximo epis[oó]dio|sequ[eê]ncia|continua(?:remos|r)?|"
                        r"voltar(?:emos)? ao tema|follow-?up)\b", re.IGNORECASE)
PART_RE = re.compile(r"\bparte\s*(\d+)\b", re.IGNORECASE)  # "EP N" é numeração do show, não sequência


# ── status ────────────────────────────────────────────────────────────────

def memory_alert(code, severity, evidence):
    return {"code": code, "severity": severity, "text_i18n_key": f"decision.alerts.{code}", "evidence": evidence}


def script_ready(ws, record):
    edir = ms.episode_dir(ws, record["episode_id"])
    for ref in ms.slot_refs(record["artifacts"], "script"):
        doc = ref if isinstance(ref, dict) else ms.read_json(edir / ref)
        if doc.get("status") == "pronto_para_gravar":
            return True
    return False


def effective_status(record):
    """Status que conta para os gates: saindo de archived, vale o anterior ao arquivamento (CRITIC M1)."""
    if record["status"] != "archived":
        return record["status"]
    last = next((h for h in reversed(record.get("history") or []) if h.get("to") == "archived"), None)
    return last["from"] if last and last.get("from") in ms.STATUSES else "idea"


def transition_alerts(ws, record, target):
    """Alertas da recomendação para ir de record.status a target (só avanço gera alerta)."""
    cur, tgt = ms.STATUSES.index(effective_status(record)), ms.STATUSES.index(target)
    alerts = []
    if tgt <= cur or target == "archived":
        return alerts
    if cur < RECORDING_AT <= tgt and not script_ready(ws, record):
        alerts.append(memory_alert("R-MEMORIA-ROTEIRO-PENDENTE", "atencao",
                            "nenhum roteiro ligado ao episódio está em pronto_para_gravar"))
    gate = (record.get("gate") or {}).get("recommendation")
    if target in PUBLISH and gate != "APPROVE":
        alerts.append(memory_alert("R-PUBLICACAO-GATE", "alta", f"gate.recommendation={gate or 'ausente'}"))
    return alerts


def check_decision(record, decision, alerts):
    """Erros (lista vazia = aceite vale) da human-decision contra os alertas exigidos."""
    need = {a["code"] for a in alerts if a["severity"] in BLOCKING}
    if not need:
        return []
    if decision is None:
        return [f"{c}: transição contra a recomendação sem human-decision | esperado: --decision "
                f"ARQ.json (references/contracts/human-decision.schema.json) com decision=seguir_contra" for c in sorted(need)]
    errs = ms.violations("human-decision", decision)
    seen = {a.get("code") for a in decision.get("alerts") or []}
    if decision.get("decision") != "seguir_contra":
        errs.append(f"decision={decision.get('decision')!r} | esperado: 'seguir_contra'")
    if decision.get("subject_ref") != record["episode_id"]:
        errs.append(f"subject_ref={decision.get('subject_ref')!r} | esperado: {record['episode_id']!r}")
    errs += [f"alerta {c} não consta como visto | esperado em decision.alerts[].code" for c in sorted(need - seen)]
    return errs


def set_gate(ws, episode_id, verdict, by):
    if verdict not in GATE_VERDICTS:
        raise ms.MemoryError_(f"gate={verdict!r} | esperado um de {GATE_VERDICTS}")
    record = ms.load_record(ws, episode_id)
    record["gate"] = {"recommendation": verdict, "by": by or "@producer", "at": ms.now_iso()}
    ms.save_record(ws, record)
    return record


def change_status(ws, episode_id, target, by=None, decision=None):
    """(record, alertas). Recusa (MemoryError_) se a transição vai contra a recomendação sem aceite."""
    if target not in ms.STATUSES:
        raise ms.MemoryError_(f"status={target!r} | esperado um de {ms.STATUSES}")
    record = ms.load_record(ws, episode_id)
    alerts = transition_alerts(ws, record, target)
    errs = check_decision(record, decision, alerts)
    if errs:
        raise ms.MemoryError_("transição recusada: " + " ; ".join(errs))
    entry = {"from": record["status"], "to": target, "at": ms.now_iso()}
    entry.update({"by": by} if by else {})
    if decision is not None and alerts:
        record["artifacts"].setdefault("decisions", []).append(decision)
        entry["decision_ref"] = decision["decision_id"]
    record.setdefault("history", []).append(entry)
    record["status"] = target
    ms.save_record(ws, record)
    return record, alerts


# ── lições, métricas, cortes ──────────────────────────────────────────────

def add_lessons(ws, episode_id, lessons=(), metrics=None, clip=None):
    record = ms.load_record(ws, episode_id)
    record["lessons"] = list(dict.fromkeys((record.get("lessons") or []) + [x for x in lessons if x.strip()]))
    if metrics:
        record["metrics"] = {**(record.get("metrics") or {}), **metrics}
    if clip:
        clips = record["artifacts"].setdefault("clips", [])
        old = next((c for c in clips if c["url"] == clip["url"]), None)
        if old:
            old.update({k: v for k, v in clip.items() if k != "metrics"})
            old["metrics"] = {**(old.get("metrics") or {}), **(clip.get("metrics") or {})}
        else:
            clips.append(clip)
    ms.save_record(ws, record)
    return record


# ── catálogo ──────────────────────────────────────────────────────────────

def entry_record(entry, show_ref, used):
    eid = ms.slug(entry.get("rotulo") or "") or ms.slug(entry.get("id") or "") or ms.slug(entry.get("titulo"))
    base, n = eid, 2
    while eid in used:
        eid, n = f"{base}-{n}", n + 1
    rec = {"episode_id": eid, "show_ref": show_ref, "title": entry.get("titulo") or entry.get("title") or "",
           "status": entry.get("status") or "published", "series_ref": entry.get("serie") or "",
           "format": entry.get("formato") or "", "guest_refs": list(entry.get("convidados") or []),
           "themes": list(entry.get("temas") or []), "artifacts": {},
           "retention": {"subject_ids": [], "keep_consent_record": True}}
    if entry.get("data"):
        rec["published_at"] = f"{entry['data']}T00:00:00-03:00"  # só a data é conhecida
    rec["published_url"] = entry.get("url") or None
    rec["metrics"] = {k: v for k, v in (("duration_s", entry.get("duracao")),) if isinstance(v, (int, float))}
    rec["metrics"].update({k: v for k, v in entry.items() if k.startswith("views") and isinstance(v, (int, float))})
    return {k: v for k, v in rec.items() if k == "artifacts" or v not in (None, "", {})}


def import_catalog(ws, entries):
    """Cria/atualiza episode-records a partir de um catálogo; preserva artefatos e lições existentes."""
    show_ref, used, out = ms.config(ws)["show_ref"], set(), []
    for entry in entries:
        rec = entry_record(entry, show_ref, used)
        used.add(rec["episode_id"])
        path = ms.episode_dir(ws, rec["episode_id"]) / ms.RECORD
        if path.is_file():
            old = ms.read_json(path)
            rec = {**old, **{k: v for k, v in rec.items() if k not in ("artifacts", "retention", "status")}}
        ms.save_record(ws, rec)
        out.append(rec["episode_id"])
    return out


def catalog(ws, include_archived=False):
    rows = []
    for eid in ms.episode_ids(ws):
        rec = ms.load_record(ws, eid)
        if rec["status"] == "archived" and not include_archived:
            continue
        rows.append({"id": eid, "titulo": rec.get("title", ""), "serie": rec.get("series_ref", ""),
                     "temas": rec.get("themes") or [], "data": (rec.get("published_at") or "")[:10],
                     "convidados": rec.get("guest_refs") or [], "status": rec["status"],
                     "url": rec.get("published_url", "")})
    return sorted(rows, key=lambda r: (r["data"] or "9999", r["id"]))


# ── surfacing ─────────────────────────────────────────────────────────────

def views(rec):
    vals = [v for k, v in (rec.get("metrics") or {}).items() if k.startswith("views")]
    return max(vals) if vals else None


def suggest_themes(records, top=8):
    by, label = defaultdict(list), {}
    for rec in records:
        for theme in rec.get("themes") or []:
            by[ms.norm(theme)].append(rec)
            label.setdefault(ms.norm(theme), theme)
    out = []
    ranked = [(k, r) for k, r in sorted(by.items(), key=lambda kv: (-len(kv[1]), kv[0])) if len(r) >= 2]
    for key, recs in ranked[:top]:
        vs = [v for v in map(views, recs) if v is not None]
        last = max((r.get("published_at") or "")[:10] for r in recs)
        why = f"{len(recs)} episódios; último em {last or 'sem data'}"
        why += f"; média de views {round(statistics.mean(vs))}" if vs else ""
        out.append({"rule": "R-SUGEST-TEMA-RECORRENTE", "title": f"Tema recorrente: {label[key]}",
                    "why": why, "evidence": [r["episode_id"] for r in recs]})
    return out


def series_key(rec):
    return ms.norm(re.split(r"\s*\(", rec.get("series_ref") or "")[0])


def suggest_sequels(records):
    parts = defaultdict(dict)
    for rec in records:
        nums = PART_RE.findall(" ".join([rec.get("title", ""), rec["episode_id"].replace("-", " ")]))
        if nums and series_key(rec):
            parts[series_key(rec)][int(nums[-1])] = rec
    out = []
    for key, by_n in sorted(parts.items()):
        last = max(by_n)
        rec = by_n[last]
        out.append({"rule": "R-SUGEST-SEQUENCIA", "title": f"Sequência aberta: {rec.get('series_ref')} — parte {last + 1}?",
                    "why": f"a série tem parte(s) {sorted(by_n)} numeradas e nenhuma parte {last + 1}; confirmar se a série acabou",
                    "evidence": [by_n[n]["episode_id"] for n in sorted(by_n)]})
    return out + suggest_promises(records)


def suggest_promises(records):
    out = []
    for rec in records:
        for lesson in rec.get("lessons") or []:
            if PROMISE_RE.search(lesson):
                out.append({"rule": "R-SUGEST-PROMESSA", "title": f"Promessa registrada em {rec['episode_id']}",
                            "why": f"lição cita continuação: {lesson[:120]}", "evidence": [rec["episode_id"]]})
    return out


def suggest_guests(records, today):
    vs = [v for v in map(views, records) if v is not None]
    median = statistics.median(vs) if vs else None
    by = defaultdict(list)
    for rec in records:
        for guest in rec.get("guest_refs") or []:
            by[re.split(r" \(| — ", guest)[0].strip()].append(rec)
    out, limit = [], (today - timedelta(days=FOLLOWUP_DAYS)).isoformat()
    for name, recs in sorted(by.items()):
        best = max((views(r) or 0) for r in recs)
        last = max((r.get("published_at") or "")[:10] for r in recs)
        if median is not None and best >= median and last and last <= limit:
            out.append({"rule": "R-SUGEST-FOLLOWUP", "title": f"Convidado para follow-up: {name}",
                        "why": f"{len(recs)} participação(ões); melhor views {best} ≥ mediana {median}; "
                               f"última em {last} (≥ {FOLLOWUP_DAYS} dias)",
                        "evidence": [r["episode_id"] for r in recs]})
    return out


def suggest(ws, today=None):
    records = [ms.load_record(ws, eid) for eid in ms.episode_ids(ws)]
    records = [r for r in records if r["status"] != "archived"]
    today = today or date.today()
    return {"temas": suggest_themes(records), "sequencias": suggest_sequels(records),
            "followup": suggest_guests(records, today)}
