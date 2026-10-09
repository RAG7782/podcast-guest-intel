#!/usr/bin/env python3
"""Ferramentas determinísticas do dossiê do convidado (task *guest-dossier).

Subcomandos:
  coverage ARQ [--intake INTAKE] [--apply]  calcula coverage.expected/found/gaps, degraded e
                                             resumo_status a partir das claims (e do intake).
  advise ARQ [--apply]                       recalcula claim.advisory (alertas do modo denúncia: fonte
                                             fraca vira alerta, não invalidação; o humano decide).
  check ARQ                                  schema + regras cruzadas; sai 1 se houver violação.
  render ARQ [-o SAIDA.md]                   dossiê -> markdown legível para o host.

ARQ é o envelope do manifesto ({dossier, resumo_status, conflitos, orcamento}) ou o dossiê puro.
`coverage` e `render` são stdlib pura; `check` precisa de jsonschema + pyyaml:
  uv run --no-project -q --with jsonschema --with pyyaml python scripts/dossier_tools.py check ARQ
"""
import argparse
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402
STATUSES = ("verificado", "autodeclarado", "inferencia")
ORIGINS = ("public_scan", "guest_intake", "guest_material", "manager_material")
USABLE = {"verificado", "autodeclarado"}  # inferencia não cobre área: vale pouco (manifesto)
DEFAULT_EXPECTED = [
    "intake", "pronuncia_nome", "cargo_atual", "trajetoria", "obra_producao",
    "posicoes_publicas", "entrevistas_anteriores", "ligacao_tema",
]


# ── leitura ────────────────────────────────────────────────────────────────

def load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"erro ao ler {path}: {exc} | esperado: arquivo JSON legível")


def split_envelope(doc):
    """(dossier, envelope|None). Envelope = saída do manifesto com chave 'dossier'."""
    if isinstance(doc, dict) and isinstance(doc.get("dossier"), dict):
        return doc["dossier"], doc
    if isinstance(doc, dict):
        return doc, None
    raise SystemExit(f"raiz é {type(doc).__name__} | esperado: objeto dossiê ou envelope")


def claims_of(dossier):
    return [c for c in dossier.get("claims") or [] if isinstance(c, dict)]


# ── coverage ───────────────────────────────────────────────────────────────

def compute_coverage(dossier, intake=None):
    """coverage + degraded. Área achada = tem claim verificado/autodeclarado com coverage_area."""
    previous = (dossier.get("coverage") or {}).get("expected") or []
    expected = list(dict.fromkeys(DEFAULT_EXPECTED + list(previous)))
    found = {c.get("coverage_area") for c in claims_of(dossier) if c.get("status") in USABLE}
    if intake is not None or dossier.get("intake_ref"):
        found.add("intake")
    found_list = [a for a in expected if a in found]
    gaps = [a for a in expected if a not in found]
    return {"expected": expected, "found": found_list, "gaps": gaps}, bool(gaps)


def summarize_status(claims):
    by_status, by_origin = Counter(), Counter()
    for claim in claims:
        by_status[claim.get("status")] += 1
        by_origin[claim.get("origin")] += 1
    return {
        "por_status": {s: by_status.get(s, 0) for s in STATUSES},
        "por_origin": {o: by_origin.get(o, 0) for o in ORIGINS},
        "total": len(claims),
    }


def apply_coverage(doc, intake=None):
    """Grava coverage/degraded no dossiê e resumo_status no envelope (se houver)."""
    dossier, envelope = split_envelope(doc)
    dossier["coverage"], dossier["degraded"] = compute_coverage(dossier, intake)
    if envelope is not None:
        envelope["resumo_status"] = summarize_status(claims_of(dossier))
    return doc


# ── check ──────────────────────────────────────────────────────────────────

