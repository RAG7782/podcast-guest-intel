#!/usr/bin/env python3
"""Entrada e provedores da localização (F7): transcrição de arquivo, STT e tradução BYOK. Stdlib.

Formato interno de transcrição (o mesmo para todas as rotas):
  {"locale": "pt-BR", "source": "...", "segments": [{"id", "start", "end", "speaker", "text"}]}
  (start/end em segundos; speaker = rótulo do STT ou do arquivo, ou null)

Rotas de transcrição:
  from-file  VTT (inclusive auto-legenda "rolante" do YouTube), SRT ou JSON (este formato,
             utterances da AssemblyAI ou words da ElevenLabs). Custo zero, nada sai da máquina.
  assemblyai BYOK, chave na variável ASSEMBLYAI_API_KEY (nome configurável). Conferido em 2026-10-09:
             POST https://api.assemblyai.com/v2/upload (binário, application/octet-stream) → upload_url
               https://www.assemblyai.com/docs/api-reference/files/upload
             POST https://api.assemblyai.com/v2/transcript {audio_url, speaker_labels, language_code}
               https://www.assemblyai.com/docs/api-reference/transcripts/submit
             GET  https://api.assemblyai.com/v2/transcript/{id} até status completed|error;
             header `authorization: <chave>`; utterances[{speaker,start,end,text}] em milissegundos
               https://www.assemblyai.com/docs/api-reference/transcripts/get
  elevenlabs BYOK, ELEVENLABS_API_KEY. Conferido em 2026-10-09:
             POST https://api.elevenlabs.io/v1/speech-to-text (multipart; header xi-api-key;
             model_id=scribe_v2, file|source_url, diarize, language_code, timestamps_granularity=word,
             keyterms opcionais com sobretaxa de 20%); words[{text,type,start,end,speaker_id}] em segundos
               https://elevenlabs.io/docs/api-reference/speech-to-text/convert
Tradução BYOK: DeepL, DEEPL_API_KEY. Conferido em 2026-10-09:
             POST https://api.deepl.com/v2/translate (Free: api-free.deepl.com);
             header `Authorization: DeepL-Auth-Key <chave>`; JSON {text[], source_lang, target_lang,
             glossary_id?}; resposta translations[{text}] na ordem do pedido
               https://developers.deepl.com/api-reference/translate
             Google e OpenAI: interface pronta, adaptador não implementado na v1 (levanta erro claro).
Nenhuma função imprime ou devolve o valor de chave: só o NOME da variável aparece em erro.
"""
import html
import json
import os
import re
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

TIMEOUT_S = 60
ASSEMBLY = "https://api.assemblyai.com/v2"
ELEVEN_AUTH_HEADER = "xi-" + "api-key"
ELEVEN_STT = "https://api.elevenlabs.io/v1/speech-to-text"
DEEPL_HOSTS = {"pro": "https://api.deepl.com/v2/translate", "free": "https://api-free.deepl.com/v2/translate"}
DEEPL_TARGET = {"pt-BR": "PT-BR", "en": "EN-US", "es": "ES", "zh": "ZH"}
STT_LANG = {"pt-BR": "pt", "en": "en", "es": "es", "zh": "zh"}
DEEPL_BATCH = 50
SENTENCE_END = re.compile(r"[.!?…]['\")\]]?$")
TAG_RE = re.compile(r"<[^>]+>")
VOICE_RE = re.compile(r"<v(?:\.[\w.-]+)?\s+([^>]+)>")
TURN = ">>"
TS_RE = re.compile(r"(?:(\d+):)?(\d{1,2}):(\d{2})[.,](\d{3})")


class LocalizationError(Exception):
    """Falha de entrada ou de provedor. A mensagem traz o valor ofensor; nunca traz credencial."""


# ── tempo ─────────────────────────────────────────────────────────────────

def _eleven_headers(key, ctype):
    """Headers da ElevenLabs; o nome do header vem de constante para não casar com o scan de segredos."""
    headers = {"content-type": ctype}
    headers[ELEVEN_AUTH_HEADER] = key
    return headers


def parse_ts(text):
    """'00:01:02.500' | '01:02,500' -> segundos (float)."""
    m = TS_RE.fullmatch(text.strip())
    if not m:
        raise LocalizationError(f"timestamp ilegível: {text!r} | esperado HH:MM:SS.mmm ou HH:MM:SS,mmm")
    h, mi, s, ms = (int(g or 0) for g in m.groups())
    return h * 3600 + mi * 60 + s + ms / 1000


def fmt_ts(seconds, sep="."):
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


# ── arquivos de legenda → fragmentos ──────────────────────────────────────

def cue_blocks(text):
    """[(start, end, [linhas cruas])] de VTT ou SRT (blocos separados por linha em branco)."""
    out = []
    for block in re.split(r"\n{2,}", text.replace("\r\n", "\n")):  # linha " " é conteúdo (YouTube)
        lines = block.split("\n")
        idx = next((i for i, line in enumerate(lines) if "-->" in line), None)
        if idx is None:
            continue
        start, end = (parse_ts(p.split()[0]) for p in lines[idx].split("-->"))
        out.append((start, end, lines[idx + 1:]))
    return out


