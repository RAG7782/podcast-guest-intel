# Checklist: SEO Podcast

**Quando usar:** Ao publicar cada episodio (otimizacao para motores de busca)

**Owner:** @editor

## Keyword Research

- [ ] Identificar keyword principal do episodio:
  - Topico especifico (ex: "como gravar podcast", "marketing para B2B")
  - Volume de busca razoavel (usar Google Keyword Planner, Ahrefs, Ubersuggest)
  - Baixa/media competicao (nao tentar ranquear para "marketing" generico)
- [ ] Identificar 3-5 keywords secundarias:
  - Long-tail (ex: "como gravar podcast com qualidade profissional")
  - Relacionadas ao topico principal
  - Usar no corpo do conteudo (naturalmente)
- [ ] Identificar intencao de busca:
  - Informacional: "como fazer X"
  - Navegacional: "podcast sobre Y"
  - Transacional: "melhores ferramentas de Z"

## Titulo do Episodio

- [ ] **Keyword principal no inicio:**
  - Bom: "Marketing para B2B: 5 Estrategias que Funcionam"
  - Ruim: "Episodio 47: Conversamos sobre Marketing"
- [ ] **Max 60 caracteres:**
  - Google trunca apos 60 chars em mobile
  - Ferramentas: Moz Title Tag Preview, Yoast SEO
- [ ] **Atrativo e claro:**
  - Evitar clickbait (promete demais)
  - Evitar vago ("Coisas Interessantes")
  - Usar numeros (ex: "7 Dicas", "3 Erros")
  - Usar poder words (ex: "Definitivo", "Essencial", "Comprovado")

## Descricao (Meta Description)

- [ ] **Keyword nos primeiros 150 caracteres:**
  - Preview em resultados de busca mostra ~150-160 chars
  - Colocar keyword + hook logo no inicio
- [ ] **Max 160 caracteres total:**
  - Google trunca apos 160 chars
  - Escrever de forma que funcione mesmo truncado
- [ ] **CTA claro:**
  - "Ouca agora", "Descubra como", "Aprenda"
- [ ] **Incluir links:**
  - Website do podcast
  - Links de guest (se aplicavel)
  - Recursos mencionados

## Show Notes (Pagina SEO)

- [ ] **2000+ palavras:**
  - Google favorece conteudo extenso (comprehensive)
  - Expandir resumo do episodio em artigo completo
  - Incluir: contexto, quotes, takeaways, recursos, transcript (parcial ou completo)
- [ ] **H1 com keyword principal:**
  - Apenas 1 H1 por pagina
  - Exemplo: `<h1>Marketing para B2B: 5 Estrategias que Funcionam</h1>`
- [ ] **H2 por topico/secao:**
  - Estrutura hierarquica (H1 > H2 > H3)
  - Incluir keywords em alguns H2 (nao forcar)
  - Exemplo:
    ```
    H1: Marketing para B2B: 5 Estrategias
    H2: Por Que Marketing B2B e Diferente de B2C
    H2: Estrategia 1: Content Marketing
    H2: Estrategia 2: LinkedIn Outreach
    ...
    ```
- [ ] **Timestamps clicaveis:**
  - Formato: `[05:23] - Topico X`
  - Link para player (se plataforma suporta jump to time)
  - Melhora UX e dwell time (SEO signal)
- [ ] **Keyword density natural:**
  - 1-2% (nao keyword stuffing)
  - Usar sinonimos e variacoes
  - LSI keywords (Latent Semantic Indexing): palavras relacionadas
- [ ] **Paragrafos curtos:**
  - Max 3-4 linhas por paragrafo
  - Facilita leitura (especialmente mobile)
- [ ] **Bullet points e listas:**
  - Google ama featured snippets (position zero)
  - Formato: "5 dicas para X", "3 erros de Y"
- [ ] **Imagens com alt text:**
  - Toda imagem deve ter alt text descritivo
  - Incluir keyword quando faz sentido
  - Exemplo: `<img src="guest.jpg" alt="Fulano, CEO da Empresa X, no podcast">`
- [ ] **Internal links:**
  - Linkar para 2-3 episodios relacionados
  - Anchor text descritivo (nao "clique aqui")
  - Exemplo: "Veja tambem nosso episodio sobre [Content Marketing para SaaS](URL-do-episodio)"
- [ ] **External links:**
  - Linkar para fontes citadas (credibilidade)
  - Linkar para guest bio/website
  - Abrir em nova aba (target="_blank")

## Transcript

- [ ] **Publicar transcript completo:**
  - Google indexa texto (nao audio)
  - Transcript = 5.000-15.000 palavras de conteudo indexavel
- [ ] **Editado (nao apenas auto-generated):**
  - Corrigir erros de transcricao
  - Adicionar pontuacao
  - Formatar em paragrafos (nao wall of text)
- [ ] **Keywords naturalmente presentes:**
  - Transcript ja contem keywords (se episodio e sobre topico)
  - Nao forcar adicional keyword stuffing
- [ ] **Formatado para leitura:**
  - Speaker labels: "Host:", "Guest:"
  - Paragrafos separados por speaker/topico
  - Destacar quotes importantes (bold ou blockquote)
- [ ] **Publicado na pagina do episodio:**
  - Abaixo das show notes ou em aba separada
  - Totalmente indexavel (nao escondido em accordion fechado)

## URL Structure

