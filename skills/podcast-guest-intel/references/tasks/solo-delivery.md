---
task: Solo Delivery
responsavel: "@host"
responsavel_type: agent
atomic_layer: task
elicit: false
Entrada: |
  - script-or-outline: Roteiro ou outline de Scout (references/tasks/script-writing.md)
  - format: Storytelling/documentário, educacional, comentário ou Q&A
Saida: |
  - recorded-solo: Episódio solo gravado (takes múltiplos por segmento quando preciso)
  - host-notes: Melhor take por segmento e timestamps para Wave
Checklist:
  - "[ ] Modo escolhido: roteiro integral, outline (padrão) ou improviso"
  - "[ ] Hook nos primeiros 60 s + promessa do episódio"
  - "[ ] 3-5 beats com transições sinalizadas"
  - "[ ] Exemplos concretos em cada beat"
  - "[ ] Pausas planejadas após afirmação forte e antes de revelação"
  - "[ ] Pausa de recuperação a cada ~30-40 min em gravação longa"
  - "[ ] Resolução/takeaways + CTA"
---

# *deliver-solo

Apresentação sem convidado: a energia vem toda do host e a estrutura precisa ser à prova de distração.

## Uso

```bash
*deliver-solo --episode EP07 --format educacional
```

## Estrutura

1. **Hook (60 s):** dado surpreendente, pergunta provocativa ou anedota; promessa "neste episódio você vai...".
2. **Corpo:** beats claros, transições sinalizadas ("primeiro X, depois Y"), pacing variando com o conteúdo.
3. **Resolução:** fecho da narrativa ou lições-chave + CTA.

## Roteiro x outline x improviso

- **Roteiro integral:** precisão; risco de soar lido sem prática de locução.
- **Outline (recomendado):** estrutura + naturalidade; exige edição de tangentes.
- **Improviso:** autenticidade máxima; risco de incoerência e edição pesada.

## Técnica por formato

- **Storytelling/documentário:** ritmo de cena, presente histórico ("É 2019. Paulo abre o e-mail."), cliffhanger entre beats.
- **Educacional:** abrir com problema reconhecível, etapas numeradas, analogias do cotidiano, aplicação imediata no fim.
- **Comentário:** contexto antes da opinião, reconhecer o outro lado, primeira pessoa explícita ("na minha visão").

## Criterios de Qualidade

- [ ] Hook testado em voz alta antes de gravar
- [ ] Nenhum beat sem exemplo concreto
