#!/usr/bin/env python3
"""Armazenamento de referência da memória do show (F6): arquivos = fonte da verdade.

Layout do workspace (o índice SQLite é cache reconstruível, ver memory_index.py):
  <ws>/memory.json                                  config do workspace (show_ref, retenção)
  <ws>/episodes/<episode_id>/episode-record.json    references/contracts/episode-record.schema.json
  <ws>/episodes/<episode_id>/<tipo>[-N].json        artefatos validados (intake, dossier, pauta, script, research)
  <ws>/notes/<note_id>.json                         notas importadas do segundo cérebro (origin=manager_material)
  <ws>/consent-records/<sha>.json                   só o registro do consentimento, sem identificação
Validação de schema reusa scripts/validate-contracts.py (jsonschema + pyyaml, import tardio):
leitura, busca e export funcionam só com stdlib.
"""
import hashlib
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dossier_tools import load_validator  # noqa: E402
from pauta_tools import norm, now_iso  # noqa: E402  (fonte única de normalização PT e de timestamp)

CONFIG = "memory.json"
RECORD = "episode-record.json"
EPISODES = "episodes"
NOTES = "notes"
CONSENTS = "consent-records"
ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{1,63}$")
STATUSES = ["idea", "planning", "briefing", "guest_outreach", "guest_confirmed", "pre_production",
            "ready_to_record", "recording_scheduled", "recorded", "editing", "review",
            "ready_to_publish", "publishing", "published", "repurposing", "archived"]
# tipo -> (schema, chave do envelope, slot em artifacts, aceita vários)
TYPES = {
    "intake": ("guest-intake", None, "intake", True),
    "dossier": ("guest-dossier", "dossier", "dossier", True),
    "pauta": ("pauta", "pauta", "pauta", False),
    "script": ("script", None, "script", True),
    "research": (None, None, "research", False),
    "decision": ("human-decision", None, "decisions", True),
}
MEDIA = {"recording": "recording", "transcript": "transcript", "edit": "edits"}
_VALIDATOR = None


class MemoryError_(Exception):
    """Erro de uso/integridade da memória; a mensagem traz valor ofensor e shape esperado."""


# ── utilitários ───────────────────────────────────────────────────────────

def slug(text, limit=60):
    out = re.sub(r"[^a-z0-9]+", "-", norm(text)).strip("-")[:limit].strip("-")
    return out if len(out) >= 2 else ""


def sha256_text(text):
    return hashlib.sha256(str(text).encode("utf-8")).hexdigest()


def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise MemoryError_(f"erro ao ler {path}: {exc} | esperado: arquivo JSON legível")


