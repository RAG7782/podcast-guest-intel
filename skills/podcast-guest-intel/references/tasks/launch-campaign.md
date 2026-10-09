---
task: Launch Campaign
responsavel: "@growth"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - episode-info: Episodio a ser lancado (especial, season premiere)
  - target-metrics: Downloads, reach, engagement
  - budget: Budget de marketing (ads, influencers)
  - channels: Email, social, cross-promo, press
Saida: |
  - campaign-plan: Plano de campanha completo (2 semanas)
  - creative-assets: Trailers, clips, posts
  - email-blast: Email para subscribers
  - press-kit: Press kit para midia
Checklist:
  - "[ ] Trailer lancado 2 semanas antes"
  - "[ ] Teaser clips (audiogram) 10 dias antes"
  - "[ ] Countdown social 7-3-1 dias antes"
  - "[ ] Email blast 3 dias antes"
  - "[ ] Cross-promo ativada (podcast swaps)"
  - "[ ] Press kit enviado para midia"
  - "[ ] Listening party (Discord/Twitter Space)"
  - "[ ] Post-launch: Social flood (clips)"
---

# *launch-campaign

Campanha de lancamento completa para episodio especial ou season premiere. Timeline de 2 semanas com trailer, teasers, countdown, email blast, cross-promo, press kit, listening party.

## Uso

```bash
# Campanha de lancamento season premiere
*launch-campaign --episode S02E01 --type season-premiere --duration 14-days

# Campanha express (1 semana)
*launch-campaign --episode S02E08 --type special-guest --duration 7-days

# Post-launch amplification
*launch-campaign --episode S02E03 --phase post-launch --clips 5
```

## Steps (Resumido)

**T-14 dias: Trailer**
- Trailer cinematico (60s)
- Upload YouTube, Instagram, feed

**T-10 dias: Teaser #1**
- Audiogram com quote viral
- Instagram/Twitter/LinkedIn

**T-7 dias: Teaser #2**
- Clip vertical (30s)
- Reels/TikTok/Shorts

**T-3 dias: Email blast**
- Subject: "[Estreia] {Titulo}"
- Subscribers list

**T-1 dia: Countdown**
- Stories countdown sticker
- Twitter/Instagram posts

**Dia 0: LANCAMENTO**
- Episodio publicado 6am
- Listening party (Discord) 8pm
- Social flood (3 posts)

**Pos-lancamento:**
- 5 clips virais ao longo da semana
- Thank you email
- Pedir reviews

## Criterios de Qualidade

- [ ] Trailer lancado T-14 dias
- [ ] 2 teasers antes do lancamento
- [ ] Email blast T-3 dias
- [ ] Listening party agendado
- [ ] Cross-promo ativada
- [ ] Press kit enviado
- [ ] 5 clips pos-lancamento
- [ ] Reviews solicitados
