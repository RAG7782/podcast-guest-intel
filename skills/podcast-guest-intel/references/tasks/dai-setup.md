---
task: Dynamic Ad Insertion Setup
responsavel: "@monetizer"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - podcast-hosting: Plataforma de hospedagem (Megaphone, Art19, Libsyn)
  - ad-inventory: Spots disponiveis (pre-roll, mid-roll, post-roll)
  - targeting-criteria: Geo, demo, device
  - sponsor-contracts: Contratos com anunciantes
Saida: |
  - dai-config: Configuracao de DAI na plataforma
  - ad-spots-defined: Pre-roll, mid-roll, post-roll configurados
  - targeting-rules: Regras de targeting por episodio
  - revenue-projection: Projecao de revenue baseada em CPM
Checklist:
  - "[ ] Escolher plataforma DAI (Megaphone, Art19, Libsyn)"
  - "[ ] Definir ad spots (pre-roll 0:00, mid-roll 50%, post-roll final)"
  - "[ ] Configurar host-read vs programmatic"
  - "[ ] Setup targeting (geo, demo, device)"
  - "[ ] Integrar com ad networks (Spotify Ad Studio, AdvertiseCast)"
  - "[ ] Monetizar back-catalog (episodios antigos)"
  - "[ ] Configurar frequency capping (nao repetir muito)"
  - "[ ] Trackear impressoes e revenue"
---

# *dai-setup

Configuracao de Dynamic Ad Insertion para monetizacao do podcast. Pre-roll, mid-roll, post-roll com targeting geografico/demografico. Back-catalog monetization.

## Uso

```bash
# Setup DAI completo
*dai-setup --platform megaphone --spots "pre,mid,post" --targeting geo

# Monetizar back-catalog
*dai-setup --enable-back-catalog --episodes "S01E01-S01E12"

# Configurar host-read spots
*dai-setup --episode S02E03 --host-read --mid-roll-timestamp "25:00"
```

## Steps (Resumido)

1. **Escolher plataforma DAI**
   - Megaphone (enterprise)
   - Art19 (mid-tier)
   - Libsyn Ads (budget)

2. **Definir ad spots**
   - Pre-roll: 0:00 (15-30s)
   - Mid-roll: 50% do episodio (60s)
   - Post-roll: Final (15-30s)

3. **Host-read vs Programmatic**
   - Host-read: Gravado pelo host (mais authentico, CPM alto)
   - Programmatic: Inserido automaticamente (escalavel, CPM baixo)

4. **Targeting**
   - Geo: US, Brasil, UK
   - Demo: 25-45 anos, tech workers
   - Device: Mobile vs desktop

5. **Integrar ad networks**
   - Spotify Ad Studio
   - AdvertiseCast
   - Podcorn

6. **Back-catalog monetization**
   - Inserir ads em episodios antigos
   - Revenue passivo

7. **Frequency capping**
   - Nao mostrar mesmo ad >2x por usuario

8. **Trackear revenue**
   - CPM: $18-$25 (US average)
   - Impressoes por episodio
   - Revenue mensal

## Criterios de Qualidade

- [ ] Ad spots configurados (pre, mid, post)
- [ ] Targeting definido (geo, demo)
- [ ] Host-read spots gravados profissionalmente
- [ ] Back-catalog monetizado
- [ ] Frequency capping configurado
- [ ] Revenue tracking funcionando
- [ ] CPM >$18 (benchmark US)
