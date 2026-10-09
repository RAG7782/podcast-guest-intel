# Audio Specs
## Especificacoes Tecnicas de Audio

---

## GRAVACAO

### Formato de Gravacao

**Arquivo Master:**
- **Formato:** WAV (uncompressed)
- **Sample Rate:** 48kHz
- **Bit Depth:** 24-bit
- **Canais:** Mono por track (gravar cada speaker em track separado)

**Por que:**
- WAV preserva qualidade maxima para edicao
- 48kHz e standard para video (caso queira fazer video depois)
- 24-bit da headroom para edicao sem degradacao
- Mono por track permite controle individual de cada voz

---

### Setup de Gravacao

**Local (In-Person):**
- Microfone: {Modelo recomendado: Shure SM7B, Rode PodMic, Blue Yeti}
- Interface: {Modelo: Focusrite Scarlett, PreSonus, etc}
- DAW: Audacity, Adobe Audition, Reaper
- Headphones: Closed-back (evita bleed)

**Remoto:**
- Plataforma: Riverside.fm, Squadcast, Zencastr (grava local, nao comprimido)
- Backup: Zoom audio-only (comprimido, mas e backup)
- Mic do convidado: Orientar usar fone com mic se possivel

---

### Naming Convention (Arquivos de Gravacao)

```
S{season}E{episode}_{tipo}_{speaker}_{versao}.wav

Exemplos:
S03E15_raw_host.wav
S03E15_raw_guest1.wav
S03E15_raw_guest2.wav
S03E15_backup_zoom.wav
```

**Tipos:**
- `raw` = Gravacao original sem edicao
- `backup` = Gravacao de backup
- `edit` = Versao editada
- `master` = Versao final masterizada

---

## EDICAO

### Niveis de Audio (Durante Edicao)

**Objetivo:**
- Voz principal (host/guest): -6dB a -3dB (peak)
- Deixar headroom de 6dB para masterizacao

**Processo:**
1. Normalizar cada track individualmente
2. Balancear volume entre speakers (usar compressao se necessario)
3. Aplicar EQ basico (tirar lows abaixo de 80Hz, realcar presenca em 2-5kHz)
4. Remover ruidos (Noise Reduction plugin)

---

### Limpeza de Audio

**Remover:**
- ✅ Cliques de boca (Mouth clicks) - uso moderado de de-clicker
- ✅ Respiracoes ruidosas (manual ou plugin de breath control)
- ✅ Background noise (Noise Reduction em -6dB a -10dB)
- ✅ Pops (Pop filter durante gravacao + de-esser na edicao)
- ✅ Silencios longos (>3 segundos)

**Manter:**
- ❌ Pequenas imperfeicoes naturais (autenticidade)
- ❌ Respiracao normal (nao ruidosa)
- ❌ Pausas naturais de pensamento (<2 segundos)

**Plugins Recomendados:**
- **Noise Reduction:** Audacity Noise Reduction, iZotope RX
- **De-esser:** Waves DeEsser, FabFilter Pro-DS
- **Compressor:** Waves C1, FabFilter Pro-C
- **EQ:** FabFilter Pro-Q, Waves REQ

---

### Trilha de Fundo e Musica

**Vinheta:**
- Duracao: 10-15 segundos
- Volume: -20dB abaixo da voz (quando voz esta presente)
- Volume: 0dB (quando so musica, no inicio/fim)
- Fade in: 0.5s
- Fade out: 1s

**Trilha de Fundo (se usar):**
- Volume: -25dB a -30dB abaixo da voz (quase imperceptivel)
- Remover durante momentos emocionais/serios (deixar voz "respirar")
- Fade in/out suave (1-2s)

**Transicoes:**
- Entre blocos: 0.5-1s de musica ou SFX
- Volume da transicao: -15dB abaixo da voz
- Nao usar transicao se fluxo da conversa e natural

---

## MASTERIZACAO

### LUFS Compliance por Plataforma

**LUFS = Loudness Units relative to Full Scale (padrao de loudness)**

| Plataforma | LUFS Alvo | True Peak | Tolerancia |
|------------|-----------|-----------|------------|
| **Spotify** | -14 LUFS | -1 dBTP | ±1 LUFS |
| **Apple Podcasts** | -16 LUFS | -1 dBTP | ±1 LUFS |
| **YouTube** | -14 LUFS | -1 dBTP | ±1 LUFS |
| **Amazon Music** | -14 LUFS | -2 dBTP | ±1 LUFS |
| **Google Podcasts** | -16 LUFS | -1 dBTP | ±1 LUFS |

**Recomendacao geral:** Masterizar para -16 LUFS (Apple Podcasts e Google). Spotify e YouTube vao normalizaco automaticamente.

---

### Como Medir LUFS

**Ferramentas:**
- Youlean Loudness Meter (plugin gratuito)
- iZotope Insight
- Audacity: Analyze > Loudness Normalization

