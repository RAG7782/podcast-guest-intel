# Padrões de Acessibilidade

## Compromisso

Este podcast se compromete a ser **acessível para todas as pessoas**, incluindo pessoas com deficiências auditivas, visuais, cognitivas e motoras.

**Referência:** Web Content Accessibility Guidelines (WCAG) 2.1, Nível AA.

---

## 1. Transcrição (Transcript)

### Obrigatoriedade

**100% dos episódios DEVEM ter transcrição completa.**

### Formato

**Transcrição Básica:**
```
[00:00] Host: Bem-vindos ao episódio 42 do [Nome do Podcast].

[00:15] Host: Hoje vamos falar sobre acessibilidade em podcasts.

[00:30] Convidado: Obrigado por me receber. É um tema muito importante.
```

**Transcrição Completa (recomendado):**
```
[00:00] [Música de abertura tocando — instrumental uptempo]

[00:08] Host (João Silva): Bem-vindos ao episódio 42 do [Nome do Podcast].
Eu sou João Silva e hoje vamos falar sobre acessibilidade em podcasts.

[00:15] Host: Comigo está Maria Santos, especialista em design inclusivo.
Oi Maria, tudo bem?

[00:20] Convidado (Maria Santos): Oi João! Obrigada por me receber.
É um tema muito importante.

[00:25] [Som de notificação]

[00:26] Host: [risos] Desculpa, esqueci de silenciar o celular.
```

**Elementos a incluir:**
- **Timestamps:** A cada mudança de fala ou evento importante (00:00, 01:23, etc.)
- **Identificação de quem fala:** [Host], [Convidado], [Nome da pessoa]
- **Sons não-verbais:** [risos], [pausa], [música], [aplausos]
- **Música e efeitos:** Descrever brevemente
- **Ênfase:** *itálico* para ênfase, **negrito** para forte ênfase (opcional)

### Formatação para Screen Readers

- **Estrutura semântica:** Usar headings (H1, H2, H3) para organizar
- **Listas:** Usar listas formatadas (`-` ou `1.`)
- **Parágrafos:** Separar falas longas em parágrafos
- **Evitar:** Blocos de texto sem quebra

### Onde Publicar

- **Show notes** (descrição do episódio)
- **Website/blog** (página dedicada)
- **PDF/TXT** (download disponível)
- **Plataformas que suportam:** YouTube (descrição ou captions), Spotify (ainda limitado)

### Como Gerar

**Opção 1: Automático + Revisão (recomendado)**
- Usar ferramenta: Descript, Otter.ai, Whisper, Rev.ai
- **SEMPRE revisar manualmente:** IA erra nomes próprios, termos técnicos, sotaques

**Opção 2: Manual**
- Transcrever manualmente (demorado, mas 100% preciso)

**Opção 3: Serviço Pago**
- Rev.com, GoTranscript (transcrição humana, $1-3/minuto)

**Prazo:** Transcrição deve estar disponível **junto com a publicação do episódio**.

---

## 2. Chapters (Capítulos)

### Obrigatoriedade

**100% dos episódios DEVEM ter chapters.**

### O Que São

Chapters permitem navegação intra-episódio, essencial para:
- Pessoas com deficiência cognitiva (pulam para seção de interesse)
- Pessoas com TDAH (navegação não-linear)
- Usuários com pouco tempo (vão direto ao ponto)

### Formato

**Padrão Podcasting 2.0 (recomendado):**
```json
{
  "version": "1.0.0",
  "chapters": [
    {
      "startTime": 0,
      "title": "Introdução",
      "img": "https://example.com/intro.jpg"
    },
    {
      "startTime": 120,
      "title": "O que é acessibilidade em podcasts?",
      "img": "https://example.com/chapter1.jpg"
    },
    {
      "startTime": 360,
      "title": "Transcrições e legendas",
      "img": "https://example.com/chapter2.jpg"
    }
  ]
}
```

**Alternativa (ID3 tags):**
Usar ferramentas como Forecast, Auphonic para adicionar chapters como metadata MP3.

### Onde Adicionar

- **RSS feed:** Tag `<podcast:chapters>` (Podcasting 2.0)
- **MP3 metadata:** ID3 tags (CHAP frames)
- **YouTube:** Timestamps na descrição

### Ferramentas

- **Forecast, Fireside, Transistor:** Suporte nativo a chapters
- **Auphonic:** Adicionar chapters automaticamente
- **Descript:** Gera chapters com base em headings

---

## 3. Show Notes Estruturados

### Princípios

- **Estrutura semântica:** Usar H1, H2, H3 corretamente
- **Listas:** Organizar informações em listas (`-`, `1.`)
- **Links descritivos:** "Acesse o site" em vez de "Clique aqui"
- **Parágrafos curtos:** Facilita leitura para pessoas com dislexia

### Template Acessível

