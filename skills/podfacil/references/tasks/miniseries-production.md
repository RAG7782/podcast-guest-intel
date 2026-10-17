---
task: Miniseries Production
responsavel: "@producer"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - miniseries-concept: Tema/angulo da miniserie (4-6 episodios)
  - target-audience: Perfil especifico do publico
  - production-budget: Orcamento disponivel para producao elevada
  - timeline: Janela de producao e lancamento
Saida: |
  - miniseries-plan: Documento completo de planejamento
  - episode-arc: Arco narrativo dos 4-6 episodios
  - production-schedule: Cronograma de gravacao e pos-producao
  - launch-strategy: Estrategia de lancamento coordenado
Checklist:
  - "[ ] Definir conceito e unique angle da miniserie"
  - "[ ] Criar arco narrativo (inicio, desenvolvimento, climax, resolucao)"
  - "[ ] Estruturar 4-6 episodios com cliffhangers entre eles"
  - "[ ] Planejar producao elevada (sound design, musica original, multi-narradores)"
  - "[ ] Definir cadencia de lancamento (binge vs semanal vs diario)"
  - "[ ] Criar materiais de marketing especificos para miniserie"
  - "[ ] Coordenar com @researcher, @engineer, @composer para recursos"
  - "[ ] Planejar lancamento estrategico (trailer 2 semanas antes)"
  - "[ ] Definir metricas de sucesso (downloads, completion rate)"
  - "[ ] Validar viabilidade com squad (tempo, budget, recursos)"
---

# *miniseries-production

Producao completa de miniserie especial de 4-6 episodios com arco narrativo estruturado, producao elevada e lancamento estrategico. Diferente de episodios regulares, miniseries requerem planejamento de story arc, investimento de producao maior e coordenacao de lancamento.

## Uso

```bash
# Planejar miniserie tematica
*miniseries-production --concept "IA e Consciencia" --episodes 6 --launch "Q2-2026"

# Miniserie de aniversario (especial)
*miniseries-production --type anniversary --episodes 4 --production-level high

# Miniserie narrativa investigativa
*miniseries-production --format narrative --topic "Golpe Cripto Brasil" --episodes 5
```

## Steps

1. **Definir conceito e unique angle**
   - Tema suficientemente profundo para 4-6 episodios
   - Angulo que ninguem explorou ainda
   - Relevancia temporal (por que AGORA?)
   - Alinhamento com content pillars do podcast-bible
   - Validar com @researcher: ha conteudo suficiente?

2. **Criar arco narrativo estruturado**

   **Estrutura classica (3 atos adaptada):**

   **Episodio 1: Setup**
   - Apresentar tema, contexto, por que importa
   - Introduzir personagens/vozes principais
   - Estabelecer tensao/pergunta central
   - Cliffhanger: revelar primeira camada do problema

   **Episodios 2-3: Development**
   - Aprofundar complexidade
   - Explorar multiplas perspectivas
   - Revelar dados/research surpreedentes
   - Aumentar stakes (o que esta em jogo)
   - Cliffhangers: twists, revelacoes parciais

   **Episodio 4-5: Climax**
   - Convergir todas as threads
   - Revelar insight principal
   - Momento de maior tensao/emocao
   - Cliffhanger: setup para resolucao

   **Episodio 6: Resolution**
   - Resolver tensao principal
   - Amarrar pontas soltas
   - Licoes/takeaways
   - Abertura para futuro (tease season 2 da miniserie?)

3. **Estruturar episodios individuais**
   - Cada episodio precisa funcionar standalone (ouvinte pode comecar do meio)
   - MAS tambem avançar o arco narrativo
   - Recap nos primeiros 30s: "Nos episodios anteriores..."
   - Cliffhanger nos ultimos 60s: "No proximo episodio..."
   - Duracao consistente (ex: todos com 35-40min)

4. **Planejar producao elevada**

   **Sound design diferenciado:**
   - Contratar @composer para trilha original (tema da miniserie)
   - Usar transicoes sonoras sofisticadas
   - Ambientes sonoros imersivos (foley, atmosferas)
   - Multi-narradores (se narrativo): casting de voiceovers

   **Estrutura tecnica:**
   - Gravacao batch de todos episodios (consistencia)
   - Mixing/mastering com atencao extra
   - Spatial audio (Dolby Atmos) se budget permitir
   - Transcricoes profissionais (nao apenas AI)

