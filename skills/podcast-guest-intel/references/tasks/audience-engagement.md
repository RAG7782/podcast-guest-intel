---
task: Audience Engagement
responsavel: "@host"
responsavel_type: agent
atomic_layer: task
elicit: false
Entrada: |
  - episode: Episódio publicado e janela (ex.: 72 h pós-publicação)
  - channels: Comentários (YouTube, Instagram, Spotify), DMs, comunidade, newsletter
Saida: |
  - engagement-report: Comentários respondidos, DMs tratadas, post de follow-up
  - feedback-routing: Sugestões encaminhadas (tema → Scout, editorial → Max, comunidade → Amp)
Checklist:
  - "[ ] Comentários de destaque respondidos pelo próprio host"
  - "[ ] Crítica respondida com reconhecimento, sem defensiva"
  - "[ ] Pedido de ajuda sensível (saúde mental, jurídico) respondido com encaminhamento a profissional/serviço, nunca com conselho"
  - "[ ] Nenhum dado pessoal de ouvinte exposto em resposta pública"
  - "[ ] Sugestões de tema encaminhadas a Scout"
  - "[ ] Loop fechado quando sugestão vira episódio (crédito ao ouvinte, com consentimento)"
  - "[ ] Tempo limitado (ex.: 30-60 min/dia) — presença consistente, não 24/7"
---

# *engage-audience

Conexão do host com a audiência fora do ar. Complementa `references/tasks/community-building.md` (dono: Amp), que estrutura a comunidade.

## Uso

```bash
*engage-audience --episode EP06 --window 72h
```

## Steps

1. **Triar** comentários e DMs: destaque, crítica, pergunta, pedido de ajuda, sugestão.
2. **Responder** em primeira pessoa; não precisa responder tudo, precisa estar presente.
3. **Encaminhar** sugestões e sinais editoriais aos agentes donos.
4. **Follow-up** público (post) quando a resposta da audiência for, ela mesma, conteúdo.
5. **Integrar** no próximo episódio ("vários pediram X, então hoje...").

Formato de saída: Output Example 3 em `agents/host.md`.

## Criterios de Qualidade

- [ ] Toda sugestão encaminhada tem destinatário
- [ ] Limites do host respeitados (horário, privacidade)
