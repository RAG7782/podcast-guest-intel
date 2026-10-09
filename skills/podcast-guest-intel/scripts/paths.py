#!/usr/bin/env python3
"""Fonte única dos caminhos de dados dos scripts — vale no repo E no pacote da skill.

  repo:   <raiz>/contracts           <raiz>/squads/podcast-production/config
  pacote: <skill>/references/contracts   <skill>/assets/config   (layout montado por build_plugin.py)

O pacote se reconhece pelo SKILL.md na raiz. Nenhum outro script calcula caminho de dado:
importa daqui. `python3 -I scripts/paths.py` sai 1 se faltar algum dado (usado pelo build --check).
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGED = (ROOT / "SKILL.md").is_file()
CONTRACTS = ROOT / ("references/contracts" if PACKAGED else "contracts")
CONFIG = ROOT / ("assets/config" if PACKAGED else "squads/podcast-production/config")
I18N = CONTRACTS / "i18n"
MODES = CONTRACTS / "approach-modes.yaml"
TREND_SOURCES = CONTRACTS / "trend-sources.yaml"
FORMATS = CONFIG / "formats.yaml"
VALIDATOR = ROOT / "scripts" / "validate-contracts.py"
INSTANCES = ROOT / "instances"   # dados do usuário: só no repo, pode não existir
REQUIRED = (CONTRACTS, I18N, I18N / "pt-BR.json", I18N / "en.json", MODES, TREND_SOURCES, FORMATS, VALIDATOR)


def missing_data():
    """Caminhos obrigatórios que não existem neste layout (lista vazia = tudo resolvido)."""
    return [p for p in REQUIRED if not p.exists()]


if __name__ == "__main__":
    gaps = missing_data()
    layout = "pacote" if PACKAGED else "repo"
    for p in gaps:
        print(f"paths: dado ausente no layout {layout}: {p.relative_to(ROOT)}", file=sys.stderr)
    print(f"paths: {len(REQUIRED) - len(gaps)}/{len(REQUIRED)} dados resolvidos (layout {layout})")
    sys.exit(1 if gaps else 0)