5. **Definir cadencia de lancamento**

   **Opcoes estrategicas:**

   **A. Binge Release (todos de uma vez):**
   - Pros: Gera buzz imediato, completion rate alto
   - Cons: Curva de downloads concentrada, menos sustentacao
   - Melhor para: Narrativas investigativas, true crime

   **B. Semanal:**
   - Pros: Sustenta conversacao por 6 semanas, builds anticipation
   - Cons: Drop-off entre episodios
   - Melhor para: Temas educacionais, entrevistas sequenciais

   **C. Diario (5 dias seguidos):**
   - Pros: Momentum rapido, hype concentrado
   - Cons: Producao precisa estar 100% pronta
   - Melhor para: Miniseries curtas (4 eps), eventos especiais

6. **Criar materiais de marketing**

   **Trailer da miniserie (2min):**
   - Producao cinematica
   - Revelar tema sem spoilar
   - Teasers das melhores falas/momentos
   - CTA: "Disponivel dia X"
   - Lancar 2 semanas antes do EP01

   **Arte especial:**
   - Cover art unica para a miniserie (diferente do show regular)
   - Cada episodio com variacao da arte (mantendo identidade)
   - Social assets (9:16 para Stories, 1:1 para feed)

   **Landing page:**
   - Site dedicado: `podcast.com/miniseries/{nome}`
   - Sinopse completa
   - Lista de episodios com descricoes
   - Embed player
   - CTA para inscrever

7. **Coordenar recursos do squad**

   **Timeline realista:**
   - Pre-producao: 3-4 semanas (research, scripting, guest booking)
   - Producao: 2 semanas (gravacao batch)
   - Pos-producao: 4-6 semanas (editing, sound design, mastering)
   - Marketing: 2 semanas (trailer, assets, outreach)
   - TOTAL: 11-16 semanas (3-4 meses)

   **Validar capacidade:**
   - @researcher: Consegue entregar 6 episode briefs?
   - @engineer: Tem capacidade de edicao elevada?
   - @composer: Pode criar trilha original?
   - @growth: Pode liderar campanha de lancamento?
   - @monetizer: Oportunidade de sponsor exclusivo?

8. **Estrategia de lancamento coordenado**

   **Timeline de lancamento:**
   - T-14 dias: Trailer publicado
   - T-10 dias: Social teaser #1 (audiogram)
   - T-7 dias: Social teaser #2 (quotes)
   - T-3 dias: Email blast para subscribers
   - T-1 dia: Listening party (Discord/Twitter Space)
   - Dia 0: EP01 lancado (ou todos se binge release)
   - Pos-lancamento: 3-5 social clips por episodio

   **Cross-promotion:**
   - Guest em outros podcasts falando da miniserie
   - Feed drop em shows parceiros
   - Press kit para midia especializada
   - Pitch para Apple Podcasts / Spotify editorial (curation)

9. **Definir metricas de sucesso**

   **Downloads:**
   - Target: 2-3x o numero de downloads de episodios regulares
   - Tracking: Downloads acumulados vs episodios regulares

   **Completion rate:**
   - Target: >60% dos ouvintes completam todos os episodios
   - Tracking: Spotify/Apple Analytics

   **Engagement social:**
   - Target: Compartilhamentos, mencoes, reviews especificas da miniserie
   - Tracking: Social listening tools

   **Revenue:**
   - Sponsor exclusivo da miniserie?
   - Product tie-in?
   - Community growth?

10. **Documentar miniseries plan**
    - Documento master em `/plans/miniseries-{nome}-plan.md`
    - Arco narrativo em `/scripts/miniseries-{nome}/arc.md`
    - Cronograma em Notion/Airtable
    - Compartilhar com todo squad para alinhamento

## Output

### miniseries-{nome}-plan.md

