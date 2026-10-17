---
task: Mixing & Mastering
responsavel: "@engineer"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - edited-audio: Arquivos editados multi-track
  - podcast-bible: Guidelines de brand (tom, vibe)
  - target-platforms: Spotify, Apple, YouTube, Amazon
  - loudness-targets: -14 LUFS (Spotify), -16 LUFS (Apple)
Saida: |
  - mixed-audio: Arquivo mixado stereo
  - mastered-audio-spotify: Master otimizado para Spotify (-14 LUFS)
  - mastered-audio-apple: Master otimizado para Apple (-16 LUFS)
  - mastered-audio-youtube: Master otimizado para YouTube (-14 LUFS)
  - loudness-report: Relatorio de loudness por plataforma
Checklist:
  - "[ ] Importar tracks editadas no projeto de mix"
  - "[ ] EQ cada track (clarity, presenca, warmth)"
  - "[ ] Compression para controlar dinamica"
  - "[ ] Panning (se stereo): center host, ligeiramente off-center guest"
  - "[ ] Adicionar vinhetas/musica com automation"
  - "[ ] Mix bus processing (EQ, compression, limiting)"
  - "[ ] Masterizar para Spotify (-14 LUFS, True Peak -1 dBFS)"
  - "[ ] Masterizar para Apple (-16 LUFS, True Peak -1 dBFS)"
  - "[ ] Masterizar para YouTube (-14 LUFS, True Peak -1 dBFS)"
  - "[ ] Validar em multiplos sistemas (fone, speaker, carro)"
---

# *mixing-mastering

> **Nota de distribuição:** via RSS todos os apps recebem o **mesmo** arquivo (um `enclosure` por episódio). O master do feed segue `assets/templates/audio-specs.md` (-16 LUFS integrado, true peak <= -1 dBTP). Masters a -14 LUFS só para destinos com upload próprio (vídeo no YouTube; Spotify apenas se o episódio for hospedado lá).

Mixagem broadcast e mastering multi-plataforma de podcast. Garante clareza, inteligibilidade e loudness otimizado para cada plataforma (Spotify, Apple, YouTube, Amazon). Gera multiplos masters com specs especificas.

## Uso

```bash
# Mix + master standard para todas plataformas
*mixing-mastering --episode S02E03 --platforms "spotify,apple,youtube,amazon"

# Mix com spatial audio (Dolby Atmos)
*mixing-mastering --episode S02E10 --format atmos --platforms "apple"

# Master rapido (apenas loudness matching)
*mixing-mastering --episode S02E05 --fast-track --loudness-only
```

## Steps

1. **Entender specs por plataforma**

   | Plataforma | Loudness Target | True Peak | Dynamic Range | Formato |
   |------------|-----------------|-----------|---------------|---------|
   | **Spotify** | -14 LUFS | -1 dBFS | 6-8 LU | MP3 192kbps, AAC |
   | **Apple Podcasts** | -16 LUFS | -1 dBFS | 8-10 LU | AAC 128kbps |
   | **YouTube** | -14 LUFS | -1 dBFS | 6-8 LU | AAC 128kbps |
   | **Amazon Music** | -14 LUFS | -1 dBFS | 6-8 LU | AAC |
   | **RSS Feed** | -16 LUFS | -1 dBFS | 8-10 LU | MP3 192kbps |

   **Por que targets diferentes?**
   - Apple normaliza para -16 LUFS (mais conservador, preserva dinamica)
   - Spotify normaliza para -14 LUFS (mais loud, competitivo com musica)
   - YouTube idem Spotify

2. **Importar projeto de mix**

   **DAW setup:**
   - Projeto: `S0{N}E0{N}_mix`
   - Tracks:
     - Track 1: Host (edited)
     - Track 2: Guest (edited)
     - Track 3: Vinheta intro
     - Track 4: Vinheta outro
     - Track 5: Music bed (se aplicavel)
     - Track 6: SFX/Transicoes
   - Master bus: Stereo out
   - Sample rate: 48kHz
   - Bit depth: 24bit

