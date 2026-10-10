#!/usr/bin/env python3
"""Ferramentas da localização do episódio (task *legendas / *traduzir / *plano-dublagem, F7).

Subcomandos:
  transcribe --provider from-file|assemblyai|elevenlabs ENTRADA --locale L [--start S --end S]
             [--key-env NOME] [--keyterms GLOSSARIO] [--intake ARQ ... | --sem-convidado] -o TRANSCRICAO.json
             assemblyai/elevenlabs: recusa (exit 2) ANTES de subir o áudio sem o aceite translation_text.
             from-file aceita VTT/SRT/JSON já existentes (ex.: auto-legenda do YouTube): custo zero.
  translate  TRANSCRICAO --target L --provider agent|deepl|google|openai [--glossary G] -o SAIDA.json
             agent: grava um PACOTE (segmentos + regras do glossário) para o LLM do harness preencher
             translated_text; depois `translate --merge PACOTE -o SAIDA`. deepl: BYOK (DEEPL_API_KEY).
             BYOK exige --intake com aceite translation_text do idioma (ou --sem-convidado), antes do HTTP.
  subtitles  TRADUZIDA [--max-chars N --max-lines N --max-cps N] (padrão pelo locale: 42/2/17; zh 16/2/9) [--job J] -o PREFIXO  → PREFIXO.srt/.vtt
  shownotes  protect|restore|check  (links e timestamps viram ⟦n⟧ antes de traduzir e voltam depois)
  disclosure --locale L --kind subtitles|dub_generic|dub_replica --source-locale L [--show NOME]
  dub-plan   JOB --translated L=ARQ ... [--intake ARQ ...] -o PLANO.json   (só PLANO: nenhum provedor de voz é chamado)
  check      JOB [--intake ARQ ...] [--glossary G] [--refresh]   schema + regras cruzadas + QA

Princípio (references/principios.md): o plugin recomenda e alerta; o humano decide (review.human_decision).
Rígido (é lei): dublagem com réplica de voz sem aceite dub_voice_replica concedido, não revogado e que
cubra o idioma → RECUSADA em dub-plan e violação em check. Nenhum valor de chave sai daqui.
Preços do dub-plan: research/06 §2.3 (páginas oficiais lidas em 2026-10-09); a conta é ESTIMATIVA.
"""
import argparse
import json
import re
import sys
import textwrap
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import localization_io as lio  # noqa: E402
from dossier_tools import load_json, load_validator  # noqa: E402
from pauta_tools import now_iso  # noqa: E402

from paths import I18N  # noqa: E402
PROTECT_RE = re.compile(r"https?://[^\s)>\]]+|\b\d{1,2}:\d{2}(?::\d{2})?\b")
NUM_RE = re.compile(r"\d+(?:[.,]\d+)*")
SEV_ACK = ("atencao", "alta")
# (id, modo, unidade, preço US$, fonte) — research/06 §2.3, lido em DUB_PRICES_READ_AT.
# Gatilho DEBT-054: reler as páginas a cada DUB_PRICES_MAX_AGE_DAYS; dub-plan avisa quando venceu.
DUB_PRICES_READ_AT = "2026-10-09"
DUB_PRICES_MAX_AGE_DAYS = 90
DUB_PRICES = [
    ("youtube_auto_dubbing", "generic", "min", 0.0, "https://support.google.com/youtube/answer/15569972 (só pt→en/es, vídeo)"),
    ("google_chirp3_hd_tts", "generic", "1M_chars", 30.0, "https://cloud.google.com/text-to-speech/pricing"),
    ("openai_tts_1_hd", "generic", "1M_chars", 30.0, "https://developers.openai.com/api/docs/pricing"),
    ("deepgram_aura_2", "generic", "1k_chars", 0.030, "https://deepgram.com/pricing"),
    ("elevenlabs_v3_tts", "generic", "1k_chars", 0.08, "https://elevenlabs.io/pricing/api"),
    ("google_instant_custom_voice", "guest_replica", "1M_chars", 60.0, "https://cloud.google.com/text-to-speech/pricing"),
    ("elevenlabs_dubbing_v1", "guest_replica", "min", 0.50, "https://elevenlabs.io/pricing/api (≤45 min/arquivo)"),
    ("elevenlabs_dubbing_v2", "guest_replica", "min", 2.20, "https://elevenlabs.io/dubbing-api"),
    ("rask_overage", "guest_replica", "min", 3.00, "https://www.rask.ai/pricing"),
]


