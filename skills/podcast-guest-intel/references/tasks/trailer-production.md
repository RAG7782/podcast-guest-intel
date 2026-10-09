---
task: Trailer Production
responsavel: "@producer"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - trailer-type: Show, Season, Mid-Season, Episode Teaser
  - target-duration: 30s, 60s, 90s, 120s
  - key-messages: 3-5 mensagens principais a transmitir
  - music-style: Genero/vibe da trilha (epico, intimista, energetico)
Saida: |
  - trailer-audio: Arquivo masterizado do trailer
  - trailer-script: Roteiro com timecodes
  - trailer-artwork: Arte de capa do trailer
  - distribution-plan: Plano de distribuicao multi-canal
Checklist:
  - "[ ] Definir tipo de trailer (show/season/episode)"
  - "[ ] Selecionar melhores momentos do conteudo (teasers)"
  - "[ ] Escrever script estruturado (hook, value, CTA)"
  - "[ ] Escolher trilha musical que reflete brand"
  - "[ ] Gravar voiceover (se novo conteudo)"
  - "[ ] Editar com ritmo cinematico (builds/drops)"
  - "[ ] Masterizar audio (-14 LUFS Spotify)"
  - "[ ] Criar arte de capa especifica do trailer"
  - "[ ] Distribuir em feed principal + social media"
  - "[ ] Trackear performance (impressoes, click-through)"
---

# *trailer-production

Producao de trailers profissionais para podcast: show trailer (permanente), season trailer (pre-temporada), mid-season trailer (hype), episode teasers (30-60s). Funciona como "movie trailer" para audio, maximizando descoberta e conversao.

## Uso

```bash
# Trailer permanente do show
*trailer-production --type show --duration 90s --distribution "feed,youtube,social"

# Trailer de temporada (pre-lancamento)
*trailer-production --type season --season 2 --duration 60s --launch-date "2026-04-01"

# Mid-season trailer (hype para segunda metade)
*trailer-production --type mid-season --season 2 --duration 45s

# Episode teaser (promover episodio especifico)
*trailer-production --type episode-teaser --episode S02E08 --duration 30s
```

## Steps

1. **Definir tipo e objetivo do trailer**

   **Show Trailer (permanente):**
   - Duracao: 60-90s
   - Objetivo: Apresentar podcast para novos ouvintes
   - Quando usar: Sempre disponivel no topo do feed
   - Conteudo: Quem e o host, sobre o que e o show, por que ouvir
   - CTA: "Inscreva-se agora"

   **Season Trailer:**
   - Duracao: 60-90s
   - Objetivo: Gerar hype para nova temporada
   - Quando usar: 2 semanas antes do lancamento da temporada
   - Conteudo: Temas da temporada, guests de destaque, novidades
   - CTA: "Estreia dia {data}"

   **Mid-Season Trailer:**
   - Duracao: 30-60s
   - Objetivo: Re-engajar audiencia no meio da temporada
   - Quando usar: No ponto medio da temporada (ex: apos EP06 de 12)
   - Conteudo: Recap primeira metade, teaser segunda metade
   - CTA: "Nao perca os proximos episodios"

   **Episode Teaser:**
   - Duracao: 30-60s
   - Objetivo: Promover episodio especifico (especialmente guests grandes)
   - Quando usar: 2-3 dias antes do lancamento do episodio
   - Conteudo: Melhor momento do episodio (cliffhanger)
   - CTA: "Episodio completo dia {data}"