3. **EQ cada track (clarity & presence)**

   **Host/Guest tracks (voz):**

   **Low-end cleanup:**
   - High-pass filter: 80-100Hz (remover rumble)
   - Slope: 12-18 dB/octave

   **Warmth (body da voz):**
   - Boost: +2-4 dB @ 200-300Hz
   - Q: 1.0 (wide)
   - Cuidado: Muito boost = muddy

   **Presenca (inteligibilidade):**
   - Boost: +3-6 dB @ 2-4 kHz
   - Q: 1.5 (medium)
   - Resultado: Voz mais clara, "na frente"

   **Air (brilho):**
   - Boost: +2-3 dB @ 10-12 kHz
   - Q: 1.0 (wide)
   - Shelf filter (nao peak)

   **Exemplo de chain EQ:**
   ```
   1. HPF @ 80Hz (rumble)
   2. +3dB @ 250Hz Q=1.0 (warmth)
   3. -2dB @ 500Hz Q=2.0 (cut boxiness)
   4. +4dB @ 3kHz Q=1.5 (presence)
   5. +2dB shelf @ 10kHz (air)
   ```

4. **Compression (controlar dinamica)**

   **Objetivo:** Reduzir diferenca entre partes altas e baixas (mais consistente)

   **Settings para voz:**
   - Ratio: 3:1 a 4:1
   - Threshold: -18 dBFS (ajustar ate ~3-6dB gain reduction)
   - Attack: 10-30ms (rapido, pega transientes)
   - Release: 50-100ms (medio, nao pumping)
   - Knee: Soft (mais natural)
   - Makeup gain: Compensar reducao

   **Test:** Sussurro e grito devem ter volume similar (mas nao identico)

5. **Panning (se stereo)**

   **Mono (recomendado para podcast):**
   - Tudo no centro (host, guest, musica)
   - Maximo compatibility (ouvintes com 1 fone funcionando)

   **Stereo (opcional, para producao elevada):**
   - Host: Centro (0%)
   - Guest: Ligeiramente off-center (15-20% L ou R)
   - Musica: Stereo width completo (100% L/R)
   - SFX: Posicionamento espacial

   **Nota:** Maioria dos podcasts e mono. Stereo so se intencional.

6. **Adicionar vinhetas/musica com automation**

   **Vinheta intro (0:00-0:15):**
   - Volume: 0 dB (full)
   - Fade in: 1s (suave)
   - Quando voz entra: Duck musica para -18 dB (sidechain compression)

   **Music bed (background durante fala):**
   - Volume: -25 a -30 dB (muito baixo, nao compete com voz)
   - EQ: Cortar medios (500Hz-2kHz) para abrir espaco para voz

   **Vinheta outro (final do episodio):**
   - Fade in: 2s (da voz para musica)
   - Volume: 0 dB (full)
   - Fade out: 3s (suave)

   **Automation:**
   - Desenhar curvas de volume no DAW
   - Ou: Usar sidechain compression (musica abaixa automaticamente quando voz ativa)

7. **Mix bus processing (master chain)**

   **Chain no master bus (ordem importa):**

   **1. EQ (subtle):**
   - HPF @ 30Hz (subsonicos inuteis)
   - +1dB shelf @ 10kHz (air no mix completo)

   **2. Multiband compression (opcional):**
   - Controlar dinamica por banda de frequencia
   - Ex: Comprimir lows (200Hz) sem afetar highs
   - Plugin: Fabfilter MB, Waves C6

   **3. Limiter (evitar clipping):**
   - Ceiling: -1 dBFS (True Peak)
   - Lookahead: 5ms
   - Release: Auto
   - Nao exagerar (nao quer brick wall, quer transparente)

8. **Masterizar para Spotify (-14 LUFS)**

   **Objetivo:** Loudness -14 LUFS ± 0.5 LU

   **Workflow:**
   - Medir loudness do mix atual (plugin loudness meter)
   - Se mix esta em -18 LUFS, precisa +4 LU
   - Adicionar gain OU compression/limiting ate -14 LUFS
   - Verificar True Peak nao excede -1 dBFS

   **Chain de mastering:**
   ```
   1. EQ (final tweaks se necessario)
   2. Multiband compressor (controlar dinamica)
   3. Limiter (FabFilter Pro-L2, Waves L2):
      - Ceiling: -1 dBFS True Peak
      - Target: -14 LUFS
      - Dither: POW-r 2 (se exportar 16bit)
   ```

   **Export settings:**
   - Formato: MP3 192kbps CBR + AAC 256kbps
   - Sample rate: 48kHz → 44.1kHz (dither)
   - Bit depth: 24bit → 16bit (dither POW-r 2)
   - Stereo (ou mono se mix mono)
   - Naming: `S02E03_master_spotify.mp3`

