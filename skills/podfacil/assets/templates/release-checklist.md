# Release Checklist
## Checklist Completo Pre-Publicacao

---

## Informacoes do Episodio

**Episodio:** S{X}E{XX}
**Titulo:** {Titulo Final}
**Data de publicacao planejada:** {YYYY-MM-DD} as {HH:MM timezone}
**Responsavel final:** {Nome - quem da o go/no-go}

---

## AUDIO MASTER ✅

### Arquivo Principal

- [ ] **Formato final:** MP3, 192kbps minimo (320kbps recomendado)
- [ ] **Naming convention:** `S{season}E{episode}_{titulo-slug}_master_v{version}.mp3`
- [ ] **Duracao verificada:** {XX:XX} - conferir se esta dentro da meta

### Qualidade Tecnica

- [ ] **LUFS compliance verificado:**
  - Spotify: -14 LUFS ±1
  - Apple Podcasts: -16 LUFS ±1
  - YouTube: -14 LUFS ±1
  - Amazon Music: -14 LUFS ±1

- [ ] **True Peak:** Abaixo de -1dBTP (evitar clipping)
- [ ] **Frequency range:** 20Hz-20kHz (sem cortes anormais)
- [ ] **Stereo balance:** Centralizado (nao pender pra esquerda/direita)

### Limpeza de Audio

- [ ] **Ruidos removidos:** Cliques, pops, respiracoes ruidosas
- [ ] **Background noise:** Reduzido sem afetar voz natural
- [ ] **Mouth clicks:** Minimizados
- [ ] **"Ahns" excessivos:** Editados (manter alguns para autenticidade)
- [ ] **Silencio excessivo:** Cortado (max 2-3 segundos)

### Elementos Sonoros

- [ ] **Vinheta:** Presente e no volume correto
- [ ] **Trilha de fundo:** -20dB abaixo da voz (se aplicavel)
- [ ] **Transicoes:** Suaves, sem cortes abruptos (exceto intencionais)
- [ ] **Fade in/out:** Inicial (0.5s) e final (2s)

### Review Final

- [ ] **Escutado do inicio ao fim:** Sem acelerar
- [ ] **Escutado em 3 dispositivos:** Fone, carro, caixa de som
- [ ] **Aprovado por:** @engineer (audio engineer)
- [ ] **Aprovado por:** @host (host - conteudo)

---

## METADATA COMPLETA ✅

### Informacoes Basicas

- [ ] **Titulo do episodio:** {Titulo - max 100 caracteres}
- [ ] **Numero do episodio:** S{X}E{XX}
- [ ] **Descricao curta:** {1-2 linhas para players - max 255 chars}
- [ ] **Descricao longa:** {Paragrafo completo - max 4000 chars}
- [ ] **Category:** {Categoria principal do podcast}
- [ ] **Subcategory:** {Subcategoria se aplicavel}
- [ ] **Language:** Portuguese (pt-BR)
- [ ] **Explicit content:** [ ] Sim (palavrões/temas adultos) [ ] Nao

### Tags e Keywords

- [ ] **Tags principais:** {tag1}, {tag2}, {tag3} (minimo 5, maximo 15)
- [ ] **Keywords SEO:** {palavra-chave 1}, {palavra-chave 2}
- [ ] **Guest name(s):** {Nome do convidado - se aplicavel}

### Timing

- [ ] **Publish date:** {YYYY-MM-DD}
- [ ] **Publish time:** {HH:MM timezone}
- [ ] **Episode type:** [ ] Full [ ] Trailer [ ] Bonus

---

## CHAPTER MARKERS ✅

- [ ] **Markers inseridos no arquivo MP3** (ID3 tags ou plataforma de hosting)
- [ ] **Minimo 3 chapters, maximo 15**
- [ ] **Cada chapter com:**
  - Timestamp preciso
  - Titulo descritivo (max 50 chars)
  - Opcional: Imagem por chapter (se plataforma suportar)

**Exemplo de chapters:**
```
[0:00] Cold Open
[0:15] Introducao
[1:30] Como Pedro comecou sem VC
[8:45] Revenue-based financing explicado
[15:20] A metrica que importa
[30:15] Lightning Round
[35:00] Onde encontrar Pedro
```

- [ ] **Chapters conferidos:** Timestamps batem com conteudo

