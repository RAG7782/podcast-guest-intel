---
task: Live Session
responsavel: "@producer"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - episode-script: Pauta/roteiro adaptado para ao vivo
  - streaming-platforms: YouTube, Twitch, LinkedIn, X
  - live-datetime: Data/hora do live
  - qna-enabled: Se havera Q&A com audiencia
Saida: |
  - live-recording: Gravacao completa do episodio ao vivo
  - chat-log: Log do chat/comentarios da audiencia
  - qna-clips: Clips das melhores perguntas/respostas
  - post-live-edit: Versao editada para feed do podcast
Checklist:
  - "[ ] Configurar streaming setup (OBS/StreamYard/Restream)"
  - "[ ] Testar multi-platform streaming (YouTube+Twitch+LinkedIn)"
  - "[ ] Definir moderador de chat (nao pode ser o host)"
  - "[ ] Preparar overlays (lower thirds, titulo episodio, chat on-screen)"
  - "[ ] Configurar gravacao local simultanea (backup)"
  - "[ ] Promover live 48h antes (email, social, comunidade)"
  - "[ ] Lembrete 2h antes e 15min antes"
  - "[ ] Iniciar streaming 5min antes (countdown)"
  - "[ ] Monitorar chat e moderar toxicidade"
  - "[ ] Gerenciar Q&A (selecionar melhores perguntas)"
  - "[ ] Exportar live completo + versao editada"
---

# *live-session

Setup e execucao de episodio de podcast ao vivo com streaming multi-plataforma, interacao com audiencia via chat/Q&A e gravacao simultanea para distribuicao posterior. Combina producao ao vivo com beneficios de conteudo on-demand.

## Uso

```bash
# Live session no YouTube + Twitch
*live-session --episode S02E08 --platforms "youtube,twitch" --qna enabled

# Live com guest remoto
*live-session --episode S02E10 --guest "Maria Santos" --platforms "youtube,linkedin" --duration 60min

# Live com multiplos co-hosts (mesa-redonda)
*live-session --episode S02E12 --format roundtable --hosts 4 --platforms "youtube,twitch,x"
```

## Steps

1. **Escolher plataforma de streaming**

   **Comparativo:**

   | Tool | Preco | Multi-stream | Qualidade | Melhor para |
   |------|-------|--------------|-----------|-------------|
   | **OBS Studio** | Gratis | Plugin (free) | 1080p60 | Controle total, customizacao |
   | **StreamYard** | $25/mes | ✅ Nativo (6 destinos) | 1080p | Facilidade, guests remotos |
   | **Restream** | $20/mes | ✅ Nativo (ilimitado) | 1080p | Multi-platform profissional |
   | **Riverside Live** | $40/mes | ❌ (1 destino) | 4K | Qualidade maxima, mas caro |

   **Recomendacao:** StreamYard para facilidade + multi-platform OU OBS para controle total.

2. **Configurar streaming setup**

   **OBS Studio setup:**
   - **Scenes:**
     - Scene 1: Full screen host (webcam)
     - Scene 2: Screen share (se aplicavel)
     - Scene 3: Picture-in-picture (host + guest)
     - Scene 4: Countdown (pre-live)
     - Scene 5: BRB (pause/problemas tecnicos)

   - **Sources por scene:**
     - Video Capture Device (webcam 1080p)
     - Audio Input (mic XLR via interface)
     - Image (lower third com nome/titulo)
     - Browser Source (chat on-screen do YouTube/Twitch)
     - Text (titulo do episodio)

   - **Settings:**
     - Output: 1080p 30fps (ou 60fps se gaming-related)
     - Bitrate: 6000 kbps (YouTube recomendado)
     - Encoder: x264 (CPU) ou NVENC (GPU Nvidia)
     - Audio: 48kHz 192kbps stereo

   **StreamYard setup (mais facil):**
   - Criar broadcast: `S02E08 - {Titulo Episodio}`
   - Adicionar destinos: YouTube, Twitch, LinkedIn, X
   - Convidar guests remotos via link (ate 6 pessoas)
   - Configurar overlays (lower thirds, banner, chat)
   - Testar com co-host antes do live

3. **Definir moderador de chat**
   - **NAO PODE SER O HOST** (host precisa focar no conteudo)
   - Responsabilidades do moderador:
     - Monitorar chat em tempo real
     - Deletar spam, toxicidade, links suspeitos
     - Selecionar melhores perguntas para Q&A
     - Avisar host de perguntas/comentarios importantes
     - Engajar comunidade (responder duvidas simples)
   - Ferramentas: Mod dashboard do YouTube, Nightbot (Twitch)

4. **Preparar overlays e branding**

   **Lower third (nome + titulo):**
   ```
   {Nome Host} | Host de {Nome Podcast}
   S02E08: {Titulo Episodio}
   ```

   **Chat on-screen (opcional):**
   - Mostrar comentarios ao vivo na tela (YouTube/Twitch chat)
   - Filtrar palavras inapropriadas
   - Limitar a 5 comentarios visiveis

   **Countdown pre-live:**
   - 5min countdown antes de comecar
   - Musica de fundo (royalty-free)
   - Texto: "Começando em {minutos}:{segundos}"