def load_validator():
    """Reusa scripts/validate-contracts.py (schemas + regras cruzadas): uma fonte de verdade."""
    path = paths.VALIDATOR
    spec = importlib.util.spec_from_file_location("validate_contracts", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rule_subject_is_guest(dossier):
    guest = dossier.get("guest_ref")
    return [f"R-DOSSIER-SUBJECT-GUEST @claims/{i}: subject={c.get('subject')!r}"
            f" | esperado: {guest!r} (terceiro nunca vira subject)"
            for i, c in enumerate(claims_of(dossier)) if c.get("subject") != guest]


def rule_cargo_dated(dossier):
    return [f"R-DOSSIER-CARGO-DATADO @claims/{i}: cargo_atual sem as_of | esperado: data do fato"
            for i, c in enumerate(claims_of(dossier))
            if c.get("coverage_area") == "cargo_atual" and not c.get("as_of")]


def rule_coverage_sets(dossier):
    cov = dossier.get("coverage") or {}
    exp, found, gaps = (set(cov.get(k) or []) for k in ("expected", "found", "gaps"))
    errs = []
    if (found | gaps) != exp:
        errs.append(f"R-DOSSIER-COVERAGE-PARTICAO @coverage: found∪gaps={sorted(found | gaps)}"
                    f" | esperado: igual a expected={sorted(exp)}")
    if found & gaps:
        errs.append(f"R-DOSSIER-COVERAGE-PARTICAO @coverage: em found e gaps ao mesmo tempo:"
                    f" {sorted(found & gaps)} | esperado: conjuntos disjuntos")
    return errs


def rule_resumo(envelope, claims):
    resumo = envelope.get("resumo_status")
    want = summarize_status(claims)
    if resumo != want:
        return [f"R-DOSSIER-RESUMO @resumo_status: {json.dumps(resumo, ensure_ascii=False)}"
                f" | esperado: {json.dumps(want, ensure_ascii=False)}"]
    return []


def rule_conflitos(envelope, ids):
    errs = []
    for i, conflict in enumerate(envelope.get("conflitos") or []):
        refs = conflict.get("claim_ids") or [] if isinstance(conflict, dict) else []
        missing = [r for r in refs if r not in ids]
        if len(refs) < 2 or missing:
            errs.append(f"R-DOSSIER-CONFLITO @conflitos/{i}: claim_ids={refs}"
                        f" | esperado: >=2 ids existentes (ausentes: {missing})")
    return errs


def rule_orcamento(envelope, degraded):
    orc = envelope.get("orcamento")
    if not isinstance(orc, dict):
        return [f"R-DOSSIER-ORCAMENTO @orcamento: {orc!r} | esperado: {{buscas, paginas_lidas,"
                " teto_buscas, teto_paginas, teto_atingido}}"]
    errs = []
    hit = orc.get("buscas", 0) >= orc.get("teto_buscas", float("inf")) or \
        orc.get("paginas_lidas", 0) >= orc.get("teto_paginas", float("inf"))
    if orc.get("teto_atingido") is not hit:
        errs.append(f"R-DOSSIER-ORCAMENTO @orcamento/teto_atingido: {orc.get('teto_atingido')!r}"
                    f" | esperado: {hit} (buscas/páginas vs tetos)")
    if hit and not degraded:
        errs.append("R-DOSSIER-ORCAMENTO @degraded: teto atingido com degraded=false"
                    " | esperado: degraded=true e lacunas nomeadas")
    return errs


def rules_envelope(envelope, dossier):
    claims = claims_of(dossier)
    ids = {c.get("id") for c in claims}
    return (rule_resumo(envelope, claims) + rule_conflitos(envelope, ids)
            + rule_orcamento(envelope, dossier.get("degraded")))


def check_doc(doc, validator=None):
    """Lista de violações (vazia = conforme)."""
    validator = validator or load_validator()
    dossier, envelope = split_envelope(doc)
    schemas, registry = validator.load_schemas()
    errs = validator.check("guest-dossier", dossier, schemas, registry)
    errs += rule_subject_is_guest(dossier) + rule_cargo_dated(dossier) + rule_coverage_sets(dossier)
    if envelope is not None:
        errs += rules_envelope(envelope, dossier)
    return errs


def apply_advisories(doc, validator=None):
    """Recalcula os alertas R-CLAIM-CONDUTA-* de cada claim; devolve quantas claims ficaram com alerta."""
    validator = validator or load_validator()
    flagged = 0
    for claim in claims_of(split_envelope(doc)[0]):
        keep = [a for a in claim.get("advisory") or [] if not str(a.get("code")).startswith("R-CLAIM-CONDUTA-")]
        claim["advisory"] = keep + validator.claim_advisories(claim)
        flagged += bool(claim["advisory"])
        if not claim["advisory"]:
            del claim["advisory"]
    return flagged


# ── render ─────────────────────────────────────────────────────────────────

STATUS_TITLE = {
    "verificado": "Verificado (fonte pública)",
    "autodeclarado": "Autodeclarado (o próprio convidado ou o gestor)",
    "inferencia": "Inferência (hipótese a confirmar com o convidado)",
}


def render_sources(claim):
    parts = []
    for s in claim.get("sources") or []:
        label = s.get("title") or s.get("url")
        tier = f"tier {s['tier']}" if s.get("tier") else "tier ?"
        who = " · ".join(f"{k} {s[k]}" for k in ("author", "outlet", "agency") if s.get(k))
        parts.append(f"[{label}]({s.get('url')}) ({tier}{', ' + who if who else ''}, acesso {s.get('accessed_at', '?')[:10]})")
    if claim.get("basis_claim_ids"):
        parts.append("base: " + ", ".join(f"`{b}`" for b in claim["basis_claim_ids"]))
    return "; ".join(parts) or "sem fonte pública"


def render_claim(claim):
    date = f" _(fato de {claim['as_of']})_" if claim.get("as_of") else ""
    area = f" `{claim['coverage_area']}`" if claim.get("coverage_area") else ""
    alerts = "".join(f" · **ALERTA {a.get('code')}** (decisão sua; aceite registrado para usar como base)"
                     for a in claim.get("advisory") or [])
    return f"- **{claim.get('text')}**{date}{area} — {render_sources(claim)} · id `{claim.get('id')}`{alerts}"


def render_header(dossier):
    lines = [f"# Dossiê — {dossier.get('guest_ref')}", "",
             f"- Gerado em {dossier.get('generated_at')} · finalidade: {dossier.get('purpose')}",
             f"- Base legal da varredura: `{(dossier.get('legal_basis') or {}).get('public_scan')}`"]
    if dossier.get("degraded"):
        gaps = ", ".join((dossier.get("coverage") or {}).get("gaps") or [])
        lines += ["", f"> **DEGRADADO** — lacunas: {gaps}. Confirme com o convidado antes de usar."]
    return lines


def render_safety(claims):
    """Anti-constrangimento: o que o host precisa acertar no ar."""
    lines = ["", "## Antes de gravar (anti-constrangimento)", ""]
    for area, label in (("pronuncia_nome", "Pronúncia"), ("cargo_atual", "Cargo atual")):
        hits = [c for c in claims if c.get("coverage_area") == area]
        if hits:
            lines += [f"- {label}: {c.get('text')} ({c.get('status')}"
                      f"{', em ' + c['as_of'] if c.get('as_of') else ''})" for c in hits]
        else:
            lines.append(f"- {label}: **não confirmado** — perguntar ao convidado")
    return lines


def render_envelope(envelope):
    lines = []
    for conflict in envelope.get("conflitos") or []:
        ids = ", ".join(f"`{i}`" for i in conflict.get("claim_ids", []))
        lines.append(f"- Conflito ({ids}): {conflict.get('descricao')}")
    orc = envelope.get("orcamento") or {}
    if orc:
        lines.append(f"- Orçamento: {orc.get('buscas')}/{orc.get('teto_buscas')} buscas · "
                     f"{orc.get('paginas_lidas')}/{orc.get('teto_paginas')} páginas · "
                     f"teto atingido: {orc.get('teto_atingido')}")
    return (["", "## Conflitos e orçamento", ""] + lines) if lines else []


def render(doc):
    dossier, envelope = split_envelope(doc)
    claims = claims_of(dossier)
    lines = render_header(dossier) + render_safety(claims)
    for status in STATUSES:
        group = [c for c in claims if c.get("status") == status]
        if group:
            lines += ["", f"## {STATUS_TITLE[status]} — {len(group)}", ""]
            lines += [render_claim(c) for c in group]
    cov = dossier.get("coverage") or {}
    lines += ["", "## Cobertura", "", f"- Achado: {', '.join(cov.get('found') or []) or '—'}",
              f"- Lacunas: {', '.join(cov.get('gaps') or []) or '—'}"]
    lines += render_envelope(envelope or {})
    return "\n".join(lines) + "\n"


# ── CLI ────────────────────────────────────────────────────────────────────

def cmd_coverage(args):
    doc = load_json(args.arquivo)
    intake = load_json(args.intake) if args.intake else None
    apply_coverage(doc, intake)
    dossier, envelope = split_envelope(doc)
    out = {"coverage": dossier["coverage"], "degraded": dossier["degraded"]}
    if envelope is not None:
        out["resumo_status"] = envelope["resumo_status"]
    if args.apply:
        Path(args.arquivo).write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


def cmd_check(args):
    doc = load_json(args.arquivo)
    errs = check_doc(doc)
    claims = claims_of(split_envelope(doc)[0])
    for err in errs:
        print(f"FALHA  {err}")
    print(f"check {args.arquivo}: claims examinadas={len(claims)} · violações={len(errs)}")
    return 1 if errs else 0


def cmd_advise(args):
    doc = load_json(args.arquivo)
    flagged = apply_advisories(doc)
    if args.apply:
        Path(args.arquivo).write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"advise {args.arquivo}: claims examinadas={len(claims_of(split_envelope(doc)[0]))} · com alerta={flagged}"
          f"{'' if args.apply else ' (dry-run; --apply grava)'}")
    return 0


def cmd_render(args):
    text = render(load_json(args.arquivo))
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    cov = sub.add_parser("coverage")
    cov.add_argument("arquivo")
    cov.add_argument("--intake")
    cov.add_argument("--apply", action="store_true", help="grava coverage/degraded/resumo no arquivo")
    adv = sub.add_parser("advise")
    adv.add_argument("arquivo")
    adv.add_argument("--apply", action="store_true", help="grava claim.advisory no arquivo")
    sub.add_parser("check").add_argument("arquivo")
    ren = sub.add_parser("render")
    ren.add_argument("arquivo")
    ren.add_argument("-o", "--output")
    args = parser.parse_args(argv)
    return {"coverage": cmd_coverage, "advise": cmd_advise, "check": cmd_check,
            "render": cmd_render}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
