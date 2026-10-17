---
task: Fact-Check Review
responsavel: "@guardian"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - episode-transcript: Transcricao completa do episodio
  - claims-list: Lista de claims factuais feitas
  - sources-cited: Fontes citadas no episodio
  - sponsor-disclosures: Patrocinios mencionados
Saida: |
  - fact-check-report: Relatorio de fact-check
  - corrections-needed: Lista de correcoes recomendadas
  - alerts: alertas de responsabilidade (R-FACTCHECK-*) para o humano decidir
  - compliance-check: LGPD, CONAR, disclosure compliance
  - diversity-scorecard: Diversity check dos guests da temporada
Checklist:
  - "[ ] Verificar todas claims factuais (data points, stats)"
  - "[ ] Validar fontes citadas (papers, estudos, livros)"
  - "[ ] Checar sponsor disclosures (CONAR compliance)"
  - "[ ] Validar LGPD compliance (dados pessoais)"
  - "[ ] Diversity check (area, regiao, trajetoria dos guests; nunca inferir atributo sensivel)"
  - "[ ] Claim nao verificavel: recomendar corte + alerta (o humano decide; seguir contra = aceite registrado)"
  - "[ ] Propor correcoes pre-publicacao"
  - "[ ] Documentar fact-check report"
---

# *fact-check-review

Validacao pre-publicacao de claims factuais, fontes, sponsor disclosures (CONAR), LGPD compliance, diversity check. Recomenda e alerta, nao veta: a decisao e do humano responsavel (references/principios.md). Excecao rigida: dado sensivel nao autodeclarado (LGPD art. 11).

## Uso

```bash
# Fact-check episodio completo
*fact-check-review --episode S02E03 --full-check

# Check apenas sponsor disclosures
*fact-check-review --episode S02E05 --check-disclosures-only

# Diversity check da temporada
*fact-check-review --season 2 --diversity-check
```

## Steps (Resumido)

1. **Verificar claims factuais**
   - Estatisticas mencionadas: Source verificavel?
   - Estudos citados: Paper existe? Revisado por pares?
   - Fatos historicos: Corretos?

2. **Validar fontes**
   - Fontes primarias > secundarias
   - Peer-reviewed > blog
   - Checar reputacao da fonte

3. **Sponsor disclosures (CONAR)**
   - Patrocinio claramente divulgado?
   - "Este episodio e patrocinado por X"
   - Nao confundir com conteudo editorial

4. **LGPD compliance**
   - Dados pessoais citados com consentimento?
   - Nomes anonimizados se necessario

5. **Diversity check**
   | Temporada | Guests | Fora do Sudeste | Junior/Mid | Areas distintas | Estreantes |
   |-----------|--------|-----------------|------------|-----------------|------------|
   | S02 | 12 | 4 (33%) | 3 (25%) | 5 | 4 (33%) |
   - Regra rigida LGPD (sem aceite possivel): ficha de convidado com raca/etnia, genero, orientacao sexual ou deficiencia
     **inferidos** (nao autodeclarados) = dado sensivel sem base legal (art. 11). Remover.

6. **RECOMENDACAO + ALERTA (nao veto)**
   - Claim sem fonte: recomendar corte; alerta `R-FACTCHECK-SEM-FONTE`
   - Disclosure faltando: recomendar inclusao; alerta `R-FACTCHECK-DISCLOSURE`
   - Dado pessoal de terceiro sem base clara: alerta `R-FACTCHECK-LGPD`
   - Dado sensivel nao autodeclarado: REMOVER (regra rigida, LGPD art. 11; nao e alerta)
   - Seguir contra qualquer alerta: aceite explicito registrado (`references/contracts/human-decision.schema.json`)

7. **Propor correcoes**
   - Lista de correcoes para @editor
   - Re-gravar se necessario

8. **Documentar report**

## Output (Template)

```markdown
# Fact-Check Report: S02E03

## Claims Verificadas: 8/8 ✅

1. **"70% das startups falham"**
   - Fonte: CB Insights 2024 Report
   - Status: ✅ Verificado

2. **"IA pode detectar depressao com 85% accuracy"**
   - Fonte: Paper Nature 2023
   - Status: ✅ Verificado

(... continua para todas claims)

## Fontes Citadas: 5/5 ✅

Todas fontes verificadas e linkadas corretamente.

## Sponsor Disclosures: ✅ Compliant

- Disclosure claro: "Este episodio e patrocinado por XYZ"
- CONAR compliant

## LGPD Compliance: ✅

Nenhum dado pessoal sensivel sem consentimento.

## Diversity Scorecard (Season 2)

| Metrica | Current | Target | Status |
|---------|---------|--------|--------|
| Fora do Sudeste | 4/12 (33%) | 20%+ | ✅ |
| Areas distintas | 5 | 4+ | ✅ |
| Internacional | 2/12 (17%) | 20%+ | ⚠️ |

## Recomendacao: ✅ APROVADO PARA PUBLICACAO

Nenhuma correcao necessaria.

---

**Fact-checked por:** @guardian
**Data:** 2026-03-14
```

## Criterios de Qualidade

- [ ] 100% claims factuais verificadas
- [ ] Fontes validadas (peer-reviewed prioritized)
- [ ] Sponsor disclosures compliant (CONAR)
- [ ] LGPD compliant (sem dados sensiveis)
- [ ] Diversity check validado
- [ ] Alertas emitidos e decisao humana registrada quando contra a recomendacao
- [ ] Correcoes propostas pre-publicacao
- [ ] Fact-check report documentado
