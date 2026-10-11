## approach-modes.yaml

```yaml
# Pacote local: só o modo grátis. Os 7 modos vêm pela tool `roteiro_modos` do MCP (plano pago).
# Registro extensível de modos de abordagem (cada entrada valida contra approach-mode.schema.json).
# Adicionar modo = 1 entrada. `extends` herda defaults de outro modo (resolvido em scripts/roteiro_tools.py).
# beats/depth/counterpoint_block moldam o roteiro (F5); o roteiro se guia pelas flags, nunca pelo id.
# Modo é ortogonal ao formato (config/formats.yaml do squad).
version: 1
modes:
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
