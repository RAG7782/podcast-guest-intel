#!/usr/bin/env python3
"""Regras do job de localização (references/contracts/localization.schema.json) e plano de dublagem (F7).

Usado por scripts/localization_tools.py (check, dub-plan). Três classes de achado:
  violação (sai 1): schema, regra rígida (réplica de voz sem aceite C3 válido) ou integridade
                    (legenda fora do formato, segmentos desalinhados, link perdido, alerta desatualizado,
                    aprovado/publicado com alerta atencao/alta sem aceite humano que o cubra);
  alerta (recomendação; o humano decide): sem aceite de tradução/voz genérica, agente político,
                    glossário, números, leitura (cps), revisão humana (info, sempre);
  regra pulada (contada): falta a entrada que ela precisa (intake, arquivo ainda não gerado).
"""
import json
from pathlib import Path

import localization_io as lio
from localization_tools import (DUB_PRICES, SEV_ACK, disclosure, glossary_coverage, missing_numbers,
                                qa_subtitle_text, shownotes_diff)


class ConsentRefusal(lio.LocalizationError):
    """Regra rígida: dublagem com réplica de voz sem aceite C3 válido. Não há aceite que libere."""


def loc_alert(code, severity, evidence=""):
    out = {"code": code, "severity": severity, "text_i18n_key": f"decision.alerts.{code}"}
    return dict(out, evidence=evidence) if evidence else out


# ── consentimento ────────────────────────────────────────────────────────

def consent_record(intakes, intake_id, kind):
    """(registro|None, motivo). intakes = {intake_id: guest-intake}."""
    intake = intakes.get(intake_id)
    if intake is None:
        return None, f"intake {intake_id!r} não fornecido (--intake)"
    rec = (intake.get("localization_consents") or {}).get(kind)
    return (rec, "") if rec else (None, f"{intake_id}: sem localization_consents.{kind}")


def consent_ok(rec, locale, replica=False):
    """Concedido, não revogado, cobre o idioma; réplica exige ainda specific/highlighted/sensitive."""
    if not rec or rec.get("granted") is not True or rec.get("revoked_at"):
        return False
    if locale not in (rec.get("target_locales") or []):
        return False
    return not replica or all(rec.get(k) is True for k in ("specific", "highlighted", "sensitive"))


def replica_refusals(job, intakes):
    """Motivos de recusa de cada dubbing guest_replica. Vazio = liberado."""
    out = []
    speakers = {s["label"]: s for s in job.get("speakers") or []}
    for i, d in enumerate(job.get("dubbing") or []):
        if d.get("voice_mode") != "guest_replica":
            continue
        intake_id, _, path = (d.get("consent_ref") or "").partition("#")
        rec, why = consent_record(intakes, intake_id, path.rsplit("/", 1)[-1]) if intake_id else (None, "sem consent_ref")
        owner = (speakers.get(d.get("speaker_label")) or {}).get("intake_ref")
        if path and not path.endswith("dub_voice_replica"):
            why = f"consent_ref aponta {path!r}, não dub_voice_replica"
        elif owner and owner != intake_id:
            why = f"falante {d.get('speaker_label')} é {owner!r}, aceite é de {intake_id!r}"
        elif not why and not consent_ok(rec, d["locale"], replica=True):
            why = f"aceite {intake_id} não concedido, revogado, incompleto ou sem o idioma {d['locale']}"
        if why:
            out.append(f"R-LOC-REPLICA-CONSENT @dubbing/{i}: {why} | esperado aceite dub_voice_replica"
                       " concedido, não revogado e que cubra o idioma (regra rígida: recusado)")
    return out


def consent_gap(speaker, intakes, kind, locales):
    """(idiomas sem aceite, pulada). Convidado sem intake_ref = nenhum aceite registrado."""
    ref = speaker.get("intake_ref")
    if not ref:
        return list(locales), False
    if ref not in intakes:
        return [], True
    rec, _ = consent_record(intakes, ref, kind)
    return [loc for loc in locales if not consent_ok(rec, loc)], False


def guest_alerts(job, intakes):
    """(alertas, regras puladas) dos aceites C1 (texto) e C2 (voz genérica) dos convidados."""
    alerts, skipped = [], []
    guests = {s["label"]: s for s in job.get("speakers") or [] if s.get("role") == "guest"}
    wanted = [(g, "translation_text", job["target_locales"], "R-LOCALIZACAO-SEM-ACEITE-TRADUCAO") for g in guests.values()]
    labels = {s["label"] for s in job.get("speakers") or []}
    for d in (d for d in job.get("dubbing") or [] if d.get("voice_mode") == "generic"):
        # rótulo fora de speakers = trilha inteira (sem diarização): cobre todos os convidados
        dubbed = [guests[d["speaker_label"]]] if d["speaker_label"] in guests else (
            [] if d["speaker_label"] in labels else list(guests.values()))
        wanted += [(g, "dub_generic_voice", [d["locale"]], "R-LOCALIZACAO-SEM-ACEITE-VOZ-GENERICA") for g in dubbed]
    for g, kind, locales, code in wanted:
        lacking, skip = consent_gap(g, intakes, kind, locales)
        if skip:
            skipped.append(f"{code}[{g['intake_ref']}]")
        elif lacking:
            alerts.append(loc_alert(code, "alta", f"{g['label']} ({g.get('intake_ref') or 'sem intake'}): {lacking}"))
    return alerts, skipped


