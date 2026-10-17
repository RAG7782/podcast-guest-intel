---
task: A/B Test
responsavel: "@analyst"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - hypothesis: "Se mudarmos X, então Y vai acontecer porque Z"
  - variable: Único elemento alterado (intro, título, capa, posição do ad, dia de lançamento, assunto do e-mail)
  - primary-metric: Métrica de sucesso primária e mínimo efeito que importa
Saida: |
  - test-design: Variantes, alocação, tamanho de amostra, duração, critério de parada
  - results: Tabela A x B com delta, intervalo de confiança e p-valor
  - decision: Adotar B / manter A / estender ou redesenhar
Checklist:
  - "[ ] Hipótese no formato se-então-porque, com mecanismo"
  - "[ ] Uma variável por teste; resto constante"
  - "[ ] Tamanho de amostra calculado ANTES de começar (efeito mínimo, alfa 0.05, poder 0.8)"
  - "[ ] Mecanismo de split viável (DAI, plataforma de e-mail, YouTube Test & Compare) — sem split real, declarar como pré/pós e não como A/B"
  - "[ ] Duração mínima de 2 semanas e ciclo semanal completo"
  - "[ ] Sem parada antecipada porque 'B já parece melhor'"
  - "[ ] Resultado reporta efeito e intervalo, não só p-valor"
  - "[ ] Learning registrado mesmo quando A vence ou empata"
---

# *run-abtest

Desenha, acompanha e analisa um experimento controlado.

## Uso

```bash
*run-abtest --hypothesis "intro de 20s aumenta completion" --metric completion_rate --mde 3pp
*run-abtest --analyze test-2026-03-intro
```

## Steps

1. **Hipótese:** "Se mudarmos [X], então [Y] porque [Z]". Sem mecanismo, não é hipótese.
2. **Design:** controle (A) × variante (B); alocação 50/50 (ou 70/30 se B for arriscada); amostra calculada; duração.
3. **Execução:** variantes produzidas por quem é dono do elemento (Wave para áudio, Clip para copy, Amp para social, Deal para posição de ad). Monitorar fatores externos (episódio viral, feriado).
4. **Análise:** comparar A × B na métrica primária; secundárias só como guarda-corpo.
5. **Decisão:** B vence → rollout; A vence/empate → manter e registrar; inconclusivo → estender ou redesenhar.

## Ideias de teste por elemento

| Elemento | Métrica |
|----------|---------|
| Duração da intro | completion rate |
| Título do episódio | taxa de clique / downloads 48 h |
| Capa/thumbnail (YouTube) | CTR |
| Posição do mid-roll | completion e ad completion |
| Dia de lançamento | downloads 48 h |
| Assunto da newsletter | open rate |

## Criterios de Qualidade

- [ ] Amostra calculada registrada antes do início
- [ ] Teste rodou até o fim planejado
- [ ] Decisão comunicada a Max e ao dono do elemento
