#!/usr/bin/env python3
"""Eliminação por titular e retenção (F6, LGPD art. 18, VI; art. 8º, §5º; art. 16).

forget:    apaga TODOS os dados de um titular — intake, dossiê, claims e menções por
           identificadores DELE (id, nome completo, nome de tratamento com 2+ palavras, @ das
           redes, e-mail e telefone do intake, mais os --name extras) em qualquer texto do
           workspace e nos .md que o export-md escreveu — e reconstrói o índice do zero. Primeiro
           nome sozinho NUNCA é padrão de busca (apagaria homônimos, CRITIC C3): vai para
           `revisar_manual`, para o humano decidir. Sem `confirm == subject` é só relatório.
retention: elimina intake e dossiê de episódios cuja data de retenção venceu (retention.delete_after,
           ou published_at + days_after_publish, padrão 90; nunca publicado: prazo-limite) e redige o
           titular no resto do episódio (research, pauta, script). Roda sozinha em todo comando da
           memória enquanto memory.json não disser auto_retention=false (ALQERA PRV-001).
Nos dois, keep_consent_record=true guarda só o registro do consentimento, sem identificação
(sha256 no lugar de ids), como ônus da prova (art. 8º, §2º).
As ORIGENS de import-md no vault do usuário nunca são tocadas: o relatório lista o que fica lá.
"""
import hashlib
import hmac
import re
import secrets
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import memory_index as mi  # noqa: E402
import memory_md as md  # noqa: E402
import memory_store as ms  # noqa: E402

REDACTED = "[titular removido]"
ACCENTS = {"a": "aáàâãä", "e": "eéèêë", "i": "iíìîï", "o": "oóòôõö", "u": "uúùûü", "c": "cç", "n": "nñ"}
FORGET_LOG = "forget-log.json"
KEY_FILE = ".consent-key"   # segredo local do workspace (gitignored); sem ele o hash do id se reverte (CRITIC B5)


# ── casamento de nome/id ─────────────────────────────────────────────────

SEP = r"[\s._-]+"   # "Bruno Fictício da Silva" também casa o slug "bruno-ficticio-da-silva" de uma URL


def mention_regex(name):
    """Casa o nome com ou sem acento, qualquer caixa, espaço/slug variável, palavra inteira."""
    parts = []
    for ch in ms.norm(name).strip():
        if ch.isspace():
            parts.append(SEP if parts and parts[-1] != SEP else "")
        else:
            parts.append(f"[{ACCENTS[ch]}]" if ch in ACCENTS else re.escape(ch))
    return re.compile(r"(?<!\w)" + "".join(parts) + r"(?!\w)", re.IGNORECASE)


def phone_regex(number):
    """Telefone por qualquer grafia (+55 (11) 99999-0000, 999990000): ancora nos 8 últimos dígitos."""
    digits = re.sub(r"\D", "", number or "")
    if len(digits) < 8:
        return None
    tail = r"[\s.()-]*".join(digits[-8:])
    return re.compile(r"(?<!\d)(?:[+(]?\d[\s.()-]*){0,7}" + tail + r"(?!\d)")


def matchers(subject, terms):
    names = [t for t in [subject, *terms["names"]] if t and len(ms.norm(t)) >= 3]
    phones = [rx for rx in map(phone_regex, terms["phones"]) if rx]
    return [mention_regex(t) for t in dict.fromkeys(names)] + phones


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


def keyed_hash(ws, text):
    """HMAC-SHA256 com o segredo do workspace: id derivado do nome (in-bruno-ficticio) não se adivinha."""
    path = ms.ws_path(ws) / KEY_FILE
    if not path.is_file():
        path.write_text(secrets.token_hex(32), encoding="utf-8")
        path.chmod(0o600)
    return hmac.new(path.read_text(encoding="utf-8").strip().encode(), str(text).encode("utf-8"),
                    hashlib.sha256).hexdigest()


def consent_stub(ws, doc, reason):
    """Registro do consentimento sem identificação (ids viram HMAC; campo *_sha256 por compatibilidade)."""
    consent = dict(doc.get("consent") or {})
    if "consent_id" in consent:
        consent["consent_id_sha256"] = keyed_hash(ws, consent.pop("consent_id"))
    return {"intake_id_sha256": keyed_hash(ws, doc.get("intake_id", "")), "consent": consent,
            "submitted_at": doc.get("submitted_at"), "kept_reason": reason, "kept_at": ms.now_iso()}


# ── forget ───────────────────────────────────────────────────────────────

