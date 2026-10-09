---
task: Pipeline Review
responsavel: "@producer"
responsavel_type: agent
atomic_layer: task
elicit: false
Entrada: |
  - season-calendar: assets/templates/season-calendar.md atualizado
  - agent-status: Status reportado por cada agente (research, gravacao, edicao, publicacao)
  - analytics-snapshot: Dados de @analyst (opcional; obrigatorio no fechamento mensal)
Saida: |
  - pipeline-status: Estado de cada episodio (BACKLOG, RESEARCH, GRAVACAO, EDICAO, APROVACAO, PUBLICADO, RISCO)
  - bottlenecks: Gargalos priorizados (vermelho/amarelo) com dono e acao
  - capacity-view: Carga por agente
  - monthly-report: Relatorio mensal consolidado (so no fechamento do mes)
Checklist:
  - "[ ] Listar todos os episodios do calendar com status e dono"
  - "[ ] Marcar como RISCO todo episodio com dependencia aberta perto da data (guest, briefing, edicao)"
  - "[ ] Priorizar gargalos: vermelho = ameaca a data; amarelo = margem curta"
  - "[ ] Atribuir acao e dono a cada gargalo"
  - "[ ] Checar carga por agente e realocar se houver sobrecarga"
  - "[ ] Conferir buffer: ha episodio READY/evergreen para substituicao?"
  - "[ ] Comunicar mudancas de calendar ao squad (nunca alterar em silencio)"
---

# *review-pipeline

Revisao semanal do pipeline de producao. Roda toda semana; no fechamento do mes inclui o relatorio mensal.

## Formato

```
PIPELINE REVIEW — Semana [dd/mm]
EP[XX] [STATUS] — [dono] — [proximo marco/data]
...
GARGALOS
🔴 EP[XX]: [problema] — Acao: [quem faz o que, ate quando]
🟡 EP[XX]: [problema] — Acao: [...]
CAPACIDADE: [agente]: [carga]
PROXIMA ACAO DO SHOWRUNNER: [...]
```

## Relatorio mensal (fechamento)

Episodios publicados × planejados (on-time %), nota GATE media, performance (@analyst), crescimento (@growth), receita (@monetizer), saude do squad (sobrecarga, gargalos recorrentes, ajustes de processo) e plano do mes seguinte (episodios, guests confirmados, riscos). Numeros sempre com a fonte do dado; sem meta sem lastro.

## Checklist

Os itens `[ ]` do frontmatter (`Checklist:`) sao o passo a passo desta task; todos precisam estar marcados antes de entregar a saida.
