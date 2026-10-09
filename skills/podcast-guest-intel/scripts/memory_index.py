#!/usr/bin/env python3
"""Índice de busca da memória (F6): SQLite FTS5, stdlib, reconstruível dos arquivos.

O índice é CACHE: `rebuild` apaga o arquivo e reindexa tudo a partir de <ws>/episodes e
<ws>/notes. Tokenização unicode61 com remove_diacritics 2 ("tributária" casa "tributaria").
Journal padrão (DELETE), nunca WAL; nunca abrir com `sqlite3 -readonly`.
"""
import re
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import memory_store as ms  # noqa: E402

INDEX = "memory-index.sqlite"
# Pesos BM25 na ordem das colunas: título e temas pesam mais que corpo (episódio > menção solta).
BM25_WEIGHTS = "0, 0, 0, 0, 0, 0, 4.0, 1.0, 1.0, 2.0"
COLUMNS = ["episode_id", "kind", "ref", "date", "guests_norm", "themes_norm", "title", "body", "guests", "themes"]
SCHEMA = ("CREATE VIRTUAL TABLE docs USING fts5(episode_id UNINDEXED, kind UNINDEXED, ref UNINDEXED, "
          "date UNINDEXED, guests_norm UNINDEXED, themes_norm UNINDEXED, title, body, guests, themes, "
          "tokenize = 'unicode61 remove_diacritics 2')")
# ponytail: busca LEXICAL (FTS5/BM25). Teto: não acha sinônimo nem paráfrase ("IA" ≠
# "inteligência artificial" sem as duas palavras no texto). Upgrade: embeddings no MCP/SaaS
# (Postgres+pgvector ou tsvector, research/04 §5 F6), com este índice como fallback lexical.


def index_path(ws):
    return ms.ws_path(ws) / INDEX


def flatten(node):
    """Todas as strings de um JSON, em ordem (URLs entram: o domínio também é busca)."""
    if isinstance(node, dict):
        return [s for v in node.values() for s in flatten(v)]
    if isinstance(node, list):
        return [s for v in node for s in flatten(v)]
    return [node] if isinstance(node, str) else []


# ── documentos por artefato ───────────────────────────────────────────────

def claim_docs(doc):
    inner = doc.get("dossier", doc)
    return [("claim", c.get("id", ""), c.get("coverage_area") or c.get("id", ""),
             " ".join([c.get("text", "")] + flatten(c.get("sources") or [])))
            for c in inner.get("claims") or [] if isinstance(c, dict)]


def pauta_docs(doc):
    trunks = doc.get("pauta", doc).get("trunks") or {}
    return [("pauta", f"{t}/{it.get('id', '')}", it.get("title", ""),
             " ".join([it.get("rationale", "")] + list(it.get("questions") or [])))
            for t, items in trunks.items() for it in items or [] if isinstance(it, dict)]


def script_docs(doc):
    sid = (doc.get("meta") or {}).get("script_id", "")
    return [("script", f"{sid}#{b.get('ordem', i)}", b.get("titulo", ""), " ".join(flatten(
        {k: v for k, v in b.items() if k in ("texto", "perguntas", "afirmacoes", "beat")})))
            for i, b in enumerate(doc.get("roteiro") or []) if isinstance(b, dict)]


def research_docs(doc):
    items = doc.get("items") if isinstance(doc, dict) else None
    if isinstance(items, list) and items:
        return [("research", str(i), str(it.get("title", "")) if isinstance(it, dict) else "",
                 " ".join(flatten(it))) for i, it in enumerate(items)]
    return [("research", "", "", " ".join(flatten(doc)))]


def intake_docs(doc):
    guest = doc.get("guest") or {}
    return [("intake", doc.get("intake_id", ""), guest.get("full_name", ""),
             " ".join(flatten({k: v for k, v in doc.items() if k not in ("consent", "contacts")})))]


EXPLODE = {"dossier": claim_docs, "pauta": pauta_docs, "script": script_docs,
           "research": research_docs, "intake": intake_docs}


def record_docs(rec):
    head = " ".join(flatten({k: rec.get(k) for k in ("title", "series_ref", "format", "approach_mode",
                                                     "themes", "guest_refs", "published_url")}))
    docs = [("episode", rec["episode_id"], rec.get("title", ""), head)]
    docs += [("lesson", str(i), "", text) for i, text in enumerate(rec.get("lessons") or [])]
    arts = rec.get("artifacts") or {}
    docs += [("clip", c.get("url", ""), c.get("title", ""), " ".join(flatten(c))) for c in arts.get("clips") or []]
    docs += [("decision", d.get("decision_id", ""), d.get("recommendation", {}).get("verdict", ""),
              " ".join(flatten(d))) for d in arts.get("decisions") or []]
    return docs