def dump_loc(doc, output):
    text = json.dumps(doc, ensure_ascii=False, indent=2) + "\n"
    Path(output).write_text(text, encoding="utf-8") if output else sys.stdout.write(text)


def i18n_text(locale, dotted):
    node = json.loads((I18N / f"{locale}.json").read_text(encoding="utf-8"))
    for part in dotted.split("."):
        node = node.get(part) if isinstance(node, dict) else None
    if not isinstance(node, str):
        raise lio.LocalizationError(f"texto {dotted!r} ausente em references/contracts/i18n/{locale}.json | esperado string")
    return node


# ── glossário ─────────────────────────────────────────────────────────────

def load_glossary(path):
    """show-profile (localization.glossary) ou {glossary: [...]}; None = sem glossário."""
    if not path:
        return []
    doc = load_json(path)
    return (doc.get("localization") or {}).get("glossary") or doc.get("glossary") or []


def glossary_rules(glossary, target):
    """[(termo, forma esperada na tradução)] para o idioma-alvo."""
    rules = []
    for g in glossary:
        if g.get("do_not_translate"):
            rules.append((g["term"], g["term"]))
        elif (g.get("translations") or {}).get(target):
            rules.append((g["term"], g["translations"][target]))
    return rules


def glossary_coverage(src_segs, tgt_segs, glossary, target):
    """{expected, ok, misses[]}: termo presente no original tem de aparecer na forma esperada."""
    tgt = {s["id"]: s["text"].casefold() for s in tgt_segs}
    out = {"expected": 0, "ok": 0, "misses": []}
    for seg in src_segs:
        for term, want in glossary_rules(glossary, target):
            if term.casefold() in seg["text"].casefold():
                out["expected"] += 1
                hit = want.casefold() in tgt.get(seg["id"], "")
                out["ok"] += hit
                out["misses"] += [] if hit else [f"{seg['id']}: {term!r} → {want!r}"]
    return out


def missing_numbers(src_segs, tgt_segs):
    """Números do original (só dígitos) ausentes na tradução, por segmento."""
    tgt = {s["id"]: Counter(re.sub(r"\D", "", n) for n in NUM_RE.findall(s["text"])) for s in tgt_segs}
    miss = []
    for seg in src_segs:
        want = Counter(re.sub(r"\D", "", n) for n in NUM_RE.findall(seg["text"]))
        lost = want - tgt.get(seg["id"], Counter())
        miss += [f"{seg['id']}: {n}" for n in lost.elements()]
    return miss


# ── tradução ─────────────────────────────────────────────────────────────

def agent_packet(doc, target, glossary):
    rules = [{"term": t, "must_appear_as": w} for t, w in glossary_rules(glossary, target)]
    return {"kind": "translation_packet", "source_locale": doc["locale"], "target_locale": target,
            "instructions": ("Traduza cada segmento para o idioma-alvo preservando sentido, tom oral e números"
                             " (datas, artigos de lei e alíquotas não mudam). Termos do glossário aparecem como"
                             " must_appear_as. Preencha translated_text; não mude id, start, end nem speaker."),
            "glossary": rules, "segments": [dict(s, translated_text="") for s in doc["segments"]]}


def merge_packet(packet, translated_by="harness_agent"):
    empty = [s["id"] for s in packet["segments"] if not str(s.get("translated_text", "")).strip()]
    if empty:
        raise lio.LocalizationError(f"pacote com {len(empty)} segmentos sem translated_text (ex.: {empty[:3]})"
                                    " | esperado todos preenchidos")
    segs = [{k: s[k] for k in ("id", "start", "end", "speaker")} | {"text": s["translated_text"].strip()}
            for s in packet["segments"]]
    return {"locale": packet["target_locale"], "source": f"translated_by:{translated_by}",
            "translated_from": packet["source_locale"], "segments": segs}