---

## TRANSCRIPT ✅

- [ ] **Transcript gerado:** Via Descript, Otter.ai, ou manual
- [ ] **Transcript revisado:** Correcao de erros de transcricao automatica
- [ ] **Formatacao correta:**
  - Identificacao clara de speakers (HOST:, GUEST:)
  - Paragrafos por ideia, nao por linha
  - Pontuacao adequada
- [ ] **Transcript em 2 formatos:**
  - HTML (para show notes - collapsible)
  - TXT ou PDF (para download)
- [ ] **Uploaded em:** {Plataforma/URL}

---

## SHOW NOTES PUBLICADAS ✅

- [ ] **Show notes escritas:** Seguindo show-notes-template.md
- [ ] **Elementos obrigatorios presentes:**
  - [ ] Resumo (2-3 paragrafos)
  - [ ] Timestamps/Chapters
  - [ ] Key Takeaways (3-5)
  - [ ] Bio do convidado (se aplicavel)
  - [ ] Links para redes do convidado
  - [ ] Recursos mencionados (com links ativos)
  - [ ] Transcript completo (collapsible)
  - [ ] CTA (Subscribe, Review, Newsletter)

- [ ] **SEO otimizado:**
  - [ ] Meta title (max 60 chars)
  - [ ] Meta description (max 155 chars)
  - [ ] Headings corretos (H1, H2, H3)
  - [ ] Keywords naturalmente distribuidos
  - [ ] Links internos (para outros episodios)
  - [ ] Links externos (fontes, recursos)

- [ ] **Links verificados:** Todos funcionando (nenhum 404)
- [ ] **Publicado em:** {URL do episodio}
- [ ] **Indexed pelo Google:** Submeter sitemap se novo

---

## SEO CONTENT PAGE ✅

- [ ] **URL amigavel:** {website.com}/s{X}e{XX}-{slug}
- [ ] **Canonical tag:** Apontando para este URL
- [ ] **Open Graph tags:**
  ```html
  og:title = {Titulo do Episodio}
  og:description = {Meta description}
  og:image = {URL da thumbnail 1200x630px}
  og:url = {URL do episodio}
  og:type = article
  ```
- [ ] **Twitter Card tags:**
  ```html
  twitter:card = summary_large_image
  twitter:title = {Titulo}
  twitter:description = {Descricao}
  twitter:image = {URL da thumbnail}
  ```
- [ ] **Schema.org markup:** PodcastEpisode structured data

---

## ARTWORK ✅

### Cover Art do Podcast (se novo episodio requer update)

- [ ] **Tamanho:** 3000x3000px (obrigatorio para Apple Podcasts)
- [ ] **Formato:** PNG ou JPG
- [ ] **Tamanho de arquivo:** Maximo 512KB
- [ ] **Resolucao:** 72dpi minimo, 300dpi recomendado
- [ ] **Espaco de cor:** RGB
- [ ] **Legivel ate 80x80px:** Testado

### Thumbnail do Episodio

- [ ] **YouTube (16:9):** 1920x1080px
- [ ] **Instagram Feed (1:1):** 1080x1080px
- [ ] **Elementos:**
  - [ ] Logo do podcast visivel
  - [ ] Numero do episodio
  - [ ] Titulo do episodio (legivel)
  - [ ] Foto do convidado (se aplicavel)
  - [ ] Alto contraste (testado em mobile)

### Social Media Assets

- [ ] **Quote cards:** 3-5 criados (1080x1080px)
- [ ] **Audiograms:** 2-3 prontos (30-90s cada)
- [ ] **Instagram Stories:** 5-7 templates prontos (1080x1920px)
- [ ] **LinkedIn banner:** 1200x627px
- [ ] **Twitter header (se episodio especial):** 1500x500px

---

## SOCIAL CLIPS PRONTOS ✅

### Audiograms

- [ ] **Clip 1:** {Tema - ex: momento controverso} - 60s
  - [ ] Audio exportado
  - [ ] Legenda/captions
  - [ ] Forma de onda sincronizada
  - [ ] Logo e CTA no final
  - [ ] Formato: 1080x1080px MP4

- [ ] **Clip 2:** {Tema - ex: framework acionavel} - 45s
  - [ ] Todos os elementos acima

