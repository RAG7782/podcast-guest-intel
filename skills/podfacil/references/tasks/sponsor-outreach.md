---
task: Sponsor Outreach
responsavel: "@monetizer"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - podcast-metrics: Downloads, demographics, engagement
  - media-kit: Media kit profissional
  - target-sponsors: Lista de sponsors alinhados com valores
  - pricing: CPM ou flat rate pricing
Saida: |
  - sponsor-pipeline: Pipeline de sponsors (50+ contacted)
  - pitch-templates: Templates de pitch customizados
  - contracts: Contratos negociados
  - revenue-projection: Projecao de revenue 12 meses
Checklist:
  - "[ ] Research sponsors alinhados com valores do podcast"
  - "[ ] Criar media kit profissional (1-pager PDF)"
  - "[ ] Definir pricing pelo rate card interno (list/floor/premium); faixa de mercado so com fonte datada"
  - "[ ] Pitch template personalizado"
  - "[ ] Negociacao (CPM vs flat, host-read vs programmatic)"
  - "[ ] Contrato (SOW, deliverables, payment terms)"
  - "[ ] Insercao (host-read ou DAI)"
  - "[ ] Performance report (impressoes, clicks, conversoes)"
---

# *sponsor-outreach

Pipeline completo de sponsorship: research, media kit, pitch, negociacao, contrato, insercao, report. Alinhamento de valores obrigatorio.

## Uso

```bash
# Research sponsors alinhados
*sponsor-outreach --research --niche "tech,saas" --alignment-required

# Pitch sponsor especifico
*sponsor-outreach --pitch --target "Company XYZ" --type host-read

# Performance report pos-campanha
*sponsor-outreach --report --sponsor "ABC Corp" --campaign "Q1-2026"
```

## Steps (Resumido)

1. **Research sponsors**
   - Alinhados com valores do podcast
   - Budget (startups vs enterprise)
   - Historico de podcast advertising

2. **Media kit (1-pager PDF)**
   ```
   - Podcast name + tagline
   - Downloads mensais
   - Demographics (idade, genero, geo)
   - Top episodes
   - Testimonials
   - Pricing (CPM ou flat)
   - Contact
   ```

3. **Pricing**
   - Rate card interno: list price (publico), floor (minimo, nao publicado), premium (categoria exclusiva/sponsor ideal)
   - CPM ou flat por episodio; host-read costuma ter premium sobre programatico
   - Faixas de mercado variam por pais, nicho e ano: so citar com fonte e data (estimativa caso contrario)

4. **Pitch template**
   ```
   Oi {Nome},

   Produzo {Nome Podcast}, um show sobre {tema} com {X} downloads/mes.

   Nossa audiencia e {demografia} - perfeitamente alinhada com {Produto da Empresa}.

   Adoraria discutir uma parceria.

   Pricing:
   - CPM {list price} ({X} impressoes estimadas)
   - Host-read (mais autentico) com premium sobre o list

   Toparia uma call?

   Abraco,
   {Nome}
   ```

5. **Negociacao**
   - CPM vs flat
   - Host-read vs programmatic
   - Exclusividade (categoria)
   - Performance bonus

6. **Contrato (SOW)**
   - Deliverables: X episodios, Y impressoes
   - Timeline: Q1 2026
   - Payment terms: Net 30
   - Performance report: Mensal

7. **Insercao**
   - Host-read: Gravar script aprovado
   - DAI: Upload para plataforma

8. **Red flags (rejeitar ou renegociar)**
   - "Pay per conversion" sem base CPM
   - Produto de baixa qualidade ou suspeito (Sentinel faz due diligence)
   - Script rigido sem liberdade do host
   - Exclusividade total que bloqueia outras categorias
   - Prazo de pagamento longo (ex.: Net 90+) sem garantia

9. **Performance report**
   - Impressoes
   - Clicks (se UTM link)
   - Conversoes (se promo code)

## Criterios de Qualidade

- [ ] 50+ sponsors researched
- [ ] Alinhamento de valores validado
- [ ] Media kit profissional (1-pager)
- [ ] 10+ pitches enviados
- [ ] 2+ contratos fechados
- [ ] CPM >= floor do rate card
- [ ] Performance report entregue
- [ ] Revenue da temporada vs meta definida com Max