def known_terms(intake):
    """Identificadores do titular. names/phones apagam; review (1 palavra só) vai para o humano."""
    guest, contacts = intake.get("guest") or {}, intake.get("contacts") or {}
    out = {"names": [], "phones": [], "review": []}
    for name in (guest.get("full_name"), guest.get("preferred_name")):
        if name and name.strip():
            out["names" if len(name.split()) >= 2 else "review"].append(name.strip())
    for h in intake.get("social_handles") or []:
        bare = str(h.get("handle", "")).strip().lstrip("@")
        if bare:
            out["names"].append("@" + bare)
            # ponytail: @ sem o símbolo só apaga se tiver _ . ou dígito (não é palavra comum); senão, revisão
            out["names" if re.search(r"[_.\d]", bare) else "review"].append(bare)
    out["names"] += [contacts["email"]] if contacts.get("email") else []
    out["phones"] += [v for k, v in contacts.items() if k in ("whatsapp", "phone") and v]
    return out


def terms_from_intakes(ws, subject, extra_names=()):
    terms = {"names": list(extra_names), "phones": [], "review": []}
    for eid in ms.episode_ids(ws):
        for kind, path in ms.artifact_files(ws, eid):
            doc = ms.read_json(path)
            if kind == "intake" and doc.get("intake_id") == subject:
                for key, vals in known_terms(doc).items():
                    terms[key] += vals
    return {k: list(dict.fromkeys(v)) for k, v in terms.items()}


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
        stub = consent_stub(ws, doc, "LGPD art. 8º, §2º: prova do consentimento")
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


def review_hits(ws, regexes):
    """Onde o primeiro nome (ou @ comum) aparece sem ser apagado: o humano revisa antes do --confirm."""
    root, out = ms.ws_path(ws), []
    for path in sorted(root.glob(f"{ms.EPISODES}/*/*.json")) + sorted(root.glob(f"{ms.NOTES}/*.json")):
        text = path.read_text(encoding="utf-8")
        out += [{"arquivo": str(path.relative_to(root)), "termo": rx.pattern} for rx in regexes if rx.search(text)]
    return out


def scrub_exports(ws, regexes, apply):
    """Os .md que o export-md escreveu (registro em exports.json) são cópia gerada: redigidos também."""
    out = []
    for path in map(Path, md.export_paths(ws)):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            new = text
            for rx in regexes:
                new = rx.sub(REDACTED, new)
            if new != text:
                out.append(str(path))
                if apply:
                    path.write_text(new, encoding="utf-8")
    return out


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


def empty_report(subject, terms):
    return {"subject_sha256": ms.sha256_text(subject), "nomes_usados": len(terms["names"]) + len(terms["phones"]),
            "aplicado": False, "arquivos_apagados": [], "arquivos_redigidos": [], "itens_removidos": 0,
            "mencoes_redigidas": 0, "revisar_manual": [], "exports_redigidos": [], "vault_nao_tocado": [],
            "residuo": None}


def forget(ws, subject, names=(), confirm=None, decided_by=None):
    """Relatório do que sai; aplica só com confirm == subject e decided_by (decisão humana)."""
    if not subject or not str(subject).strip():
        raise ms.MemoryError_(f"subject={subject!r} | esperado: id do titular (guest_ref ou intake_id)")
    apply = confirm is not None
    if apply and (confirm != subject or not decided_by):
        raise ms.MemoryError_(f"confirmação={confirm!r}, decided_by={decided_by!r} | esperado: --confirm "
                              f"igual ao subject ({subject!r}) e --decided-by com o nome de quem decidiu")
    terms = terms_from_intakes(ws, subject, names)
    regexes = matchers(subject, terms)
    report = empty_report(subject, terms)
    report["revisar_manual"] = review_hits(ws, [mention_regex(t) for t in terms["review"]])
    for eid in ms.episode_ids(ws):
        plan_episode(ws, eid, subject, regexes, apply, report)
    scrub_files(ws, subject, regexes, apply, report)
    report["exports_redigidos"] = scrub_exports(ws, regexes, apply)
    report["vault_nao_tocado"] = vault_sources(ws, regexes)
    if apply:
        finish_forget(ws, subject, terms, decided_by, report)
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


def finish_forget(ws, subject, terms, decided_by, report):
    mi.rebuild(ws)
    report["aplicado"] = True
    report["residuo"] = residue(ws, subject, terms)
    log_path = ms.ws_path(ws) / FORGET_LOG
    log = ms.read_json(log_path) if log_path.is_file() else []
    log.append({"at": ms.now_iso(), "subject_sha256": report["subject_sha256"], "decided_by": decided_by,
                "arquivos_apagados": len(report["arquivos_apagados"]),
                "arquivos_redigidos": len(report["arquivos_redigidos"])})
    ms.write_json(log_path, log)


def residue(ws, subject, terms):
    """Conferência contra o MUNDO: índice + bytes de todo arquivo do workspace + exports, pelos
    MESMOS identificadores da redação (nome, @, e-mail, telefone) — sem isso o verde é falso."""
    hits = sum(len(mi.search(ws, f'"{t}"', limit=50)) for t in [subject, *terms["names"]] if mi_terms(t))
    regexes = matchers(subject, terms)
    root = ms.ws_path(ws)
    files = [p for p in root.rglob("*") if p.is_file() and p.name != FORGET_LOG]
    cites = [p for p in files if any(rx.search(p.read_bytes().decode("utf-8", "ignore")) for rx in regexes)]
    exports = [p for p in map(Path, md.export_paths(ws)) if p.is_file()
               and any(rx.search(p.read_text(encoding="utf-8")) for rx in regexes)]
    return {"busca_hits": hits, "arquivos_com_mencao": [str(p.relative_to(root)) for p in cites],
            "exports_com_mencao": [str(p) for p in exports], "arquivos_examinados": len(files) + len(exports)}