- [ ] **URL amigavel (slug):**
  - Incluir keyword principal
  - Formato: `/podcast/S01E05-marketing-para-b2b/`
  - Evitar: `/podcast/?p=12345` (nao descritivo)
- [ ] **Curta e limpa:**
  - Remover stop words (e, de, para, com) se URL ficar muito longa
  - Max 3-5 palavras no slug
- [ ] **Lowercase e hifens:**
  - Nao underscores (Google prefere hifens)
  - Nao espacos ou caracteres especiais

## Meta Tags (HTML)

- [ ] **Title tag:**
  - `<title>Marketing para B2B: 5 Estrategias | Nome do Podcast</title>`
  - Keyword + Nome do podcast (branding)
- [ ] **Meta description:**
  - `<meta name="description" content="Descubra as 5 estrategias de marketing B2B que realmente funcionam. Com Fulano, CEO da Empresa X.">`
- [ ] **Open Graph (preview em social):**
  - `<meta property="og:title" content="Marketing para B2B: 5 Estrategias">`
  - `<meta property="og:description" content="...">`
  - `<meta property="og:image" content="https://...">`
  - `<meta property="og:url" content="https://...">`
- [ ] **Twitter Card:**
  - `<meta name="twitter:card" content="summary_large_image">`
  - `<meta name="twitter:title" content="...">`
  - `<meta name="twitter:description" content="...">`
  - `<meta name="twitter:image" content="...">`

## Schema Markup (Structured Data)

- [ ] **PodcastEpisode schema:**
  ```json
  {
    "@context": "https://schema.org",
    "@type": "PodcastEpisode",
    "name": "Marketing para B2B: 5 Estrategias",
    "description": "Descubra as 5 estrategias...",
    "url": "https://podcast.com/S01E05",
    "datePublished": "2024-01-15",
    "timeRequired": "PT45M",
    "audio": {
      "@type": "AudioObject",
      "contentUrl": "https://podcast.com/audio.mp3"
    },
    "partOfSeries": {
      "@type": "PodcastSeries",
      "name": "Nome do Podcast",
      "url": "https://podcast.com"
    }
  }
  ```
- [ ] **Validar schema:**
  - Usar Google Rich Results Test
  - Verificar: nenhum erro, warnings ok

## Tags & Categories

- [ ] **5-10 tags relevantes:**
  - Mix de broad e niche
  - Exemplo: "marketing", "B2B", "estrategias de marketing", "growth hacking"
- [ ] **Categorias (RSS feed):**
  - Primary category (ex: Business)
  - Secondary category (ex: Marketing)
  - Seguir categorias do Apple Podcasts/Spotify

## Internal Linking Strategy

- [ ] **Linkar de paginas antigas para novo episodio:**
  - Encontrar episodios relacionados
  - Adicionar link no fim: "Update: Veja tambem nosso episodio sobre [X](URL-do-episodio)"
- [ ] **Criar content clusters:**
  - Pillar page (ex: "Guia Completo de Marketing B2B")
  - Cluster pages: episodios sobre sub-topicos
  - Linkar cluster pages para pillar (e vice-versa)

## Sitemap & Indexacao

- [ ] **Adicionar episodio ao sitemap.xml:**
  - Atualizar automaticamente (plugin ou script)
  - Submeter novo sitemap ao Google Search Console
- [ ] **Verificar indexacao:**
  - Google Search Console: "URL Inspection"
  - Se nao indexado: "Request Indexing"
- [ ] **Robots.txt:**
  - Garantir que pagina do episodio NAO esta bloqueada
  - Bloquear apenas admin, duplicates, etc.

## Performance (Core Web Vitals)

- [ ] **Page load rapida:**
  - Meta: <3s (ideal: <1.5s)
  - Otimizar imagens (WebP, lazy load)
  - Minificar CSS/JS
- [ ] **Mobile-friendly:**
  - Responsive design
  - Texto legivel sem zoom
  - Botoes/links clicaveis (min 48x48px)
- [ ] **HTTPS:**
  - Site deve ter SSL (Google penaliza HTTP)

## Backlinks & Promocao

- [ ] **Compartilhar em social:**
  - Cada share = potential backlink
- [ ] **Outreach para guest:**
  - Pedir guest para compartilhar (backlink do site dele)
- [ ] **Submeter a diretorios:**
  - Apple Podcasts, Spotify, Google Podcasts
  - Podcast directories (Podchaser, Listen Notes)
- [ ] **Guest post:**
  - Escrever artigo para blog de guest
  - Mencionar episodio + link

## Monitoring

- [ ] **Google Search Console:**
  - Acompanhar: impressions, clicks, CTR, position
  - Identificar: keywords que ranqueiam
- [ ] **Google Analytics:**
  - Organic traffic para pagina do episodio
  - Dwell time (tempo na pagina)
  - Bounce rate
- [ ] **Ajustar baseado em dados:**
  - Se CTR baixo: melhorar title/description
  - Se bounce rate alto: melhorar conteudo/UX

---

**Tools Recomendados:**
- **Keyword Research:** Google Keyword Planner, Ahrefs, Ubersuggest, AnswerThePublic
- **SEO Audit:** Yoast SEO (WordPress), Screaming Frog, Ahrefs Site Audit
- **Schema Validator:** Google Rich Results Test, Schema.org Validator
- **Performance:** Google PageSpeed Insights, GTmetrix
- **Rank Tracking:** Ahrefs, SEMrush, Google Search Console

---

**Assinatura do Content Creator:** _______________
**Data:** _______________
**Episodio:** S___E___