**Processo:**
1. Aplicar LUFS normalization para -16 LUFS (integrated)
2. Checar True Peak (nao deve ultrapassar -1 dBTP)
3. Se True Peak estiver acima de -1dB, aplicar limiter

---

### True Peak

**O que e:**
Pico real do audio incluindo intersample peaks.

**Por que importa:**
Evita clipping/distorcao ao converter formatos.

**Meta:** Abaixo de -1 dBTP (alguns preferem -2 dBTP para ser ultra-safe)

---

### Formato Final (Master)

**Arquivo para Distribuicao:**
- **Formato:** MP3
- **Bitrate:** 192 kbps (minimo), 320 kbps (recomendado)
- **Sample Rate:** 44.1kHz (standard para audio)
- **Canais:** Stereo (mesmo se gravado mono)
- **Metadata:** ID3v2.4
  - Titulo do Episodio
  - Artista: {Nome do Podcast}
  - Album: {Nome do Podcast}
  - Ano: {YYYY}
  - Genre: Podcast
  - Cover Art: 3000x3000px (embedado)
  - Chapter Markers (se suportado)

---

### Naming Convention (Master Final)

```
S{season}E{episode}_{titulo-slug}_master_v{version}.mp3

Exemplo:
S03E15_como-escalar-sem-vc_master_v1.mp3
```

**Versoes:**
- v1 = Primeira versao masterizada
- v2 = Correcao ou re-master

---

## SPATIAL AUDIO (Opcional/Avancado)

**Para plataformas que suportam (Apple Music, Tidal):**

**Dolby Atmos:**
- Formato: 7.1.4 (7 canais base, 1 LFE, 4 height)
- Binaural Stereo Fold-Down: Para headphones

**Processo:**
1. Master em stereo normal primeiro
2. Usar Dolby Atmos Production Suite
3. Posicionar vozes no espaco 3D
4. Exportar em Dolby Atmos + Binaural Stereo

**Nota:** So faz sentido se podcast tiver producao complexa (multiplos speakers, sound design elaborado). Para conversas simples, stereo normal e suficiente.

---

## BACKUP E ARQUIVAMENTO

### O Que Salvar

**Essencial (3 copias - regra 3-2-1):**
- Raw audio (WAV originais de cada speaker)
- Projeto de edicao (Audacity .aup, Audition .sesx, etc)
- Master final (MP3)

**Recomendado:**
- Versoes intermediarias de edicao
- Backup da gravacao (Zoom, Riverside)
- Transcript

---

### Onde Salvar

**Local:**
- HD Externo 1: `Podcasts/S{season}/E{episode}/`

**Cloud 1:**
- Google Drive: `Podcast Production/Episodes/S{season}/E{episode}/`

**Cloud 2:**
- Dropbox/Backblaze/AWS S3: Backup automatico

**Naming da Pasta:**
```
S{season}/E{episode}_{slug}/
├── raw/
│   ├── S{X}E{XX}_raw_host.wav
│   ├── S{X}E{XX}_raw_guest.wav
│   └── S{X}E{XX}_backup_zoom.wav
├── project/
│   └── S{X}E{XX}_edit.aup3
├── master/
│   └── S{X}E{XX}_{slug}_master_v1.mp3
└── assets/
    ├── cover-art.png
    └── show-notes.md
```

---

## CHECKLIST DE QUALIDADE DE AUDIO

### Pre-Gravacao

- [ ] Teste de som 15 min antes
- [ ] Niveis de input: -12dB a -6dB (falando normal)
- [ ] Headroom adequado (nao clipping)
- [ ] Background noise minimo (<-50dB)
- [ ] Backup recording ligado

---

### Pos-Gravacao

- [ ] Audio de cada speaker gravado separadamente
- [ ] Backup salvo em local diferente
- [ ] Naming convention seguida
- [ ] Audio nao esta clipado (sem red peaks)

---

### Pos-Edicao

- [ ] Noise reduction aplicado (se necessario)
- [ ] Volume balanceado entre speakers
- [ ] Respiracoes ruidosas removidas
- [ ] Silencios longos cortados
- [ ] Trilha de fundo em -25dB (se usar)
- [ ] Transicoes suaves

---

### Pos-Masterizacao

- [ ] LUFS medido: -16 LUFS ±1
- [ ] True Peak medido: <-1 dBTP
- [ ] Escutado em 3 dispositivos: Fone, Carro, Caixa
- [ ] Nenhum clipping ou distorcao
- [ ] Chapter markers inseridos (se aplicavel)
- [ ] Metadata completa (titulo, artista, cover art)
- [ ] Formato final: MP3 192kbps ou 320kbps

---

## TROUBLESHOOTING COMUM

### Problema 1: Voz Muito Baixa

**Sintoma:** Voz esta em -20dB ou abaixo
**Solucao:**
1. Normalizar para -6dB (peak)
2. Aplicar compressao (ratio 3:1, threshold -10dB)
3. Checar LUFS apos compressao