```markdown
# Miniseries Plan: {Nome da Miniserie}

## Conceito

**Titulo:** {Nome}
**Tema:** {Descricao 1-paragrafo}
**Unique Angle:** {O que diferencia esta miniserie}
**Target Audience:** {Perfil especifico}
**Content Pillar:** {Qual pilar do podcast-bible}

**Por que AGORA?**
{Relevancia temporal - evento, tendencia, momento cultural}

---

## Arco Narrativo (6 Episodios)

### EP01: {Titulo} - Setup
**Duracao:** 35min
**Lancamento:** {Data}

**Sinopse:**
{2-3 frases sobre o episodio}

**Objetivos narrativos:**
- Apresentar tema e contexto
- Estabelecer tensao central
- Introduzir vozes principais

**Cliffhanger:**
"{Ultima frase que prende o ouvinte}"

---

### EP02: {Titulo} - Development I
**Duracao:** 38min
**Lancamento:** {Data}

**Sinopse:**
{2-3 frases}

**Objetivos narrativos:**
- Aprofundar complexidade
- Revelar primeira camada de dados surpreedentes
- Aumentar stakes

**Cliffhanger:**
"{Twist que leva ao EP03}"

---

(Repetir para EP03-EP06)

---

## Producao Elevada

### Sound Design
- **Trilha original:** @composer criando tema de 2min + 5 stingers
- **Ambientes:** Gravacao de foley e atmosferas
- **Multi-narradores:** 3 voiceovers para cenas dramaticas

### Estrutura Tecnica
- **Gravacao:** Batch recording (todas gravacoes em 2 semanas)
- **Mixing:** Spatial audio (Dolby Atmos) para listening imersivo
- **Transcricoes:** Revisao humana profissional (nao apenas AI)

---

## Cadencia de Lancamento

**Estrategia:** Semanal (1 episodio/semana por 6 semanas)

**Justificativa:**
- Sustenta conversacao por 6 semanas
- Builds anticipation entre episodios
- Permite ajustar marketing baseado em resposta

**Timeline:**
- 2026-04-01: EP01
- 2026-04-08: EP02
- 2026-04-15: EP03
- 2026-04-22: EP04
- 2026-04-29: EP05
- 2026-05-06: EP06 (finale)

---

## Marketing

### Trailer (2min)
- **Producao:** Cinematica, revela tema sem spoilar
- **Lancamento:** 2026-03-18 (2 semanas antes EP01)
- **Distribuicao:** YouTube, Instagram, feed principal

### Arte Especial
- Cover art unica (3000x3000)
- Variacao por episodio (mantendo identidade)
- Social assets (9:16, 1:1, 16:9)

### Landing Page
- URL: `podcast.com/miniseries/{nome}`
- Embed player + lista de episodios + sinopse
- CTA: Inscrever para notificacoes

### Campanha de Lancamento
- T-14: Trailer
- T-10: Social teaser #1
- T-7: Social teaser #2
- T-3: Email blast
- T-1: Listening party (Discord)
- Dia 0: EP01 publicado

---

## Recursos e Timeline

### Pre-Producao (4 semanas)
- @researcher: 6 episode briefs
- @researcher: 6 scripts completos
- @guest-coordinator: Booking de 12 entrevistados

### Producao (2 semanas)
- @engineer: Gravacao batch de todas entrevistas
- @composer: Trilha original

### Pos-Producao (6 semanas)
- @engineer: Edicao + mixing + mastering (6 episodios)
- @composer: Sound design + foley
- @editor: Transcricoes + show notes

### Marketing (2 semanas)
- @growth: Trailer + assets + outreach
- @designer: Arte + social clips

**TOTAL:** 14 semanas (3.5 meses)

---

## Budget

| Item | Custo |
|------|-------|
| Trilha original (@composer) | ${valor} |
| Voiceovers (3 atores) | ${valor} |
| Sound design elevado | ${valor} |
| Marketing (ads, assets) | ${valor} |
| Equipamento (se necessario) | ${valor} |
| **TOTAL** | **${valor}** |

---

## Metricas de Sucesso

| Metrica | Target | Tracking |
|---------|--------|----------|
| Downloads totais | {numero} (3x regular) | Spotify/Apple Analytics |
| Completion rate | >60% | Spotify Analytics |
| Social mentions | {numero} | Social listening |
| Reviews | {numero} reviews especificas | Apple Podcasts |
| Sponsor revenue | ${valor} | @monetizer |

---

## Risks & Mitigation

| Risk | Mitigation |
|------|------------|
| Producao atrasada | Buffer de 2 semanas antes do lancamento |
| Baixo engagement | Marketing antecipado 2 semanas antes |
| Budget estourado | Aprovar orcamento antes de iniciar |

---

**Preparado por:** @producer
**Data:** {data}
**Status:** {Planning / In Production / Launching}
```

## Criterios de Qualidade

- [ ] Conceito suficientemente profundo para 4-6 episodios
- [ ] Unique angle claramente articulado (nao e episodio regular extendido)
- [ ] Arco narrativo estruturado com inicio, desenvolvimento, climax, resolucao
- [ ] Cliffhangers entre episodios para manter engagement
- [ ] Producao elevada planejada (trilha original, sound design, multi-narradores)
- [ ] Cadencia de lancamento justificada (binge vs semanal vs diario)
- [ ] Timeline realista (11-16 semanas total)
- [ ] Validacao de capacidade com todo o squad
- [ ] Budget detalhado e aprovado antes de iniciar
- [ ] Materiais de marketing planejados (trailer, arte, landing page)
- [ ] Estrategia de lancamento coordenada (timeline de 2 semanas)
- [ ] Metricas de sucesso definidas e trackable
- [ ] Buy-in de todo o squad (todos entendem o investimento extra)