def write_json(path, doc):
    """Escrita atômica (tmp + replace): queda no meio não deixa JSON truncado."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


# ── validação (fonte única: validate-contracts.py) ────────────────────────

def violations(schema_name, doc):
    global _VALIDATOR
    if _VALIDATOR is None:
        mod = load_validator()
        _VALIDATOR = (mod, *mod.load_schemas())
    mod, schemas, registry = _VALIDATOR
    return mod.check(schema_name, doc, schemas, registry)


def require_valid(schema_name, doc, what):
    errs = violations(schema_name, doc)
    if errs:
        raise MemoryError_(f"{what} inválido contra {schema_name}.schema.json ({len(errs)} violação(ões)): "
                           + " ; ".join(errs[:3]))


# ── workspace ─────────────────────────────────────────────────────────────

def ws_path(ws):
    path = Path(ws)
    if not (path / CONFIG).is_file():
        raise MemoryError_(f"workspace sem {CONFIG}: {path} | esperado: rodar `memory_tools.py init` antes")
    return path


def config(ws):
    return read_json(ws_path(ws) / CONFIG)


def init_workspace(ws, show_ref, retention_days=None):
    path = Path(ws)
    if not ID_RE.match(show_ref or ""):
        raise MemoryError_(f"show_ref={show_ref!r} | esperado: id {ID_RE.pattern}")
    cfg = {"schema": "podcast-memory/v1", "show_ref": show_ref, "created_at": now_iso(),
           "retention_days_after_publish": retention_days}
    if (path / CONFIG).is_file():
        cfg = dict(read_json(path / CONFIG), show_ref=show_ref, retention_days_after_publish=retention_days)
    write_json(path / CONFIG, cfg)
    for sub in (EPISODES, NOTES):
        (path / sub).mkdir(parents=True, exist_ok=True)
    return cfg


def episode_dir(ws, episode_id):
    if not ID_RE.match(episode_id or ""):
        raise MemoryError_(f"episode_id={episode_id!r} | esperado: {ID_RE.pattern}")
    return ws_path(ws) / EPISODES / episode_id


def episode_ids(ws):
    root = ws_path(ws) / EPISODES
    return sorted(p.name for p in root.iterdir() if (p / RECORD).is_file()) if root.is_dir() else []


def load_record(ws, episode_id):
    path = episode_dir(ws, episode_id) / RECORD
    if not path.is_file():
        raise MemoryError_(f"episódio {episode_id!r} não existe em {ws} | esperado: `new` antes de `add`")
    return read_json(path)


def save_record(ws, record):
    require_valid("episode-record", record, f"episode-record {record.get('episode_id')!r}")
    write_json(episode_dir(ws, record["episode_id"]) / RECORD, record)


def new_record(ws, episode_id, title="", status="idea", **extra):
    cfg = config(ws)
    if (episode_dir(ws, episode_id) / RECORD).is_file():
        raise MemoryError_(f"episódio {episode_id!r} já existe | esperado: id novo ou `add` no existente")
    record = {"episode_id": episode_id, "show_ref": cfg["show_ref"], "title": title, "status": status,
              "artifacts": {}, "retention": {"subject_ids": [], "keep_consent_record": True}}
    record.update({k: v for k, v in extra.items() if v not in (None, "", [])})
    save_record(ws, record)
    return record


# ── artefatos ─────────────────────────────────────────────────────────────

def unwrap(kind, doc):
    """(documento interno validado, documento a guardar). Envelope é guardado inteiro."""
    key = TYPES[kind][1]
    if key and isinstance(doc, dict) and isinstance(doc.get(key), dict):
        return doc[key], doc
    if not isinstance(doc, (dict, list)):
        raise MemoryError_(f"artefato {kind} é {type(doc).__name__} | esperado: objeto JSON")
    return doc, doc


def artifact_id(kind, inner):
    if not isinstance(inner, dict):
        return None
    keys = {"intake": "intake_id", "dossier": "dossier_id", "pauta": "pauta_id", "decision": "decision_id"}
    if kind == "script":
        return (inner.get("meta") or {}).get("script_id")
    return inner.get(keys.get(kind, ""))


def slot_refs(artifacts, slot):
    value = artifacts.get(slot)
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def set_slot(artifacts, slot, refs, multi):
    refs = [r for r in refs if isinstance(r, str)]
    if not refs:
        artifacts.pop(slot, None)
    else:
        artifacts[slot] = refs if (multi and len(refs) > 1) else refs[0]


def find_same(edir, refs, kind, art_id):
    for ref in refs:
        path = edir / ref
        if art_id and path.is_file() and artifact_id(kind, unwrap(kind, read_json(path))[0]) == art_id:
            return ref
    return None


def free_name(kind, refs):
    names = {kind + ".json"} | {f"{kind}-{n}.json" for n in range(2, 100)}
    for name in sorted(names, key=lambda s: (len(s), s)):
        if name not in refs:
            return name
    raise MemoryError_(f"mais de 99 artefatos {kind} no episódio | esperado: menos de 100")


def validate_artifact(kind, doc):
    if kind not in TYPES:
        raise MemoryError_(f"tipo={kind!r} | esperado um de {sorted(TYPES) + sorted(MEDIA)}")
    inner, stored = unwrap(kind, doc)
    schema = TYPES[kind][0]
    if schema:
        require_valid(schema, inner, f"artefato {kind}")
    return inner, stored


def add_artifact(ws, episode_id, kind, doc):
    """Valida, grava o arquivo e liga ao episode-record. Inválido nunca chega ao disco."""
    record = load_record(ws, episode_id)
    inner, stored = validate_artifact(kind, doc)
    _schema, _key, slot, multi = TYPES[kind]
    arts = record["artifacts"]
    if kind == "decision":
        arts["decisions"] = [d for d in arts.get("decisions", []) if d.get("decision_id") != inner["decision_id"]]
        arts["decisions"].append(inner)
        save_record(ws, record)
        return record, None
    refs = slot_refs(arts, slot)
    edir = episode_dir(ws, episode_id)
    ref = find_same(edir, refs, kind, artifact_id(kind, inner)) or free_name(kind, refs)
    write_json(edir / ref, stored)
    set_slot(arts, slot, refs + ([ref] if ref not in refs else []), multi)
    link_subject(record, kind, inner, config(ws).get("retention_days_after_publish"))
    save_record(ws, record)
    return record, ref


def link_subject(record, kind, inner, days=None):
    """Titular entra em retention.subject_ids: é por ali que forget/retention o acham."""
    subject = {"intake": inner.get("intake_id"), "dossier": inner.get("guest_ref")}.get(kind)
    ret = record["retention"]
    if subject and subject not in ret["subject_ids"]:
        ret["subject_ids"].append(subject)
    if subject and days is not None:
        ret.setdefault("days_after_publish", days)  # prazo do show-profile, gravado em init


# ── mídia por referência ─────────────────────────────────────────────────

def file_digest(path):
    """sha256 em blocos de 1 MiB: RAM constante mesmo para vídeo de vários GB."""
    digest, size = hashlib.sha256(), 0
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
            size += len(block)
    return digest.hexdigest(), size


def media_ref(ref, duration_s=None, platform=None, title=None):
    # ponytail: guarda só a REFERÊNCIA (caminho/URL + sha256 + duração); o binário fica onde o
    # usuário já guarda. Teto: arquivo movido/apagado quebra a ref (o sha256 acusa troca de
    # conteúdo). Upgrade: storage de objetos do SaaS, com a mesma ref como chave.
    media = {"ref": ref}
    if Path(ref).is_file():
        media["sha256"], media["bytes"] = file_digest(ref)
    extra = {"duration_s": duration_s, "platform": platform, "title": title}
    media.update({k: v for k, v in extra.items() if v not in (None, "")})
    return media


def add_media(ws, episode_id, kind, media):
    record = load_record(ws, episode_id)
    slot = MEDIA.get(kind)
    if slot is None:
        raise MemoryError_(f"mídia={kind!r} | esperado um de {sorted(MEDIA)}")
    arts = record["artifacts"]
    if slot == "edits":
        arts["edits"] = [e for e in arts.get("edits", []) if (e.get("ref") if isinstance(e, dict) else e) != media["ref"]]
        arts["edits"].append(media)
    else:
        arts[slot] = media
    save_record(ws, record)
    return record


def artifact_files(ws, episode_id):
    """[(tipo, caminho)] dos artefatos em arquivo ligados ao record."""
    record, edir = load_record(ws, episode_id), episode_dir(ws, episode_id)
    out = []
    for kind, (_s, _k, slot, _m) in TYPES.items():
        out += [(kind, edir / ref) for ref in slot_refs(record["artifacts"], slot)
                if isinstance(ref, str) and (edir / ref).is_file()]
    return out
