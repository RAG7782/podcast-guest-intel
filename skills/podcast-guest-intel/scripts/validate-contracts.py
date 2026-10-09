#!/usr/bin/env python3
"""Valida os contratos (references/contracts/*.schema.json) contra fixtures nos DOIS sentidos.

- fixtures/valid/<schema>--<caso>.(json|yaml): tem de passar.
- fixtures/invalid/<schema>--<caso>.json: tem de falhar COM a regra esperada
  (fixtures/expected-failures.json: arquivo -> trecho que deve aparecer num erro).
- Registros (approach-modes.yaml, trend-sources.yaml) e instances/*/<schema>.json: têm de passar.

Uso: uv run --no-project --with jsonschema --with pyyaml python scripts/validate-contracts.py
Imprime o denominador: examinados / passaram / falharam / pulados. Sai 1 se falhou algo ou se 0 examinados.
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import CONTRACTS, INSTANCES, ROOT  # noqa: E402
FIXTURES = CONTRACTS / "fixtures"
SECRET_RE = re.compile(r"(sk-[A-Za-z0-9]{8,}|ghp_[A-Za-z0-9]{8,}|xox[abp]-|AKIA[0-9A-Z]{12,}|AIza[0-9A-Za-z_-]{20,}|[A-Za-z0-9_\-]{32,})")


def load_schemas():
    """Carrega todos os *.schema.json num Registry (refs relativas entre contratos)."""
    schemas, resources = {}, []
    for path in sorted(CONTRACTS.glob("*.schema.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        schemas[path.name.removesuffix(".schema.json")] = schema
        resources.append((schema["$id"], Resource.from_contents(schema)))
    return schemas, Registry().with_resources(resources)


def load_data(path):
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text) if path.suffix in (".yaml", ".yml") else json.loads(text)


def short(value, limit=80):
    text = json.dumps(value, ensure_ascii=False, default=str)
    return text if len(text) <= limit else text[:limit] + "…"


def format_error(err):
    """Linha com regra, caminho, valor ofensor e shape esperado."""
    rule = err.schema.get("x-rule") if isinstance(err.schema, dict) else None
    label = rule or f"schema:{err.validator}"
    path = "/".join(str(p) for p in err.absolute_path) or "<raiz>"
    return (f"{label} @{path}: {err.message} | valor={short(err.instance, 60)}"
            f" | esperado {err.validator}={short(err.validator_value, 60)}")


def schema_errors(name, data, schemas, registry):
    validator = Draft202012Validator(schemas[name], registry=registry,
                                     format_checker=Draft202012Validator.FORMAT_CHECKER)
    return [format_error(e) for e in validator.iter_errors(data)]


def walk_strings(node, path=""):
    if isinstance(node, dict):
        for key, value in node.items():
            yield from walk_strings(value, f"{path}/{key}")
    elif isinstance(node, list):
        for i, value in enumerate(node):
            yield from walk_strings(value, f"{path}/{i}")
    elif isinstance(node, str):
        yield path, node


def rules_trend_sources(data):
    errs = []
    for path, text in walk_strings(data):
        if path.endswith("endpoint_template"):
            continue
        if SECRET_RE.search(text):
            errs.append(f"R-TREND-NO-SECRET-VALUE @{path}: string com forma de credencial"
                        f" (len={len(text)}) | esperado: só ref {{store, name}} para env/cofre")
    sources = data.get("sources", []) if isinstance(data, dict) else []
    byok = [s for s in sources if isinstance(s, dict) and s.get("kind") == "byok"]
    x = [s for s in byok if s.get("id") == "x"]
    if x and any(s.get("priority", 99) < x[0].get("priority", 99) for s in byok if s is not x[0]):
        errs.append(f"R-TREND-X-PRIORITY @sources/x: priority={x[0].get('priority')}"
                    " | esperado: X com a menor priority entre as fontes byok")
    return errs + duplicate_ids(sources, "R-TREND-ID-UNIQUE", "sources")


def duplicate_ids(items, rule, where, key="id"):
    seen, errs = set(), []
    for item in items:
        ident = item.get(key) if isinstance(item, dict) else None
        if ident in seen:
            errs.append(f"{rule} @{where}: id repetido {short(ident)} | esperado: ids únicos")
        seen.add(ident)
    return errs


def source_domain(url):
    """Domínio sem 'www.' — base da independência entre fontes."""
    host = (urlsplit(url).hostname or "") if isinstance(url, str) else ""
    return host.removeprefix("www.")


def alert(code, severity, evidence=""):
    """Alerta de responsabilidade (human-decision.schema.json#/$defs/alert); texto em contracts/i18n."""
    out = {"code": code, "severity": severity, "text_i18n_key": f"decision.alerts.{code}"}
    return dict(out, evidence=evidence) if evidence else out


def source_card(src):
    """O que o humano precisa ver para julgar independência: domínio, autor, veículo, agência."""
    return (f"tier {src.get('tier', '?')} · {source_domain(src.get('url')) or '?'} · autor {src.get('author') or '?'}"
            f" · veículo {src.get('outlet') or '?'} · agência {src.get('agency') or '—'}")


def independent(a, b):
    """Domínios distintos e, quando informados, autor e agência distintos.
    ponytail: não detecta reescrita sem crédito de agência; o humano vê autor/veículo/agência no evidence."""
    same = lambda k: bool(a.get(k)) and a.get(k) == b.get(k)  # noqa: E731
    return source_domain(a.get("url")) != source_domain(b.get("url")) and not same("agency") and not same("author")


def claim_advisories(claim):
    """Modo denúncia: fonte fraca não invalida a claim; vira alerta que o consumidor exige aceitar."""
    if not isinstance(claim, dict) or claim.get("conduct_allegation") is not True:
        return []
    sources = [s for s in claim.get("sources") or [] if isinstance(s, dict)]
    evidence = "; ".join(source_card(s) for s in sources) or "sem fonte"
    tier2 = [s for s in sources if s.get("tier") == 2]
    if any(s.get("tier") == 1 for s in sources) and claim.get("status") == "verificado":
        return []
    if claim.get("status") != "verificado" or len(tier2) < 2:
        return [alert("R-CLAIM-CONDUTA-FONTES", "alta", evidence)]
    if not any(independent(a, b) for i, a in enumerate(tier2) for b in tier2[i + 1:]):
        return [alert("R-CLAIM-CONDUTA-INDEPENDENCIA", "alta", evidence)]
    return []


def rules_claim(claim, where="<raiz>"):
    """O alerta devido tem de estar registrado em claim.advisory: o humano precisa vê-lo (não decide por ele)."""
    have = {a.get("code") for a in (claim.get("advisory") or []) if isinstance(a, dict)} if isinstance(claim, dict) else set()
    return [f"R-CLAIM-ADVISORY-AUSENTE[{a['code']}] @{where}/advisory: alerta devido não registrado"
            f" ({a['evidence']}) | esperado: advisory com code {a['code']} (dossier_tools.py advise --apply)"
            for a in claim_advisories(claim) if a["code"] not in have]


I18N = CONTRACTS / "i18n"


def i18n_has(key, locale):
    node = json.loads((I18N / f"{locale}.json").read_text(encoding="utf-8"))
    for part in key.split(".", 2):
        node = node.get(part) if isinstance(node, dict) else None
    return isinstance(node, str) and bool(node.strip())


def rules_i18n_keys(data):
    """Todo texto de alerta/aceite referenciado existe em pt-BR e en (es/zh são esqueleto)."""
    errs = []
    for path, text in walk_strings(data):
        if path.endswith(("/text_i18n_key", "/acknowledgment_text_version")):
            missing = [loc for loc in ("pt-BR", "en") if not i18n_has(text, loc)]
            if missing:
                errs.append(f"R-DECISION-I18N-KEY @{path}: {text!r} ausente em {missing}"
                            " | esperado: chave em contracts/i18n/{pt-BR,en}.json")
    return errs


def rules_pauta(data):
    """Teto de itens por tronco: max_items_per_trunk da pauta (default 5)."""
    if not isinstance(data, dict):
        return []
    limit = data.get("max_items_per_trunk", 5)
    trunks = data.get("trunks") if isinstance(data.get("trunks"), dict) else {}
    return [f"R-PAUTA-MAX-ITEMS @trunks/{name}: {len(items)} itens | esperado: <= {limit}"
            " (max_items_per_trunk; default 5)"
            for name, items in trunks.items() if isinstance(items, list) and len(items) > limit]


def rules_guest_dossier(data):
    claims = data.get("claims", []) if isinstance(data, dict) else []
    ids = {c.get("id") for c in claims if isinstance(c, dict)}
    errs = duplicate_ids(claims, "R-DOSSIER-CLAIM-ID-UNIQUE", "claims")
    for i, claim in enumerate(claims):
        errs += rules_claim(claim, f"claims/{i}")
    for i, claim in enumerate(claims):
        for ref in (claim.get("basis_claim_ids") or []) if isinstance(claim, dict) else []:
            if ref not in ids:
                errs.append(f"R-DOSSIER-BASIS-REF @claims/{i}/basis_claim_ids: {short(ref)} não existe"
                            f" | esperado: um de {short(sorted(i for i in ids if i))}")
    return errs


def rules_approach_modes(data, schemas, registry):
    modes = data.get("modes", []) if isinstance(data, dict) else []
    errs = [f"modes/{i}: {e}" for i, m in enumerate(modes)
            for e in schema_errors("approach-mode", m, schemas, registry)]
    errs += duplicate_ids(modes, "R-MODES-ID-UNIQUE", "modes")
    ids = {m.get("id") for m in modes if isinstance(m, dict)}
    for m in modes:
        if isinstance(m, dict) and m.get("extends") and m["extends"] not in ids:
            errs.append(f"R-MODES-EXTENDS @{m.get('id')}: extends={short(m['extends'])} | esperado: um de {sorted(ids)}")
    den = next((m for m in modes if isinstance(m, dict) and m.get("id") == "denuncia"), None)
    if not den or not den.get("requires_guardian_gate") or den.get("legal_risk") != "alto":
        errs.append(f"R-MODES-DENUNCIA @denuncia: {short(den)} | esperado: requires_guardian_gate=true e legal_risk=alto")
    return errs


HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")


def relative_luminance(hex_color):
    """WCAG 2.2 (SC 1.4.3): luminância relativa sRGB, limiar 0.04045."""
    def lin(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast_ratio(a, b):
    hi, lo = sorted((relative_luminance(a), relative_luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def rules_show_profile(data):
    """R-BRAND-CONTRAST: texto sobre fundo do convite >= 4.5:1 (AA, texto normal). Sem arredondar."""
    colors = ((data.get("brand") or {}).get("colors") or {}) if isinstance(data, dict) else {}
    text, bg = colors.get("text"), colors.get("background")
    if not all(isinstance(c, str) and HEX_RE.match(c) for c in (text, bg)):
        return []  # ausente ou hex inválido: o schema (R-BRAND-HEX/required) já acusa
    ratio = contrast_ratio(text, bg)
    if ratio >= 4.5:
        return []
    return [f"R-BRAND-CONTRAST @brand/colors: text={text} sobre background={bg} = {ratio:.2f}:1"
            " | esperado: >= 4.5:1 (WCAG 2.2 SC 1.4.3, AA)"]


CROSS_RULES = {"trend-sources": rules_trend_sources, "guest-dossier": rules_guest_dossier,
               "claim": rules_claim, "pauta": rules_pauta, "show-profile": rules_show_profile}


def check(name, data, schemas, registry):
    """Todas as violações (schema + regras cruzadas em Python) de um documento."""
    if name == "approach-modes":
        return rules_approach_modes(data, schemas, registry)
    errs = schema_errors(name, data, schemas, registry) + rules_i18n_keys(data)
    return errs + CROSS_RULES.get(name, lambda _d: [])(data)


def targets():
    """(caminho, schema, sentido) para cada alvo; schema=None => pulado."""
    expected = json.loads((FIXTURES / "expected-failures.json").read_text(encoding="utf-8"))
    for path in sorted((FIXTURES / "valid").glob("*.*")):
        yield path, path.name.split("--")[0], "valid", None
    for path in sorted((FIXTURES / "invalid").glob("*.*")):
        yield path, path.name.split("--")[0], "invalid", expected.get(path.name)
    yield CONTRACTS / "approach-modes.yaml", "approach-modes", "valid", None
    yield CONTRACTS / "trend-sources.yaml", "trend-sources", "valid", None
    for path in sorted(INSTANCES.glob("*/*.json")):
        yield path, path.stem, "valid", None


def judge(errs, sense, expect):
    """(ok, motivo) segundo o sentido do alvo."""
    if sense == "valid":
        return (not errs), (errs[0] if errs else "")
    if expect is None:
        return False, "fixture inválida sem entrada em expected-failures.json"
    if any(expect in e for e in errs):
        return True, f"falhou como esperado ({expect})"
    return False, f"esperava '{expect}', obteve {errs[:2] or 'NENHUM erro (passou)'}"


def main():
    schemas, registry = load_schemas()
    known = set(schemas) | {"approach-modes"}
    stats = {"examinados": 0, "passaram": 0, "falharam": 0, "pulados": 0}
    for path, name, sense, expect in targets():
        rel = path.relative_to(ROOT)
        if name not in known:
            stats["pulados"] += 1
            print(f"PULADO  {rel}: schema '{name}' desconhecido; esperado um de {sorted(known)}")
            continue
        stats["examinados"] += 1
        ok, why = judge(check(name, load_data(path), schemas, registry), sense, expect)
        stats["passaram" if ok else "falharam"] += 1
        print(f"{'OK  ' if ok else 'FALHA'}  [{sense:7}] {rel}" + (f"  — {why}" if why else ""))
    print("\nDenominador: " + " · ".join(f"{k}={v}" for k, v in stats.items()))
    return 0 if stats["falharam"] == 0 and stats["examinados"] > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
