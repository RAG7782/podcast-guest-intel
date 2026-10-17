---
task: Ethics Review
responsavel: "@guardian"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - transcript: Transcricao do episodio (de @editor)
  - sponsor-list: Sponsors e integracoes do episodio
  - guest-disclosures: Vinculos declarados pelo convidado (formulario/booking)
Saida: |
  - ethics-verdict: recomendacao APROVADO | APROVADO COM AJUSTES | VETADO, com alertas de responsabilidade (decision.alerts.*)
  - required-changes: Ajustes obrigatorios (disclosure, content warning, corte, contexto)
  - recommended-changes: Ajustes recomendados
Checklist:
  - "[ ] Conflito de interesse: host/guest/sponsor com interesse no tema? Disclosure no audio e nas shownotes"
  - "[ ] Vies e equilibrio: tema controverso apresenta outras perspectivas? Linguagem carregada?"
  - "[ ] Potencial de dano: incitacao a violencia/odio (recomendacao VETADO imediata); gatilhos (content warning); desinformacao de saude/seguranca"
  - "[ ] Privacidade e consentimento (LGPD): terceiros identificaveis citados com base legal ou anonimizados; guest ciente de que o episodio e publico"
  - "[ ] Fairness: representacao justa de pessoas/grupos; citacao em contexto; sem estatistica cherry-picked"
  - "[ ] Opiniao nao e fact-checkavel — nao confundir opiniao polemica com desinformacao"
  - "[ ] Consultar assets/templates/editorial-ethics-code.md e assets/templates/sensitive-topics-guide.md"
  - "[ ] Registrar a recomendacao e motivos; se VETADO, acionar @producer com evidencia e alternativas para o humano decidir"
---

# *ethics-review

Auditoria de etica editorial de um episodio antes da publicacao. Complementa `references/tasks/fact-check-review.md` (fatos) e alimenta o quality gate de `references/tasks/episode-approval.md`.

## Recomendacao VETADO

Reservada a: risco legal alto (difamacao clara, violacao de direito autoral critica), quebra etica grave (incitacao, desinformacao perigosa deliberada) ou risco reputacional catastrofico. Nunca como censura de escolha editorial. Ao recomendar VETADO: evidencia + solucoes (regravar segmento, disclaimer robusto, adiar para consulta juridica) + alertas de responsabilidade. A palavra final e do humano responsavel pelo programa; seguir contra exige aceite explicito registrado (`references/contracts/human-decision.schema.json`). Regra rigida, sem aceite possivel: dado sensivel nao autodeclarado (LGPD art. 11).

## Formato de saida

```
ETHICS REVIEW — EP[XX]
Recomendacao: [APROVADO | APROVADO COM AJUSTES | VETADO]
Alertas: [codigo — severidade]
Obrigatorio: [item — responsavel — prazo]
Recomendado: [item]
Base: [secao do editorial-ethics-code / sensitive-topics-guide]
```

## Checklist

Os itens `[ ]` do frontmatter (`Checklist:`) sao o passo a passo desta task; todos precisam estar marcados antes de entregar a saida.