def episode_rows(ws, episode_id):
    rec = ms.load_record(ws, episode_id)
    guests = list(rec.get("guest_refs") or [])
    docs = record_docs(rec)
    for kind, path in ms.artifact_files(ws, episode_id):
        doc = ms.read_json(path)
        docs += EXPLODE[kind](doc) if kind in EXPLODE else []
        if kind == "intake":
            guests.append((doc.get("guest") or {}).get("full_name", ""))
    date = (rec.get("published_at") or "")[:10]
    themes = " | ".join(rec.get("themes") or [])
    meta = (episode_id, date, ms.norm(" | ".join(guests)), ms.norm(themes), " | ".join(guests), themes)
    return [row(meta, kind, ref, title, body) for kind, ref, title, body in docs]


def row(meta, kind, ref, title, body):
    episode_id, date, guests_norm, themes_norm, guests, themes = meta
    return (episode_id, kind, ref, date, guests_norm, themes_norm, title, body, guests, themes)


def note_rows(ws):
    root = ms.ws_path(ws) / ms.NOTES
    rows = []
    for path in sorted(root.glob("*.json")) if root.is_dir() else []:
        note = ms.read_json(path)
        tags = " | ".join(note.get("tags") or [])
        meta = (note.get("episode_ref") or "", (note.get("date") or "")[:10], "", ms.norm(tags), "", tags)
        rows.append(row(meta, "note", note.get("note_id", path.stem), note.get("title", ""), note.get("body", "")))
    return rows


# ── construção ────────────────────────────────────────────────────────────

def rebuild(ws):
    """Apaga o cache e reconstrói dos arquivos. Devolve o nº de documentos indexados."""
    # ponytail: reconstrução TOTAL a cada escrita (O(docs do workspace)); garante que forget não
    # deixe texto em página livre do SQLite. Teto: ~10^4 episódios fica lento. Upgrade:
    # reindex por episódio (DELETE WHERE episode_id) + VACUUM só no forget.
    path = index_path(ws)
    for leftover in (path, Path(str(path) + "-journal")):
        leftover.unlink(missing_ok=True)
    rows = [r for eid in ms.episode_ids(ws) for r in episode_rows(ws, eid)] + note_rows(ws)
    con = sqlite3.connect(path)
    try:
        con.execute(SCHEMA)
        con.executemany(f"INSERT INTO docs ({', '.join(COLUMNS)}) VALUES ({', '.join('?' * len(COLUMNS))})", rows)
        con.commit()
    finally:
        con.close()
    return len(rows)


def dump(ws):
    """Linhas do índice ordenadas (para conferir que reindex reconstrói igual)."""
    con = sqlite3.connect(index_path(ws))
    try:
        return sorted(con.execute(f"SELECT {', '.join(COLUMNS)} FROM docs").fetchall())
    finally:
        con.close()


# ── busca ─────────────────────────────────────────────────────────────────

def fts_query(text):
    """Termos entre aspas, E implícito (ou frase, se a consulta vier entre aspas): pontuação do usuário nunca vira sintaxe FTS5."""
    raw = str(text or "").strip()
    terms = re.findall(r"\w+", raw)
    if not terms:
        raise ms.MemoryError_(f"consulta={text!r} sem termos | esperado: ao menos uma palavra")
    if len(raw) > 1 and raw[0] == raw[-1] == '"':
        return '"' + " ".join(terms) + '"'  # "entre aspas" = frase exata
    return " ".join(f'"{t}"' for t in terms)


def filters(kind=None, guest=None, theme=None, since=None, until=None):
    clauses, args = [], []
    for cond, value in (("kind = ?", kind), ("instr(guests_norm, ?) > 0", ms.norm(guest) if guest else None),
                        ("instr(themes_norm, ?) > 0", ms.norm(theme) if theme else None),
                        ("date >= ?", since), ("date != '' AND date <= ?", until)):
        if value:
            clauses.append(cond)
            args.append(value)
    return "".join(f" AND {c}" for c in clauses), args


def search(ws, text, limit=10, **flt):
    """[{episode_id, kind, ref, date, title, snippet}] por relevância BM25, trecho com «destaque»."""
    path = index_path(ws)
    if not path.is_file():
        rebuild(ws)
    where, args = filters(**flt)
    sql = (f"SELECT episode_id, kind, ref, date, title, snippet(docs, -1, '«', '»', '…', 14) FROM docs "
           f"WHERE docs MATCH ?{where} ORDER BY bm25(docs, {BM25_WEIGHTS}) LIMIT ?")
    con = sqlite3.connect(path)
    try:
        rows = con.execute(sql, [fts_query(text), *args, int(limit)]).fetchall()
    finally:
        con.close()
    keys = ("episode_id", "kind", "ref", "date", "title", "snippet")
    return [dict(zip(keys, r)) for r in rows]
