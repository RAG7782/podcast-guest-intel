---
task: Revenue Report
responsavel: "@monetizer"
responsavel_type: agent
atomic_layer: task
elicit: false
Entrada: |
  - contracts: Contratos de sponsor (início, fim, CPM/flat, receita por episódio)
  - membership: Membros, MRR, novos, cancelamentos
  - other-revenue: Afiliados, produtos, eventos, value4value
  - ad-performance: Impressões, completion de ad, conversões (Pulse)
Saida: |
  - revenue-report: Relatório mensal no formato de assets/templates/revenue-report.md
  - forecast: Próximo mês (confirmado x pipeline x riscos)
  - recommendations: Ações com dono
Checklist:
  - "[ ] Receita total, crescimento MoM e receita por episódio"
  - "[ ] Breakdown por fonte com % do total"
  - "[ ] Performance por sponsor (episódios, impressões, conversões, CPM efetivo)"
  - "[ ] Membership: MRR, membros, churn, receita média por membro"
  - "[ ] Status de pagamento (faturado, pago, atrasado)"
  - "[ ] Concentração: nenhuma fonte/sponsor acima do teto acordado com Max"
  - "[ ] Forecast separando confirmado de pipeline"
  - "[ ] Renovações dos próximos 30 dias listadas"
---

# *revenue-report

Fechamento financeiro mensal da monetização, para Max.

## Uso

```bash
*revenue-report --month 2026-01
```

## Steps

1. Consolidar contratos, membership e outras fontes (planilha ou CRM: Airtable, Notion, Google Sheets).
2. Cruzar com dados de ad performance de Pulse.
3. Preencher `assets/templates/revenue-report.md`.
4. Forecast: contratos confirmados + pipeline ponderado + riscos (não renovação, sazonalidade).
5. Recomendações: prospectar categorias vazias, renegociar sponsors com conversão acima da média, ajustes de membership.

Exemplo preenchido: Output Example 2 em `agents/monetizer.md`.

## Criterios de Qualidade

- [ ] Totais batem com a soma das fontes
- [ ] Toda recomendação com dono
