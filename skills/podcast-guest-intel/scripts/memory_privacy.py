#!/usr/bin/env python3
"""Eliminação por titular e retenção (F6, LGPD art. 18, VI; art. 8º, §5º; art. 16).

forget:    apaga TODOS os dados de um titular — intake, dossiê, claims e menções (id, nome,
           nome de tratamento e @ das redes lidos do intake, mais os --name extras, em
           qualquer texto dos arquivos do workspace) — e reconstrói o índice do zero. Sem
           confirmação explícita (`confirm == subject`) é só relatório (dry-run).
retention: elimina intake e dossiê de episódios cuja data de retenção venceu
           (retention.delete_after, ou published_at + retention.days_after_publish).
Nos dois, keep_consent_record=true guarda só o registro do consentimento, sem identificação
(sha256 no lugar de ids), como ônus da prova (art. 8º, §2º).
O vault do usuário (origem de import-md) NUNCA é tocado: o relatório lista o que fica lá.
"""
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import memory_index as mi  # noqa: E402
import memory_store as ms  # noqa: E402

REDACTED = "[titular removido]"
ACCENTS = {"a": "aáàâãä", "e": "eéèêë", "i": "iíìîï", "o": "oóòôõö", "u": "uúùûü", "c": "cç", "n": "nñ"}
FORGET_LOG = "forget-log.json"


# ── casamento de nome/id ─────────────────────────────────────────────────

def mention_regex(name):
    """Casa o nome com ou sem acento, qualquer caixa, espaços variáveis, palavra inteira."""
    parts = []
    for ch in ms.norm(name).strip():
        if ch.isspace():
            parts.append(r"\s+" if parts and parts[-1] != r"\s+" else "")
        else:
            parts.append(f"[{ACCENTS[ch]}]" if ch in ACCENTS else re.escape(ch))
    return re.compile(r"(?<!\w)" + "".join(parts) + r"(?!\w)", re.IGNORECASE)


def matchers(subject, names):
    terms = [t for t in [subject, *names] if t and len(ms.norm(t)) >= 3]
    return [mention_regex(t) for t in dict.fromkeys(terms)]


def is_subject(value, subject, regexes):
    return isinstance(value, str) and (value == subject or any(r.fullmatch(value.strip()) for r in regexes))


# ── transformação de documento ───────────────────────────────────────────

def scrub(node, subject, regexes, stats):
    """Remove itens que SÃO o titular (refs, claims dele) e redige menções em texto."""
    if isinstance(node, dict):
        return {k: scrub(v, subject, regexes, stats) for k, v in node.items()}
    if isinstance(node, list):
        kept = [v for v in node if not (is_subject(v, subject, regexes) or
                                        (isinstance(v, dict) and v.get("subject") == subject))]
        stats["itens_removidos"] += len(node) - len(kept)
        return [scrub(v, subject, regexes, stats) for v in kept]
    if isinstance(node, str):
        out = node
        for rx in regexes:
            out, n = rx.subn(REDACTED, out)
            stats["mencoes_redigidas"] += n
        return out
    return node


def belongs(kind, doc, subject, regexes):
    """O artefato inteiro é do titular? (intake/dossiê dele são apagados, não redigidos)."""
    inner = doc.get("dossier", doc) if isinstance(doc, dict) else {}
    if kind == "intake":
        return inner.get("intake_id") == subject or is_subject((inner.get("guest") or {}).get("full_name"),
                                                               subject, regexes)
    if kind == "dossier":
        return subject in (inner.get("guest_ref"), inner.get("intake_ref"))
    return False


def consent_stub(doc, reason):
    """Registro do consentimento sem identificação (ids viram sha256)."""
    consent = dict(doc.get("consent") or {})
    if "consent_id" in consent:
        consent["consent_id_sha256"] = ms.sha256_text(consent.pop("consent_id"))
    return {"intake_id_sha256": ms.sha256_text(doc.get("intake_id", "")), "consent": consent,
            "submitted_at": doc.get("submitted_at"), "kept_reason": reason, "kept_at": ms.now_iso()}


