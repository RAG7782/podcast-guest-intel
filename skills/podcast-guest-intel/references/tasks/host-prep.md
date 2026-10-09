---
task: Host Prep
responsavel: "@host"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - host-briefing: Briefing do convidado (saída de references/tasks/interview-prep.md) ou brief do episódio solo (references/tasks/episode-briefing.md)
  - script: Pauta/roteiro de Scout (references/tasks/script-writing.md)
  - recording-slot: Data, hora, formato (presencial/remoto, entrevista/solo/painel)
Saida: |
  - prep-sheet: Resumo do briefing, pesquisa adicional, perguntas âncora, aprofundamentos, plano de pacing
  - open-questions: Dúvidas devolvidas a Scout ou Link antes da gravação
Checklist:
  - "[ ] Briefing lido inteiro, incluindo pitfalls e áreas sensíveis"
  - "[ ] Pesquisa adicional: entrevistas anteriores do convidado (o que já foi perguntado) e trabalho publicado"
  - "[ ] 1 ângulo que ninguém perguntou ainda"
  - "[ ] 5-8 perguntas âncora abertas (nenhuma fechada ou indutora)"
  - "[ ] Perguntas de aprofundamento para as respostas mais prováveis"
  - "[ ] Plano de pacing: tom de abertura, transição de maior peso, energia prevista"
  - "[ ] Checklist ANCHOR revisado (abertura, naturalidade, controle, humanidade, outro)"
  - "[ ] Aquecimento vocal agendado (5 min antes)"
---

# *prepare-episode

Preparação do próprio host. Consome o briefing que Link (`*interview-prep`) e Scout produzem; não o substitui.

## Uso

```bash
*prepare-episode --episode EP06 --guest "Nome" --date "2026-04-10 14:00"
*prepare-episode --episode EP07 --solo
```

## Steps

1. **Ler** o briefing e a pauta. Sem briefing, no mínimo as perguntas âncora e os pitfalls.
2. **Pesquisar** 30-60 min: entrevistas anteriores (não repetir), livros/artigos/palestras, o ângulo inédito.
3. **Perguntas âncora** (5-8): o núcleo que precisa acontecer, em ordem lógica mas não rígida. Do banco de 20-25 do briefing, usar 8-12.
4. **Pacing:** tom inicial, energia, onde desacelerar (momento de peso) e onde acelerar (recap).
5. **Mentalizar:** conversa, não interrogatório. Aquecimento vocal 5 min antes.

Formato de saída: Output Example 1 em `agents/host.md`.

## Criterios de Qualidade

- [ ] Nenhuma pergunta âncora já respondida pelo convidado em entrevista anterior
- [ ] Áreas sensíveis do briefing refletidas no plano
