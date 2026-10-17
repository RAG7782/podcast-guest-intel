---
task: Audio Editing
responsavel: "@engineer"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - raw-audio-files: Arquivos multi-track da gravacao
  - session-notes: Notas do engineer com timestamps
  - editing-style: Minimal, standard, heavy (conforme podcast-bible)
  - duration-target: Duracao final desejada
Saida: |
  - edited-audio: Arquivo editado pre-mixagem
  - edit-decision-list: Log de todos os cortes/ajustes
  - removed-content: Arquivo com trechos cortados (backup)
  - quality-report: Relatorio de qualidade pos-edicao
Checklist:
  - "[ ] Importar multi-track no DAW e sincronizar"
  - "[ ] Remover erros tecnicos (ruidos, clipping, pops)"
  - "[ ] Cortar fillers excessivos (ahh, umm, tipo, sabe)"
  - "[ ] Ajustar pacing (pausas longas, repeticoes)"
  - "[ ] Noise reduction com iZotope RX ou similar"
  - "[ ] De-ess (controlar sibilancia)"
  - "[ ] De-reverb (se gravacao com eco)"
  - "[ ] Filler word removal via Descript (opcional)"
  - "[ ] Nivelamento de volume entre participantes"
  - "[ ] Exportar versao editada para mixagem"
---

# *audio-editing

Edicao tecnica completa de audio de podcast: cortes, limpeza de ruidos, nivelamento, pacing adjustments. Transforma gravacao raw em conteudo polido pronto para mixagem/mastering.

## Uso

```bash
# Edicao standard de entrevista
*audio-editing --episode S02E03 --style standard --tracks 2

# Edicao heavy (narrativo com muito cleanup)
*audio-editing --episode S02E10 --style heavy --noise-reduction high

# Edicao minimal (conversacional natural)
*audio-editing --episode S02E05 --style minimal --preserve-natural-flow
```

## Steps

1. **Importar e sincronizar multi-track**

   **DAW setup:**
   - Criar projeto: `S0{N}E0{N}_editing`
   - Import tracks:
     - Track 1: Host audio
     - Track 2: Guest audio
     - Track 3: Music bed (se aplicavel)
     - Track 4: SFX/Vinhetas
   - Sample rate: 48kHz
   - Bit depth: 24bit

   **Sincronizacao:**
   - Se gravacao remota (Riverside/Zencastr): Ja vem sincronizado
   - Se dual recording local: Alinhar pela forma de onda
   - Validar: Momentos onde ambos falam devem bater perfeitamente
   - Marcar sync point no inicio (bater palma ou countdown)

2. **Primeira passagem: Identificar problemas tecnicos**

   **Ouvir episodio completo (1x speed) e marcar:**
   - Clipping (distorcao)
   - Pops/clicks (cabo, mic)
   - Ruido de fundo (AC, trafego, cachorro)
   - Sibilancia excessiva (S, T, P)
   - Reverb/eco
   - Volume inconsistente
   - Pausas muito longas

   **Usar markers no DAW:**
   - M = Problema tecnico (ruido, clipping)
   - C = Cortar (erro do host, "corta isso")
   - G = Gold (momento incrivel para clip)

3. **Remover erros tecnicos criticos**

   **Clipping:**
   - Identificar regioes clippadas (forma de onda cortada no topo)
   - iZotope RX: De-Clip module
   - Se muito severo: Usar backup recording

   **Pops/Clicks:**
   - iZotope RX: De-Click module
   - Threshold: Ajustar ate remover sem afetar voz
   - Manual: Zoom in, desenhar curva suave sobre o pop

   **Ground loop hum (60Hz):**
   - EQ parametrico: Notch filter em 60Hz + harmonicos (120Hz, 180Hz)
   - Q factor: 10-20 (muito estreito)

4. **Noise reduction (ruido de fundo)**

   **iZotope RX (industry standard):**
   - Selecionar trecho de room tone (5s so ruido)
   - Voice De-noise module: Learn noise profile
   - Apply to full track
   - Threshold: 6-12 dB reduction (nao exagerar, fica robotico)

   **Alternativas gratuitas:**
   - Reaper: ReaFIR (FFT noise reduction)
   - Audacity: Noise Reduction tool

   **Quando usar:**
   - Ruido constante (AC, computador, geladeira)
   - NAO usar para: Ruidos intermitentes (cachorro, carro passando) → cortar manualmente

5. **De-ess (controlar sibilancia)**

   **Problema:** Sons "S", "T", "P" muito estridentes (6-10kHz)

   **Solucao:**
   - Plugin de-esser (FabFilter DS, Waves DeEsser, Logic DeEsser)
   - Frequency range: 6-10kHz
   - Threshold: Ajustar ate sibilantes ficarem controladas (nao eliminadas)
   - Reduction: 3-6 dB

   **Test:** Ouvir frase com muito S ("Sistemas inteligentes") antes/depois