# ── arquivos: legendas, traduções, show notes ────────────────────────────

def subtitle_findings(job, base):
    errs, alerts, skipped, final = [], [], [], job.get("status") in ("aprovado", "publicado")
    for i, s in enumerate(job.get("subtitles") or []):
        path = base / s["path"]
        if not path.exists():
            (errs.append(f"R-LOC-SUBTITLE-QA @subtitles/{i}: {s['path']} ausente com status {job['status']}")
             if final else skipped.append(f"R-LOC-SUBTITLE-QA[{s['path']}]"))
            continue
        rep = qa_subtitle_text(path.read_text(encoding="utf-8"), s["max_chars_per_line"], s["max_lines"], s.get("max_cps"))
        errs += [f"R-LOC-SUBTITLE-QA @subtitles/{i} ({s['path']}, {rep['examined']} cues): {v}" for v in rep["violations"]]
        if rep["cps_over"]:
            alerts.append(loc_alert("R-LOCALIZACAO-CPS", "info", f"{s['path']}: {len(rep['cps_over'])}/{rep['examined']} cues"))
    return errs, alerts, skipped


def translation_findings(job, base, glossary):
    errs, alerts, skipped = [], [], []
    src_path = base / job["transcript_ref"]
    if not src_path.exists():
        return errs, alerts, ["R-LOC-ALIGN", "R-LOCALIZACAO-GLOSSARIO", "R-LOCALIZACAO-NUMEROS"]
    src = json.loads(src_path.read_text(encoding="utf-8"))["segments"]
    for t in job.get("translations") or []:
        if not (base / t["path"]).exists():
            skipped.append(f"R-LOC-ALIGN[{t['path']}]")
            continue
        tgt = json.loads((base / t["path"]).read_text(encoding="utf-8"))["segments"]
        if [s["id"] for s in src] != [s["id"] for s in tgt]:
            errs.append(f"R-LOC-ALIGN @{t['path']}: {len(tgt)} segmentos vs {len(src)} no original"
                        " | esperado mesmos ids na mesma ordem")
            continue
        cov = glossary_coverage(src, tgt, glossary, t["locale"])
        if cov["misses"]:
            alerts.append(loc_alert("R-LOCALIZACAO-GLOSSARIO", "atencao", f"{t['locale']}: {cov['ok']}/{cov['expected']}; {cov['misses'][:5]}"))
        lost = missing_numbers(src, tgt)
        if lost:
            alerts.append(loc_alert("R-LOCALIZACAO-NUMEROS", "atencao", f"{t['locale']}: {lost[:8]}"))
    return errs, alerts, skipped


def shownotes_findings(job, base):
    errs = []
    for i, s in enumerate(job.get("show_notes_translated") or []):
        src, tgt = base / (s.get("source_path") or ""), base / s["path"]
        if s.get("source_path") and src.is_file() and tgt.is_file():
            lost, extra = shownotes_diff(src.read_text(encoding="utf-8"), tgt.read_text(encoding="utf-8"))
            if lost or extra:
                errs.append(f"R-LOC-SHOWNOTES-LINKS @show_notes_translated/{i}: perdidos={lost} sobrando={extra}"
                            " | esperado links e timestamps idênticos ao original")
    return errs


# ── regras do job ────────────────────────────────────────────────────────

def structure_errors(job):
    errs, targets = [], set(job.get("target_locales") or [])
    for key in ("subtitles", "translations", "show_notes_translated", "dubbing"):
        for i, item in enumerate(job.get(key) or []):
            if item.get("locale") not in targets:
                errs.append(f"R-LOC-TARGETS @{key}/{i}: locale {item.get('locale')!r} | esperado um de {sorted(targets)}")
    for i, d in enumerate(job.get("dubbing") or []):
        want = "localization.disclosure." + ("dub_replica" if d.get("voice_mode") == "guest_replica" else "dub_generic")
        if d.get("disclosure_text_key") != want:
            errs.append(f"R-LOC-DISCLOSURE @dubbing/{i}: {d.get('disclosure_text_key')!r} | esperado {want!r}")
    return errs