```markdown
# Episódio 42: Acessibilidade em Podcasts

## Descrição
Neste episódio, conversamos com Maria Santos sobre como tornar podcasts
acessíveis para todas as pessoas.

## Convidado
**Maria Santos**
Especialista em design inclusivo
[Site da Maria](https://mariaexemplo.com) | [Twitter](https://twitter.com/maria)

## Tópicos Discutidos
- [00:00] Introdução
- [02:00] O que é acessibilidade?
- [06:00] Importância de transcrições
- [12:00] Legendas em vídeos
- [18:00] Design inclusivo

## Links Mencionados
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Podcasting 2.0 Chapters](https://podcastindex.org/namespace/1.0)

## Transcrição Completa
[Link para transcrição completa](https://podcast.com/ep42/transcript)

## Apoie o Podcast
[Link para apoio](https://podcast.com/apoie)
```

### Evitar

- ❌ Paredes de texto sem headings
- ❌ "Clique aqui" (link não-descritivo)
- ❌ Emojis excessivos (screen readers leem "emoji coração emoji fogo emoji estrela")
- ❌ ASCII art (incompreensível para screen readers)

---

## 4. Alt Text (Texto Alternativo)

### Onde Usar

**TODAS as imagens DEVEM ter alt text:**
- Artwork do podcast
- Thumbnails de episódios
- Imagens em posts de redes sociais
- Gráficos/infográficos nos show notes

### Como Escrever

**Bom alt text:**
- Descreve o conteúdo da imagem
- Conciso (120-150 caracteres)
- Contextualizado

**Exemplos:**

**❌ Ruim:**
```
alt="imagem"
alt="foto"
alt=""
```

**✅ Bom:**
```
alt="João Silva, host do podcast, sorrindo em frente a microfone"
alt="Gráfico de barras mostrando crescimento de 50% em acessibilidade de podcasts em 2025"
alt="Logo do podcast: letras azuis sobre fundo branco"
```

**Para imagens decorativas:**
```
alt=""
(vazio, indica para screen reader ignorar)
```

### Ferramentas

- **Twitter/X:** Campo "Descrição" ao adicionar imagem
- **Instagram:** "Texto alternativo" em configurações avançadas
- **LinkedIn:** "Adicionar texto alternativo"
- **WordPress/sites:** Campo "Alt text" em upload de mídia

---

## 5. Content Warnings (Avisos de Conteúdo)

### Quando Usar

**Tópicos sensíveis que podem causar desconforto:**
- Violência (física, psicológica, sexual)
- Saúde mental (suicídio, automutilação, transtornos)
- Trauma (abuso, guerra, desastres)
- Discriminação (racismo, homofobia, capacitismo)
- Substâncias (álcool, drogas)
- Temas médicos (procedimentos cirúrgicos, sangue)

### Formato

**No início do episódio (áudio):**
```
"Antes de começar, este episódio contém discussões sobre [tópico sensível].
Se você preferir pular esta parte, vá direto para o minuto [XX:XX]."
```

**Nos show notes (escrito):**
```
⚠️ Content Warning: Este episódio discute [tópico].
Timestamps: [02:30] - [08:45]
```

**Timestamped (recomendado):**
Indicar exatamente onde o conteúdo sensível ocorre, permitindo que ouvintes pulem apenas aquela parte.

### Princípio

**Não é censura, é escolha informada.**
Pessoas podem decidir se querem ou não consumir o conteúdo.

---

## 6. Vídeo — Legendas

### Obrigatoriedade

**100% dos vídeos DEVEM ter legendas (closed captions).**

### Formato

**Legendas automáticas (YouTube, Descript):**
- ✅ Melhor que nada
- ❌ SEMPRE revisar (erros em nomes, termos técnicos)

**Legendas humanas (recomendado):**
- Rev.com, GoTranscript, 3Play Media
- Custo: $1-3/minuto

**Formato de arquivo:**
- `.srt` (mais comum)
- `.vtt` (WebVTT, para web)

### Onde Adicionar

- **YouTube:** Upload de arquivo .srt OU edição de auto-captions
- **Vimeo:** Upload de arquivo .srt
- **Redes sociais:** TikTok, Instagram Reels (legendas automáticas OK, revisar)

### Elementos a Incluir

**Não apenas palavras:**
- `[música tocando]`
- `[risos]`
- `[porta batendo]`
- `[pausa]`

**Identificação de quem fala (se múltiplas pessoas):**
```
João: Como você está?
Maria: Muito bem, obrigada!
```

---

## 7. Website — Navegação por Teclado

Se o podcast tem website próprio:

### Obrigatoriedade

**Site DEVE ser navegável 100% por teclado (sem mouse).**

### Checklist

- [ ] Tab navega entre links/botões
- [ ] Enter/Space ativa links/botões
- [ ] Foco visível (borda ao redor do elemento focado)
- [ ] Ordem lógica de tabulação
- [ ] Sem "keyboard trap" (ficar preso em elemento)
- [ ] Skip link ("Pular para conteúdo principal")

### Ferramentas de Teste