9. **Masterizar para Apple Podcasts (-16 LUFS)**

   **Objetivo:** Loudness -16 LUFS ± 0.5 LU (mais conservador)

   **Diferenca:** -2 LU mais baixo que Spotify = mais dinamica preservada

   **Ajustar limiter:**
   - Target: -16 LUFS
   - Ceiling: -1 dBFS True Peak
   - Menos compression que versao Spotify

   **Export settings:**
   - Formato: AAC 128kbps (Apple spec)
   - Sample rate: 44.1kHz
   - Bit depth: 16bit
   - Naming: `S02E03_master_apple.m4a`

10. **Masterizar para YouTube (-14 LUFS)**

    **Specs identicos ao Spotify:**
    - Loudness: -14 LUFS
    - True Peak: -1 dBFS

    **Export settings:**
    - Formato: AAC 128kbps (ou melhor: AAC 256kbps)
    - Sample rate: 48kHz (YouTube prefere 48kHz)
    - Bit depth: 16bit
    - Naming: `S02E03_master_youtube.m4a`

11. **Validar loudness com metering**

    **Plugins de loudness metering:**
    - **Youlean Loudness Meter** (gratis, preciso)
    - **iZotope Insight** (profissional)
    - **Logic Pro:** Built-in loudness meter

    **Validar cada master:**
    ```
    S02E03_master_spotify.mp3:
    - Integrated Loudness: -14.0 LUFS ✅
    - True Peak: -0.8 dBFS ✅
    - Dynamic Range: 7 LU ✅

    S02E03_master_apple.m4a:
    - Integrated Loudness: -16.1 LUFS ✅
    - True Peak: -0.9 dBFS ✅
    - Dynamic Range: 9 LU ✅

    S02E03_master_youtube.m4a:
    - Integrated Loudness: -14.0 LUFS ✅
    - True Peak: -0.7 dBFS ✅
    - Dynamic Range: 7 LU ✅
    ```

12. **Validar em multiplos sistemas (critical)**

    **Playback em:**
    - [ ] Fone profissional (Sony MDR7506, Audio-Technica M50x)
    - [ ] Fone consumer (AirPods, Beats)
    - [ ] Speaker monitor (KRK, Yamaha HS)
    - [ ] Laptop speaker (worst case scenario)
    - [ ] Carro (se possivel)

    **Checar:**
    - Voz inteligivel em todos os sistemas?
    - Musica nao compete com voz?
    - Sibilancia controlada (nao estridente em fone)?
    - Volume consistente do inicio ao fim?

13. **Documentar loudness report**

## Output

### loudness-report-S0{N}E0{N}.md

