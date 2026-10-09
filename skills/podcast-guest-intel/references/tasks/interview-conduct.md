---
task: Interview Conduct
responsavel: "@host"
responsavel_type: agent
atomic_layer: task
elicit: false
Entrada: |
  - prep-sheet: Saída de references/tasks/host-prep.md
  - recording-setup: Sessão preparada por Wave (references/tasks/recording-session.md ou references/tasks/remote-recording.md)
Saida: |
  - recorded-interview: Conversa gravada
  - host-notes: Timestamps de momentos-chave, retakes necessários e quotes para Amp/Clip
Checklist:
  - "[ ] Rapport real antes de gravar (5-10 min, não 2 min de small talk)"
  - "[ ] Abertura: cold open, apresentação que justifica o convidado, roadmap"
  - "[ ] Follow-ups nascem da resposta, não da próxima linha da lista"
  - "[ ] Convidado fala a maior parte do tempo (referência prática: host ~30%)"
  - "[ ] Nenhuma interrupção no meio de pensamento importante"
  - "[ ] Pergunta sensível anunciada com opção de não responder"
  - "[ ] Sinal técnico de Wave = pausa imediata"
  - "[ ] Outro: 3 takeaways sintetizados pelo host, onde encontrar o convidado, agradecimento, CTA específico"
  - "[ ] Timestamps de destaque anotados e passados a Wave/Amp"
---

# *conduct-interview

Condução da entrevista segundo o framework ANCHOR (`agents/host.md`).

## Uso

```bash
*conduct-interview --episode EP06
*conduct-interview --episode EP08 --panel 3
```

## Tipos de pergunta

| Tipo | Quando usar | Exemplo |
|------|-------------|---------|
| Aberta | puxar história | "Como foi essa experiência?" |
| Sondagem | resposta rasa | "Pode dar um exemplo?" |
| Esclarecimento | garantir entendimento | "Quando você diz X, quer dizer Y?" |
| Desafio | testar premissa, com gentileza | "E se alguém argumentar Z?" |
| Reflexiva | sintetizar | "Então o que você está dizendo é..." |
| Hipotética | explorar cenário | "Se pudesse voltar, faria diferente?" |
| Fechada | confirmar fato (pouco) | "Isso foi em 2020?" |

## Momentos difíceis

- **Convidado desconfortável ou monossilábico:** compartilhar algo vulnerável primeiro; trocar opinião ("o que você acha") por experiência ("me conta uma situação em que..."); oferecer outro ângulo.
- **Convidado foge da pergunta:** reformular uma vez; se persistir, deixar ir e marcar para a edição.
- **Tangente longa:** "Quero voltar a um ponto que você disse antes...".
- **Falha técnica:** manter a calma, conversa leve enquanto Wave resolve, retomar com recap ("estávamos falando de X").

## Por formato

- **Especialista técnico:** traduzir sem simplificar demais; pedir exemplo concreto quando abstrair ("e quem nunca ouviu falar disso?").
- **Founder/empreendedor:** deixar a história se desenrolar; silêncio após revelação é conteúdo.
- **Painel (2-3):** orquestrar a palavra, provocar diálogo entre convidados, redistribuir atenção.
- **Convidado de acesso raro:** pesquisar além do habitual, nada de pergunta óbvia, assumir que há menos tempo que o combinado.
- **Tema sensível:** seguir `assets/templates/trauma-informed-interview.md`.

## Criterios de Qualidade

- [ ] Todas as perguntas âncora aconteceram ou a ausência foi registrada
- [ ] Notas de host entregues a Wave em até 1 h após a gravação