- [ ] **Clip 3:** {Tema - ex: story pessoal} - 90s
  - [ ] Todos os elementos acima

### Video Clips (se houver video)

- [ ] **Clip 1:** TikTok/Reels - 30-60s
  - [ ] Hook text sobreposto
  - [ ] Caption escrita
  - [ ] Hashtags selecionadas
  - [ ] Formato: 1080x1920px MP4

- [ ] **Clip 2:** YouTube Short - 60s
- [ ] **Clip 3:** LinkedIn video - 90s

### Armazenamento

- [ ] **Todos os clips em:** {Pasta no Google Drive/Dropbox}
- [ ] **Assets prontos para @growth agendar:**

---

## NEWSLETTER ✅

- [ ] **Newsletter draft pronto:** Seguindo newsletter teaser template
- [ ] **Subject line:** {Testado em previewer - max 50 chars}
- [ ] **Preview text:** {Primera linha - max 90 chars}
- [ ] **Conteudo:**
  - [ ] Hook forte
  - [ ] Resumo do episodio
  - [ ] Key takeaways
  - [ ] CTA clara (link do episodio)
  - [ ] P.S. com valor extra
- [ ] **Links testados:** Todos funcionando
- [ ] **Agendado para:** {Data/hora - geralmente dia da publicacao, 9h}
- [ ] **Plataforma:** {Mailchimp, ConvertKit, Substack}

---

## DISCLOSURE E COMPLIANCE ✅

### Patrocinio

- [ ] **Disclosure inserido no audio:** "Este episodio e apresentado por..."
- [ ] **Disclosure nos show notes:** Mencionado no topo
- [ ] **FTC compliance:** Claramente identificado como conteudo patrocinado
- [ ] **Affiliate links:** Marcados com "#ad" ou "link afiliado"

### Consentimento

- [ ] **Release assinado pelo convidado:** (se aplicavel)
- [ ] **Permissao para usar nome/imagem:** Confirmada
- [ ] **Convidado revisou trecho (se pediu):** Aprovacao documentada

### Fact-Checking

- [ ] **Fact-check aprovado:** @guardian verificou claims factuais
- [ ] **Fontes citadas:** Corretamente atribuidas
- [ ] **Dados/estatisticas:** Verificados e atualizados
- [ ] **Nenhuma informacao confidencial vazada:** Duplo-check

### Ethical Review

- [ ] **Sensitive topics:** Content warning inserido se necessario
- [ ] **Diversidade check:** Episodios da temporada balanceados
- [ ] **Nenhuma violacao do editorial-ethics-code.md**

---

## BACKUP E ARQUIVAMENTO ✅

- [ ] **Arquivo master salvo em 3 locais:**
  1. [ ] Local (HD externo)
  2. [ ] Cloud 1 ({Google Drive, Dropbox})
  3. [ ] Cloud 2 ({Backup alternativo})

- [ ] **Arquivos fonte salvos:**
  - [ ] Projeto de edicao (Descript, Audacity, etc)
  - [ ] Audio bruto individual de cada speaker
  - [ ] Video bruto (se houver)

- [ ] **Naming convention seguida:**
  ```
  squads/podcast-production/episodes/S{season}/E{episode}/
  ├── master/
  │   └── S{X}E{XX}_{slug}_master_v1.mp3
  ├── raw/
  │   ├── host_raw.wav
  │   ├── guest_raw.wav
  │   └── backup_raw.wav
  ├── project/
  │   └── {projeto de edicao}
  └── assets/
      ├── thumbnail.png
      ├── clips/
      └── show-notes.md
  ```

---

## PUBLICACAO NAS PLATAFORMAS ✅

### Hosting Platform (ex: Buzzsprout, Anchor, Transistor)

- [ ] **Episodio uploaded**
- [ ] **Metadata completa inserida**
- [ ] **Artwork do episodio anexado**
- [ ] **Scheduled para:** {Data/hora}
- [ ] **RSS feed atualizado:** Conferir em {URL do RSS}

### Distribuicao Automatica Confirmada

- [ ] **Spotify:** Feed conectado e funcionando
- [ ] **Apple Podcasts:** Feed conectado
- [ ] **Google Podcasts:** Feed conectado
- [ ] **Amazon Music:** Feed conectado
- [ ] **Overcast, Pocket Casts, etc:** Via RSS

