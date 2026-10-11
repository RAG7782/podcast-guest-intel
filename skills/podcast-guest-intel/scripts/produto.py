"""Endereços e identidade HTTP do produto, lidos de references/contracts/produto.json (fonte única; vale no repo e no pacote).

O servidor pode ser trocado sem editar código: env PODFACIL_SERVER_URL (testes, servidor próprio, domínio novo
antes de republicar o pacote). Stdlib.
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import PRODUTO  # noqa: E402

CHAVES = ("servidor_mcp", "precos", "user_agent", "licenca_revalidar_horas", "licenca_offline_horas")


def carregar(path=PRODUTO):
    """Dicionário de references/contracts/produto.json; falta de chave para aqui, com o nome do que falta."""
    try:
        doc = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise SystemExit(f"{path}: {exc} | esperado JSON com {list(CHAVES)}") from exc
    faltam = [k for k in CHAVES if k not in doc]
    if faltam:
        raise SystemExit(f"{path}: faltam {faltam} | esperado {list(CHAVES)}")
    return doc


_DOC = carregar()
SERVER_URL = os.environ.get("PODFACIL_SERVER_URL") or _DOC["servidor_mcp"]
PRICING_URL = _DOC["precos"]
USER_AGENT = _DOC["user_agent"]
REVALIDAR_H = float(_DOC["licenca_revalidar_horas"])
OFFLINE_H = float(_DOC["licenca_offline_horas"])
