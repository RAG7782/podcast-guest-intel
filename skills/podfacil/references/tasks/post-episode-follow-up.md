---
task: Post-Episode Follow-up
responsavel: "@guest-coordinator"
responsavel_type: agent
atomic_layer: task
elicit: false
Entrada: |
  - recording-done: Gravacao concluida (data D)
  - publish-date: Data de publicacao definida pelo @producer
  - promo-assets: Audiogram, quote cards e links (de @designer e @growth)
  - episode-metrics: Metricas da primeira semana (de @analyst)
Saida: |
  - thank-you-sent: Agradecimento enviado em D+1
  - assets-delivered: Kit de divulgacao entregue ao convidado
  - guest-feedback: Respostas da pesquisa de satisfacao (guest-review-protocol)
  - crm-updated: Registro do convidado atualizado (status, referrals, retorno)
Checklist:
  - "[ ] D+1: agradecimento + data estimada de publicacao (prazo canonico: references/workflows/guest-pipeline.md, Etapa 8)"
  - "[ ] Confirmar bio, foto e links para as show notes"
  - "[ ] Antes da publicacao: preview + assets de divulgacao"
  - "[ ] Dia da publicacao: avisar o convidado, marcar nas redes (com @growth)"
  - "[ ] ~1 semana apos: metricas + pesquisa de feedback (assets/templates/guest-review-protocol.md)"
  - "[ ] Pedir indicacao de proximos convidados"
  - "[ ] Atualizar CRM: status, nota de feedback, potencial de retorno"
---

# *follow-up

Fecha o ciclo com o convidado depois da gravacao: agradecimento, entrega do kit de
divulgacao, metricas e pedido de feedback e de indicacao. Dono unico:
@guest-coordinator. Prazos: a tabela canonica fica em `references/workflows/guest-pipeline.md`;
esta task nao os redefine.

## Steps

1. **Agradecimento (D+1).** E-mail personalizado citando um momento concreto da
   conversa, com a data estimada de publicacao e os proximos passos. Usar
   `assets/templates/guest-follow-up.md` (Template 1).
2. **Revisao opcional.** Se o convidado pediu para revisar algum trecho, seguir
   `assets/templates/guest-review-protocol.md`. Revisao cobre precisao factual, nunca
   veto editorial.
3. **Pre-publicacao.** Enviar preview e kit (audiogram, quote cards, links diretos),
   com copy sugerida para o convidado postar (Template 2).
4. **Dia da publicacao.** Avisar que esta no ar e coordenar com @growth o
   agradecimento publico (Templates 3 e 7).
5. **Uma semana depois.** Compartilhar metricas reais (sem arredondar para cima),
   enviar a pesquisa curta de satisfacao e pedir indicacoes (Template 4).
6. **CRM.** Registrar status, feedback, indicacoes e potencial de retorno.

## Regras

- Metricas so com numero medido pelo @analyst; sem dado, nao citar numero.
- Nunca pedir ao convidado dado sensivel (LGPD art. 11) na pesquisa de feedback.
- Se o convidado nao compartilhar, um lembrete gentil no maximo (Template 6).
