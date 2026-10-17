---
task: Episode Briefing
responsavel: "@researcher"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - episode-topic: Tema do episodio conforme season plan
  - content-pillar: Qual dos 3-5 pillars este episodio atende
  - guest-info: Dados do convidado (se entrevista) ou tema (se solo)
  - target-audience: Perfil do ouvinte ideal deste episodio
Saida: |
  - episode-brief: Documento de 1-2 paginas com research completo
  - key-angles: 3-5 angulos unicos para abordar o tema
  - data-points: Estatisticas, estudos, fatos relevantes
  - sources-list: Lista de fontes verificadas (minimo 5)
  - talking-points: Lista de topicos para o host cobrir
Checklist:
  - "[ ] Research profundo sobre o tema (minimo 2h)"
  - "[ ] Identificar angulo unico que diferencia de outros podcasts"
  - "[ ] Coletar 5-10 data points verificados (estudos, stats, fatos)"
  - "[ ] Listar fontes primarias e secundarias (papers, livros, especialistas)"
  - "[ ] Criar lista de talking points para o host"
  - "[ ] Sugerir perguntas provocativas (se entrevista)"
  - "[ ] Identificar potenciais controversias ou areas sensiveis"
  - "[ ] Adicionar context sobre momento atual do tema"
  - "[ ] Incluir competitive analysis (o que outros podcasts ja fizeram)"
  - "[ ] Validar fact-check preliminar de todas as claims"
---

# *episode-briefing

Research completo e briefing estrategico para um episodio especifico. Transforma um topico em conteudo acionavel para o host, com angulos unicos, dados verificados e estrutura narrativa clara. Base fundamental para episodios de qualidade.

## Uso

```bash
# Briefing para episodio de entrevista
*episode-briefing --episode S02E03 --guest "Maria Santos" --pillar "inovacao"

# Briefing para episodio solo
*episode-briefing --episode S02E05 --type solo --topic "10 licoes de 2025"

# Briefing urgente (research acelerado)
*episode-briefing --episode S02E08 --fast-track --deadline "48h"
```

## Steps

1. **Deep research sobre o tema**
   - Pesquisar Google Scholar, PubMed, ResearchGate para papers
   - Consultar livros de referencia via Amazon/Goodreads
   - Buscar podcasts/videos existentes sobre o tema (competitive analysis)
   - Monitorar Twitter/LinkedIn/Reddit para discussoes atuais
   - Tempo minimo: 2h de research focado

2. **Identificar angulo unico**
   - Perguntar: "O que ninguem esta falando sobre isso?"
   - Cruzar temas (ex: "IA + etica em saude mental infantil")
   - Buscar contrarian takes com base em evidencias
   - Conectar tema ao momento cultural atual
   - Validar com podcast-bible.md se o angulo esta on-brand

3. **Coletar data points verificados**
   - Minimo 5-10 estatisticas/estudos/fatos solidos
   - SEMPRE anotar fonte completa (autor, ano, publicacao, link)
   - Priorizar fontes primarias (papers originais > noticias)
   - Verificar reputacao da fonte (peer-reviewed > blog)
   - Evitar data points sensacionalistas sem base

4. **Mapear estrutura narrativa**
   - Cold open: hook emocional ou data point chocante
   - Value promise: "neste episodio voce vai aprender X"
   - Blocos de conteudo (3-5 blocos tematicos)
   - Climax: insight mais valioso do episodio
   - CTA: acao especifica para o ouvinte tomar

5. **Criar talking points para o host**
   - Lista de 8-12 topicos a cobrir
   - Ordem logica (intro → desenvolvimento → conclusao)
   - Incluir transicoes sugeridas entre topicos
   - Destacar momentos de pausa para enfase

6. **Preparar perguntas (se entrevista)**
   - 15-20 perguntas abertas
   - Evitar sim/nao (usar "como", "por que", "conte-me sobre")
   - Incluir 2-3 perguntas provocativas/desconfortaveis
   - Preparar follow-ups para respostas previsiveis
   - Marcar perguntas essenciais vs opcionais