### YouTube (se aplicavel)

- [ ] **Video uploaded:** Audio + imagem estatica OU video completo
- [ ] **Metadata YouTube:**
  - [ ] Titulo (max 100 chars)
  - [ ] Descricao completa com timestamps
  - [ ] Tags (minimo 5)
  - [ ] Thumbnail customizado
  - [ ] End screen configurado
  - [ ] Cards inseridos (links relevantes)
- [ ] **Playlist:** Adicionado a playlist da temporada
- [ ] **Monetization:** Configurado (se aplicavel)
- [ ] **Scheduled para:** {Data/hora}

### Website Proprio

- [ ] **Post publicado:** Show notes completas
- [ ] **Player embed funcionando**
- [ ] **Pagina acessivel em:** {URL}
- [ ] **Adicionado a listagem de episodios**

---

## GUEST REVIEW PROTOCOL ✅

(Se o convidado pediu review)

- [ ] **Trecho relevante enviado para review:** Minimo 3 dias antes da publicacao
- [ ] **Prazo de resposta comunicado:** 48 horas
- [ ] **Feedback recebido e implementado:** (se aplicavel)
- [ ] **Aprovacao final documentada:** Email salvo

**Nota:** Se convidado nao responder no prazo, prosseguir com publicacao (comunicado previamente).

---

## DIVERSITY CHECK DA TEMPORADA ✅

- [ ] **Atualizado planilha de diversidade:**
  - Regiao, area de expertise, senioridade/trajetoria (nada inferido sobre identidade)
  - Perspectivas divergentes

- [ ] **Este episodio contribui para balanceamento?** [ ] Sim [ ] Nao
- [ ] **Proximos episodios planejados levam em conta gaps?**

---

## SCHEDULED EM TODAS AS PLATAFORMAS ✅

Confirmar agendamento:

- [ ] **Hosting platform:** {Data/hora}
- [ ] **YouTube:** {Data/hora}
- [ ] **Instagram Feed:** {Data/hora}
- [ ] **Instagram Stories:** {Data/hora - sequencia de 5-7}
- [ ] **Twitter/X:** {Data/hora - 3 posts ao longo do dia}
- [ ] **LinkedIn:** {Data/hora}
- [ ] **TikTok:** {Data/hora}
- [ ] **Newsletter:** {Data/hora}
- [ ] **Discord/Telegram (se aplicavel):** {Data/hora}

---

## MONITORING SETUP ✅

- [ ] **Analytics preparado:**
  - [ ] Buzzsprout/Hosting analytics ativos
  - [ ] Google Analytics configurado (se website proprio)
  - [ ] YouTube Analytics
  - [ ] Social media insights habilitados

- [ ] **Alertas configurados:**
  - [ ] Notificacao se episodio nao publicar no horario
  - [ ] Alertas de comentarios/reviews
  - [ ] Mencoes em redes sociais

---

## CONTINGENCY PLAN ✅

Se algo der errado:

- [ ] **Backup plan documentado:**
  - Se hosting cair: {Plano B}
  - Se convidado pedir remocao last-minute: {Protocolo}
  - Se erro grave for descoberto apos publicacao: {Processo de correcao}

- [ ] **Pessoa de plantao no dia do lancamento:** {Nome + contato}

---

## GO / NO-GO FINAL

**Pre-flight checklist:**

- [ ] Audio master perfeito e aprovado
- [ ] Metadata 100% completa
- [ ] Show notes publicadas e SEO ok
- [ ] Social assets prontos e agendados
- [ ] Convidado aprovado (se aplicavel)
- [ ] Fact-check aprovado
- [ ] Backups em 3 locais
- [ ] Scheduled em todas as plataformas
- [ ] Nenhum item critico pendente

---

**Decisao final:**

[ ] **GO:** Publicar conforme agendado

[ ] **NO-GO:** Adiar publicacao. Razao: {___________}

**Aprovado por:** {Nome} - {Data/hora}

---

**Versao:** 1.0
**Criado por:** @engineer + @producer
**Episodio:** S{X}E{XX}
**Ultima atualizacao:** {YYYY-MM-DD}

---

*Um episodio so e lancado quando TODOS os itens estao checados. Qualidade > Velocidade.*
