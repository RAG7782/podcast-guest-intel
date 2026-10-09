---
task: Episode Approval
responsavel: "@producer"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - final-audio: Master final entregue por @engineer
  - show-notes: Shownotes e capitulos de @editor
  - artwork: Arte do episodio de @designer
  - guardian-verdict: Resultado de *fact-check / *ethics-review de @guardian
  - release-date: Data planejada no season-calendar
Saida: |
  - gate-verdict: recomendacao APPROVE | REQUEST CHANGES | HOLD, com motivo por dimensao GATE e alertas de responsabilidade
  - human-decision: registro do humano responsavel (references/contracts/human-decision.schema.json) quando ele decide publicar contra a recomendacao
  - change-requests: Lista de ajustes com responsavel e prazo (se REQUEST CHANGES)
  - release-notice: Comunicacao de greenlight para @distributor e @growth (se APPROVE)
Checklist:
  - "[ ] Ouvir o episodio completo (sem aprovacao por amostra)"
  - "[ ] G — Goal: alinhado ao content pillar; mensagem central clara no inicio"
  - "[ ] A — Audience: serve a audiencia; densidade calibrada"
  - "[ ] T — Technical: loudness/true peak conforme assets/templates/audio-specs.md; shownotes, artwork e RSS prontos"
  - "[ ] E — Ethical: recomendacao de @guardian anexada; pendencia aberta vira alerta para o humano"
  - "[ ] S — Schedule: @distributor e @growth prontos; guest avisado da data"
  - "[ ] Percorrer assets/templates/release-checklist.md"
  - "[ ] Registrar decisao e motivo; se HOLD, abrir assets/templates/episode-postmortem.md quando resolvido"
---

# *approve-episode

Quality gate final do episodio. Aplica o framework GATE (5 dimensoes) descrito em `agents/producer.md` e RECOMENDA APPROVE, REQUEST CHANGES ou HOLD. A decisao de publicar e do humano responsavel pelo programa (references/principios.md, "a decisao e sempre humana").

## Regras de decisao

- **APPROVE**: as 5 dimensoes passaram e @guardian nao tem pendencia.
- **REQUEST CHANGES**: 1-2 dimensoes falharam e a correcao cabe antes da data de publicacao. Cada item vai para o agente dono, com prazo.
- **HOLD**: falha etica apontada por @guardian, guest pede retirada de trecho, fato central contestado apos a gravacao, ou crise externa torna o tema inadequado. Publicacao e promocao suspensas ate a decisao do humano responsavel.

A recomendacao de @guardian entra no gate como alerta (ver `agents/guardian.md`). Publicar contra o gate ou contra @guardian exige aceite explicito registrado (`references/contracts/human-decision.schema.json`, alerta `R-PUBLICACAO-GATE`): quem, quando, quais alertas viu. Regra rigida, sem aceite possivel: dado sensivel nao autodeclarado pelo titular (LGPD art. 11) sai do episodio.

## Saida

Usar os blocos "Comunicacoes do Showrunner" de `agents/producer.md` (APROVADO / AJUSTES / HOLD). Depois do APPROVE, a publicacao segue em `references/tasks/episode-publishing.md` (@distributor).

## Checklist

Os itens `[ ]` do frontmatter (`Checklist:`) sao o passo a passo desta task; todos precisam estar marcados antes de entregar a saida.