- **Teste manual:** Navegar site usando apenas Tab, Enter, Arrows
- **Lighthouse (Chrome DevTools):** Auditoria de acessibilidade
- **axe DevTools:** Extensão para teste de a11y

---

## 8. Contraste de Cores (WCAG AA)

### Website e Materiais Visuais

**Contraste mínimo:**
- **Texto normal:** 4.5:1
- **Texto grande (18pt+ ou 14pt bold):** 3:1

### Ferramentas de Teste

- **WebAIM Contrast Checker:** `webaim.org/resources/contrastchecker/`
- **Coolors Contrast Checker:** `coolors.co/contrast-checker`

### Evitar

- ❌ Texto cinza-claro sobre branco
- ❌ Texto amarelo sobre branco
- ❌ Texto sobre imagens (sem fundo sólido/opaco)

---

## 9. Áudio — Qualidade e Clareza

### Princípios

**Para pessoas com deficiência auditiva parcial ou processamento auditivo:**

- ✅ **Volume consistente:** Normalizar áudio (Auphonic, Adobe Podcast)
- ✅ **Voz clara:** Falar articulado, não muito rápido
- ✅ **Reduzir ruído de fundo:** Tratamento acústico, edição
- ✅ **Evitar sobreposição de vozes:** Não falar ao mesmo tempo
- ✅ **Pausas:** Dar tempo para processar informação

### Dependência de Áudio

**NUNCA depender APENAS de áudio para informação crítica.**

**❌ Ruim:**
```
"Como vocês podem ver neste gráfico..." — sem descrever o gráfico
```

**✅ Bom:**
```
"Este gráfico mostra crescimento de 50% em acessibilidade entre 2024 e 2025,
com a barra azul representando 2024 (30%) e a barra verde representando 2025 (45%)."
```

---

## 10. Feedback e Melhoria Contínua

### Canal para Reportar Problemas

**Criar canal específico para feedback de acessibilidade:**

- Email: `acessibilidade@podcast.com`
- Formulário no site
- Menção nos show notes: "Encontrou problema de acessibilidade? Nos avise em [email]"

### Resposta

- **Prazo:** Responder em até 5 dias úteis
- **Ação:** Corrigir problema em até 14 dias
- **Transparência:** Agradecer feedback publicamente (com permissão)

---

## 11. Checklist de Acessibilidade — Pré-Publicação

Antes de publicar episódio:

- [ ] Transcrição completa disponível?
- [ ] Chapters adicionados?
- [ ] Show notes estruturados (H1-H3)?
- [ ] Alt text em todas as imagens?
- [ ] Content warning (se aplicável)?
- [ ] Legendas no vídeo (se aplicável)?
- [ ] Áudio normalizado e claro?
- [ ] Links descritivos nos show notes?

---

## 12. Ferramentas Recomendadas

### Transcrição
- **Descript:** Auto-transcribe + edição
- **Otter.ai:** Transcrição em tempo real
- **OpenAI Whisper:** Open-source, grátis
- **Rev.com:** Humano, pago

### Chapters
- **Forecast, Fireside, Transistor:** Hosting com chapters
- **Auphonic:** Geração automática de chapters

### Legendas
- **Rev.com:** Captions humanos
- **YouTube:** Auto-captions (revisar)
- **Descript:** Export .srt

### Alt Text
- **Manual:** Sempre melhor
- **AI (auxílio):** GPT-4 Vision, Azure Computer Vision (SEMPRE revisar)

### Testes
- **Lighthouse:** Auditoria web
- **WAVE:** Avaliação de acessibilidade web
- **NVDA/JAWS:** Screen readers para testar

---

## 13. Objetivo — Acessível Para

Este podcast deve ser acessível para:

- ✅ Pessoas com deficiência auditiva (transcrição, legendas)
- ✅ Pessoas com deficiência visual (alt text, site navegável por teclado, screen reader-friendly)
- ✅ Pessoas com deficiência cognitiva (chapters, linguagem clara, pausas)
- ✅ Pessoas com deficiência motora (navegação por teclado, controles grandes)
- ✅ Pessoas com baixa velocidade de internet (transcrição texto como alternativa)
- ✅ Pessoas em ambientes silenciosos (transcrição como alternativa)
- ✅ Pessoas não-nativas em português (transcrição para traduzir)

---

## 14. Responsável

- **Implementação:** @editor (Clip) + @designer (Pixel)
- **Validação:** @guardian (Sentinel)
- **Checklist pré-publicação:** @producer (Max)

---

## 15. Recursos Adicionais

- **WCAG 2.1:** `w3.org/WAI/WCAG21/quickref/`
- **WebAIM:** `webaim.org` (artigos, ferramentas)
- **A11y Project:** `a11yproject.com` (checklist, recursos)
- **Podcasting 2.0:** `podcastindex.org/namespace/1.0`

---

**Última atualização:** 2026-02-11

**Princípio orientador:** "Acessibilidade não é favor, é direito."