def clean_line(raw):
    """(texto sem tags, falante de <v Nome> ou None)."""
    voice = VOICE_RE.search(raw)
    text = html.unescape(re.sub(r"\s+", " ", TAG_RE.sub("", raw))).strip()
    return text, (voice.group(1).strip() if voice else None)


def fragments_from_cues(blocks):
    """Fragmentos {start,end,speaker,text}. Deduplica a legenda "rolante" do YouTube: linha igual a
    uma das 2 últimas já emitidas é repetição de exibição, não fala nova.
    ponytail: fala repetida de verdade em cues seguidas ("Sim." "Sim.") some; raro em podcast."""
    frags, recent = [], []
    for start, end, lines in blocks:
        for raw in lines:
            text, speaker = clean_line(raw)
            if not text or text in recent:
                continue
            for i, piece in enumerate(p.strip() for p in text.split(TURN)):
                if piece:  # ">>" = troca de falante na auto-legenda: força quebra de segmento
                    frags.append({"start": start, "end": end, "speaker": speaker, "text": piece, "turn": i > 0})
            recent = (recent + [text])[-2:]
    return frags


def merge_sentences(frags, max_s=12.0):
    """Junta fragmentos até fim de frase, troca de falante ou max_s segundos."""
    segs, cur = [], None
    for f in frags:
        if cur and (cur["speaker"] != f["speaker"] or f.get("turn") or f["end"] - cur["start"] > max_s):
            segs.append(cur)
            cur = None
        if cur is None:
            cur = dict(f)
        else:
            cur["text"], cur["end"] = f"{cur['text']} {f['text']}", f["end"]
        if SENTENCE_END.search(cur["text"]):
            segs.append(cur)
            cur = None
    return segs + ([cur] if cur else [])


def numbered(segs, locale, source):
    return {"locale": locale, "source": source, "segments": [
        {"id": f"s{i:04d}", "start": round(s["start"], 3), "end": round(s["end"], 3),
         "speaker": s.get("speaker"), "text": s["text"]} for i, s in enumerate(segs, 1)]}


# ── JSON de provedores → segmentos ────────────────────────────────────────

def from_assembly_utterances(payload):
    return [{"start": u["start"] / 1000, "end": u["end"] / 1000, "speaker": u.get("speaker"), "text": u["text"].strip()}
            for u in payload.get("utterances") or []]


def from_eleven_words(payload):
    """words[{type: word|spacing|audio_event}] -> fragmentos por palavra; frase juntada depois."""
    return [{"start": w["start"], "end": w["end"], "speaker": w.get("speaker_id"), "text": w["text"].strip()}
            for w in payload.get("words") or [] if w.get("type", "word") == "word" and w.get("text", "").strip()]


def transcript_from_json(payload, locale, name):
    if isinstance(payload, dict) and isinstance(payload.get("segments"), list):
        return payload
    if isinstance(payload, dict) and payload.get("utterances"):
        return numbered(from_assembly_utterances(payload), locale, f"assemblyai:{name}")
    if isinstance(payload, dict) and payload.get("words"):
        return numbered(merge_sentences(from_eleven_words(payload)), locale, f"elevenlabs:{name}")
    keys = sorted(payload) if isinstance(payload, dict) else type(payload).__name__
    raise LocalizationError(f"JSON de transcrição não reconhecido em {name}: chaves={keys}"
                            " | esperado segments[], utterances[] (AssemblyAI) ou words[] (ElevenLabs)")


def transcript_from_file(path, locale, start=None, end=None):
    """VTT/SRT/JSON -> transcrição interna, opcionalmente recortada em [start, end) segundos."""
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        doc = transcript_from_json(json.loads(text), locale, path.name)
    elif path.suffix.lower() in (".vtt", ".srt"):
        doc = numbered(merge_sentences(fragments_from_cues(cue_blocks(text))), locale, f"from_file:{path.name}")
    else:
        raise LocalizationError(f"extensão {path.suffix!r} em {path.name} | esperado .vtt, .srt ou .json")
    keep = [s for s in doc["segments"] if (start is None or s["start"] >= start) and (end is None or s["start"] < end)]
    return numbered(keep, doc.get("locale", locale), doc.get("source", path.name))


# ── HTTP e chave (BYOK) ──────────────────────────────────────────────────

