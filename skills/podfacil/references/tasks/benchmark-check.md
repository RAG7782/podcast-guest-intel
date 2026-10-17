---
task: Benchmark Check
responsavel: "@analyst"
responsavel_type: agent
atomic_layer: task
elicit: false
Entrada: |
  - own-metrics: Downloads/episódio, completion, crescimento, retenção do período
  - history: Mesmo período do ano anterior e trimestres anteriores
  - external-benchmarks: Relatórios públicos com fonte e data (opcional)
Saida: |
  - benchmark-report: Tabelas vs histórico próprio, vs pares e vs mercado (só com fonte)
  - gaps: Lacunas e pontos fortes priorizados
  - recommendations: Ações com dono
Checklist:
  - "[ ] Benchmark principal = histórico próprio (MoM, YoY, por formato de episódio)"
  - "[ ] Todo número de mercado tem fonte, data e definição de métrica; sem fonte, não entra"
  - "[ ] Pares estimados (reviews, ranking, seguidores) rotulados como estimativa"
  - "[ ] Comparação só entre métricas com a mesma definição"
  - "[ ] Gaps priorizados por impacto e com dono"
---

# *benchmark-check

Coloca as métricas do show em contexto. Trimestral, ou quando uma decisão depende de "estamos bem ou mal?".

## Uso

```bash
*benchmark-check --quarter Q1 --year 2026
*benchmark-check --vs-self --format entrevista
```

## Steps

1. **Vs. histórico próprio:** MoM, YoY e por formato (entrevista × solo × narrativo). É o benchmark mais confiável.
2. **Vs. pares:** podcasts da mesma categoria e porte. Dados raramente são públicos; usar proxies (contagem de reviews, posição em ranking, seguidores) marcados como estimativa, ou troca de dados com outros produtores.
3. **Vs. mercado:** só relatórios com fonte e data (ex.: estatísticas publicadas por hosts como Buzzsprout, relatórios de Edison Research). Registrar a definição de cada métrica; sem isso, não comparar.
4. **Leitura:** gaps e pontos fortes, com hipótese de causa e ação proposta.

## Template de saída

```markdown
# Benchmark — Q[X] [Ano]
| Métrica | Atual | Mesmo trimestre ano anterior | Variação |
| Comparação externa (fonte, data) | Nosso | Referência | Delta |
## Gaps e recomendações (dono)
```

## Criterios de Qualidade

- [ ] Nenhum número externo sem fonte
- [ ] Estimativas rotuladas
