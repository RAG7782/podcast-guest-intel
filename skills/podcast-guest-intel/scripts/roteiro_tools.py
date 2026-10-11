#!/usr/bin/env python3
"""Ferramentas determinísticas do roteiro por modo de abordagem (task *roteiro, F5).

Subcomandos:
  build   --pauta P [--dossier D] --script-id ID [--approach-mode M] [--itens t1,c3]
          [--duracao-min N] [-o SAIDA.json]
          ESQUELETO a partir da pauta + flags do modo (hook, pacing, beats, profundidade,
          contraponto). A redação final (texto, perguntas, cortes) é do agente; o modo é do
          humano (--approach-mode só quando ele troca o modo da pauta).
  refresh ARQ [--dossier D]           recalcula rastreabilidade e gate.alertas e grava.
  check   ARQ [--pauta P] [--dossier D]
          schema + regras cruzadas. ALERTA (recomendação) não falha; violação (rígida ou de
          integridade) sai 1. Regra sem a entrada que precisa é PULADA e contada.
  render  ARQ [--formato completo|teleprompter|cartao] [-o SAIDA.md]

Princípio (references/principios.md): o plugin recomenda e alerta; o humano decide. Seguir contra
um alerta de severidade atencao/alta exige gate.human_decision (references/contracts/human-decision.schema.json).
Rígido: validade de schema, dado sensível só autodeclarado pelo titular, nenhuma credencial na saída.
build/render são stdlib + pyyaml (registro de modos); check reusa scripts/validate-contracts.py.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dossier_tools import load_json, load_validator, split_envelope as split_dossier  # noqa: E402
from pauta_tools import TRUNKS, now_iso, split_pauta  # noqa: E402

from paths import FORMATS, MODES, PACKAGED, load_yaml  # noqa: E402
PACING = {"lento": (3, 90), "moderado": (4, 60), "rapido": (5, 40)}  # (itens, abertura em s)
DEPTH_BY_PACING = {"lento": "profunda", "moderado": "media", "rapido": "superficie"}
QUESTIONS_BY_DEPTH = {"superficie": 1, "media": 2, "profunda": 3}
DEFAULT_BEATS = ["contexto", "desenvolvimento", "pergunta"]
MODE_KEYS = ("source_rigor", "requires_counterpoint", "requires_guardian_gate", "legal_risk", "hook_style", "pacing")
CLOSE_S, BRIDGE_S, TIMING_TOL = 60, 15, 0.15
GATE_CODE = {"vetado": ("R-ROTEIRO-GATE-VETADO", "alta"), "aprovado_com_ajustes": ("R-ROTEIRO-GATE-AJUSTES", "atencao")}


# ── modo ──────────────────────────────────────────────────────────────────

# O pacote local traz só o modo grátis em approach-modes.yaml (build_plugin.py filtra); os outros são servidos
# pelo MCP. Mensagem só no layout de pacote: no repo, modo ausente é erro de digitação.
MODO_PAGO = ("approach_mode {modo!r} é do plano pago e não vem no pacote local | esperado: um de {livres} aqui, ou a"
             " tool `roteiro_modos` do MCP do PodFácil com a chave de licença para os 7 modos")


def load_modes():
    return {m.get("id"): m for m in load_yaml(MODES).get("modes") or []}


def resolve_mode(mode_id, modes=None):
    """Flags efetivas com extends resolvido. Modo inexistente para; nunca cai num padrão silencioso."""
    modes, chain, cur = modes or load_modes(), [], mode_id
    while cur:
        if cur not in modes and PACKAGED:
            raise ValueError(MODO_PAGO.format(modo=cur, livres=sorted(modes)))
        if cur not in modes or cur in chain:
            raise ValueError(f"approach_mode {cur!r} {'não existe' if cur not in modes else 'em ciclo de extends'}"
                             f" | esperado: um de {sorted(modes)}")
        chain.append(cur)
        cur = modes[cur].get("extends")
    merged = {}
    for mid in reversed(chain):
        merged.update(modes[mid])
    out = {"id": mode_id, "extends_resolvido": chain[1:], **{k: merged[k] for k in MODE_KEYS}}
    out["beats"] = merged.get("beats") or DEFAULT_BEATS
    out["depth"] = merged.get("depth") or DEPTH_BY_PACING[merged["pacing"]]
    return out, bool(merged.get("counterpoint_block"))


def target_minutes(fmt, override):
    if override:
        return int(override)
    spec = (load_yaml(FORMATS) or {}).get(fmt) or {}
    hit = re.search(r"\d+", str(spec.get("duration", "")))
    return int(hit.group()) if hit else 45


# ── build ─────────────────────────────────────────────────────────────────

def pick_items(pauta, wanted, n):
    """Itens explícitos (curadoria do agente/humano) ou round-robin por rank entre os troncos."""
    trunks = {t: sorted((pauta.get("trunks") or {}).get(t) or [], key=lambda i: i.get("rank", 99)) for t in TRUNKS}
    pool = {i["id"]: i for items in trunks.values() for i in items}
    if wanted:
        missing = [w for w in wanted if w not in pool]
        if missing:
            raise SystemExit(f"--itens {missing} não existe(m) na pauta | esperado: um de {sorted(pool)}")
        return [pool[w] for w in wanted]
    order = [items[r] for r in range(10) for items in trunks.values() if r < len(items)]
    return order[:n]


def claim_ressalvas(cls, degraded, rationale):
    notes = []
    if degraded and cls:
        notes.append("dossiê degradado: confirmar com o convidado antes de afirmar")
    if any(c.get("status") == "autodeclarado" for c in cls):
        notes.append("autodeclarado: atribuir ao convidado (\"segundo você...\")")
    if "revalidar" in str(rationale):
        notes.append("fato da semana: revalidar a fonte antes de gravar")
    notes += [f"ALERTA {a.get('code')} na claim {c['id']}: usar como base exige aceite humano"
              for c in cls for a in c.get("advisory") or []]
    return notes


def item_block(item, mode, claims, degraded, ordem):
    cls = [claims[c] for c in item.get("claim_ids") or [] if c in claims and not claims[c].get("sensitive")]
    nq = QUESTIONS_BY_DEPTH[mode["depth"]]
    qs = [{"texto": q, "tipo": "ancora" if i == 0 else "aprofundamento"}
          for i, q in enumerate((item.get("questions") or [])[:nq])]
    qs += [{"texto": f"[{beat}] pergunta aberta sobre: {item['title']}", "tipo": "aprofundamento"}
           for beat in mode["beats"][len(qs):nq]]
    afirm = []
    for c in cls:
        nature = "hipotese" if c.get("status") == "inferencia" else "fato"
        afirm.append({"texto": c.get("text"), "natureza": nature, "claim_ids": [c["id"]],
                      "fontes": [s["url"] for s in c.get("sources") or [] if s.get("url")]})
        if nature == "hipotese":
            qs.append({"texto": f"Confere? {c.get('text')}", "tipo": "confirmacao", "claim_ids": [c["id"]]})
    return {"ordem": ordem, "tipo": "bloco", "titulo": item["title"], "beat": " → ".join(mode["beats"]),
            "texto": f"({' → '.join(mode['beats'])}) {item['title']}. Por quê: {item.get('rationale', '')}",
            "duracao_seg": 0, "pauta_item_refs": [item["id"]], "perguntas": qs,
            "afirmacoes": [{k: v for k, v in a.items() if v} for a in afirm],
            "ressalvas": claim_ressalvas(cls, degraded, item.get("rationale"))}


def simple_block(tipo, titulo, texto, perguntas=()):
    return {"ordem": 0, "tipo": tipo, "titulo": titulo, "texto": texto, "duracao_seg": 0,
            "perguntas": list(perguntas), "afirmacoes": [], "ressalvas": []}


def counterpoint_block(mode):
    qs = [{"texto": "Qual é o argumento mais forte contra o que você defendeu aqui?", "tipo": "contraponto"}]
    if mode["requires_counterpoint"]:
        qs.append({"texto": "O que a parte citada respondeu ao pedido de contraditório (ou que ficou sem resposta)?",
                   "tipo": "contraponto"})
    return simple_block("contraponto", "Contraponto", "Opinião assumida como opinião; o outro lado com a "
                        "melhor versão dele.", qs)


def allocate(blocks, minutes, opening_s):
    """Abertura pelo pacing, encerramento 60 s, ponte 15 s; o resto em partes iguais (contraponto vale 0,6)."""
    weight = {"bloco": 1.0, "contraponto": 0.6}
    fixed = {"abertura": opening_s, "encerramento": CLOSE_S, "transicao": BRIDGE_S}
    free = max(minutes * 60 - sum(fixed.get(b["tipo"], 0) for b in blocks), 60)
    total_w = sum(weight.get(b["tipo"], 0) for b in blocks) or 1
    for n, b in enumerate(blocks, 1):
        b["ordem"] = n
        b["duracao_seg"] = fixed.get(b["tipo"]) or max(int(free * weight[b["tipo"]] / total_w), 30)
    return blocks


def build_script(pauta_doc, dossier=None, meta=None):
    pauta, meta = split_pauta(pauta_doc)[0], meta or {}
    mode_id = meta.get("approach_mode") or pauta.get("approach_mode")
    mode, extra_counter = resolve_mode(mode_id)
    claims = {c.get("id"): c for c in (dossier or {}).get("claims") or [] if isinstance(c, dict)}
    degraded = bool(pauta.get("dossier_degraded"))
    n_items, opening_s = PACING[mode["pacing"]]
    items = pick_items(pauta, meta.get("itens"), n_items)
    blocks = [simple_block("abertura", "Abertura", f"Gancho ({mode['hook_style']}): {items[0]['title'] if items else ''}")]
    for i, item in enumerate(items):
        if i:
            blocks.append(simple_block("transicao", "Ponte", f"De \"{items[i - 1]['title']}\" para \"{item['title']}\"."))
        blocks.append(item_block(item, mode, claims, degraded, 0))
    if mode["requires_counterpoint"] or extra_counter:
        blocks.append(counterpoint_block(mode))
    blocks.append(simple_block("encerramento", "Encerramento", "Síntese em uma frase, pergunta final ao convidado"
                               " e onde encontrá-lo.", [{"texto": "O que você quer que o ouvinte leve daqui?",
                                                         "tipo": "ancora"}]))
    minutes = target_minutes(pauta.get("format"), meta.get("duracao_min"))
    script = {
        "meta": {k: v for k, v in {
            "script_id": meta["script_id"], "pauta_ref": pauta.get("pauta_id"), "episode_ref": pauta.get("episode_ref"),
            "dossier_ref": pauta.get("dossier_ref"), "host_profile_ref": pauta.get("host_profile_ref"),
            "format": pauta.get("format"), "locale": pauta.get("locale", "pt-BR"), "dossier_degraded": degraded,
            "duracao_alvo_min": minutes, "modo_escolhido_pelo_humano": mode_id != pauta.get("approach_mode") or None,
            "generated_at": meta.get("generated_at") or now_iso()}.items() if v is not None},
        "modo": mode, "roteiro": allocate(blocks, minutes, opening_s),
        "rastreabilidade": {"afirmacoes_total": 0, "com_lastro": 0, "cortadas": 0},
        "contraditorio": [] if mode["requires_counterpoint"] else None,
        "gate": {"exigido": mode["requires_guardian_gate"], "task": "fact-check-review",
                 "veredito": "pendente" if mode["requires_guardian_gate"] else "nao_aplicavel",
                 "revisao_juridica": "pendente" if mode["legal_risk"] == "alto" else "nao_aplicavel", "alertas": []},
        "status": "aguardando_gate" if mode["requires_guardian_gate"] else "rascunho"}
    return refresh(script, claims)


# ── alertas e rastreabilidade ─────────────────────────────────────────────

def facts(script):
    for i, b in enumerate(script.get("roteiro") or []):
        for j, a in enumerate(b.get("afirmacoes") or []):
            if a.get("natureza") == "fato":
                yield f"roteiro/{i}/afirmacoes/{j}", b, a


def traceability(script):
    total = list(facts(script))
    lastro = [a for _w, _b, a in total if a.get("claim_ids") or a.get("fontes")]
    return len(total), len(lastro)


def fact_alerts(where, block, af, claims, mode):
    cls = [claims[c] for c in af.get("claim_ids") or [] if c in claims]
    out = []
    if not (af.get("claim_ids") or af.get("fontes")):
        out.append(("R-ROTEIRO-SEM-LASTRO", "alta", where))
    if any(c.get("status") == "inferencia" for c in cls):
        out.append(("R-ROTEIRO-INFERENCIA-COMO-FATO", "alta", where))
    if mode.get("source_rigor") in ("alto", "maximo") and cls and not af.get("fontes") \
            and all(c.get("status") == "autodeclarado" for c in cls):
        out.append(("R-ROTEIRO-RIGOR", "atencao", where))
    if cls and (claims.get("__degraded__") and not block.get("ressalvas")):
        out.append(("R-ROTEIRO-DEGRADADO", "atencao", where))
    out += [(a.get("code"), a.get("severity", "alta"), f"claim {c['id']}: {a.get('evidence', '')}".strip())
            for c in cls for a in c.get("advisory") or []]
    return out


def compute_alerts(script, claims, validator):
    """Um alerta por código, com a evidência agregada. Recomendação: nunca bloqueia sozinho."""
    mode, gate, raw = script.get("modo") or {}, script.get("gate") or {}, []
    claims = dict(claims, __degraded__=(script.get("meta") or {}).get("dossier_degraded"))
    if gate.get("exigido") and gate.get("veredito") != "aprovado":
        code, sev = GATE_CODE.get(gate.get("veredito"), ("R-ROTEIRO-GATE-PENDENTE", "alta"))
        raw.append((code, sev, f"veredito do @guardian: {gate.get('veredito')}"))
    if mode.get("requires_counterpoint") and not script.get("contraditorio"):
        raw.append(("R-ROTEIRO-CONTRADITORIO", "alta", "nenhum pedido de contraditório registrado"))
    if mode.get("legal_risk") == "alto" and gate.get("revisao_juridica") != "feita":
        raw.append(("R-ROTEIRO-REVISAO-JURIDICA", "alta", f"revisão jurídica: {gate.get('revisao_juridica')}"))
    for where, block, af in facts(script):
        raw += fact_alerts(where, block, af, claims, mode)
    total_s = sum(b.get("duracao_seg", 0) for b in script.get("roteiro") or [])
    target = (script.get("meta") or {}).get("duracao_alvo_min", 0) * 60
    if target and abs(total_s - target) > TIMING_TOL * target:
        raw.append(("R-ROTEIRO-TIMING", "info", f"{total_s // 60} min de {target // 60} min"))
    rank, merged = {"info": 0, "atencao": 1, "alta": 2}, {}
    for code, sev, ev in raw:
        cur = merged.setdefault(code, [sev, []])
        cur[0] = max(cur[0], sev, key=rank.get)
        if ev not in cur[1]:
            cur[1].append(ev)
    return [validator.alert(code, sev, "; ".join(evs)[:400]) for code, (sev, evs) in sorted(merged.items())]


def refresh(script, claims, validator=None):
    total, lastro = traceability(script)
    script["rastreabilidade"].update(afirmacoes_total=total, com_lastro=lastro)
    script["gate"]["alertas"] = compute_alerts(script, claims, validator or load_validator())
    return script


def required_ack(alerts):
    return sorted({a["code"] for a in alerts if a.get("severity") in ("atencao", "alta")})


# ── check ─────────────────────────────────────────────────────────────────

def rule_mode(script):
    mode = script.get("modo") or {}
    try:
        want = resolve_mode(mode.get("id"))[0]
    except ValueError as exc:
        return [f"R-ROTEIRO-MODO @modo/id: {exc}"]
    diff = {k: (mode.get(k), want[k]) for k in MODE_KEYS + ("extends_resolvido",) if mode.get(k) != want[k]}
    errs = [f"R-ROTEIRO-MODO @modo: flags divergem do registro {diff} | esperado: (valor, registro) iguais"] if diff else []
    if (script.get("gate") or {}).get("exigido") != want["requires_guardian_gate"]:
        errs.append(f"R-ROTEIRO-GATE-EXIGIDO @gate/exigido: {script['gate'].get('exigido')!r}"
                    f" | esperado: {want['requires_guardian_gate']} (requires_guardian_gate do modo)")
    return errs


def rule_order(script):
    blocks = script.get("roteiro") or []
    tipos, ordens = [b.get("tipo") for b in blocks], [b.get("ordem") for b in blocks]
    errs = [] if ordens == list(range(1, len(blocks) + 1)) else [
        f"R-ROTEIRO-ORDEM @roteiro: ordem={ordens} | esperado: 1..{len(blocks)} em sequência"]
    if tipos[:1] != ["abertura"] or tipos[-1:] != ["encerramento"]:
        errs.append(f"R-ROTEIRO-ORDEM @roteiro: tipos={tipos} | esperado: abertura primeiro, encerramento por último")
    return errs


def rule_traceability(script):
    total, lastro = traceability(script)
    got = script.get("rastreabilidade") or {}
    if (got.get("afirmacoes_total"), got.get("com_lastro")) == (total, lastro):
        return []
    return [f"R-ROTEIRO-RASTREABILIDADE @rastreabilidade: total={got.get('afirmacoes_total')}"
            f" com_lastro={got.get('com_lastro')} | esperado: total={total} com_lastro={lastro} (refresh)"]


def all_refs(script, key):
    for i, b in enumerate(script.get("roteiro") or []):
        for ref in b.get(key) or []:
            yield f"roteiro/{i}/{key}", ref
        for kind in ("afirmacoes", "perguntas"):
            for j, x in enumerate(b.get(kind) or []):
                for ref in x.get(key) or []:
                    yield f"roteiro/{i}/{kind}/{j}/{key}", ref


def rule_script_refs(script, key, known, rule):
    return [f"{rule} @{where}: {ref!r} não existe | esperado: um de {sorted(known)[:8]}"
            for where, ref in all_refs(script, key) if ref not in known]


def rule_sensitive(script, claims):
    """RÍGIDO (LGPD art. 11): dado sensível só autodeclarado pelo titular, com consentimento."""
    return [f"R-ROTEIRO-SENSIVEL @{where}: claim {ref!r} sensível sem autodeclaração/consentimento do titular"
            " | esperado: origin=guest_intake, status=autodeclarado e consent_ref (regra rígida, sem aceite)"
            for where, ref in all_refs(script, "claim_ids")
            for c in [claims.get(ref) or {}] if c.get("sensitive") and not (
                c.get("origin") == "guest_intake" and c.get("status") == "autodeclarado" and c.get("consent_ref"))]


def rule_alerts_current(script, computed):
    have = sorted(a.get("code") for a in (script.get("gate") or {}).get("alertas") or [])
    want = sorted(a["code"] for a in computed)
    return [] if have == want else [f"R-ROTEIRO-ALERTAS @gate/alertas: {have} | esperado: {want}"
                                    " (rode roteiro_tools.py refresh: o humano precisa ver os alertas atuais)"]


def rule_human_ack(script, alerts):
    """pronto_para_gravar com alerta atencao/alta exige aceite humano 'seguir_contra' que cubra todos."""
    need = required_ack(alerts)
    if script.get("status") != "pronto_para_gravar" or not need:
        return []
    hd = (script.get("gate") or {}).get("human_decision") or {}
    seen = {a.get("code") for a in hd.get("alerts") or []}
    if hd.get("decision") == "seguir_contra" and set(need) <= seen:
        return []
    return [f"R-ROTEIRO-HUMAN-ACK @gate/human_decision: decisão={hd.get('decision')!r}, alertas vistos={sorted(seen)}"
            f" | esperado: seguir_contra com aceite de {need} (ou status antes de pronto_para_gravar)"]


def rule_script_no_secret(script, validator):
    return [f"R-ROTEIRO-NO-SECRET @{path}: string com forma de credencial (len={len(text)})"
            " | esperado: nenhum valor de chave na saída (regra rígida)"
            for path, text in validator.walk_strings(script)
            if "/fontes/" not in path and not path.endswith("url") and validator.SECRET_RE.search(text)]


def check_script(script, refs=None, validator=None):
    """(violações, alertas, regras puladas). refs: pauta, dossier (opcionais)."""
    refs, validator = refs or {}, validator or load_validator()
    schemas, registry = validator.load_schemas()
    errs = validator.check("script", script, schemas, registry)
    errs += rule_mode(script) + rule_order(script) + rule_traceability(script) + rule_script_no_secret(script, validator)
    pauta = split_pauta(refs["pauta"])[0] if refs.get("pauta") else None
    dossier = split_dossier(refs["dossier"])[0] if refs.get("dossier") else None
    claims = {c.get("id"): c for c in (dossier or {}).get("claims") or [] if isinstance(c, dict)}
    computed = compute_alerts(script, claims, validator)
    stored = (script.get("gate") or {}).get("alertas") or []
    skipped = []
    if pauta is None:
        skipped.append("R-ROTEIRO-REF-PAUTA")
    else:
        ids = {i.get("id") for t in TRUNKS for i in (pauta.get("trunks") or {}).get(t) or []}
        errs += rule_script_refs(script, "pauta_item_refs", ids, "R-ROTEIRO-REF-PAUTA")
    if dossier is None:
        skipped += ["R-ROTEIRO-REF-CLAIM", "R-ROTEIRO-SENSIVEL", "R-ROTEIRO-ALERTAS"]
        alerts = computed + [a for a in stored if a.get("code") not in {c["code"] for c in computed}]
    else:
        errs += rule_script_refs(script, "claim_ids", set(claims), "R-ROTEIRO-REF-CLAIM") + rule_sensitive(script, claims)
        errs += rule_alerts_current(script, computed)
        alerts = computed
    return errs + rule_human_ack(script, alerts), alerts, skipped


# ── CLI ───────────────────────────────────────────────────────────────────

def opt_dossier(path):
    return split_dossier(load_json(path))[0] if path else None


def claims_of_path(path):
    return {c.get("id"): c for c in (opt_dossier(path) or {}).get("claims") or [] if isinstance(c, dict)}


def write_or_print(text, output):
    Path(output).write_text(text, encoding="utf-8") if output else sys.stdout.write(text)


def cmd_build(args):
    meta = {"script_id": args.script_id, "approach_mode": args.approach_mode, "duracao_min": args.duracao_min,
            "itens": [i.strip() for i in args.itens.split(",")] if args.itens else None}
    try:
        script = build_script(load_json(args.pauta), opt_dossier(args.dossier), meta)
    except ValueError as exc:
        raise SystemExit(f"build: {exc}")
    write_or_print(json.dumps(script, ensure_ascii=False, indent=2) + "\n", args.output)
    return 0


def cmd_refresh(args):
    script = refresh(load_json(args.arquivo), claims_of_path(args.dossier))
    Path(args.arquivo).write_text(json.dumps(script, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"refresh {args.arquivo}: alertas={[a['code'] for a in script['gate']['alertas']]}"
          f" · rastreabilidade={script['rastreabilidade']}")
    return 0


def cmd_check(args):
    refs = {"pauta": load_json(args.pauta) if args.pauta else None,
            "dossier": load_json(args.dossier) if args.dossier else None}
    script = load_json(args.arquivo)
    errs, alerts, skipped = check_script(script, refs)
    for a in alerts:
        print(f"ALERTA {a['code']} ({a['severity']}) — recomendação; decisão humana: {a.get('evidence', '')}")
    for err in errs:
        print(f"FALHA  {err}")
    print(f"check {args.arquivo}: blocos={len(script.get('roteiro') or [])} · violações={len(errs)}"
          f" · alertas={len(alerts)} (exigem aceite para gravar: {required_ack(alerts)})"
          f" · regras puladas={len(skipped)} {skipped if skipped else ''}".rstrip())
    return 1 if errs else 0


def cmd_render(args):
    from roteiro_render import FORMATS as RENDERERS
    write_or_print(RENDERERS[args.formato](load_json(args.arquivo)), args.output)
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    bld = sub.add_parser("build")
    bld.add_argument("--pauta", required=True)
    bld.add_argument("--script-id", required=True)
    for name in ("--dossier", "--approach-mode", "--itens", "-o"):
        bld.add_argument(name, dest={"-o": "output"}.get(name))
    bld.add_argument("--duracao-min", type=int)
    ref = sub.add_parser("refresh")
    ref.add_argument("arquivo")
    ref.add_argument("--dossier")
    chk = sub.add_parser("check")
    chk.add_argument("arquivo")
    chk.add_argument("--pauta")
    chk.add_argument("--dossier")
    ren = sub.add_parser("render")
    ren.add_argument("arquivo")
    ren.add_argument("--formato", choices=("completo", "teleprompter", "cartao"), default="completo")
    ren.add_argument("-o", "--output")
    args = parser.parse_args(argv)
    return {"build": cmd_build, "refresh": cmd_refresh, "check": cmd_check, "render": cmd_render}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
