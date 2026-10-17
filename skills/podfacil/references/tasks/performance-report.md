---
task: Performance Report
responsavel: "@analyst"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - analytics-data: Spotify, Apple, YouTube, RSS analytics
  - timeframe: Mensal, trimestral, anual
  - benchmarks: Historico proprio; benchmark de mercado so com fonte e data (ver references/tasks/benchmark-check.md)
  - qualitative-feedback: Reviews, NPS, community sentiment
Saida: |
  - performance-report: Relatorio completo mensal
  - downloads-breakdown: Downloads por plataforma
  - retention-analysis: Retention curve, drop-off points
  - audience-demographics: Idade, genero, geo, device
  - revenue-metrics: CPM, sponsor revenue, products
  - recommendations: Acoes baseadas em dados
Checklist:
  - "[ ] Coletar dados de Spotify for Creators"
  - "[ ] Coletar dados de Apple Podcasts Connect"
  - "[ ] Coletar dados de YouTube Analytics"
  - "[ ] Calcular retention curve (AI analysis)"
  - "[ ] Identificar drop-off points (onde abandonam)"
  - "[ ] Audience demographics (idade, genero, geo)"
  - "[ ] Top episodios (mais baixados)"
  - "[ ] Growth rate vs mes anterior"
  - "[ ] Revenue metrics (CPM, sponsors, products)"
  - "[ ] Qualitative feedback (reviews, NPS)"
  - "[ ] Benchmark comparison (historico proprio; mercado so com fonte)"
  - "[ ] Recommendations baseadas em dados"
---

# *performance-report

Relatorio mensal completo: downloads, retention curve, drop-off analysis (AI), demographics, top episodes, growth rate, revenue, feedback, benchmarks, recommendations.

## Uso

```bash
# Report mensal
*performance-report --month march --year 2026

# Report trimestral (Q1)
*performance-report --quarter Q1 --year 2026

# Report anual
*performance-report --year 2025 --full-year
```

## Output (Template Resumido)

```markdown
# Performance Report: Marco 2026

## Executive Summary

- Downloads: 45,230 (+18% vs fev)
- Retention: 68% (primeiros 80% do episodio)
- Top episode: S02E03 (8,420 downloads)
- Revenue: $3,200 (sponsors + products)
- Reviews: +12 (5 estrelas)

## Downloads por Plataforma

| Plataforma | Downloads | % Total | Growth |
|------------|-----------|---------|--------|
| Spotify | 22,100 | 49% | +15% |
| Apple Podcasts | 15,800 | 35% | +20% |
| YouTube | 4,500 | 10% | +25% |
| RSS (outros) | 2,830 | 6% | +12% |

## Retention Curve (AI Analysis)

- 0-25%: 95% retencao (strong hook)
- 25-50%: 80% retencao (bom)
- 50-75%: 68% retencao (drop esperado)
- 75-100%: 58% retencao (excelente)

**Drop-off points:**
- 12:30 - Divagacao longa (cortar futuro)
- 28:00 - Ad mid-roll (esperado)

## Audience Demographics

- **Idade:** 25-34 (45%), 35-44 (30%), 18-24 (15%)
- **Genero:** 60% masculino, 38% feminino, 2% outro
- **Geo:** Brasil (65%), EUA (20%), Portugal (10%), outros (5%)
- **Device:** Mobile (75%), Desktop (20%), Smart speaker (5%)

## Top Episodes (Marco)

1. S02E03 - IA e Etica (8,420 downloads)
2. S02E02 - Futuro do Trabalho (7,100)
3. S02E01 - Season Premiere (6,800)

## Growth Metrics

- Downloads: +18% vs fev
- Subscribers: +250 novos
- Reviews: +12 (total: 187)
- Social followers: +320

## Revenue

| Source | Valor | % Total |
|--------|-------|---------|
| Sponsor A (CPM) | $2,100 | 66% |
| Sponsor B (Flat) | $800 | 25% |
| Products/Merch | $300 | 9% |
| **TOTAL** | **$3,200** | **100%** |

## Qualitative Feedback

### Reviews (Best of)
- "Melhor podcast de tech em PT-BR!" - 5 estrelas
- "Episodio com Maria Santos mudou minha perspectiva" - 5 estrelas

### NPS: 68 (Excelente)

## Benchmark Comparison

| Metrica | Fev 2026 | Mar 2026 | Mar 2025 (YoY) |
|---------|----------|----------|----------------|
| Downloads/ep | 3,190 | 3,770 | 2,640 |
| Retention | 65% | 68% | 63% |
| Reviews | 171 | 187 | 98 |

Comparacao com mercado so com fonte e data citadas (ver `references/tasks/benchmark-check.md`).

## Recommendations

1. **Reduzir divagacoes:** Drop-off em 12:30 (cortar 2-3min)
2. **Aumentar YouTube:** +25% growth, investir em video
3. **Pitch sponsors maiores:** CPM atual $18, target $25
4. **Review campaign:** 187 reviews → target 250 ate Q2
5. **Guest diversity:** Aumentar internacional (17% → 25%)

---

**Preparado por:** @analyst
**Data:** 2026-04-05
**Proximo report:** Maio 2026
```

## Criterios de Qualidade

- [ ] Dados de todas plataformas coletados
- [ ] Retention curve calculada (AI analysis)
- [ ] Drop-off points identificados
- [ ] Demographics completos
- [ ] Growth rate vs mes anterior
- [ ] Revenue breakdown
- [ ] Qualitative feedback (reviews, NPS)
- [ ] Benchmark comparison
- [ ] 3-5 recommendations acionaveis
- [ ] Report entregue ate dia 5 do mes seguinte
