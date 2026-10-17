---
task: Audience Analysis
responsavel: "@analyst"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - platform-data: Exports de Apple Podcasts Connect, Spotify for Creators, YouTube Analytics e host
  - owned-data: Newsletter, comunidade, membership (agregados, sem dado pessoal identificável)
  - question: Pergunta de negócio que a análise responde (ex.: "quem é público de membership?")
Saida: |
  - segments: 3-5 segmentos por comportamento, com tamanho e método
  - listener-journey: Funil visita -> 1o episódio -> assinatura -> ativo -> super fã
  - cohort-retention: Retenção 30/60/90 dias por coorte de entrada
  - recommendations: Ações por segmento, cada uma com agente dono
Checklist:
  - "[ ] Pergunta de negócio escrita antes de abrir os dados"
  - "[ ] Métricas de plataformas diferentes analisadas separadamente (definições não batem)"
  - "[ ] Só dados agregados das plataformas — nenhuma inferência individual de atributo sensível (LGPD art. 11)"
  - "[ ] Segmentação por comportamento (frequência, temas, completion), método declarado"
  - "[ ] Funil com taxa de conversão por etapa e denominador"
  - "[ ] Coortes com n por coorte"
  - "[ ] Cada recomendação tem dono e métrica de sucesso"
---

# *analyze-audience

Deep dive em quem ouve, como chega e onde se perde. Responde a uma pergunta de negócio; não é relatório genérico.

## Uso

```bash
*analyze-audience --question "quem é público de membership?" --period Q1-2026
*analyze-audience --cohorts --since 2026-01
```

## Steps

1. **Pergunta:** fixar a decisão que a análise informa e quem decide.
2. **Coleta:** exports das plataformas + canais próprios. Registrar a definição de cada métrica (ex.: o que cada plataforma conta como "play").
3. **Segmentação comportamental:** clustering (ex.: K-means) ou regras simples sobre frequência, temas e completion. Declarar método, k e tamanho de cada segmento.
4. **Funil e coortes:** conversão por etapa; retenção 30/60/90 dias por coorte de entrada.
5. **Sinais qualitativos (opcional):** temas e sentimento em reviews e comentários (topic modeling / classificação por LLM), sempre com amostra e taxa de erro conhecida.
6. **Recomendações:** por segmento, com dono (Amp, Deal, Scout, Link) e métrica de validação.

## Criterios de Qualidade

- [ ] Toda porcentagem com denominador
- [ ] Método de segmentação reprodutível
- [ ] Hipóteses marcadas como hipóteses, não como causa
