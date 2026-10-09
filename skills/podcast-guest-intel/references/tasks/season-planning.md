---
task: Season Planning
responsavel: "@producer"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - podcast-bible: Documento base com brand identity, valores, target audience
  - content-pillars: 3-5 pilares tematicos principais do show
  - calendar-constraints: Feriados, eventos da industria, temporadas sazonais
  - performance-data: Metricas de temporadas anteriores (se existirem)
Saida: |
  - season-plan: Documento completo de planejamento (90 dias)
  - editorial-calendar: Calendario com datas, temas, formatos
  - guest-wishlist: Lista priorizada de convidados desejados
  - production-schedule: Timeline de producao com milestones
  - success-metrics: Metas por tier (awareness, engagement, revenue)
Checklist:
  - "[ ] Revisar podcast-bible.md e extrair content pillars"
  - "[ ] Definir numero de episodios da temporada (8-24 eps tipico)"
  - "[ ] Distribuir content pillars ao longo da temporada"
  - "[ ] Variar formatos (solo, entrevista, narrativo, mesa-redonda)"
  - "[ ] Incluir 1-2 semanas de descanso para pre-producao"
  - "[ ] Criar guest wishlist com 3x mais nomes que vagas"
  - "[ ] Alinhar calendario com eventos relevantes da industria"
  - "[ ] Definir KPIs por tier (reach, retention, revenue)"
  - "[ ] Planejar episodios especiais (season premiere, mid-season, finale)"
  - "[ ] Validar viabilidade com @engineer sobre capacidade de producao"
---

# *season-planning

Planejamento estrategico completo de temporada de podcast, baseado em content pillars e alinhado com os objetivos de negocio definidos no podcast-bible.md. Esta task cria o roadmap editorial para 90 dias com visao clara de temas, formatos, convidados e metas.

## Uso

```bash
# Invocar planejamento de nova temporada
*season-planning --season 2 --duration 90-days --episodes 12

# Re-planejar temporada com ajustes
*season-planning --season 2 --adjust --reason "mudanca de pillar"

# Planejar miniserie especial
*season-planning --type miniseries --episodes 6 --theme "especial-aniversario"
```

## Steps

1. **Analisar podcast-bible.md**
   - Extrair content pillars (3-5 temas principais)
   - Revisar target audience e pain points
   - Confirmar brand voice e valores
   - Identificar unique selling proposition

2. **Definir estrutura da temporada**
   - Numero de episodios (8-12 para iniciantes, 12-24 para estabelecidos)
   - Cadencia de publicacao (semanal, quinzenal, diaria)
   - Duracao media por episodio
   - Distribuicao de formatos (60% entrevista, 20% solo, 20% especiais)

3. **Mapear calendario editorial**
   - Distribuir content pillars ao longo de 90 dias
   - Alternar temas para evitar fadiga
   - Alinhar com eventos sazonais/industria
   - Planejar episodios especiais (premiere, mid-season climax, finale)
   - Incluir 1-2 semanas de buffer para pre-producao

4. **Criar guest wishlist estrategica**
   - Listar 3x mais convidados que vagas (ex: 36 nomes para 12 episodios)
   - Priorizar por: relevancia, alcance, alinhamento de valores
   - Incluir diversity check por criterios nao sensiveis (area, regiao, trajetoria, pensamento; nada inferido — `references/checklists/diversity-check.md`)
   - Categorizar por tier (A-list dream, B-list realistic, C-list backup)
   - Anotar conexoes existentes para facilitar outreach

5. **Definir metas por tier**
   - **Awareness:** downloads target, novos ouvintes, impressoes sociais
   - **Engagement:** retention rate, completion rate, social shares
   - **Revenue:** sponsors, products, community contributions
   - Estabelecer baselines e growth targets (ex: +20% downloads vs temporada anterior)

6. **Planejar producao**
   - Timeline de gravacao (batch recording vs episodio por episodio)
   - Milestones criticos (launch date, mid-season, finale)
   - Recursos necessarios (equipamento, locacao, equipe)
   - Budget estimado por episodio

7. **Documentar season plan**
   - Documento master em `/plans/season-{number}-plan.md`
   - Calendario visual em Notion/Airtable/Google Sheets
   - Compartilhar com todo squad para alinhamento

## Output

### season-{number}-plan.md

```markdown
# Season {N} Planning - {Nome do Show}

## Overview
- **Temporada:** {numero}
- **Periodo:** {data inicio} a {data fim} (90 dias)
- **Episodios:** {numero total}
- **Cadencia:** {semanal/quinzenal}
- **Formato principal:** {entrevista/solo/narrativo}

## Content Pillars
1. **Pillar 1:** {nome} - {descricao} - {X episodios}
2. **Pillar 2:** {nome} - {descricao} - {X episodios}
3. **Pillar 3:** {nome} - {descricao} - {X episodios}

## Editorial Calendar

| Sem | Data Pub | Episodio | Pillar | Formato | Guest/Tema | Status |
|-----|----------|----------|--------|---------|------------|--------|
| 01  | 2026-03-01 | S02E01 | Pillar 1 | Entrevista | João Silva | Pre-producao |
| 02  | 2026-03-08 | S02E02 | Pillar 2 | Solo | - | Briefing |
| ... | ... | ... | ... | ... | ... | ... |

## Guest Wishlist (Top 12)

### Tier A (Dream Guests)
1. **Nome** - bio 1-linha - conexao existente? - topico
2. **Nome** - bio 1-linha - conexao existente? - topico

### Tier B (Realistic)
...

### Tier C (Backup)
...

## Success Metrics

### Awareness
- Downloads target: {numero} (+X% vs S01)
- Novos ouvintes: {numero}
- Social reach: {numero impressoes}

### Engagement
- Retention rate: {percentual}% (primeiro 80% do episodio)
- Completion rate: {percentual}%
- Social shares: {numero}

### Revenue
- Sponsor deals: {numero} x ${valor}
- Product sales: ${valor}
- Community contributions: ${valor}

## Production Timeline

- **Pre-producao:** {datas} - research, briefings, guest booking
- **Gravacao:** {datas} - batch recording S02E01-E04
- **Pos-producao:** {datas} - editing, mixing, mastering
- **Launch:** {data} - S02E01 premiere
- **Mid-season:** {data} - S02E06 especial
- **Finale:** {data} - S02E12 season finale

## Budget Estimado
- Producao: ${valor}
- Marketing: ${valor}
- Equipamento: ${valor}
- Total: ${valor}

## Risks & Mitigation
- **Risk:** Guest cancellation - **Mitigation:** Backup guests tier C sempre prontos
- **Risk:** Atraso de producao - **Mitigation:** Buffer de 2 semanas
```

## Criterios de Qualidade

- [ ] Content pillars representam 100% dos episodios (nada fora de brand)
- [ ] Calendario viavel com buffers adequados
- [ ] Guest wishlist 3x maior que vagas necessarias
- [ ] Diversidade de convidados (area, regiao, trajetoria, pensamento; nada inferido)
- [ ] Variacao de formatos para evitar monotonia
- [ ] KPIs SMART (especificos, mensuraveis, alcancaveis, relevantes, temporais)
- [ ] Alinhamento com eventos da industria e sazonalidade
- [ ] Buy-in de todo o squad (validacao com @engineer, @growth, @monetizer)
- [ ] Documento acessivel e versionado (GitHub/Notion)
- [ ] Timeline realista validada por producoes anteriores
