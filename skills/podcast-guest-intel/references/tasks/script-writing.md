---
task: Script Writing
responsavel: "@researcher"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - roteiro: saida de *roteiro (references/contracts/script.schema.json) — modo, blocos, perguntas, lastro e alertas
  - episode-brief: Briefing completo do episodio
  - format-type: Solo, entrevista, narrativo, mesa-redonda
  - duration-target: Duracao estimada (15min, 30min, 60min)
  - approach_mode: vem do roteiro (references/contracts/approach-modes.yaml); o tom do host vem do host-profile
Saida: |
  - script-file: Roteiro completo com timecodes
  - talking-points-outline: Versao resumida para impressao
  - chapter-markers: Marcadores de capitulo para Podcasting 2.0
  - cue-sheet: Lista de vinhetas/musicas com timecodes
Checklist:
  - "[ ] Definir estrutura por formato (solo vs entrevista vs narrativo)"
  - "[ ] Escrever cold open (15s) com hook forte"
  - "[ ] Criar value promise clara (15s)"
  - "[ ] Estruturar blocos de conteudo com timecodes"
  - "[ ] Inserir pontos de respiracao/pausa"
  - "[ ] Adicionar transicoes entre blocos"
  - "[ ] Incluir CTAs estrategicos (mid-roll e outro)"
  - "[ ] Marcar spots para vinhetas/musica"
  - "[ ] Criar chapter markers descritivos"
  - "[ ] Seguir o modo e a voz do roteiro de *roteiro; nao reescrever conteudo editorial nem esconder alertas"
---

# *script-writing

> **F5 (2026-10-09):** o conteúdo editorial do roteiro nasce em `references/tasks/roteiro.md` (`*roteiro`,
> por modo de abordagem, com alertas e decisão humana). Esta task é a camada de produção sobre
> ele — timecodes, cue sheet, chapter markers — e o formato narrativo (roteiro lido). Não
> duplica blocos, perguntas nem lastro.

Criacao de roteiro/pauta detalhado com timecodes para episodios de podcast. Adapta estrutura por formato (solo, entrevista, narrativo, mesa-redonda) e garante fluxo narrativo otimizado para retencao de audiencia.

## Uso

```bash
# Script para episodio solo
*script-writing --episode S02E05 --format solo --duration 30min

# Pauta para entrevista
*script-writing --episode S02E03 --format interview --duration 60min --guest "Maria Santos"

# Roteiro narrativo (story-driven)
*script-writing --episode S02E10 --format narrative --duration 45min --acts 3

# Mesa-redonda com multiplos hosts
*script-writing --episode S02E12 --format roundtable --hosts 3 --duration 90min
```

## Steps

1. **Analisar briefing e formato**
   - Ler episode-brief completo
   - Identificar formato (solo/entrevista/narrativo/mesa)
   - Ajustar estrutura ao formato escolhido
   - Revisar podcast-bible para tom do host

2. **Estrutura por formato**

   **SOLO (monologo estruturado):**
   - Cold open (0:00-0:15) - hook
   - Value promise (0:15-0:30)
   - Vinheta (0:30-0:45)
   - Bloco 1 (0:45-8:00) - contexto/problema
   - Transicao musical (8:00-8:15)
   - Bloco 2 (8:15-15:00) - solucao/insights
   - Transicao musical (15:00-15:15)
   - Bloco 3 (15:15-22:00) - aplicacao pratica
   - CTA mid-roll (22:00-22:30) - avaliar/compartilhar
   - Bloco 4 (22:30-28:00) - casos de estudo
   - Outro (28:00-29:00) - recap + CTA final
   - Vinheta closing (29:00-29:30)

   **ENTREVISTA (conversacional):**
   - Cold open (0:00-0:30) - teaser da melhor fala do guest
   - Vinheta (0:30-0:45)
   - Intro guest (0:45-2:00) - bio + credibilidade
   - Warmup (2:00-8:00) - perguntas leves
   - Core bloco 1 (8:00-20:00) - topico principal
   - Break/Transicao (20:00-20:30) - sponsor ou musical
   - Core bloco 2 (20:30-40:00) - aprofundamento
   - Lightning round (40:00-45:00) - perguntas rapidas
   - Closing (45:00-48:00) - onde encontrar guest + CTA
   - Outro (48:00-49:00)

   **NARRATIVO (story-driven):**
   - Cold open (0:00-1:00) - cena dramatica in media res
   - Vinheta (1:00-1:15)
   - Ato 1: Setup (1:15-10:00) - personagens, contexto, conflito
   - Transicao com musica tensa (10:00-10:30)
   - Ato 2: Confrontation (10:30-25:00) - desenvolvimento, obstaculos
   - Break (25:00-25:30)
   - Ato 3: Resolution (25:30-38:00) - climax, resolucao
   - Epilogo (38:00-40:00) - licoes, onde estao agora
   - Outro (40:00-41:00)

   **MESA-REDONDA (debate):**
   - Cold open (0:00-0:30) - hook sobre topico controverso
   - Vinheta (0:30-0:45)
   - Intro hosts (0:45-2:00) - apresentacao de cada um
   - Topico 1 (2:00-20:00) - debate aberto
   - Transicao (20:00-20:15)
   - Topico 2 (20:15-40:00) - debate continuado
   - Lightning opinions (40:00-45:00) - takes rapidos
   - Closing (45:00-48:00) - recap + onde discordam
   - Outro (48:00-49:00)