def mi_terms(text):
    return bool(re.findall(r"\w+", text or ""))


# ── retenção ─────────────────────────────────────────────────────────────

DEFAULT_RETENTION_DAYS = 90     # o mesmo padrão que o consentimento mostra (core.js retention_days)
UNPUBLISHED_LIMIT_DAYS = 180    # ponytail: gravado e nunca publicado vence aqui, contado do envio do intake;
                                # virar campo do show-profile se algum host precisar de outro prazo


def started_at(ws, record, files):
    """Início do episódio para quem nunca publicou: 1º envio de intake ou 1ª transição registrada."""
    stamps = [ms.read_json(p).get("submitted_at") for k, p in files if k == "intake"]
    stamps += [h.get("at") for h in record.get("history") or []]
    days = [datetime.fromisoformat(t.replace("Z", "+00:00")).date() for t in stamps if t]
    return min(days) if days else None


def due_date(record, started=None):
    """Data em que o dado do titular vence (ALQERA PRV-001). delete_after prevalece; sem prazo gravado,
    vale o padrão do consentimento; sem publicação, o prazo-limite contado do início."""
    ret = record.get("retention") or {}
    if ret.get("delete_after"):
        return date.fromisoformat(ret["delete_after"])
    if not ret.get("subject_ids"):
        return None
    days = ret.get("days_after_publish")
    days = DEFAULT_RETENTION_DAYS if days is None else int(days)
    published = record.get("published_at")
    if published:
        return datetime.fromisoformat(published.replace("Z", "+00:00")).date() + timedelta(days=days)
    return started + timedelta(days=UNPUBLISHED_LIMIT_DAYS) if started else None


def episode_matchers(record, files):
    """Identificadores de TODO titular do episódio (ids + nome, @, e-mail e telefone dos intakes)."""
    terms = {"names": list(record["retention"]["subject_ids"]), "phones": [], "review": []}
    for kind, path in files:
        if kind == "intake":
            for key, vals in known_terms(ms.read_json(path)).items():
                terms[key] += vals
    return matchers("", terms)


def scrub_episode(ws, eid, regexes, apply):
    """Redige o titular em todo arquivo do episódio (research, pauta, script, record, .md). -> nomes."""
    out = []
    for path in sorted(ms.episode_dir(ws, eid).iterdir()):
        if path.suffix == ".json":
            doc = ms.read_json(path)
            new = scrub(doc, "", regexes, {"itens_removidos": 0, "mencoes_redigidas": 0})
            changed, write = new != doc, lambda p=path, n=new: ms.write_json(p, n)
        elif path.suffix == ".md":
            text = path.read_text(encoding="utf-8")
            new = text
            for rx in regexes:
                new = rx.sub(REDACTED, new)
            changed, write = new != text, lambda p=path, n=new: p.write_text(n, encoding="utf-8")
        else:
            continue
        if changed:
            out.append(path.name)
            if apply:
                write()
    return out


def retention(ws, today=None, apply=False):
    """[{episode_id, vence_em, apagar, redigir}] dos episódios vencidos: apaga intake/dossiê e redige o
    titular no resto do episódio; aplica com apply=True. Episódio sem nada a fazer não aparece."""
    today = today or date.today()
    out = []
    for eid in ms.episode_ids(ws):
        record = ms.load_record(ws, eid)
        files = ms.artifact_files(ws, eid)
        due = due_date(record, started_at(ws, record, files))
        if due is None or due > today:
            continue
        drop = [(k, p) for k, p in files if k in ("intake", "dossier")]
        regexes = episode_matchers(record, files)
        redact = [n for n in scrub_episode(ws, eid, regexes, False) if n not in {p.name for _k, p in drop}]
        if not drop and not redact:
            continue
        out.append({"episode_id": eid, "vence_em": due.isoformat(), "apagar": [p.name for _k, p in drop],
                    "redigir": redact})
        if apply:
            apply_retention(ws, record, drop, regexes)
    if apply and out:
        mi.rebuild(ws)
    return out


def apply_retention(ws, record, files, regexes):
    keep = record["retention"].get("keep_consent_record", True)
    for kind, path in files:
        drop_artifact(ws, record, kind, path, ms.read_json(path), keep)
    ms.save_record(ws, record)
    scrub_episode(ws, record["episode_id"], regexes, True)   # reescreve o record também (subject_ids)
    record = ms.load_record(ws, record["episode_id"])
    record["retention"]["applied_at"] = ms.now_iso()
    ms.save_record(ws, record)