def provider_translate(doc, target, provider, **kw):
    texts = lio.TRANSLATORS[provider]([s["text"] for s in doc["segments"]], doc["locale"], target, **kw)
    segs = [dict(s, text=t) for s, t in zip(doc["segments"], texts)]
    return {"locale": target, "source": f"translated_by:{provider}", "translated_from": doc["locale"], "segments": segs}


def dub_prices_stale(today=None):
    """Aviso quando a tabela DUB_PRICES passou do prazo de releitura (DEBT-054); None se está em dia."""
    from datetime import date
    age = ((today or date.today()) - date.fromisoformat(DUB_PRICES_READ_AT)).days
    if age <= DUB_PRICES_MAX_AGE_DAYS:
        return None
    return (f"AVISO DEBT-054: preços de TTS/dublagem lidos há {age} dias (prazo {DUB_PRICES_MAX_AGE_DAYS});"
            " as estimativas podem estar defasadas: releia as fontes de DUB_PRICES")


# ── legendas ─────────────────────────────────────────────────────────────

# Limites (car./linha, linhas, car./s) por locale. Padrão: Netflix geral/pt-BR (research/06 §diagramação).
# zh: guia Netflix Chinese (Simplified), 16 car./linha e até 9 car./s no adulto
# (partnerhelp.netflixstudios.com/hc/en-us/articles/215986007, consultado 2026-10-09 via busca).
SUBTITLE_LIMITS = {"zh": (16, 2, 9)}
DEFAULT_SUBTITLE_LIMITS = (42, 2, 17)


def subtitle_limits(locale):
    return SUBTITLE_LIMITS.get(str(locale or "").split("-")[0], DEFAULT_SUBTITLE_LIMITS)


def wrap_lines(text, max_chars):
    """textwrap por palavra; trecho sem espaço maior que a linha (chinês, URL) é cortado por caractere."""
    lines = []
    for line in textwrap.wrap(text, width=max_chars, break_long_words=False) or [""]:
        lines += [line[i:i + max_chars] for i in range(0, len(line), max_chars)] or [""]
    return lines


def segment_cues(seg, max_chars, max_lines):
    """Quebra um segmento em cues de até max_lines linhas; tempo proporcional aos caracteres."""
    lines = wrap_lines(seg["text"], max_chars)
    chunks = [lines[i:i + max_lines] for i in range(0, len(lines), max_lines)]
    total = sum(len(" ".join(c)) for c in chunks) or 1
    t, span, cues = seg["start"], seg["end"] - seg["start"], []
    for c in chunks:
        dur = span * len(" ".join(c)) / total
        cues.append({"start": round(t, 3), "end": round(t + dur, 3), "lines": c, "speaker": seg.get("speaker")})
        t += dur
    return cues


def build_cues(doc, max_chars=42, max_lines=2):
    return [c for seg in doc["segments"] for c in segment_cues(seg, max_chars, max_lines)]


def render_srt(cues):
    return "".join(f"{i}\n{lio.fmt_ts(c['start'], ',')} --> {lio.fmt_ts(c['end'], ',')}\n" + "\n".join(c["lines"]) + "\n\n"
                   for i, c in enumerate(cues, 1))


def render_vtt(cues, names=None):
    """VTT com <v Nome> quando o falante é conhecido (Apple mostra o nome)."""
    out = ["WEBVTT", ""]
    for c in cues:
        name = (names or {}).get(c.get("speaker")) or c.get("speaker")
        text = "\n".join(c["lines"])
        out += [f"{lio.fmt_ts(c['start'])} --> {lio.fmt_ts(c['end'])}", f"<v {name}>{text}" if name else text, ""]
    return "\n".join(out)