2. **Selecionar melhores momentos (se baseado em conteudo existente)**

   **Criterios para selecao:**
   - **Emotional impact:** Momento que da arrepio/risada/surpresa
   - **Insight valioso:** Quote que faz ouvinte pensar "preciso ouvir isso"
   - **Controversy:** Hot take que gera curiosidade
   - **Celebrity/Authority:** Fala de guest reconhecido

   **Exemplos de teasers eficazes:**
   - "E se eu te dissesse que 70% das startups falham por um erro evitavel?"
   - "Eu perdi $2 milhoes em 48 horas. Aqui esta o que aprendi."
   - "A verdade e: ninguem sabe o que esta fazendo. Nem os experts."

   **Numero de clips:**
   - 60s trailer: 3-4 momentos (15s cada)
   - 90s trailer: 5-6 momentos (15s cada)
   - 120s trailer: 6-8 momentos (15s cada)

3. **Escrever script estruturado**

   **Estrutura classica (3 atos):**

   **Ato 1: HOOK (0-15s)**
   - Frase/pergunta/som que prende atencao imediatamente
   - Exemplo: "Eu estava a 24 horas de falir..."

   **Ato 2: VALUE PROMISE (15-45s)**
   - O que o ouvinte vai aprender/sentir
   - Clips dos melhores momentos
   - Build de tensao/curiosidade

   **Ato 3: CTA (45-60s)**
   - Call to action claro
   - "Inscreva-se", "Disponivel agora", "Estreia dia X"

   **Exemplo de script (60s Season Trailer):**

   ```
   [0:00-0:03] SFX: Tensao musical crescente

   [0:03-0:08] HOST VO: "2026 vai mudar tudo que voce sabe sobre IA."

   [0:08-0:10] MUSICA: Drop dramatico

   [0:10-0:15] GUEST 1 (clip): "A singularidade nao esta em 2045. Esta em 2028."

   [0:15-0:18] HOST VO: "Temporada 2 de {Nome Podcast}."

   [0:18-0:25] GUEST 2 (clip): "Eu treinei o GPT-5. Aqui esta o que ninguem sabe."

   [0:25-0:32] GUEST 3 (clip): "IA consciente nao e ficçao. E inevitavel."

   [0:32-0:35] MUSICA: Build epico

   [0:35-0:42] HOST VO: "12 episodios. Os maiores nomes em IA. Verdades desconfortaveis."

   [0:42-0:50] GUEST 4 (clip): "Se voce nao entende IA em 2026, voce ja esta atrasado."

   [0:50-0:55] MUSICA: Climax + fade

   [0:55-0:60] HOST VO: "{Nome Podcast} Temporada 2. Estreia 1o de abril. Inscreva-se agora."
   ```

4. **Escolher trilha musical**

   **Criterios:**
   - Alinhada com brand do podcast (epico, intimista, energetico)
   - Royalty-free (Epidemic Sound, Artlist, AudioJungle)
   - Com builds/drops para criar tensao
   - Nao competir com voz (frequency space)

   **Generos por vibe:**
   - **Epico/Cinematico:** Trailer podcasts de historia, true crime, investigativo
   - **Eletronico/Synth:** Tech, futuro, inovacao
   - **Acustico/Intimista:** Self-help, entrevistas pessoais
   - **Hip-Hop/Urban:** Cultura, empreendedorismo, lifestyle
   - **Orquestral:** Educacional, academico, gravitas

5. **Gravar voiceover (se novo conteudo)**

   **Setup:**
   - Usar mesma cadeia de audio do podcast (mic + interface)
   - Gravar em ambiente tratado (zero reverb)
   - Niveis: -12 dBFS peaks
   - Tom: Energetico, confiante, ligeiramente mais dramatico que episodios

   **Dicas de performance:**
   - Ler script 3-5 vezes (escolher melhor take)
   - Enfatizar palavras-chave
   - Variar ritmo (rapido para build, lento para impacto)
   - Pausas estrategicas (respiracao, tensao)

