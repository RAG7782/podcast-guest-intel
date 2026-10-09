# Checklist: Quality Audio

**Quando usar:** Validacao tecnica do audio final (antes de publicar)

**Owner:** @engineer

## Loudness (LUFS - Loudness Units relative to Full Scale)

- [ ] **Spotify:** -14 LUFS (±1 LU)
  - Spotify normaliza para -14 LUFS
  - Se muito alto: comprimido (perde dinamica)
  - Se muito baixo: listener aumenta volume (experiencia ruim)
- [ ] **Apple Podcasts:** -16 LUFS (±1 LU)
  - Apple e mais conservador
  - Episodios mais "quietos" que Spotify
- [ ] **YouTube:** -14 LUFS (±1 LU)
  - Mesma spec do Spotify
  - Videos muito altos sao penalizados (menos views)
- [ ] **Amazon Music:** -14 LUFS (±1 LU)
  - Segue padrao Spotify

**Como medir:** Usar plugin de loudness meter (ex: Youlean Loudness Meter, iZotope Insight)

**Dica:** Se publicar em multiplas plataformas, masterizar para -16 LUFS (Apple). Spotify vai subir um pouco, mas prefere isso a compressao excessiva.

## True Peak

- [ ] **Max -1 dB True Peak** (ideal: -1.5 dB)
  - True peak e o pico REAL do sinal (nao apenas sample peak)
  - Garante que nenhuma plataforma trunca o audio
  - Se clipar: distorcao horrivel

**Como verificar:** Usar true peak limiter (ex: FabFilter Pro-L2, Ozone Maximizer)

## Noise Floor

- [ ] **Abaixo de -60 dBFS** durante silêncios
  - Noise floor = ruido de fundo constante
  - Se acima de -60 dB: sinal de AC, computador, geladeira audivel
  - Idealmente: -70 dBFS ou melhor

**Como medir:** Selecionar secao de silencio (entre falas), ver nivel RMS

**Como corrigir:** Noise reduction plugin (ex: iZotope RX, Audacity Noise Reduction)

## Frequencias

- [ ] **Voz clara e presente** (2-5 kHz e a faixa de inteligibilidade)
  - Boostar levemente: 2-4 kHz (claridade)
  - Reduzir: 200-400 Hz se voz "muddy"
- [ ] **Sem picos excessivos:**
  - Sem sibilancia (6-8 kHz): usar de-esser se necessario
  - Sem harshness (4-6 kHz): reduzir se dolorido nos ouvidos
- [ ] **Baixas frequencias controladas:**
  - High-pass filter em 80-100 Hz (remove rumble de AC, handling noise)
  - Nao remover TODAS as baixas (voz fica fina)
- [ ] **Nenhum peak extremo** (verificar em spectrum analyzer)

**Como verificar:** Usar EQ visual (ex: FabFilter Pro-Q3, Waves Q10)

## Edicao

- [ ] **Sem cortes audiveis:**
  - Transicoes suaves (usar fade in/out de 10-50ms)
  - Nao cortar no meio de respiracao (soa robotico)
- [ ] **Transicoes naturais:**
  - Entre blocos/topicos: usar fade out + fade in
  - Evitar cortes abruptos (jarring)
- [ ] **Sem clicks/pops:**
  - Clicks = cortes mal feitos (zero-crossing nao respeitado)
  - Pops = plosivas nao tratadas (p, b, t)
  - **Como corrigir:** De-clicker plugin ou editar manualmente (zoom in, fade)
- [ ] **Respiracoes controladas:**
  - Reduzir volume de respiracoes (nao remover todas)
  - Manter naturalidade (host e humano, nao robo)

## Vinheta (Intro/Outro/Transicoes)

- [ ] **Volume consistente com conteudo:**
  - Vinheta nao deve ser MUITO mais alta que voz
  - Ou MUITO mais baixa (listener nao percebe)
  - Diferenca ideal: -3 a -6 dB vs. voz