3. **Escrever cold open (critical)**
   - 15-30 segundos maximo
   - Hook emocional OU data point chocante OU pergunta provocativa
   - Testar 3 versoes, escolher a mais forte
   - Exemplo: "E se eu te dissesse que 70% das startups falham por um unico erro evitavel?"

4. **Value promise clara**
   - 15 segundos explicando o que o ouvinte vai aprender
   - Usar "Neste episodio voce vai..." ou "Hoje vamos explorar..."
   - Ser especifico (evitar generalidades)

5. **Blocos de conteudo com timecodes**
   - Dividir conteudo em 3-5 blocos tematicos
   - Cada bloco com inicio/fim marcados (ex: 8:00-15:00)
   - Dentro de cada bloco: talking points numerados
   - Incluir pontos de respiracao [PAUSA 2s]
   - Marcar enfases **EM CAIXA ALTA**

6. **Transicoes e musica**
   - Inserir transicoes musicais entre blocos (15-30s)
   - Marcar vinhetas (intro, outro, breaks)
   - Criar cue sheet com nome do arquivo de audio
   - Exemplo: `[MUSICA: transition-upbeat-01.mp3 - 15s]`

7. **CTAs estrategicos**
   - Mid-roll CTA (metade do episodio): avaliar/compartilhar
   - Outro CTA: proxximo episodio, site, comunidade
   - Sponsor reads (se aplicavel): natural, nao forcado

8. **Chapter markers (Podcasting 2.0)**
   - Criar 5-8 markers descritivos
   - Formato: `00:00:45 - Introducao do guest Maria Santos`
   - Facilita navegacao e melhora experiencia

9. **Documentar script final**
   - Script completo em `/scripts/S0{N}E0{N}-script.md`
   - Versao resumida (talking points) para impressao
   - Chapter markers em arquivo separado

## Output

### S0{N}E0{N}-script.md

