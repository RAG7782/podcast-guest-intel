## approach-modes.yaml

```yaml
# Registro extensível de modos de abordagem (cada entrada valida contra approach-mode.schema.json).
# Adicionar modo = 1 entrada. `extends` herda defaults de outro modo (resolvido em scripts/roteiro_tools.py).
# beats/depth/counterpoint_block moldam o roteiro (F5); o roteiro se guia pelas flags, nunca pelo id.
# Modo é ortogonal ao formato (config/formats.yaml do squad).
version: 1
modes:
  - id: cauda-longa
    label: { pt-BR: Cauda longa, en: Long tail, es: Cola larga }
    description: Tema perene, buscável por anos; profundidade acima de urgência.
    hook_style: pergunta que o ouvinte digitaria numa busca
    pacing: moderado
    source_rigor: alto
    requires_counterpoint: false
    requires_guardian_gate: false
    legal_risk: baixo
    shelf_life: evergreen
    beats: [pergunta-de-busca, resposta-direta, aprofundamento, aplicacao]
    depth: profunda
    counterpoint_block: false

  - id: hype
    label: { pt-BR: Hype, en: Hype, es: Tendencia }
    description: Assunto em alta agora; janela curta, entra rápido, cita a fonte da tendência.
    hook_style: o fato da semana em uma frase
    pacing: rapido
    source_rigor: alto
    requires_counterpoint: false
    requires_guardian_gate: false
    legal_risk: medio
    shelf_life: timely
    beats: [o-fato, por-que-importa, o-que-observar]
    depth: superficie
    counterpoint_block: false

  - id: nicho
    label: { pt-BR: Nicho, en: Niche, es: Nicho }
    description: Público especializado; vocabulário técnico permitido, menos tradução para leigo.
    hook_style: dor específica do nicho
    pacing: moderado
    source_rigor: alto
    requires_counterpoint: false
    requires_guardian_gate: false
    legal_risk: baixo
    shelf_life: misto
    beats: [dor, tecnica, caso]
    depth: profunda
    counterpoint_block: false

  - id: denuncia
    label: { pt-BR: Denúncia, en: Exposé, es: Denuncia }
    description: >-
      Trata condutas de terceiros que não consentiram. Só fontes públicas. O plugin RECOMENDA
      contraditório do denunciado, gate do guardian + fact-check-review antes de gravar e revisão
      jurídica (difamação) humana; não decide por ninguém (research/00-escopo.md, "a decisão é
      sempre humana"). Afirmação sobre conduta de terceiro é claim com conduct_allegation=true; sem
      status verificado com >=1 fonte tier 1 OU >=2 fontes tier 2 independentes, a claim carrega
      advisory (R-CLAIM-CONDUTA-FONTES / R-CLAIM-CONDUTA-INDEPENDENCIA) e só vira base do roteiro
      com aceite humano registrado (contracts/human-decision.schema.json).
    hook_style: o fato documentado, sem adjetivo
    pacing: moderado
    source_rigor: maximo
    requires_counterpoint: true
    requires_guardian_gate: true
    legal_risk: alto
    shelf_life: timely
    beats: [fato-documentado, evidencia, outro-lado, o-que-falta-saber]
    depth: profunda
    counterpoint_block: true

  - id: professoral
    label: { pt-BR: Professoral, en: Lecture, es: Profesoral }
    description: Definição, distinção, caso prático; traduz o técnico para o leigo.
    hook_style: pergunta conceitual (o que é e o que não é)
    pacing: lento
    source_rigor: alto
    requires_counterpoint: false
    requires_guardian_gate: false
    legal_risk: baixo
    shelf_life: evergreen
    beats: [definicao, distincao, caso-pratico, sintese]
    depth: profunda
    counterpoint_block: false

  - id: informativo
    label: { pt-BR: Informativo, en: Informative, es: Informativo }
    description: Atualização objetiva; o que mudou, para quem, a partir de quando.
    hook_style: o que muda para você
    pacing: rapido
    source_rigor: alto
    requires_counterpoint: false
    requires_guardian_gate: false
    legal_risk: medio
    shelf_life: timely
    beats: [o-que-mudou, para-quem, a-partir-de-quando]
    depth: media
    counterpoint_block: false

  - id: reflexivo
    label: { pt-BR: Reflexivo, en: Reflective, es: Reflexivo }
    description: Pergunta aberta, filosofia aplicada, experiência pessoal; opinião assumida como opinião.
    hook_style: pergunta-dilema
    pacing: lento
    source_rigor: padrao
    requires_counterpoint: false
    requires_guardian_gate: false
    legal_risk: baixo
    shelf_life: evergreen
    beats: [dilema, experiencia, contraponto, pergunta-aberta]
    depth: media
    counterpoint_block: true

```


## trend-sources.yaml

```yaml
# Fontes de tendência padrão (valida contra trend-sources.schema.json).
# keyless: funcionam sem chave e são o fallback. Endpoints conferidos em 2026-10-09 (HTTP 200).
# byok: chave do próprio usuário. O arquivo guarda SÓ a referência (env/cofre) e o status da
# verificação feita quando a chave é fornecida. Valor de chave aqui = falha de validação.
version: 1
sources:
  - id: x
    kind: byok
    provider: X (Twitter) API
    priority: 1
    enabled: false
    credential:
      ref: { store: env, name: TREND_X_BEARER }
      status: not_provided

  - id: tiktok
    kind: byok
    provider: TikTok Research/Display API
    priority: 2
    enabled: false
    credential:
      ref: { store: env, name: TREND_TIKTOK_TOKEN }
      status: not_provided

  - id: reddit
    kind: byok
    provider: Reddit API (OAuth)
    priority: 3
    enabled: false
    credential:
      ref: { store: env, name: TREND_REDDIT_CLIENT }
      status: not_provided

  - id: linkedin
    kind: byok
    provider: LinkedIn API
    priority: 4
    enabled: false
    credential:
      ref: { store: env, name: TREND_LINKEDIN_TOKEN }
      status: not_provided

  - id: youtube
    kind: byok
    provider: YouTube Data API v3
    priority: 5
    enabled: false
    credential:
      ref: { store: env, name: TREND_YOUTUBE_KEY }
      status: not_provided

  - id: google_trends_rss
    kind: keyless
    provider: Google Trends (RSS diário por país)
    priority: 10
    enabled: true
    endpoint_template: "https://trends.google.com/trending/rss?geo={geo}"

  - id: google_news_rss
    kind: keyless
    provider: Google News (RSS de busca)
    priority: 11
    enabled: true
    endpoint_template: "https://news.google.com/rss/search?q={query}&hl={hl}&gl={geo}&ceid={geo}:{ceid_lang}"

```