5. **Gravacao local simultanea (backup)**
   - **OBS:** Configurar "Record" ao mesmo tempo que "Stream"
   - **StreamYard:** Opcao "Record locally" ativada
   - **Backup adicional:** Zoom/Riverside gravando em paralelo
   - **Por que:** Se stream cair, gravacao local nao perde conteudo

6. **Promocao pre-live (48h antes)**

   **Email blast:**
   ```
   Assunto: [AO VIVO] {Titulo Episodio} - {Data} {Hora}

   Oi {Nome},

   Episodio ESPECIAL ao vivo dia {data} as {hora} {fuso}!

   Tema: {Descricao 1-frase}

   Voce pode:
   - Assistir ao vivo e interagir no chat
   - Fazer perguntas pro {Host/Guest}
   - Ganhar [incentivo: sorteio, early access, etc]

   Links:
   YouTube: {link}
   Twitch: {link}

   Nos vemos la!
   ```

   **Social media (Twitter/LinkedIn/Instagram):**
   - Post anunciando 48h antes
   - Stories/Reels teaser 24h antes
   - Reminder 2h antes
   - Reminder 15min antes (pinned post)

   **Comunidade (Discord/Telegram):**
   - Anuncio + evento no calendario
   - Ping @everyone 30min antes

7. **Lembretes automatizados**
   - Email 2h antes: "Começando em 2h! Link: {url}"
   - Social post 15min antes: "AGORA! Ao vivo em 15min"
   - Discord/Telegram ping 5min antes

8. **Iniciar streaming (5min antes)**
   - Comecar stream com countdown scene (5min)
   - Testar audio/video funcionando
   - Verificar chat ativo e moderador online
   - Musica de fundo tocando
   - Host preparado (agua, roteiro, mindset)

9. **Execucao do live**

   **Estrutura sugerida (60min):**

   **0:00-2:00 - Intro**
   - "Oi pessoal, bem-vindos ao live!"
   - Explicar tema do episodio
   - Pedir para interagir no chat
   - Avisar quando sera Q&A (ex: ultimos 15min)

   **2:00-40:00 - Conteudo principal**
   - Seguir roteiro (mas ser flexivel)
   - Reconhecer chat ocasionalmente: "Oi {nome}, boa pergunta!"
   - Moderador destaca comentarios importantes

   **40:00-55:00 - Q&A com audiencia**
   - Moderador seleciona 8-10 melhores perguntas
   - Host responde ao vivo
   - Dar shoutout a quem perguntou

   **55:00-60:00 - Closing**
   - Recap dos principais pontos
   - Agradecer audiencia
   - CTA: Inscrever, avaliar podcast, proximos episodios
   - "Ate a proxima!"

10. **Monitorar chat e moderar**

    **Responsabilidades do moderador:**
    - Deletar: Spam, links suspeitos, linguagem ofensiva, spoilers
    - Timeout/Ban: Usuarios toxicos ou trolls
    - Pin: Melhores comentarios ou perguntas
    - Responder: Duvidas tecnicas (audio, onde encontrar links)
    - Alertar host: Comentarios/perguntas muito bons

    **Ferramentas:**
    - YouTube: Mod dashboard + filtros automaticos
    - Twitch: Nightbot, Moobot (moderation bots)
    - StreamYard: Chat integrado (moderador ve tudo)

11. **Gerenciar Q&A estrategicamente**

    **Como selecionar perguntas:**
    - Relevantes ao tema (nao off-topic)
    - Abertas (nao sim/nao)
    - Variedade (nao repetir pergunta similar)
    - Dar preferencia a membros/supporters da comunidade

    **Como apresentar:**
    - Ler pergunta completa
    - Dar shoutout: "Otima pergunta do {nome}!"
    - Responder com depth
    - Seguir com proxima pergunta

12. **Finalizacao e pos-live**

    - Agradecer, encerrar graciosamente
    - Parar stream
    - **NAO deletar stream do YouTube** (deixar como VOD)
    - Baixar gravacao local (backup)
    - Exportar chat log (para analise)

13. **Pos-producao para feed do podcast**

    - Editar versao "limpa" da gravacao:
      - Cortar countdown inicial
      - Remover pausas/problemas tecnicos
      - Cortar partes irrelevantes do Q&A
      - Adicionar intro/outro padroes do podcast
      - Masterizar audio (normalizar levels)
    - Publicar no feed regular do podcast
    - Marcar como "Episodio ao vivo com audiencia"

14. **Criar clips das melhores partes**
    - Q&A com perguntas mais interessantes
    - Momentos virais (risadas, insights, hot takes)
    - Distribuir em social media (Reels/Shorts/TikTok)

## Output

### live-session-report-S0{N}E0{N}.md

