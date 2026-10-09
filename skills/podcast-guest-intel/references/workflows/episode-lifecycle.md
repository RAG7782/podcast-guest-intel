# Workflow: Episode Lifecycle

## Visao Geral
- **Objetivo:** Producao completa de um episodio de podcast, da ideia ate a publicacao
- **SLA Total:** 7-14 dias
- **Owner:** @producer

## Etapas

### Etapa 1: Idea & Briefing
- **Owner:** @producer
- **SLA:** 2 dias
- **Entrada:** Topic ideas, audience feedback, content calendar
- **Saida:** Episode brief aprovado (tema, angulo, guest, formato)
- **Checklist:**
  - [ ] Validar alinhamento com content pillars do podcast bible
  - [ ] Verificar se topico ja foi coberto (buscar episodios anteriores)
  - [ ] Definir formato (solo, entrevista, painel, storytelling)
  - [ ] Identificar guest ideal (se aplicavel)
  - [ ] Criar brief com objetivo, perguntas-chave, CTA
  - [ ] Aprovar brief com host

### Etapa 2: Script Writing
- **Owner:** @researcher
- **SLA:** 2 dias
- **Entrada:** Episode brief, research materials
- **Saida:** Script aprovado (roteiro, perguntas, estrutura)
- **Checklist:**
  - [ ] Estruturar introducao (hook + contexto)
  - [ ] Desenvolver corpo (3-5 blocos tematicos)
  - [ ] Escrever conclusao (recap + CTA)
  - [ ] Inserir vinhetas e transicoes
  - [ ] Incluir timestamps estimados
  - [ ] Revisar com @guardian (fact-check inicial)
  - [ ] Aprovar script com host

**GATE 1: Script Approval** - Host deve aprovar antes de prosseguir

### Etapa 3: Recording
- **Owner:** @host + @engineer
- **SLA:** 1 dia
- **Entrada:** Script aprovado, guest confirmado (se aplicavel)
- **Saida:** Audio raw gravado (WAV dual recording)
- **Checklist:**
  - [ ] Executar checklist pre-gravacao (ver references/checklists/pre-gravacao.md)
  - [ ] Configurar dual recording (DAW + backup)
  - [ ] Gravar intro/corpo/conclusao
  - [ ] Gravar retakes se necessario
  - [ ] Salvar arquivos com naming: S{XX}E{XX}_{titulo}_raw.wav
  - [ ] Backup imediato em 2 locais

### Etapa 4: Editing
- **Owner:** @engineer
- **SLA:** 2 dias
- **Entrada:** Audio raw
- **Saida:** Audio editado (sem master)
- **Checklist:**
  - [ ] Remover silêncios, ums/ahs, erros
  - [ ] Ajustar niveis e equalizacao
  - [ ] Inserir vinhetas (intro/outro/transicoes)
  - [ ] Adicionar musica de fundo (se aplicavel)
  - [ ] Cortar para tempo ideal (respeitar formato)
  - [ ] Exportar versao edited para review

### Etapa 5: Mixing & Mastering
- **Owner:** @engineer
- **SLA:** 1 dia
- **Entrada:** Audio editado aprovado
- **Saida:** Masters finais por plataforma
- **Checklist:**
  - [ ] Mix final (balance, EQ, compression)
  - [ ] Master para Spotify (-14 LUFS)
  - [ ] Master para Apple Podcasts (-16 LUFS)
  - [ ] Master para YouTube (-14 LUFS)
  - [ ] Master para Amazon Music (-14 LUFS)
  - [ ] Executar checklist quality-audio.md
  - [ ] Listening test em diferentes devices

**GATE 2: Audio Quality Check** - Audio engineer deve aprovar qualidade tecnica

### Etapa 6: Content Creation
- **Owner:** @editor
- **SLA:** 2 dias (paralelo com etapa 5)
- **Entrada:** Script, audio editado
- **Saida:** Show notes, SEO page, social clips
- **Checklist:**
  - [ ] Escrever show notes (2000+ palavras, timestamps)
  - [ ] Criar SEO content page (checklist seo-podcast.md)
  - [ ] Gerar transcript e publicar
  - [ ] Criar 3-5 clips para social (Shorts/Reels/TikTok)
  - [ ] Criar audiograms
  - [ ] Escrever copies para cada canal
  - [ ] Criar artwork/thumbnail

### Etapa 7: Review & Fact-Check
- **Owner:** @guardian
- **SLA:** 1 dia
- **Entrada:** Audio master, show notes, transcript
- **Saida:** Aprovacao final ou lista de correcoes
- **Checklist:**
  - [ ] Fact-check de claims principais
  - [ ] Verificar disclosures (sponsors, afiliados)
  - [ ] Validar compliance (LGPD, direitos autorais)
  - [ ] Revisar linguagem (evitar conteudo problematico)
  - [ ] Confirmar diversidade (se convidado, atualizar diversity-check)
  - [ ] Aprovar ou solicitar correcoes

**GATE 3: Fact-Check Approval** - Guardian deve aprovar antes de publicar

### Etapa 8: Publishing
- **Owner:** @distributor
- **SLA:** 1 dia
- **Entrada:** Masters aprovados, content aprovado
- **Saida:** Episodio publicado em todas as plataformas
- **Checklist:**
  - [ ] Executar checklist pre-publicacao.md
  - [ ] Upload para hosting (RSS feed)
  - [ ] Publicar show notes no site
  - [ ] Agendar posts sociais
  - [ ] Enviar newsletter
  - [ ] Publicar video no YouTube (se aplicavel)
  - [ ] Ativar monetizacao (ads, V4V)
  - [ ] Notificar equipe

**GATE 4: Final Approval** - Producer faz validacao final antes do go-live

## Diagrama

```
[Idea/Briefing] (2d)
      |
      v
[Script Writing] (2d)
      |
      v
   GATE 1: Script Approval
      |
      v
[Recording] (1d)
      |
      v
[Editing] (2d)
      |
      +-------------------+
      |                   |
      v                   v
[Mixing/Master] (1d)  [Content Creation] (2d)
      |                   |
      +--------+----------+
               |
               v
        GATE 2: Audio Quality Check
               |
               v
     [Fact-Check] (1d)
               |
               v
        GATE 3: Guardian Approval
               |
               v
        [Publishing] (1d)
               |
               v
        GATE 4: Final Approval
               |
               v
           [LIVE]
```

## Metricas de Sucesso
- **SLA Compliance:** 90%+ dos episodios dentro do prazo
- **Quality Score:** Media 4.5+ (5.0 scale) em listener feedback
- **Zero Fact-Check Issues:** Nenhum episodio publicado com erros factuais graves
- **Republish Rate:** <5% dos episodios precisam de re-upload
- **Time to Publish:** Media de 10 dias (meta: 7-14 dias)

## Pontos de Falha Comuns
- **Guest No-Show:** Sempre ter backup plan (episodio solo ou repescagem)
- **Audio Quality Issues:** Descoberto tarde demais → fazer tech check antes da gravacao
- **Fact-Check Delays:** Guardian sobrecarregado → agendar review com antecedencia
- **Content Bottleneck:** Content creator atrasado → produzir content em paralelo com master
- **Last-Minute Changes:** Host quer refazer algo → definir deadline de changes (24h antes do publish)
- **Missing Approvals:** Gate sem owner → sempre designar aprovador antes de comecar