def qa_subtitle_text(text, max_chars, max_lines, max_cps=None):
    """Relê o arquivo gerado. {examined, violations[], cps_over[]} — violação = formato/tempo/linhas."""
    blocks, rep = lio.cue_blocks(text), {"examined": 0, "violations": [], "cps_over": []}
    prev_end = 0.0
    for i, (start, end, raw) in enumerate(blocks, 1):
        lines = [lio.clean_line(r)[0] for r in raw if r.strip()]
        rep["examined"] += 1
        if not start < end:
            rep["violations"].append(f"cue {i}: início {start} >= fim {end}")
        if start < prev_end - 1e-3:
            rep["violations"].append(f"cue {i}: começa em {start} antes do fim da anterior ({prev_end})")
        if len(lines) > max_lines or any(len(line) > max_chars for line in lines):
            rep["violations"].append(f"cue {i}: {len(lines)} linhas, maior {max(map(len, lines), default=0)} car."
                                     f" | esperado <= {max_lines} linhas e <= {max_chars} car.")
        cps = sum(map(len, lines)) / max(end - start, 1e-3)
        if max_cps and cps > max_cps:
            rep["cps_over"].append(f"cue {i}: {cps:.1f} car./s")
        prev_end = end
    if not blocks:
        rep["violations"].append("nenhuma cue encontrada | esperado arquivo SRT/VTT com cues")
    return rep


# ── show notes ───────────────────────────────────────────────────────────

def protect(text):
    """Links e timestamps viram ⟦n⟧ (o tradutor não toca). Devolve (texto, tokens)."""
    tokens = []

    def keep(m):
        tokens.append(m.group(0))
        return f"⟦{len(tokens) - 1}⟧"
    return PROTECT_RE.sub(keep, text), tokens


def restore(text, tokens):
    missing = [i for i in range(len(tokens)) if f"⟦{i}⟧" not in text]
    if missing:
        raise lio.LocalizationError(f"marcadores {['⟦%d⟧' % i for i in missing]} sumiram na tradução"
                                    " | esperado todos preservados")
    return re.sub(r"⟦(\d+)⟧", lambda m: tokens[int(m.group(1))], text)


def shownotes_diff(src, tgt):
    """Links/timestamps do original ausentes (ou sobrando) na tradução."""
    a, b = Counter(PROTECT_RE.findall(src)), Counter(PROTECT_RE.findall(tgt))
    return sorted((a - b).elements()), sorted((b - a).elements())


def disclosure(locale, kind, source_locale, show=""):
    text = i18n_text(locale, f"localization.disclosure.{kind}")
    lang = i18n_text(locale, f"localization.language_names.{source_locale}")
    return text.replace("{{source_language}}", lang).replace("{{show}}", show)


# ── CLI ───────────────────────────────────────────────────────────────────

def load_intakes(paths):
    docs = [load_json(p) for p in paths or []]
    return {d.get("intake_id"): d for d in docs}


def require_byok_consent(args, target=None):
    """Recusa (ConsentRefusal) antes de qualquer chamada BYOK sem aceite do convidado (ALQERA PRV-004)."""
    import localization_check as lc
    why = lc.byok_refusal(load_intakes(args.intake), target, args.sem_convidado)
    if why:
        raise lc.ConsentRefusal(f"{args.provider}: {why}; nada foi enviado ao provedor")


def cmd_loc_transcribe(args):
    if args.provider != "from-file":
        require_byok_consent(args)
    if args.provider == "from-file":
        doc = lio.transcript_from_file(args.entrada, args.locale, args.start, args.end)
    elif args.provider == "assemblyai":
        doc = lio.assemblyai_transcribe(args.entrada, args.locale, args.key_env or "ASSEMBLYAI_API_KEY")
    else:
        terms = [g["term"] for g in load_glossary(args.keyterms)]
        doc = lio.elevenlabs_transcribe(args.entrada, args.locale, args.key_env or "ELEVENLABS_API_KEY", keyterms=terms)
    dump_loc(doc, args.output)
    print(f"transcribe {args.provider}: {len(doc['segments'])} segmentos", file=sys.stderr)
    return 0