6. **Edicao com ritmo cinematico**

   **Estrutura de timeline (DAW):**
   ```
   Track 1: Musica (full stereo)
   Track 2: Voiceover host (center)
   Track 3: Clip guest 1 (center)
   Track 4: Clip guest 2 (center)
   Track 5: SFX (transicoes, whooshes, impacts)
   ```

   **Tecnicas de edicao:**
   - **Cuts no beat:** Cortar clips no tempo da musica (mais dinamico)
   - **Builds:** Aumentar intensidade gradualmente (volume, filtering, pitch)
   - **Drops:** Momento de release (silencio subito → drop pesado)
   - **Transicoes:** Whooshes, impacts, risers entre clips
   - **Ducking:** Musica abaixa quando voz entra (sidechain compression)

   **Ritmo:**
   - Primeiros 5s: Hook FORTE (se nao prender, perdeu ouvinte)
   - 5-45s: Build de tensao (clips cada vez mais impactantes)
   - 45-55s: Climax (momento mais eletrizante)
   - 55-60s: CTA claro + fade

7. **Masterizar audio**

   **Specs:**
   - Loudness: -14 LUFS (Spotify/Apple Podcasts)
   - True Peak: -1 dBFS
   - Dynamic range: 6-8 LU (mais comprimido que episodio normal)
   - Export: WAV 48kHz/24bit + MP3 320kbps

   **Chain de mastering:**
   1. EQ: Cortar lows <40Hz, boost presenca 2-4kHz
   2. Multiband compression: Controlar dinamica por banda
   3. Limiter: True Peak -1 dBFS, ceiling -0.3 dBFS
   4. Dither: 24bit → 16bit (se necessario)

8. **Criar arte de capa especifica**

   **Show Trailer:**
   - Arte padrao do podcast + badge "TRAILER"

   **Season Trailer:**
   - Arte customizada com "SEASON 2" grande
   - Paleta de cores diferente (mas on-brand)

   **Episode Teaser:**
   - Foto do guest (se entrevista)
   - Quote visual (texto do teaser)

   **Specs:**
   - 3000x3000px (Apple Podcasts)
   - RGB (para digital)
   - Texto legivel em thumbnail pequeno (teste 300x300px)

9. **Distribuir multi-canal**

   **Feed do podcast:**
   - Publicar como "episodio" separado
   - Titulo: "[TRAILER] {Descricao}"
   - Marcar como "trailer" nos settings (Apple Podcasts)

   **YouTube:**
   - Upload como video (audiogram com waveform)
   - Thumbnail chamativo
   - Titulo SEO: "{Nome Podcast} Season 2 Trailer | {Tema}"

   **Social Media:**
   - Instagram: Feed post (1:1) + Stories (9:16)
   - Twitter: Video com legenda
   - TikTok: Versao 30s (mais dinamica)
   - LinkedIn: Post para audiencia profissional

   **Ads (se budget):**
   - YouTube Pre-roll (15s ou 30s)
   - Spotify Audio Ads
   - Instagram/Facebook Ads

10. **Trackear performance**

    **Metricas:**
    - Downloads do trailer (feed)
    - Click-through rate (trailer → episodios)
    - Views (YouTube/social)
    - Engagement (likes, shares, comments)
    - Conversao (novos inscritos apos trailer)

    **Tools:**
    - Spotify for Podcasters / Apple Podcasts Analytics
    - YouTube Analytics
    - Bitly (links trackeaveis)

## Output

### trailer-script-{type}.md