```markdown
# Script: S02E05 - {Titulo Episodio}

**Formato:** Solo
**Duracao target:** 30min
**Host:** {Nome}
**Gravacao:** {Data}

---

## [0:00-0:15] COLD OPEN

> E se eu te dissesse que voce esta perdendo 40% da sua audiencia nos primeiros 60 segundos? [PAUSA 2s] A ciencia dos cold opens pode mudar isso.

[MUSICA: tension-build-up.mp3 - fade in]

---

## [0:15-0:30] VALUE PROMISE

> Oi, eu sou {Host}, e neste episodio voce vai aprender:
> - Como escrever cold opens que prendem atencao
> - A formula dos 3Cs para hooks inesqueciveis
> - Exemplos reais de podcasts top 10 da Apple

---

## [0:30-0:45] VINHETA INTRO

[VINHETA: show-intro-v2.mp3 - 15s]

---

## [0:45-8:00] BLOCO 1: O Problema dos Primeiros 60 Segundos

### Talking Points

1. **Estatistica chocante:** 40% drop-off nos primeiros 60s (fonte: Spotify 2024 Report)

2. **Por que isso acontece?**
   - Ouvinte esta multitasking (dirigindo, academia, cozinhando)
   - Atencao fragmentada em 2026
   - Primeiros segundos decidem se continua ou pula

3. **Caso de estudo: Podcast X**
   - Antes: intro musical de 45s → 50% drop-off
   - Depois: cold open de 15s → 18% drop-off [PAUSA 2s]
   - Resultado: +120% de retencao

4. **Transicao:** "Mas como criar um cold open que funciona? Existem 3 elementos..."

[MUSICA: transition-light.mp3 - 15s]

---

## [8:00-15:00] BLOCO 2: A Formula dos 3Cs

### Talking Points

1. **C1: Curiosity (Curiosidade)**
   - Fazer pergunta provocativa
   - Exemplo: "E se tudo que voce sabe sobre X estiver errado?"

2. **C2: Contrast (Contraste)**
   - Juxtapor dois extremos
   - Exemplo: "Ela tinha $10 na conta. 18 meses depois, $10 milhoes."

3. **C3: Conflict (Conflito)**
   - Apresentar tensao nao resolvida
   - Exemplo: "O email que destruiu uma empresa de $50M chegou as 9h47 de uma segunda-feira."

4. **Quando usar cada C**
   - Curiosity: episodios educacionais
   - Contrast: historias de transformacao
   - Conflict: narrativas dramaticas

[PAUSA 3s - respirar]

[MUSICA: transition-medium.mp3 - 15s]

---

## [15:00-22:00] BLOCO 3: Aplicacao Pratica

### Talking Points

1. **Exercicio: Reescrever seu cold open**
   - Pegar episodio existente
   - Identificar qual C falta
   - Reescrever em 15s

2. **Testing e iteracao**
   - A/B test com 2 versoes
   - Medir drop-off no Spotify/Apple Analytics
   - Ajustar baseado em dados

3. **Erros comuns**
   - Cold open muito longo (>30s)
   - Spoilar todo o episodio
   - Tom inconsistente com o resto do show

[MUSICA: transition-upbeat.mp3 - 15s]

---

## [22:00-22:30] CTA MID-ROLL

> Se voce esta gostando deste episodio, me ajuda com 5 segundos: abre o app e da 5 estrelas. **ISSO MUDA TUDO** para o algoritmo mostrar o show para mais gente como voce. [PAUSA 2s] Valeu!

---

## [22:30-28:00] BLOCO 4: Casos de Estudo Reais

### Talking Points

1. **Podcast A: The Daily (NYT)**
   - Cold open estilo: Conflict
   - Exemplo: "The phone call came at 3am..."
   - Resultado: top 5 Apple Podcasts por 4 anos

2. **Podcast B: Huberman Lab**
   - Cold open estilo: Curiosity
   - Exemplo: "Today we're exploring a protocol that can change your biology in 8 minutes..."
   - Resultado: 4M+ subscribers no YouTube

3. **Podcast C: SmartLess**
   - Cold open estilo: Contrast
   - Exemplo: banter comico → reveal do guest surpresa
   - Resultado: $100M deal Amazon

---

## [28:00-29:00] OUTRO

> Entao, recap: [PAUSA 2s]
> - Cold opens decidem 40% da retencao
> - Use a formula dos 3Cs: Curiosity, Contrast, Conflict
> - Teste, meça, itere

> Proxima semana: "Como escrever show notes que ranqueiam no Google". Ate la! [PAUSA 1s]

[MUSICA: outro-uplifting.mp3 - fade out]

---

## [29:00-29:30] VINHETA CLOSING

[VINHETA: show-outro-v2.mp3 - 30s]

---

## CHAPTER MARKERS

- 00:00:00 - Introducao: O problema dos primeiros 60 segundos
- 00:00:45 - Bloco 1: Por que 40% da audiencia abandona rapido
- 00:08:00 - Bloco 2: A formula dos 3Cs para cold opens
- 00:15:00 - Bloco 3: Como aplicar na pratica
- 00:22:30 - Bloco 4: Casos de estudo de podcasts top 10
- 00:28:00 - Recap e proximos passos

---

## CUE SHEET (Musica/Vinhetas)

| Timecode | Arquivo | Duracao | Fade |
|----------|---------|---------|------|
| 0:00:12 | tension-build-up.mp3 | 3s | In |
| 0:00:30 | show-intro-v2.mp3 | 15s | - |
| 0:08:00 | transition-light.mp3 | 15s | In/Out |
| 0:15:00 | transition-medium.mp3 | 15s | In/Out |
| 0:22:00 | transition-upbeat.mp3 | 15s | In/Out |
| 0:28:00 | outro-uplifting.mp3 | 60s | Out |
| 0:29:00 | show-outro-v2.mp3 | 30s | - |

---

**Preparado por:** @researcher
**Data:** {data}
**Versao:** 1.0
```

## Criterios de Qualidade

- [ ] Cold open de 15-30s com hook forte (testado 3 versoes)
- [ ] Value promise clara nos primeiros 60s
- [ ] Estrutura adaptada ao formato (solo/entrevista/narrativo/mesa)
- [ ] Timecodes precisos para todos os blocos
- [ ] Transicoes suaves entre blocos
- [ ] Pontos de respiracao/pausa marcados [PAUSA Xs]
- [ ] CTAs estrategicos (mid-roll + outro)
- [ ] Chapter markers descritivos (5-8 markers)
- [ ] Cue sheet completo com todos os arquivos de audio
- [ ] Tom consistente com host style do podcast-bible
- [ ] Duracao total dentro do target (+/- 2min)
- [ ] Versao resumida (talking points) para impressao criada