def cmd_loc_translate(args):
    if args.merge:
        return dump_loc(merge_packet(load_json(args.merge)), args.output) or 0
    doc, glossary = load_json(args.transcricao), load_glossary(args.glossary)
    if args.provider == "agent":
        return dump_loc(agent_packet(doc, args.target, glossary), args.output) or 0
    require_byok_consent(args, args.target)
    kw = {"key_env": args.key_env or "DEEPL_API_KEY", "host": args.deepl_host} if args.provider == "deepl" else {}
    out = provider_translate(doc, args.target, args.provider, **kw)
    cov = glossary_coverage(doc["segments"], out["segments"], glossary, args.target)
    print(f"translate {args.provider}: glossário {cov['ok']}/{cov['expected']}", file=sys.stderr)
    return dump_loc(out, args.output) or 0


def cmd_loc_subtitles(args):
    doc = load_json(args.traduzida)
    names = {s["label"]: s.get("display_name") for s in (load_json(args.job).get("speakers") or [])} if args.job else {}
    lim = subtitle_limits(doc.get("locale"))
    args.max_chars, args.max_lines, args.max_cps = (v if v is not None else d for v, d in
                                                    zip((args.max_chars, args.max_lines, args.max_cps), lim))
    cues, bad = build_cues(doc, args.max_chars, args.max_lines), 0
    for ext, text in (("srt", render_srt(cues)), ("vtt", render_vtt(cues, names))):
        Path(f"{args.output}.{ext}").write_text(text, encoding="utf-8")
        rep = qa_subtitle_text(text, args.max_chars, args.max_lines, args.max_cps)
        bad += len(rep["violations"])
        print(f"{args.output}.{ext}: cues={rep['examined']} · violações={len(rep['violations'])}"
              f" · acima de {args.max_cps} car./s={len(rep['cps_over'])}")
    return 1 if bad else 0


def cmd_loc_shownotes(args):
    text = Path(args.arquivo).read_text(encoding="utf-8")
    if args.acao == "protect":
        prot, tokens = protect(text)
        return dump_loc({"text": prot, "tokens": tokens}, args.output) or 0
    if args.acao == "restore":
        pack = load_json(args.tokens)
        out = restore(text, pack["tokens"])
        Path(args.output).write_text(out, encoding="utf-8") if args.output else sys.stdout.write(out)
        return 0
    lost, extra = shownotes_diff(Path(args.original).read_text(encoding="utf-8"), text)
    print(f"shownotes check: perdidos={lost} sobrando={extra}")
    return 1 if lost or extra else 0


def cmd_loc_disclosure(args):
    print(disclosure(args.locale, args.kind, args.source_locale, args.show or ""))
    return 0


def cmd_loc_dub_plan(args):
    import localization_check as lc
    translated = {k: load_json(v) for k, v in (t.split("=", 1) for t in args.translated or [])}
    try:
        plan = lc.dub_plan(load_json(args.job), translated, load_intakes(args.intake))
    except lc.ConsentRefusal as exc:
        print(f"RECUSADO (regra rígida, LGPD art. 11): {exc}", file=sys.stderr)
        return 2
    plan["generated_at"] = now_iso()
    dump_loc(plan, args.output)
    if stale := dub_prices_stale():
        print(stale, file=sys.stderr)
    for p in plan["plans"]:
        best = min((c["estimate_usd"] for c in p["cost_estimates"]), default=0)
        print(f"dub-plan {p['locale']}/{p['speaker_label']} ({p['voice_mode']}): {p['totals']} · menor estimativa US$ {best}",
              file=sys.stderr)
    return 0