```markdown
# Trailer Script: Season 2 Trailer

**Tipo:** Season Trailer
**Duracao:** 60s
**Lancamento:** 2026-03-18 (2 semanas antes da Season 2)
**Musica:** Epidemic Sound - "Epic Cinematic Trailer"

---

## Timeline

| Timecode | Element | Content |
|----------|---------|---------|
| 0:00-0:03 | MUSICA | Tensao crescente (strings) |
| 0:03-0:08 | HOST VO | "2026 vai mudar tudo que voce sabe sobre IA." |
| 0:08-0:10 | MUSICA | Drop dramatico (bass hit) |
| 0:10-0:15 | GUEST 1 | "A singularidade nao esta em 2045. Esta em 2028." |
| 0:15-0:18 | HOST VO | "Temporada 2 de {Nome Podcast}." |
| 0:18-0:25 | GUEST 2 | "Eu treinei o GPT-5. Aqui esta o que ninguem sabe." |
| 0:25-0:32 | GUEST 3 | "IA consciente nao e ficcao. E inevitavel." |
| 0:32-0:35 | MUSICA | Build epico (orquestra full) |
| 0:35-0:42 | HOST VO | "12 episodios. Os maiores nomes em IA. Verdades desconfortaveis." |
| 0:42-0:50 | GUEST 4 | "Se voce nao entende IA em 2026, voce ja esta atrasado." |
| 0:50-0:55 | MUSICA | Climax + fade out |
| 0:55-0:60 | HOST VO + CTA | "{Nome Podcast} Temporada 2. Estreia 1o de abril. Inscreva-se agora." |

---

## Voiceover Script (Host)

```
[ENERGETICO, CONFIANTE]

"2026 vai mudar tudo que voce sabe sobre IA."

[PAUSA 2s]

"Temporada 2 de {Nome Podcast}."

[PAUSA 3s]

"12 episodios. Os maiores nomes em IA. Verdades desconfortaveis."

[PAUSA 2s]

"{Nome Podcast} Temporada 2. Estreia primeiro de abril. Inscreva-se agora."
```

---

## Guest Clips Sources

| Clip | Source Episode | Timecode | Duration |
|------|----------------|----------|----------|
| Guest 1 | S02E01 preview | 12:30 | 5s |
| Guest 2 | S02E03 preview | 08:15 | 7s |
| Guest 3 | S02E05 preview | 18:40 | 7s |
| Guest 4 | S02E08 preview | 22:10 | 8s |

---

## Music

- **Track:** "Epic Cinematic Trailer" (Epidemic Sound)
- **License:** Royalty-free (Epidemic subscription)
- **BPM:** 120
- **Key:** C minor
- **Mood:** Tenso, epico, futurista

---

## Distribution Plan

| Canal | Formato | Duracao | Launch Date |
|-------|---------|---------|-------------|
| Podcast feed | Audio MP3 | 60s | 2026-03-18 |
| YouTube | Audiogram video | 60s | 2026-03-18 |
| Instagram Feed | Audiogram 1:1 | 60s | 2026-03-18 |
| Instagram Stories | Audiogram 9:16 | 30s | 2026-03-18 |
| Twitter | Video | 60s | 2026-03-18 |
| TikTok | Video dinamico | 30s | 2026-03-19 |
| Email blast | Embed player | 60s | 2026-03-20 |

---

## Artwork

- **Filename:** `season-2-trailer-cover.jpg`
- **Dimensions:** 3000x3000px
- **Text:** "SEASON 2 | Coming April 1"
- **Visual:** Arte customizada (futurista, cores vibrantes)

---

**Criado por:** @producer + @composer
**Data:** 2026-03-10
**Status:** ✅ Aprovado para lancamento
```

## Criterios de Qualidade

- [ ] Tipo de trailer claramente definido (show/season/mid-season/episode)
- [ ] Hook forte nos primeiros 5s (prende atencao)
- [ ] 3-5 momentos impactantes selecionados (emotional/insight/controversy)
- [ ] Script estruturado com ritmo cinematico (build → climax → CTA)
- [ ] Trilha musical alinhada com brand e com builds/drops
- [ ] Voiceover energetico e confiante (se novo conteudo)
- [ ] Edicao dinamica (cuts no beat, transicoes, ducking)
- [ ] Masterizado para -14 LUFS (Spotify spec)
- [ ] Arte de capa especifica criada (3000x3000px)
- [ ] Distribuido multi-canal (feed + YouTube + social)
- [ ] CTA claro e acionavel ("Inscreva-se", "Estreia dia X")
- [ ] Performance trackeada (downloads, views, conversao)
- [ ] Duracao dentro do target (+/- 5s)