```markdown
# Live Session Report: S02E08

**Data:** 2026-03-22 20h BRT
**Episodio:** S02E08 - IA no Jornalismo
**Plataformas:** YouTube, Twitch, LinkedIn
**Duracao:** 62min
**Produtor:** @producer
**Moderador:** {Nome}

---

## Performance por Plataforma

| Plataforma | Peak Viewers | Avg Viewers | Total Views (24h) | Chat Messages |
|------------|--------------|-------------|-------------------|---------------|
| YouTube | 340 | 215 | 1.240 | 420 |
| Twitch | 120 | 85 | 380 | 180 |
| LinkedIn | 45 | 30 | 150 | 25 |
| **TOTAL** | **505** | **330** | **1.770** | **625** |

---

## Qualidade Tecnica

- **Streaming:** Estavel, zero drops
- **Audio:** Limpo, -16 LUFS
- **Video:** 1080p 30fps (YouTube/Twitch), 720p (LinkedIn)
- **Latencia:** 3-5s (normal para YouTube)

---

## Highlights da Audiencia

### Melhores Comentarios
1. **@maria_tech (YouTube):** "Essa discussao sobre bias em IA e exatamente o que o jornalismo precisa"
2. **@joao_dev (Twitch):** "Primeira vez aqui, mas ja me inscrevi. Conteudo top!"
3. **@ana_costa (LinkedIn):** "Vou compartilhar isso com meu time de data journalism"

### Melhores Perguntas (Q&A)
1. **@pedro_silva:** "Como jornalistas podem usar GPT sem perder fact-checking?"
2. **@carla_rocha:** "IA pode substituir jornalistas investigativos?"
3. **@lucas_mendes:** "Qual ferramenta de IA voce usa no dia-a-dia?"

---

## Problemas Encontrados

### 1. Audio dropou por 5s (12:30)
- **Causa:** Cabo USB do mic deu mau contato
- **Fix:** Reconectar cabo, audio voltou
- **Impacto:** Baixo (editavel na pos-producao)

### 2. Troll no chat (35:00)
- **Causa:** Usuario spam com links maliciosos
- **Fix:** Moderador baniu imediatamente
- **Impacto:** Zero (comunidade nem notou)

---

## Arquivos Gerados

- ✅ Gravacao local: `S02E08_live_raw.mp4` (4.2GB, 1080p)
- ✅ VOD YouTube: Disponivel em youtube.com/watch?v={id}
- ✅ Chat log: `S02E08_chat_log.txt` (625 mensagens)
- ✅ Versao editada (pos-producao): `S02E08_live_edited.wav` (para feed)

---

## Clips Criados

1. **"IA nao substitui jornalistas"** (45s) - Viral potential
2. **Q&A: Ferramentas de IA para jornalismo** (2min) - Educacional
3. **Momento de risada espontanea** (15s) - Humaniza

---

## Metricas de Engajamento

- **Likes:** 340 (YouTube) + 85 (Twitch) = 425
- **Shares:** 120
- **Novos inscritos:** 85 (YouTube), 30 (Twitch)
- **Comments pos-live:** 60+

---

## Feedback da Audiencia

### Positivo
- "Formato ao vivo e incrivel, da pra interagir!"
- "Q&A foi o melhor, quero mais"
- "Qualidade de video/audio profissional"

### Construtivo
- "Poderia ser 90min, passou rapido"
- "Chat on-screen seria legal"
- "Avisar horario com mais antecedencia"

---

## Proximos Passos

- [x] Versao editada pronta para feed
- [ ] Publicar clips em Reels/Shorts/TikTok
- [ ] Email de thank you para quem participou
- [ ] Analisar quais perguntas viraram topicos para proximos episodios
- [ ] Agendar proximo live (mensal?)

---

**ROI:**
- Custo: $0 (StreamYard ja na assinatura)
- Alcance: 1.770 views em 24h (4x episodio regular)
- Engagement: 625 chat messages + 425 likes
- Growth: 115 novos inscritos

**Conclusao:** SUCESSO. Repetir mensalmente.
```

## Criterios de Qualidade

- [ ] Streaming setup testado 24h antes
- [ ] Multi-platform streaming funcionando (YouTube+Twitch+LinkedIn)
- [ ] Moderador de chat designado (nao o host)
- [ ] Gravacao local simultanea configurada (backup)
- [ ] Promocao feita 48h antes (email + social + comunidade)
- [ ] Lembretes enviados (2h e 15min antes)
- [ ] Countdown iniciado 5min antes (musica + timer)
- [ ] Zero downtime ou problemas tecnicos criticos
- [ ] Chat moderado ativamente (zero toxicidade visivel)
- [ ] Q&A bem gerenciado (8-10 perguntas respondidas)
- [ ] VOD disponivel imediatamente pos-live
- [ ] Versao editada publicada no feed (dentro de 48h)
- [ ] Clips criados e distribuidos em social media
- [ ] Performance documentada (viewers, engagement, feedback)
- [ ] ROI positivo (alcance > episodio regular)
