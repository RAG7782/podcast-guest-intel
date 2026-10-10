#!/usr/bin/env python3
"""Ponte com o "segundo cérebro" do usuário (F6): Markdown com frontmatter (Obsidian/Logseq).

export-md: um .md por episódio, frontmatter YAML (valores em JSON, que é YAML válido) com
           type/episode_id/status/date/series/guests/themes/tags; corpo sem URL nua, tabelas
           com pipe escapado (passa no markdownlint do repo).
import-md: OPT-IN explícito e só a pasta indicada pelo usuário. Cada nota vira
           <ws>/notes/<id>.json com origin=manager_material (material do gestor, contracts/claim
           origin). Nota com `private: true` ou `podcast: false` no frontmatter é pulada.
           Link simbólico para fora da pasta é recusado. O vault nunca é escrito.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import memory_store as ms  # noqa: E402

MAX_NOTE_BYTES = 1 << 20
ORIGIN = "manager_material"


# ── export ───────────────────────────────────────────────────────────────

def yaml_list(key, items):
    return [f"{key}: []"] if not items else [f"{key}:"] + [f"  - {json.dumps(i, ensure_ascii=False)}" for i in items]


def guest_name(ref):
    return re.split(r" \(| — ", str(ref))[0].strip()


def frontmatter(rec):
    themes = rec.get("themes") or []
    tags = ["podcast/episodio", f"podcast/status/{rec['status']}"] + [f"tema/{ms.slug(t)}" for t in themes if ms.slug(t)]
    lines = ["---", "type: episodio-podcast", f"episode_id: {rec['episode_id']}",
             f"title: {json.dumps(rec.get('title', ''), ensure_ascii=False)}", f"status: {rec['status']}",
             f"date: {(rec.get('published_at') or '')[:10] or 'null'}",
             f"series: {json.dumps(rec.get('series_ref', ''), ensure_ascii=False)}"]
    lines += yaml_list("guests", [f"[[{guest_name(g)}]]" for g in rec.get("guest_refs") or []])
    lines += yaml_list("themes", themes) + yaml_list("tags", tags)
    return lines + ["source: podcast-memory", "---", ""]


def cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


def section(title, lines):
    return ["", f"## {title}", ""] + lines if lines else []


def clips_table(clips):
    if not clips:
        return []
    rows = ["| Plataforma | Link | Postado em | Métricas |", "| --- | --- | --- | --- |"]
    for c in clips:
        metrics = ", ".join(f"{k}={v}" for k, v in sorted((c.get("metrics") or {}).items()))
        rows.append(f"| {cell(c['platform'])} | <{c['url']}> | {cell(c.get('posted_at', ''))} | {cell(metrics)} |")
    return rows


def artifact_lines(rec):
    arts = rec.get("artifacts") or {}
    out = []
    for key in ("intake", "dossier", "research", "pauta", "script", "recording", "transcript", "edits"):
        for ref in ms.slot_refs(arts, key):
            out.append(f"- {key}: `{ref.get('ref') if isinstance(ref, dict) else ref}`")
    return out


def episode_markdown(rec):
    head = [f"- Status: {rec['status']}"]
    head += [f"- Publicado em: {rec['published_at'][:10]}"] if rec.get("published_at") else []
    head += [f"- Link: <{rec['published_url']}>"] if rec.get("published_url") else []
    head += [f"- Série: {rec['series_ref']}"] if rec.get("series_ref") else []
    metrics = [f"- {k}: {v}" for k, v in sorted((rec.get("metrics") or {}).items())]
    body = ["", f"# {rec.get('title') or rec['episode_id']}", ""] + head
    body += section("Convidados", [f"- [[{guest_name(g)}]]" for g in rec.get("guest_refs") or []])
    body += section("Temas", [f"- {t}" for t in rec.get("themes") or []])
    body += section("Métricas", metrics) + section("Lições", [f"- {x}" for x in rec.get("lessons") or []])
    body += section("Cortes postados", clips_table((rec.get("artifacts") or {}).get("clips")))
    return "\n".join(frontmatter(rec)[:-1] + body + section("Artefatos", artifact_lines(rec))) + "\n"


EXPORTS_LOG = "exports.json"   # destinos já escritos: o forget redige e confere também esses (CRITIC C3)


def export_paths(ws):
    path = ms.ws_path(ws) / EXPORTS_LOG
    return ms.read_json(path) if path.is_file() else []


def export_md(ws, out_dir, episode_ids=None):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    written = []
    for eid in episode_ids or ms.episode_ids(ws):
        path = out / f"{eid}.md"
        path.write_text(episode_markdown(ms.load_record(ws, eid)), encoding="utf-8")
        written.append(str(path))
    known = export_paths(ws)
    ms.write_json(ms.ws_path(ws) / EXPORTS_LOG, known + [str(Path(w).resolve()) for w in written
                                                         if str(Path(w).resolve()) not in known])
    return written


# ── import ───────────────────────────────────────────────────────────────

def parse_scalar(value):
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        return [parse_scalar(v) for v in value[1:-1].split(",") if v.strip()]
    if len(value) > 1 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return {"true": True, "false": False, "null": None, "": None}.get(value.lower(), value)


UNPARSED = "__linhas_nao_lidas__"


def parse_frontmatter(text):
    """(meta, corpo). Subconjunto de YAML: `chave: valor`, listas `- item` e `[a, b]`."""
    # ponytail: parser mínimo, stdlib. Teto: YAML aninhado/multilinha vira string ou some.
    # Upgrade: pyyaml (já é dependência do check) quando o vault usar YAML rico.
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if not match:
        return {}, text
    meta, key = {}, None
    for line in match.group(1).splitlines():
        item = re.match(r"^\s+-\s*(.*)$", line)
        if item and key:
            meta[key] = (meta[key] if isinstance(meta.get(key), list) else []) + [parse_scalar(item.group(1))]
        elif re.match(r"^[\w-]+\s*:", line):
            key, _, value = line.partition(":")
            key = key.strip()
            meta[key] = parse_scalar(value)
        elif line.strip() and not line.lstrip().startswith("#"):
            meta.setdefault(UNPARSED, []).append(line)   # gatilho DEBT-017: o import reporta, não some
    return meta, text[match.end():]


def note_record(path, root, meta, body, text):
    rel = path.relative_to(root)
    title = meta.get("title") or path.stem
    tags = meta.get("tags") or []
    return {"note_id": ms.slug(str(rel.with_suffix(""))) or ms.sha256_text(str(rel))[:16], "origin": ORIGIN,
            "source_path": str(path), "imported_at": ms.now_iso(), "sha256": ms.sha256_text(text),
            "title": str(title), "tags": tags if isinstance(tags, list) else [str(tags)],
            "episode_ref": meta.get("episode") or meta.get("episode_id"), "date": str(meta.get("date") or ""),
            "body": body.strip()}


def path_skip_reason(path, root):
    """Antes de LER: nada fora da pasta indicada entra, nem por link simbólico."""
    if not path.resolve().is_relative_to(root.resolve()):
        return "link para fora da pasta indicada"
    if path.stat().st_size > MAX_NOTE_BYTES:
        return f"maior que {MAX_NOTE_BYTES} bytes"
    return None


YES = {True, "yes", "y", "on", "1", "sim"}   # YAML 1.1 do Obsidian: `private: yes` é verdadeiro (CRITIC M6)
NO = {False, "no", "n", "off", "0", "nao", "não"}


def meta_skip_reason(meta):
    private, podcast = (v.lower() if isinstance(v, str) else v for v in (meta.get("private"), meta.get("podcast")))
    if private in YES or podcast in NO:
        return "nota marcada private:true/yes ou podcast:false/no"
    return None


def import_md(ws, folder, opt_in=False):
    """{importadas, puladas:[(arquivo, motivo)]}. Sem opt_in: recusa e não escreve nada."""
    if opt_in is not True:
        raise ms.MemoryError_("import-md sem opt-in | esperado: --opt-in explícito (o usuário escolhe "
                              "ligar o segundo cérebro e qual pasta entra)")
    root = Path(folder)
    if not root.is_dir():
        raise ms.MemoryError_(f"pasta={folder!r} não existe | esperado: diretório do vault indicado pelo usuário")
    notes_dir = ms.ws_path(ws) / ms.NOTES
    done, skipped, partial = [], [], []
    for path in sorted(root.rglob("*.md")):
        reason = path_skip_reason(path, root)
        text = "" if reason else path.read_text(encoding="utf-8", errors="replace")
        meta, body = parse_frontmatter(text)
        reason = reason or meta_skip_reason(meta)
        if reason:
            skipped.append((str(path), reason))
            continue
        note = note_record(path, root, meta, body, text)
        if note["note_id"] in done:   # a/b.md e a-b.md têm o mesmo slug: não sobrescrever em silêncio
            note["note_id"] += "-" + ms.sha256_text(str(path.relative_to(root)))[:8]
        ms.write_json(notes_dir / f"{note['note_id']}.json", note)
        done.append(note["note_id"])
        if meta.get(UNPARSED):
            partial.append((str(path), f"{len(meta[UNPARSED])} linha(s) de frontmatter não lida(s): YAML aninhado"
                                       " ou multilinha (DEBT-017)"))
    return {"importadas": done, "puladas": skipped, "frontmatter_parcial": partial}