# ── forget ───────────────────────────────────────────────────────────────

def known_names(intake):
    """Formas pelas quais o titular aparece: nome, nome de tratamento e @ das redes (com e sem @)."""
    guest = intake.get("guest") or {}
    found = [guest.get("full_name", ""), guest.get("preferred_name", "")]
    for h in intake.get("social_handles") or []:
        handle = str(h.get("handle", "")).strip()
        found += [handle, handle.lstrip("@")]
    return [n for n in found if n]


def names_from_intakes(ws, subject):
    found = []
    for eid in ms.episode_ids(ws):
        for kind, path in ms.artifact_files(ws, eid):
            doc = ms.read_json(path)
            if kind == "intake" and doc.get("intake_id") == subject:
                found += known_names(doc)
    return list(dict.fromkeys(found))


def plan_episode(ws, eid, subject, regexes, apply, report):
    record = ms.load_record(ws, eid)
    edir = ms.episode_dir(ws, eid)
    keep = record["retention"].get("keep_consent_record", True)
    for kind, path in ms.artifact_files(ws, eid):
        doc = ms.read_json(path)
        if belongs(kind, doc, subject, regexes):
            report["arquivos_apagados"].append(str(path.relative_to(ms.ws_path(ws))))
            if apply:
                drop_artifact(ws, record, kind, path, doc, keep)
    if apply:
        ms.write_json(edir / ms.RECORD, record)


def drop_artifact(ws, record, kind, path, doc, keep_consent):
    if kind == "intake" and keep_consent:
        stub = consent_stub(doc, "LGPD art. 8º, §2º: prova do consentimento")
        ms.write_json(ms.ws_path(ws) / ms.CONSENTS / f"{stub['intake_id_sha256'][:16]}.json", stub)
    slot, multi = ms.TYPES[kind][2], ms.TYPES[kind][3]
    refs = [r for r in ms.slot_refs(record["artifacts"], slot) if r != path.name]
    ms.set_slot(record["artifacts"], slot, refs, multi)
    path.unlink()


def scrub_files(ws, subject, regexes, apply, report):
    root = ms.ws_path(ws)
    paths = sorted(root.glob(f"{ms.EPISODES}/*/*.json")) + sorted(root.glob(f"{ms.NOTES}/*.json"))
    for path in paths:
        stats = {"itens_removidos": 0, "mencoes_redigidas": 0}
        doc = ms.read_json(path)
        new = scrub(doc, subject, regexes, stats)
        if new != doc:
            report["arquivos_redigidos"].append(str(path.relative_to(root)))
            for key in stats:
                report[key] += stats[key]
            if apply:
                ms.write_json(path, new)
    scrub_markdown(root, regexes, apply, report)


