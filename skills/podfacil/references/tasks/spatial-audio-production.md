---
task: Spatial Audio Production
responsavel: "@composer"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - mixed-stereo-audio: Arquivo mixado stereo
  - episode-script: Roteiro com posicionamento espacial
  - target-format: Dolby Atmos, binaural, 360 audio
  - platform: Apple Podcasts (Atmos), Spatial Audio apps
Saida: |
  - atmos-mix: Mix Dolby Atmos (ADM BWF)
  - binaural-mix: Mix binaural para headphones
  - spatial-metadata: Metadata de posicionamento 3D
  - compatibility-check: Validacao downmix stereo
Checklist:
  - "[ ] Setup Logic Pro Dolby Atmos Renderer"
  - "[ ] Posicionar objetos audio em espaco 3D"
  - "[ ] Criar movimento espacial (voz circulando)"
  - "[ ] Adicionar altura (elementos acima/abaixo)"
  - "[ ] Mixar para speakers (7.1.4) e binaural"
  - "[ ] Validar downmix stereo compatibility"
  - "[ ] Exportar ADM BWF (Apple Podcasts Atmos)"
  - "[ ] Validar em AirPods Max/Pro com Spatial Audio"
---

# *spatial-audio-production

Producao de podcast em Dolby Atmos e audio binaural 3D. Posicionamento espacial de vozes, musica e SFX em ambiente imersivo. Suportado por Apple Podcasts (2023+) e apps de spatial audio.

## Uso

```bash
# Producao Dolby Atmos para Apple Podcasts
*spatial-audio-production --episode S02E10 --format atmos --platform apple

# Binaural mix para headphones
*spatial-audio-production --episode S02E10 --format binaural --headphones-only

# Validar compatibility com stereo downmix
*spatial-audio-production --episode S02E10 --check-downmix
```

## Steps (Resumido)

1. **Setup Logic Pro Dolby Atmos**
   - Logic Pro 10.7+ com Dolby Atmos Renderer
   - Configurar bed (7.1.4 speakers) + objects (128 canais)

2. **Posicionamento espacial**
   - Host: Centro frontal (0°, 0m elevation)
   - Guest: 30° esquerda ou direita
   - Musica: Surround bed (envolvente)
   - SFX: Objetos 3D (passaros acima, passos ao lado)

3. **Criar movimento**
   - Automation de pan 3D: Voz circulando ouvinte
   - Elevacao: Elementos acima (helicoptero) ou abaixo (subwoofer)

4. **Mix binaural**
   - Usar Atmos Renderer: Binaural monitoring
   - Testar com AirPods Max/Pro

5. **Validar downmix stereo**
   - Garantir que mix Atmos soa bem em stereo
   - Nao perder inteligibilidade

6. **Export Dolby Atmos ADM BWF**
   - Formato: ADM BWF (Audio Definition Model Broadcast Wave)
   - Upload Apple Podcasts Connect

## Criterios de Qualidade

- [ ] Posicionamento 3D imersivo mas sutil
- [ ] Voz principal sempre inteligivel (centro)
- [ ] Movimento espacial nao marea ouvinte
- [ ] Downmix stereo preserva qualidade
- [ ] Validado em AirPods com Spatial Audio
- [ ] ADM BWF exportado corretamente