```markdown
# Loudness Report: S02E03

**Episodio:** S02E03 - IA e Etica com Maria Santos
**Duracao:** 52min
**Engineer:** @engineer
**Data:** 2026-03-17

---

## Master por Plataforma

### Spotify Master

**Arquivo:** `S02E03_master_spotify.mp3`
**Formato:** MP3 192kbps CBR, 44.1kHz, 16bit Stereo

| Metrica | Target | Result | Status |
|---------|--------|--------|--------|
| Integrated Loudness | -14.0 LUFS | -14.1 LUFS | ✅ |
| True Peak | <-1.0 dBFS | -0.8 dBFS | ✅ |
| Loudness Range | 6-8 LU | 7.2 LU | ✅ |
| Dynamic Range | 6-8 dB | 7.5 dB | ✅ |

---

### Apple Podcasts Master

**Arquivo:** `S02E03_master_apple.m4a`
**Formato:** AAC 128kbps, 44.1kHz, 16bit Stereo

| Metrica | Target | Result | Status |
|---------|--------|--------|--------|
| Integrated Loudness | -16.0 LUFS | -16.1 LUFS | ✅ |
| True Peak | <-1.0 dBFS | -0.9 dBFS | ✅ |
| Loudness Range | 8-10 LU | 9.1 LU | ✅ |
| Dynamic Range | 8-10 dB | 9.3 dB | ✅ |

---

### YouTube Master

**Arquivo:** `S02E03_master_youtube.m4a`
**Formato:** AAC 256kbps, 48kHz, 16bit Stereo

| Metrica | Target | Result | Status |
|---------|--------|--------|--------|
| Integrated Loudness | -14.0 LUFS | -14.0 LUFS | ✅ |
| True Peak | <-1.0 dBFS | -0.7 dBFS | ✅ |
| Loudness Range | 6-8 LU | 7.0 LU | ✅ |
| Dynamic Range | 6-8 dB | 7.2 dB | ✅ |

---

### Amazon Music Master

**Arquivo:** `S02E03_master_amazon.m4a`
**Formato:** AAC 192kbps, 44.1kHz, 16bit Stereo

| Metrica | Target | Result | Status |
|---------|--------|--------|--------|
| Integrated Loudness | -14.0 LUFS | -13.9 LUFS | ✅ |
| True Peak | <-1.0 dBFS | -0.8 dBFS | ✅ |

---

## Mix Processing

### Host Track (Channel 1)
- EQ: HPF 80Hz, +3dB @ 250Hz, +4dB @ 3kHz, +2dB shelf 10kHz
- Compression: 3.5:1, -18dB threshold, 4dB GR, 20ms attack, 80ms release
- De-esser: -4dB @ 7kHz

### Guest Track (Channel 2)
- EQ: HPF 80Hz, +2dB @ 250Hz, +5dB @ 3kHz, +2dB shelf 10kHz
- Compression: 4:1, -20dB threshold, 5dB GR, 15ms attack, 70ms release
- De-esser: -5dB @ 7kHz (sibilancia mais pronunciada)
- De-reverb: -8dB (home office reverb)

### Music/Vinhetas
- Vinheta intro: 0dB → duck to -18dB quando voz entra
- Music bed: -28dB constant, EQ cut 500Hz-2kHz
- Vinheta outro: fade in 2s, fade out 3s

---

## Master Bus Processing

1. **EQ (FabFilter Pro-Q3):**
   - HPF @ 30Hz (subsonicos)
   - +1dB shelf @ 10kHz (air)

2. **Multiband Compression (FabFilter Pro-MB):**
   - Low (20-200Hz): 2:1, -2dB GR
   - Mid (200-2kHz): 1.5:1, -1dB GR
   - High (2kHz+): 2:1, -1.5dB GR

3. **Limiter (FabFilter Pro-L2):**
   - Ceiling: -1.0 dBFS True Peak
   - Lookahead: 5ms
   - Style: Transparent (minimal coloration)
   - Dither: POW-r 2 (24bit → 16bit)

---

## Validation Playback

| Sistema | Inteligibilidade | Musica Balance | Sibilancia | Overall |
|---------|------------------|----------------|------------|---------|
| Sony MDR7506 (fone pro) | Excelente | Perfeito | Controlada | 10/10 |
| AirPods (consumer) | Otima | Bom | Controlada | 9/10 |
| MacBook Speaker | Boa | Musica baixa | Ok | 7/10 |
| KRK Rokit 5 (monitor) | Excelente | Perfeito | Controlada | 10/10 |

**Conclusao:** Mix translates bem em todos os sistemas. Laptop speaker e o "worst case", mas ainda inteligivel.

---

## File Deliverables

| Arquivo | Plataforma | Tamanho | Formato |
|---------|------------|---------|---------|
| S02E03_master_spotify.mp3 | Spotify, RSS feed | 72 MB | MP3 192kbps |
| S02E03_master_apple.m4a | Apple Podcasts | 48 MB | AAC 128kbps |
| S02E03_master_youtube.m4a | YouTube | 96 MB | AAC 256kbps |
| S02E03_master_amazon.m4a | Amazon Music | 72 MB | AAC 192kbps |
| S02E03_master_archive.wav | Backup/Archive | 2.1 GB | WAV 48kHz/24bit |

---

## Proximos Passos

- [x] Mastering completo para 4 plataformas
- [x] Loudness validado (dentro de specs)
- [x] Playback validation em multiplos sistemas
- [ ] Upload para distribuidor (Spotify, Apple, etc)
- [ ] Enviar para @distributor

---

**Aprovado por:** @engineer
**Data:** 2026-03-17
**Status:** ✅ Pronto para distribuicao
```

## Criterios de Qualidade

- [ ] Mix com voz clara e inteligivel (presence EQ)
- [ ] Compression controlando dinamica sem pumping
- [ ] Musica/vinhetas nao competem com voz
- [ ] Spotify master: -14 LUFS ± 0.5 LU, True Peak < -1 dBFS
- [ ] Apple master: -16 LUFS ± 0.5 LU, True Peak < -1 dBFS
- [ ] YouTube master: -14 LUFS ± 0.5 LU, True Peak < -1 dBFS
- [ ] Dynamic range preservado (nao brick wall)
- [ ] Sibilancia controlada (de-ess aplicado)
- [ ] Zero clipping ou distorcao
- [ ] Validado em multiplos sistemas (fone, speaker, laptop)
- [ ] Loudness report documentado com todas metricas
- [ ] Multiplos exports gerados (Spotify, Apple, YouTube, Amazon)
- [ ] Arquivo WAV archive salvo (backup lossless)