def scrub_markdown(root, regexes, apply, report):
    for path in sorted(root.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        new = text
        for rx in regexes:
            new = rx.sub(REDACTED, new)
        if new != text:
            report["arquivos_redigidos"].append(str(path.relative_to(root)))
            if apply:
                path.write_text(new, encoding="utf-8")


def empty_report(subject, names):
    return {"subject_sha256": ms.sha256_text(subject), "nomes_usados": len(names), "aplicado": False,
            "arquivos_apagados": [], "arquivos_redigidos": [], "itens_removidos": 0, "mencoes_redigidas": 0,
            "vault_nao_tocado": [], "residuo": None}


def forget(ws, subject, names=(), confirm=None, decided_by=None):
    """Relatório do que sai; aplica só com confirm == subject e decided_by (decisão humana)."""
    if not subject or not str(subject).strip():
        raise ms.MemoryError_(f"subject={subject!r} | esperado: id do titular (guest_ref ou intake_id)")
    apply = confirm is not None
    if apply and (confirm != subject or not decided_by):
        raise ms.MemoryError_(f"confirmação={confirm!r}, decided_by={decided_by!r} | esperado: --confirm "
                              f"igual ao subject ({subject!r}) e --decided-by com o nome de quem decidiu")
    names = list(dict.fromkeys([*names, *names_from_intakes(ws, subject)]))
    regexes = matchers(subject, names)
    report = empty_report(subject, names)
    for eid in ms.episode_ids(ws):
        plan_episode(ws, eid, subject, regexes, apply, report)
    scrub_files(ws, subject, regexes, apply, report)
    report["vault_nao_tocado"] = vault_sources(ws, regexes)
    if apply:
        finish_forget(ws, subject, names, decided_by, report)
    return report


def vault_sources(ws, regexes):
    """Notas importadas cuja ORIGEM no vault do usuário cita o titular: o usuário apaga lá."""
    out = []
    for path in sorted((ms.ws_path(ws) / ms.NOTES).glob("*.json")):
        src = ms.read_json(path).get("source_path", "")
        origin = Path(src)
        if origin.is_file() and any(rx.search(origin.read_text(encoding="utf-8")) for rx in regexes):
            out.append(src)
    return out


def finish_forget(ws, subject, names, decided_by, report):
    mi.rebuild(ws)
    report["aplicado"] = True
    report["residuo"] = residue(ws, subject, names)
    log_path = ms.ws_path(ws) / FORGET_LOG
    log = ms.read_json(log_path) if log_path.is_file() else []
    log.append({"at": ms.now_iso(), "subject_sha256": report["subject_sha256"], "decided_by": decided_by,
                "arquivos_apagados": len(report["arquivos_apagados"]),
                "arquivos_redigidos": len(report["arquivos_redigidos"])})
    ms.write_json(log_path, log)


def residue(ws, subject, names):
    """Conferência contra o MUNDO: busca no índice + varredura de bytes de todo arquivo."""
    hits = sum(len(mi.search(ws, f'"{t}"', limit=50)) for t in [subject, *names] if mi_terms(t))
    regexes = matchers(subject, names)
    root = ms.ws_path(ws)
    files = [p for p in root.rglob("*") if p.is_file() and p.name != FORGET_LOG]
    in_files = [str(p.relative_to(root)) for p in files
                if any(rx.search(p.read_bytes().decode("utf-8", "ignore")) for rx in regexes)]
    return {"busca_hits": hits, "arquivos_com_mencao": in_files, "arquivos_examinados": len(files)}


def mi_terms(text):
    return bool(re.findall(r"\w+", text or ""))


# ── retenção ─────────────────────────────────────────────────────────────

def due_date(record):
    ret = record.get("retention") or {}
    if ret.get("delete_after"):
        return date.fromisoformat(ret["delete_after"])
    days, published = ret.get("days_after_publish"), record.get("published_at")
    if days is None or not published:
        return None
    return datetime.fromisoformat(published.replace("Z", "+00:00")).date() + timedelta(days=int(days))


def retention(ws, today=None, apply=False):
    """[{episode_id, vence_em, apagar:[...]}] para intake/dossiê vencidos; aplica com apply=True."""
    today = today or date.today()
    out = []
    for eid in ms.episode_ids(ws):
        record = ms.load_record(ws, eid)
        due = due_date(record)
        files = [(k, p) for k, p in ms.artifact_files(ws, eid) if k in ("intake", "dossier")]
        if due is None or due > today or not files:
            continue
        out.append({"episode_id": eid, "vence_em": due.isoformat(), "apagar": [p.name for _k, p in files]})
        if apply:
            apply_retention(ws, record, files)
    if apply and out:
        mi.rebuild(ws)
    return out


def apply_retention(ws, record, files):
    keep = record["retention"].get("keep_consent_record", True)
    for kind, path in files:
        drop_artifact(ws, record, kind, path, ms.read_json(path), keep)
    record["retention"]["applied_at"] = ms.now_iso()
    ms.save_record(ws, record)