def loc_compute_alerts(job, base, intakes, glossary):
    """(violações de arquivo, alertas, puladas)."""
    alerts = [loc_alert("R-LOCALIZACAO-REVISAO-HUMANA", "info")]
    pol = job.get("political_exposure") or {}
    if pol.get("is_political_agent") and job.get("dubbing"):
        alerts.append(loc_alert("R-LOCALIZACAO-AGENTE-POLITICO", "alta", pol.get("basis", "")))
    g_alerts, skipped = guest_alerts(job, intakes)
    errs, sub_alerts, sub_skip = subtitle_findings(job, base)
    t_errs, t_alerts, t_skip = translation_findings(job, base, glossary)
    return errs + t_errs + shownotes_findings(job, base), alerts + g_alerts + sub_alerts + t_alerts, skipped + sub_skip + t_skip


def human_ack_errors(job, alerts):
    if job.get("status") not in ("aprovado", "publicado"):
        return []
    need = sorted({a["code"] for a in alerts if a["severity"] in SEV_ACK})
    hd = (job.get("review") or {}).get("human_decision") or {}
    seen = {a.get("code") for a in hd.get("alerts") or []}
    if need and (hd.get("decision") != "seguir_contra" or not set(need) <= seen):
        return [f"R-LOC-HUMAN-ACK @review/human_decision: alertas {need} sem aceite (decision={hd.get('decision')!r},"
                f" vistos={sorted(c for c in seen if c)}) | esperado seguir_contra cobrindo todos"]
    return []


def check_job(job, base, intakes=None, glossary=None, validator=None, refresh=False):
    """(violações, alertas, puladas). refresh=True grava review.alertas recalculados no job (em memória)."""
    validator = validator or __import__("dossier_tools").load_validator()
    schemas, registry = validator.load_schemas()
    errs = validator.check("localization", job, schemas, registry)
    if errs:
        return errs, [], ["demais regras (schema inválido)"]
    errs += structure_errors(job) + replica_refusals(job, intakes or {})
    f_errs, alerts, skipped = loc_compute_alerts(job, Path(base), intakes or {}, glossary or [])
    if refresh:
        job["review"]["alertas"] = alerts
    stored = sorted(a.get("code") for a in job["review"].get("alertas") or [])
    if stored != sorted(a["code"] for a in alerts):
        errs.append(f"R-LOC-ALERTAS-DESATUALIZADOS @review/alertas: {stored} | esperado"
                    f" {sorted(a['code'] for a in alerts)} (rode check --refresh)")
    return errs + f_errs + human_ack_errors(job, alerts), alerts, skipped


# ── plano de dublagem ────────────────────────────────────────────────────

def price_estimate(mode, locale, chars, minutes):
    out = []
    for pid, pmode, unit, price, src in DUB_PRICES:
        if pmode != mode or (pid == "youtube_auto_dubbing" and locale not in ("en", "es")):
            continue
        qty = {"min": minutes, "1M_chars": chars / 1e6, "1k_chars": chars / 1000}[unit]
        out.append({"provider": pid, "unit": unit, "unit_price_usd": price, "estimate_usd": round(qty * price, 4),
                    "source": src, "kind": "ESTIMATIVA"})
    return out


def dub_plan(job, translated, intakes):
    """Roteiro de dublagem por segmento + custo por provedor. Réplica sem aceite → ConsentRefusal."""
    refusals = replica_refusals(job, intakes)
    if refusals:
        raise ConsentRefusal("; ".join(refusals))
    plans = []
    for d in job.get("dubbing") or []:
        doc = translated.get(d["locale"])
        if doc is None:
            raise lio.LocalizationError(f"sem tradução para {d['locale']} | esperado --translated {d['locale']}=ARQ")
        labelled = any(s.get("speaker") for s in doc["segments"])
        segs = [s for s in doc["segments"] if not labelled or s.get("speaker") == d["speaker_label"]]
        chars, minutes = sum(len(s["text"]) for s in segs), sum(s["end"] - s["start"] for s in segs) / 60
        plans.append({"locale": d["locale"], "speaker_label": d["speaker_label"], "voice_mode": d["voice_mode"],
                      "provider": d["provider"], "consent_ref": d.get("consent_ref"),
                      "disclosure": disclosure(d["locale"], d["disclosure_text_key"].rsplit(".", 1)[-1], job["source_locale"]),
                      "note": "" if labelled else "transcrição sem diarização: todos os segmentos atribuídos a este falante",
                      "totals": {"segments": len(segs), "chars": chars, "source_minutes": round(minutes, 2)},
                      "cost_estimates": price_estimate(d["voice_mode"], d["locale"], chars, minutes),
                      "segments": [{"segment_id": s["id"], "start": s["start"], "end": s["end"], "text": s["text"],
                                    "chars": len(s["text"])} for s in segs]})
    return {"kind": "dub_plan", "localization_id": job["localization_id"], "provider_called": False, "plans": plans}