---

### Problema 2: Clipping

**Sintoma:** Audio distorcido, peaks em 0dB ou acima
**Solucao:**
- **Se nao gravou ainda:** Diminuir gain do mic
- **Se ja gravou:** Tentar recuperar com de-clipper (iZotope RX)
- **Se nao recuperar:** Re-gravar (se possivel) ou avisar que audio tem limitacoes

---

### Problema 3: Background Noise

**Sintoma:** Hiss, hum, ruido de fundo constante
**Solucao:**
1. Capturar "noise profile" (2 segundos de silencio com so o ruido)
2. Aplicar Noise Reduction (Audacity: -6dB a -10dB)
3. Se ruido e muito alto: Avisar convidado para mudar ambiente

---

### Problema 4: Eco/Reverb

**Sintoma:** Voz soa "em uma caverna"
**Solucao:**
- **Prevencao:** Gravar em sala com cortinas, tapetes, moveis (absorvem som)
- **Correcao:** Plugin de de-reverb (iZotope RX, Waves Clarity Vx)
- **Se muito grave:** Pedir pra regravar

---

### Problema 5: Voz Muito "Fina" ou "Grossa"

**Sintoma:** Falta de corpo ou excesso de graves
**Solucao:**
- EQ:
  - **Voz fina:** Boost em 200-400 Hz (+3dB)
  - **Voz grossa:** Cut em 200-400 Hz (-3dB)
  - Sempre realcar presenca em 2-5 kHz (+2dB)

---

## FERRAMENTAS RECOMENDADAS

### Gratuitas

**DAW:**
- Audacity (Windows, Mac, Linux)
- Reaper (Trial gratuito, $60 licenca)
- GarageBand (Mac, iOS)

**Plugins:**
- Youlean Loudness Meter (LUFS)
- iZotope RX Elements (Noise reduction)
- Waves (versoes gratuitas em promos)

---

### Pagas (Profissionais)

**DAW:**
- Adobe Audition ($20/mes)
- Logic Pro ($200 one-time, Mac only)
- Reaper ($60 licenca)

**Plugins:**
- iZotope RX Suite ($1200 - gold standard para limpeza)
- Waves Bundles ($200-$500)
- FabFilter Pro-Q/Pro-C ($200 cada)

**Plataformas de Gravacao Remota:**
- Riverside.fm ($20/mes)
- Squadcast ($20/mes)
- Zencastr ($20/mes)

---

## TEMPLATES DE CONFIGURACAO

### Audacity (Gratuito)

**Noise Reduction:**
1. Selecionar 2s de ruido de fundo
2. Effect > Noise Reduction > Get Noise Profile
3. Selecionar audio inteiro
4. Effect > Noise Reduction > OK (Reduction: 6-10dB, Sensitivity: 6)

**Normalizacao:**
1. Selecionar audio inteiro
2. Effect > Loudness Normalization
3. Integrated LUFS: -16
4. OK

**Export:**
1. File > Export > Export Audio
2. Format: MP3 Files
3. Bit Rate Mode: Constant
4. Quality: 192 kbps ou 320 kbps

---

### Adobe Audition (Pago)

**Noise Reduction:**
1. Effects > Noise Reduction/Restoration > Capture Noise Print
2. Selecionar audio inteiro
3. Effects > Noise Reduction/Restoration > Noise Reduction (Process)
4. Reduction: 60-80%

**Match Loudness:**
1. Effects > Amplitude and Compression > Match Loudness
2. ITU-R BS.1770-3 Loudness
3. Target Loudness: -16 LUFS
4. Tolerance: 0.5 LU

**Export:**
1. File > Export > Multitrack Mixdown > Entire Session
2. Format: MP3
3. Bitrate: 320 kbps

---

## GLOSSARIO DE TERMOS

| Termo | Definicao |
|-------|-----------|
| **LUFS** | Loudness Units Full Scale - padrao de medicao de loudness |
| **True Peak** | Pico real incluindo intersample peaks |
| **dBFS** | Decibeis Full Scale - 0dB e maximo digital |
| **Sample Rate** | Numero de samples por segundo (Hz) |
| **Bit Depth** | Numero de bits por sample (mais bits = mais resolucao) |
| **Headroom** | Espaco entre peak e 0dB (evita clipping) |
| **Compression** | Reduz dinamica (diferenca entre loud e quiet) |
| **EQ** | Equalizacao - ajusta frequencias |
| **Noise Floor** | Nivel de ruido de fundo |
| **Clipping** | Distorcao quando audio excede 0dB |

---

**Versao:** 1.0
**Responsavel:** @engineer
**Aprovado por:** @producer
**Data:** {YYYY-MM-DD}
**Proxima revisao:** Anual

---

*Audio de qualidade nao e acidente. E resultado de specs claras e processo consistente.*