7. **Identificar areas sensiveis**
   - Topicos controversos ou politizados
   - Potenciais conflitos de interesse do guest
   - Areas onde guest pode ter vieses
   - Compliance (LGPD, direitos autorais, difamacao)

8. **Documentar briefing final**
   - Documento de 1-2 paginas, maximo 1000 palavras
   - Formato scannable (bullets, negrito, headings)
   - Salvar em `/briefs/S0{N}E0{N}-brief.md`

## Output

### S0{N}E0{N}-brief.md

```markdown
# Episode Brief: S02E03 - {Titulo Episodio}

## Meta
- **Pillar:** {content pillar}
- **Formato:** {entrevista/solo/narrativo}
- **Guest:** {nome} - {bio 1-linha}
- **Duracao target:** {minutos}
- **Gravacao:** {data}

## Angulo Unico
{1-2 paragrafos explicando o angulo diferenciado deste episodio e por que importa AGORA}

## Key Takeaways (3-5)
1. {Insight principal 1}
2. {Insight principal 2}
3. {Insight principal 3}

## Data Points Verificados

1. **{Estatistica/Fato}**
   - Fonte: {Autor, Ano, Publicacao, Link}
   - Context: {Por que isso importa}

2. **{Estatistica/Fato}**
   - Fonte: {Autor, Ano, Publicacao, Link}
   - Context: {Por que isso importa}

(Minimo 5 data points)

## Estrutura Narrativa

### Cold Open (0:00-0:30)
{Hook emocional ou data point chocante para prender atencao}

### Value Promise (0:30-1:00)
"Neste episodio voce vai aprender: {X, Y, Z}"

### Bloco 1: {Titulo} (1:00-10:00)
- Talking point 1
- Talking point 2
- Transicao: {sugestao}

### Bloco 2: {Titulo} (10:00-20:00)
...

### Climax (20:00-25:00)
{O insight mais valioso do episodio}

### CTA (25:00-26:00)
{Acao especifica: avaliar no Apple Podcasts, visitar site, etc}

## Talking Points (Host)

1. {Topico 1 - 1 frase}
2. {Topico 2 - 1 frase}
3. {Topico 3 - 1 frase}
...

## Perguntas (Se Entrevista)

### Warmup (3-5 perguntas)
1. {Pergunta aberta basica}
2. {Pergunta sobre trajetoria}

### Core (8-10 perguntas)
1. {Pergunta profunda sobre topico central}
2. {Pergunta provocativa} ⚠️
3. {Pergunta sobre controversia} ⚠️

### Closing (2-3 perguntas)
1. {Pergunta sobre futuro/visao}
2. {Pergunta rapida tipo lightning round}

## Areas Sensiveis ⚠️
- {Topico 1 que pode ser controverso}
- {Possivel conflito de interesse}
- {Area onde guest pode ter vies forte}

## Competitive Analysis
- **Podcast X:** Ja cobriu em {data} com angulo {Y}
- **Podcast Z:** Entrevistou pessoa similar, focou em {tema}
- **Nossa diferenciacao:** {Como seremos diferentes/melhores}

## Resources
- [Fonte 1](link)
- [Fonte 2](link)
- [Fonte 3](link)
...

---
**Preparado por:** @researcher
**Data:** {data}
**Tempo de research:** {horas}
```

## Criterios de Qualidade

- [ ] Research minimo de 2h investidas
- [ ] Angulo unico identificado e articulado claramente
- [ ] Minimo 5 data points com fontes verificadas e linkadas
- [ ] Fontes primarias priorizadas (papers > noticias > blogs)
- [ ] Estrutura narrativa completa com timecodes estimados
- [ ] Talking points claros e em ordem logica
- [ ] Perguntas abertas (evitar sim/nao)
- [ ] Areas sensiveis mapeadas com flags ⚠️
- [ ] Competitive analysis feita (o que ja existe la fora)
- [ ] Documento scannable (maximo 2 paginas, muito bullet point)
- [ ] Validado fact-check preliminar (nenhuma claim sem fonte)
- [ ] Entregue 48h antes da gravacao para o host absorver