6. **De-reverb (remover eco)**

   **Problema:** Gravacao em sala com paredes lisas, sem tratamento

   **Solucao:**
   - iZotope RX: De-reverb module
   - Reduction: 6-10 dB (comecar conservador)
   - Preview: Ouvir residual (o que esta sendo removido)
   - Se soar artificial: Reduzir amount

   **Alternativa:** Usar EQ para minimizar frequencias de reverb (200-500Hz)

7. **Cortar fillers e ajustar pacing**

   **Definir editing style (conforme podcast-bible):**

   **MINIMAL (conversacional natural):**
   - Cortar apenas: Erros tecnicos, "corta isso", pausas >5s
   - Manter: Fillers naturais (ahh, umm ocasionais), pausas de pensamento
   - Objetivo: Soar 95% raw, apenas remover fricao tecnica

   **STANDARD (profissional polido):**
   - Cortar: Fillers excessivos (>3 por minuto), pausas >3s, gagueiras, repeticoes
   - Manter: Fillers ocasionais (humaniza), pausas naturais de 1-2s
   - Objetivo: Soar natural mas polido, sem obviamente editado

   **HEAVY (narrativo producao elevada):**
   - Cortar: Todos fillers, todas pausas >1s, respiracoes audveis, clicks de boca
   - Manter: Apenas conteudo essencial, fluxo perfeito
   - Objetivo: Producao de radio/audiobook, zero imperfeicoes

   **Ferramentas:**
   - Manual: Ouvir 1.5x speed, cortar com Cmd+T (split) + Delete
   - Automatizado: Descript (AI remove fillers), Adobe Podcast Enhance
   - Hybrid: Descript para primeira passada, manual para refinamento

8. **Filler word removal via Descript (opcional)**

   **Workflow:**
   - Upload audio no Descript
   - Transcricao automatica
   - Marcar fillers (ahh, umm, tipo, sabe, ne) → Delete
   - Descript corta audio automaticamente
   - Export audio editado
   - Revisar no DAW (Descript pode cortar demais)

   **Quando usar:**
   - Episodios >60min (economiza tempo)
   - Guest com MUITOS fillers
   - Editing style Standard ou Heavy

   **Quando NAO usar:**
   - Style Minimal (quer manter fillers)
   - Episodios <30min (manual e mais rapido)

9. **Nivelamento de volume entre participantes**

   **Problema:** Host em -12 dBFS, guest em -24 dBFS

   **Solucao:**
   - Medir RMS de cada track (plugin metering)
   - Ajustar gain para igualar:
     - Target: -18 dBFS RMS para ambos
     - Usar Gain plugin (nao volume fader, para preservar headroom)
   - Usar compressao suave para controlar dinamica:
     - Ratio: 3:1
     - Threshold: -16 dBFS
     - Attack: 10ms, Release: 100ms

   **Automacao de volume:**
   - Se participante varia muito (sussurra depois grita)
   - Desenhar automacao manual no DAW
   - Ou: Usar compressor multibanda

10. **Segunda passagem: Smoothness check**

    **Ouvir episodio completo (1x speed) e validar:**
    - [ ] Transicoes entre cortes soam naturais (nao abrupto)?
    - [ ] Volume consistente entre participantes?
    - [ ] Pacing agradavel (nao muito rapido ou lento)?
    - [ ] Zero ruidos tecnicos audveis?
    - [ ] Sibilancia controlada (nao estridente)?

    **Ajustes finais:**
    - Adicionar fades curtos (10-50ms) em cortes abrupto
    - Suavizar transicoes com crossfades

11. **Exportar versao editada**

    **Settings:**
    - Formato: WAV (ainda precisa de mixagem/mastering)
    - Sample rate: 48kHz
    - Bit depth: 24bit
    - Stereo: Manter tracks separadas para mixagem
    - Naming: `S0{N}E0{N}_edited_{track}.wav`

    **Arquivos gerados:**
    - `S02E03_edited_host.wav`
    - `S02E03_edited_guest.wav`
    - `S02E03_edited_music.wav` (se aplicavel)

12. **Documentar edit decision list**

    **Log de todos cortes/ajustes:**
    - Timestamp: 12:30 - Cortado filler "tipo" (3x em 10s)
    - Timestamp: 18:45 - Removido ruido de cachorro (5s)
    - Timestamp: 25:10 - Ajustado volume do guest (+6dB)

    **Salvar removed content (backup):**
    - Exportar trechos cortados em arquivo separado
    - `S02E03_removed_content.wav`
    - Se guest pedir para revisar algo removido, tem backup

## Output

### edit-decision-list-S0{N}E0{N}.md