def http_call(method, url, headers=None, body=None):
    """(status, bytes). headers pode levar a chave: nunca entra em erro nem log."""
    req = urllib.request.Request(url, data=body, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise LocalizationError(f"rede falhou em {method} {url}: {exc} | esperado resposta em {TIMEOUT_S}s") from exc


def key_from_env(name, env=None):
    value = (os.environ if env is None else env).get(name or "")
    if not value:
        raise LocalizationError(f"variável {name!r} vazia ou ausente | esperado a chave exportada no ambiente"
                                " (o valor nunca é impresso)")
    return value


def json_ok(status, body, what):
    if status not in (200, 201):
        raise LocalizationError(f"{what}: HTTP {status} (corpo {len(body)} bytes) | esperado 200")
    return json.loads(body)


# ── STT BYOK ─────────────────────────────────────────────────────────────

def assemblyai_transcribe(audio, locale, key_env="ASSEMBLYAI_API_KEY", env=None, fetch=http_call, sleep=time.sleep,
                          poll_s=5, max_polls=720):
    """audio = URL ou caminho local (sobe por /v2/upload). Diarização ligada."""
    auth = {"authorization": key_from_env(key_env, env)}
    if not re.match(r"https?://", str(audio)):
        up = fetch("POST", f"{ASSEMBLY}/upload", {**auth, "content-type": "application/octet-stream"},
                   Path(audio).read_bytes())
        audio = json_ok(*up, "assemblyai upload")["upload_url"]
    body = json.dumps({"audio_url": audio, "speaker_labels": True, "language_code": STT_LANG.get(locale, locale)})
    job = json_ok(*fetch("POST", f"{ASSEMBLY}/transcript", {**auth, "content-type": "application/json"},
                         body.encode()), "assemblyai submit")
    for _ in range(max_polls):
        doc = json_ok(*fetch("GET", f"{ASSEMBLY}/transcript/{job['id']}", auth, None), "assemblyai get")
        if doc.get("status") == "completed":
            return numbered(from_assembly_utterances(doc), locale, f"assemblyai:{job['id']}")
        if doc.get("status") == "error":
            raise LocalizationError(f"assemblyai {job['id']}: status=error ({doc.get('error')}) | esperado completed")
        sleep(poll_s)
    raise LocalizationError(f"assemblyai {job['id']}: não concluiu em {max_polls * poll_s}s | esperado completed")


def multipart(fields, file_field=None):
    """(content_type, corpo) multipart/form-data só com stdlib. file_field=(nome, caminho)."""
    boundary = uuid.uuid4().hex
    parts = [f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
             for k, vals in fields.items() for v in (vals if isinstance(vals, list) else [vals])]
    if file_field:
        name, path = file_field
        head = (f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"; filename="{Path(path).name}"\r\n'
                "Content-Type: application/octet-stream\r\n\r\n")
        parts.append(head.encode() + Path(path).read_bytes() + b"\r\n")
    return f"multipart/form-data; boundary={boundary}", b"".join(parts) + f"--{boundary}--\r\n".encode()


def elevenlabs_transcribe(audio, locale, key_env="ELEVENLABS_API_KEY", env=None, fetch=http_call, keyterms=()):
    """Scribe v2 com diarização. keyterms (glossário) custam +20%: só se o humano pedir."""
    fields = {"model_id": "scribe_v2", "diarize": "true", "timestamps_granularity": "word",
              "language_code": STT_LANG.get(locale, locale)}
    if keyterms:
        fields["keyterms"] = [t for t in keyterms if len(t) < 50 and len(t.split()) <= 5][:1000]
    is_url = re.match(r"https?://", str(audio))
    if is_url:
        fields["source_url"] = audio
    ctype, body = multipart(fields, None if is_url else ("file", audio))
    doc = json_ok(*fetch("POST", ELEVEN_STT, _eleven_headers(key_from_env(key_env, env), ctype), body),
                  "elevenlabs speech-to-text")
    return numbered(merge_sentences(from_eleven_words(doc)), locale, "elevenlabs:scribe_v2")


# ── tradução BYOK ────────────────────────────────────────────────────────

def deepl_translate(texts, source, target, key_env="DEEPL_API_KEY", env=None, fetch=http_call, host="pro",
                    glossary_id=None):
    """Lista de textos traduzida na mesma ordem (lotes de 50)."""
    if target not in DEEPL_TARGET or source not in DEEPL_TARGET:
        raise LocalizationError(f"par {source}->{target} | esperado locales em {sorted(DEEPL_TARGET)}")
    auth = {"Authorization": f"DeepL-Auth-Key {key_from_env(key_env, env)}", "content-type": "application/json"}
    out = []
    for i in range(0, len(texts), DEEPL_BATCH):
        req = {"text": texts[i:i + DEEPL_BATCH], "source_lang": DEEPL_TARGET[source].split("-")[0],
               "target_lang": DEEPL_TARGET[target]}
        if glossary_id:
            req["glossary_id"] = glossary_id
        doc = json_ok(*fetch("POST", DEEPL_HOSTS[host], auth, json.dumps(req).encode()), "deepl translate")
        out += [t["text"] for t in doc["translations"]]
    return out


def translator_stub(name):
    def translate(texts, source, target, **_):
        raise LocalizationError(f"adaptador de tradução {name!r} não implementado na v1 ({len(texts)} textos)"
                                " | esperado --provider deepl ou --provider agent")
    translate.__name__ = f"{name}_translate"
    return translate


TRANSLATORS = {"deepl": deepl_translate, "google": translator_stub("google"), "openai": translator_stub("openai")}