- [ ] **Transicao suave:**
  - Fade in no inicio da vinheta (nao comecar abrupto)
  - Fade out no final (ou duck quando voz entra)
- [ ] **Ducking (se vinheta rola sob a voz):**
  - Reduzir volume da musica quando host fala
  - -15 a -20 dB abaixo da voz

## Stereo & Fase

- [ ] **Mono-compatible:**
  - Testar em mono (alguns devices/plataformas fazem downmix)
  - Se cancelamento de fase: voz some ou fica "hollow"
  - **Como testar:** Ativar mono no DAW e ouvir
- [ ] **Sem problemas de fase:**
  - Usar correlation meter (deve ficar entre +0.5 e +1.0)
  - Se abaixo de 0: problema de fase grave
- [ ] **Stereo width adequado:**
  - Voz: centro (mono ou narrow stereo)
  - Musica/vinheta: pode ser stereo wide
  - Nao exagerar no widening (causa problemas em mono)

## Listening Test

- [ ] **Headphones de referencia:**
  - Ouvir em fones de qualidade (ex: Audio-Technica M50x, Sony MDR-7506)
  - Verificar: claridade, balance, sem artifacts
- [ ] **Speaker de celular:**
  - Maioria dos listeners ouve assim
  - Voz deve ser inteligivel mesmo em speaker pequeno
  - Se "muddy" ou "thin": ajustar EQ
- [ ] **Car audio:**
  - Ambiente ruidoso (motor, rua)
  - Voz deve se destacar sobre ruido
  - Testar em volume medio (nao muito alto)
- [ ] **Smart speaker (Alexa, Google Home):**
  - Se audiencia usa muito
  - Testar: "Alexa, toca meu podcast" e ouvir

## Dinamica

- [ ] **Nao over-compressed:**
  - Compressao excessiva = voz cansativa, sem respiracao
  - Usar compression moderado: ratio 3:1 a 4:1
- [ ] **Nao muito dinamico:**
  - Se whisper + grito no mesmo episodio: aplicar compression/limiting
  - Listener nao deve ajustar volume constantemente
- [ ] **Consistent levels entre speakers:**
  - Se entrevista: host e guest no mesmo volume (±2 dB)
  - Se desbalanceado: listener favorece um speaker

## Export Settings

- [ ] **Formato final:**
  - WAV: 48kHz, 24-bit (master)
  - MP3: 320kbps, 44.1kHz (para hosting)
  - AAC: 256kbps (para YouTube, se aplicavel)
- [ ] **Metadata no MP3:**
  - ID3 tags: titulo, artist, album, track number
  - Artwork embedded (3000x3000px)
  - Chapters (se suportado)

## Final Check

- [ ] Ouvir episodio COMPLETO (nao apenas samples)
- [ ] Verificar: NENHUM artifact (clicks, pops, distorcao)
- [ ] Verificar: levels consistentes do inicio ao fim
- [ ] Verificar: vinhetas no lugar certo
- [ ] Comparar com episodio anterior (consistency)
- [ ] Se ALGO parecer errado: investigar e corrigir (nao publicar "quase bom")

---

**Tools Recomendados:**
- **Loudness Meter:** Youlean Loudness Meter (gratis), iZotope Insight
- **True Peak Limiter:** FabFilter Pro-L2, Ozone Maximizer
- **Noise Reduction:** iZotope RX, Audacity Noise Reduction
- **EQ:** FabFilter Pro-Q3, Waves Q10
- **De-esser:** Waves DeEsser, FabFilter Pro-DS
- **Compression:** Waves CLA-2A, FabFilter Pro-C2
- **Spectrum Analyzer:** Voxengo SPAN (gratis), FabFilter Pro-Q3

---

**Assinatura do Audio Engineer:** _______________
**Data:** _______________
**Episodio:** S___E___