```markdown
# Edit Decision List: S02E03

**Episodio:** S02E03 - IA e Etica com Maria Santos
**Duracao raw:** 58min
**Duracao editada:** 52min
**Editing style:** Standard
**Engineer:** @engineer
**Data:** 2026-03-16

---

## Sumario

- **Cortes totais:** 18 cortes (6min removido)
- **Fillers removidos:** 24 instancias ("ahh" x8, "tipo" x12, "sabe" x4)
- **Ruidos corrigidos:** 3 instancias (cachorro, clipping, pop)
- **Volume ajustado:** Guest track (+4dB overall)

---

## Timeline de Edicoes

| Timestamp | Acao | Detalhe | Duracao Removida |
|-----------|------|---------|------------------|
| 03:42-03:45 | Corte | Host pediu para refazer frase | 3s |
| 08:15-08:20 | Corte | Pausa longa (host pensando) | 5s |
| 12:30 | Noise reduction | Cachorro latiu ao fundo | - |
| 18:32 | De-clip | Guest clippou por 2s | - |
| 23:10-23:12 | Corte | Guest disse "tipo" 3x seguidas | 2s |
| 27:45 | Pop removal | Pop de cabo | - |
| 34:50-35:10 | Corte | Pausa para agua (silencio) | 20s |
| 41:20 | Volume adjust | Guest muito baixo, +6dB | - |
| 48:20 | Filler removal | "ahh" prolongado | 2s |
| 52:15-53:00 | Corte | Divagacao off-topic | 45s |

(... continua para todos os 18 cortes)

---

## Processamento Aplicado

### Noise Reduction
- **Plugin:** iZotope RX Voice De-noise
- **Threshold:** 8 dB reduction
- **Applied to:** Ambas tracks (host + guest)
- **Result:** Room tone limpo, -60 dBFS noise floor

### De-Ess
- **Plugin:** FabFilter Pro-DS
- **Frequency range:** 6-10 kHz
- **Reduction:** 4 dB
- **Applied to:** Guest track (sibilancia mais pronunciada)

### De-Reverb
- **Plugin:** iZotope RX De-reverb
- **Reduction:** 8 dB
- **Applied to:** Guest track (home office com reverb)
- **Result:** Voz mais seca, inteligibilidade melhorada

### Volume Leveling
- **Host track:** -18 dBFS RMS (no adjustment needed)
- **Guest track:** -22 dBFS RMS → adjusted to -18 dBFS (+4dB)
- **Method:** Gain plugin + gentle compression (3:1 ratio)

---

## Removed Content

**Total removido:** 6min 15s

Conteudo removido salvo em:
`/audio/removed/S02E03_removed_content.wav`

### Breakdown
- Fillers: 1min 30s
- Pausas longas: 2min 45s
- Erros/recomeco: 45s
- Divagacao off-topic: 45s
- Pausa agua: 20s
- Outros: 30s

---

## Quality Metrics (Pos-Edicao)

| Metrica | Target | Result | Status |
|---------|--------|--------|--------|
| Noise floor | <-60 dBFS | -62 dBFS | ✅ |
| Peak level | -6 dBFS | -8 dBFS | ✅ |
| RMS average | -18 dBFS | -18 dBFS | ✅ |
| Sibilancia | Controlada | 4dB reducao | ✅ |
| Reverb | Minimizado | 8dB reducao | ✅ |
| Pacing | Natural | 52min (target 50min) | ✅ |

---

## Gold Moments (Para Clips)

| Timestamp | Momento | Potencial Viral |
|-----------|---------|-----------------|
| 12:30 | Quote sobre etica em IA | Alto |
| 28:45 | Hot take sobre regulacao | Medio |
| 48:20 | Risada espontanea | Baixo (humaniza) |

---

## Proximos Passos

- [x] Edicao completa
- [x] Export tracks editadas
- [ ] Enviar para @engineer (mixing/mastering)
- [ ] Avisar @growth sobre gold moments para clips

---

**Arquivos gerados:**
- `S02E03_edited_host.wav` (2.0GB)
- `S02E03_edited_guest.wav` (1.8GB)
- `S02E03_removed_content.wav` (800MB backup)
```

## Criterios de Qualidade

- [ ] Multi-track sincronizado perfeitamente
- [ ] Zero problemas tecnicos audveis (clipping, pops, ruidos)
- [ ] Noise floor < -60 dBFS
- [ ] Sibilancia controlada (de-ess aplicado)
- [ ] Reverb minimizado (se presente na gravacao)
- [ ] Fillers removidos conforme editing style (minimal/standard/heavy)
- [ ] Pacing natural (nao muito rapido ou robotic)
- [ ] Volume nivelado entre participantes (-18 dBFS RMS)
- [ ] Transicoes suaves (fades em cortes abrupto)
- [ ] Duracao dentro do target (+/- 5min)
- [ ] Edit decision list documentado
- [ ] Removed content salvo como backup
- [ ] Quality report com metricas pos-edicao
- [ ] Pronto para mixagem (WAV 48kHz/24bit)
