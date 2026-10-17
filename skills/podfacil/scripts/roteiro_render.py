"""Render do roteiro (references/contracts/script.schema.json) em três formatos, stdlib pura.

  completo      roteiro inteiro para o host e a produção, com alertas em linguagem clara;
  teleprompter  só o que o host fala e pergunta, em ordem, sem metadado;
  cartao        uma página: gancho, blocos com tempo e 1 pergunta, alertas abertos, ressalvas.
Chamado por scripts/roteiro_tools.py render.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import I18N  # noqa: E402

CARD_MAX_NOTES = 5


def mmss(seconds):
    return f"{int(seconds) // 60:02d}:{int(seconds) % 60:02d}"


def alert_text(code, locale):
    """Texto do alerta no locale do roteiro; esqueleto (es/zh) ou ausente cai para en."""
    for loc in (locale, "en"):
        path = I18N / f"{loc}.json"
        if path.is_file():
            text = (json.loads(path.read_text(encoding="utf-8")).get("decision") or {}).get("alerts", {}).get(code)
            if text and not text.startswith("[TODO"):
                return text
    return code


def ack_text(version, locale):
    for loc in (locale, "en"):
        path = I18N / f"{loc}.json"
        node = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
        for part in str(version).split(".", 2):
            node = node.get(part) if isinstance(node, dict) else None
        if isinstance(node, str) and not node.startswith("[TODO"):
            return node
    return version


def render_alerts(script):
    gate, locale = script.get("gate") or {}, (script.get("meta") or {}).get("locale", "pt-BR")
    alerts = gate.get("alertas") or []
    if not alerts:
        return ["", "## Alertas", "", "Nenhum alerta aberto."]
    lines = ["", "## Alertas (o plugin recomenda; a decisão é sua)", ""]
    for a in alerts:
        lines.append(f"- **{a['code']}** ({a['severity']}): {alert_text(a['code'], locale)}")
        if a.get("evidence"):
            lines.append(f"  - Evidência: {a['evidence']}")
    hd = gate.get("human_decision")
    if hd:
        lines += ["", f"Decisão humana registrada: **{hd['decision']}** por {hd['decided_by']} em {hd['decided_at']}"
                  f" (alertas vistos: {', '.join(x['code'] for x in hd['alerts'])}).",
                  f"Aceite ({hd['acknowledgment_text_version']}): \"{ack_text(hd['acknowledgment_text_version'], locale)}\""]
    return lines


def render_lastro(af):
    parts = [f"`{c}`" for c in af.get("claim_ids") or []] + [f"<{u}>" for u in af.get("fontes") or []]
    return ", ".join(parts) or "**sem lastro**"


def render_block(b):
    lines = ["", f"## {b['ordem']}. {b['titulo']} — {b['tipo']} · {mmss(b['duracao_seg'])}", "", b["texto"]]
    if b.get("pauta_item_refs"):
        lines.append(f"\n_Itens da pauta: {', '.join(b['pauta_item_refs'])}_")
    lines += [f"- Pergunta ({q['tipo']}): {q['texto']}" for q in b.get("perguntas") or []]
    lines += [f"- Afirmação ({a['natureza']}): {a['texto']} — {render_lastro(a)}" for a in b.get("afirmacoes") or []]
    lines += [f"- Ressalva: {r}" for r in b.get("ressalvas") or []]
    return lines


def header(script):
    meta, mode = script.get("meta") or {}, script.get("modo") or {}
    total = sum(b.get("duracao_seg", 0) for b in script.get("roteiro") or [])
    chosen = " (modo escolhido pelo humano)" if meta.get("modo_escolhido_pelo_humano") else ""
    return [f"# Roteiro — {meta.get('episode_ref')} · modo {mode.get('id')}", "",
            f"- Modo `{mode.get('id')}`{chosen}: gancho \"{mode.get('hook_style')}\", ritmo {mode.get('pacing')},"
            f" profundidade {mode.get('depth')}, rigor {mode.get('source_rigor')}, risco jurídico {mode.get('legal_risk')}",
            f"- Duração: {mmss(total)} de {meta.get('duracao_alvo_min')} min alvo · status **{script.get('status')}**",
            f"- Pauta `{meta.get('pauta_ref')}` · gerado em {meta.get('generated_at')}"]


def render_full(script):
    lines = header(script) + render_alerts(script)
    for b in script.get("roteiro") or []:
        lines += render_block(b)
    rast, contra = script.get("rastreabilidade") or {}, script.get("contraditorio")
    lines += ["", "## Rastreabilidade e contraditório", "",
              f"- Afirmações de fato: {rast.get('afirmacoes_total')} · com lastro: {rast.get('com_lastro')}"
              f" · cortadas: {rast.get('cortadas')}"]
    if contra is None:
        lines.append("- Contraditório: o modo não recomenda.")
    for p in contra or []:
        lines.append(f"- Contraditório ({p['situacao']}): {p['parte']} via {p['canal']}, prazo {p['prazo']}."
                     " O agente só redige; quem envia é você.")
    return "\n".join(lines) + "\n"


def render_teleprompter(script):
    lines = [f"# Teleprompter — {(script.get('meta') or {}).get('episode_ref')}"]
    for b in script.get("roteiro") or []:
        lines += ["", f"## {b['titulo'].upper()} · {mmss(b['duracao_seg'])}", "", b["texto"]]
        lines += [f"\n> {q['texto']}" for q in b.get("perguntas") or []]
    return "\n".join(lines) + "\n"


def render_card(script):
    meta, mode = script.get("meta") or {}, script.get("modo") or {}
    blocks = script.get("roteiro") or []
    lines = [f"# Cartão — {meta.get('episode_ref')} · {mode.get('id')}", "",
             f"**{blocks[0]['texto'] if blocks else ''}**", ""]
    clock = 0
    for b in blocks:
        first = next((q["texto"] for q in b.get("perguntas") or []), "")
        lines.append(f"- {mmss(clock)} **{b['titulo']}**" + (f" — {first}" if first else ""))
        clock += b.get("duracao_seg", 0)
    lines.append(f"- {mmss(clock)} fim")
    alerts = (script.get("gate") or {}).get("alertas") or []
    open_codes = [a["code"] for a in alerts if a.get("severity") != "info"]
    lines += ["", f"**Alertas abertos:** {', '.join(open_codes) or 'nenhum'} · status **{script.get('status')}**"]
    notes = list(dict.fromkeys(r for b in blocks for r in b.get("ressalvas") or []))
    if notes:
        lines += ["", "**Antes de gravar:**", ""] + [f"- {n}" for n in notes[:CARD_MAX_NOTES]]
    return "\n".join(lines) + "\n"


FORMATS = {"completo": render_full, "teleprompter": render_teleprompter, "cartao": render_card}