def cmd_loc_check(args):
    import localization_check as lc
    job, base = load_json(args.job), Path(args.job).parent
    gloss = args.glossary or (str(base / job["glossary_ref"]) if job.get("glossary_ref") else None)
    errs, alerts, skipped = lc.check_job(job, base, load_intakes(args.intake), load_glossary(gloss),
                                         load_validator(), args.refresh)
    if args.refresh:
        Path(args.job).write_text(json.dumps(job, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for a in alerts:
        print(f"ALERTA {a['code']} ({a['severity']}) — recomendação; decisão humana: {a.get('evidence', '')}")
    for e in errs:
        print(f"FALHA  {e}")
    need = sorted({a["code"] for a in alerts if a["severity"] in SEV_ACK})
    print(f"check {args.job}: violações={len(errs)} · alertas={len(alerts)} (exigem aceite para aprovar: {need})"
          f" · regras puladas={len(skipped)} {skipped if skipped else ''}".rstrip())
    return 1 if errs else 0


def build_parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("transcribe")
    t.add_argument("entrada")
    t.add_argument("--provider", choices=("from-file", "assemblyai", "elevenlabs"), default="from-file")
    t.add_argument("--locale", required=True)
    t.add_argument("--start", type=float)
    t.add_argument("--end", type=float)
    for name in ("--key-env", "--keyterms", "-o"):
        t.add_argument(name, dest={"-o": "output"}.get(name))
    t.add_argument("--intake", action="append", help="intake do convidado (aceite translation_text); BYOK exige")
    t.add_argument("--sem-convidado", action="store_true", help="declara que o áudio não tem convidado")
    tr = sub.add_parser("translate")
    tr.add_argument("transcricao", nargs="?")
    tr.add_argument("--target")
    tr.add_argument("--provider", choices=("agent", "deepl", "google", "openai"), default="agent")
    tr.add_argument("--deepl-host", choices=("pro", "free"), default="pro")
    for name in ("--glossary", "--merge", "--key-env", "-o"):
        tr.add_argument(name, dest={"-o": "output"}.get(name))
    tr.add_argument("--intake", action="append", help="intake do convidado (aceite translation_text do idioma); BYOK exige")
    tr.add_argument("--sem-convidado", action="store_true", help="declara que as falas não têm convidado")
    s = sub.add_parser("subtitles")
    s.add_argument("traduzida")
    s.add_argument("--max-chars", type=int, default=None)
    s.add_argument("--max-lines", type=int, default=None)
    s.add_argument("--max-cps", type=float, default=None)
    s.add_argument("--job")
    s.add_argument("-o", "--output", required=True)
    n = sub.add_parser("shownotes")
    n.add_argument("acao", choices=("protect", "restore", "check"))
    n.add_argument("arquivo")
    for name in ("--tokens", "--original", "-o"):
        n.add_argument(name, dest={"-o": "output"}.get(name))
    d = sub.add_parser("disclosure")
    d.add_argument("--locale", required=True)
    d.add_argument("--kind", choices=("subtitles", "dub_generic", "dub_replica"), required=True)
    d.add_argument("--source-locale", required=True)
    d.add_argument("--show")
    dp = sub.add_parser("dub-plan")
    dp.add_argument("job")
    dp.add_argument("--translated", action="append")
    dp.add_argument("--intake", action="append")
    dp.add_argument("-o", "--output")
    c = sub.add_parser("check")
    c.add_argument("job")
    c.add_argument("--intake", action="append")
    c.add_argument("--glossary")
    c.add_argument("--refresh", action="store_true")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    handlers = {"transcribe": cmd_loc_transcribe, "translate": cmd_loc_translate, "subtitles": cmd_loc_subtitles,
                "shownotes": cmd_loc_shownotes, "disclosure": cmd_loc_disclosure, "dub-plan": cmd_loc_dub_plan,
                "check": cmd_loc_check}
    import localization_check as lc
    try:
        return handlers[args.cmd](args)
    except lc.ConsentRefusal as exc:   # aceite ausente antes do BYOK (PRV-004): nada saiu da máquina
        print(f"RECUSADO (aceite do convidado, LGPD): {exc}", file=sys.stderr)
        return 2
    except lio.LocalizationError as exc:
        print(f"{args.cmd}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
