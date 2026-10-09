---
task: Remote Recording
responsavel: "@engineer"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - guest-info: Dados do convidado remoto
  - episode-script: Pauta/roteiro do episodio
  - platform-choice: Riverside, Zencastr, SquadCast, Zoom
  - recording-datetime: Data/hora da gravacao
Saida: |
  - multi-track-files: Arquivos separados por participante
  - sync-notes: Notas de sincronizacao entre tracks
  - tech-report: Relatorio de qualidade tecnica
  - guest-tech-checklist: Checklist validado do setup do guest
Checklist:
  - "[ ] Enviar tech requirements ao guest (7 dias antes)"
  - "[ ] Agendar tech check (10min antes da gravacao)"
  - "[ ] Validar setup do guest (mic, fone, internet, ambiente)"
  - "[ ] Configurar plataforma para local recording (Riverside/Zencastr)"
  - "[ ] Iniciar gravacao com countdown (3, 2, 1)"
  - "[ ] Monitorar sync e quality durante gravacao"
  - "[ ] Troubleshooting em tempo real (latencia, ruido, drop)"
  - "[ ] Download multi-track separado ao final"
  - "[ ] Verificar sync entre tracks (audio deve bater)"
  - "[ ] Backup imediato dos arquivos"
---

# *remote-recording

Setup e execucao de gravacao remota profissional usando plataformas com local recording (Riverside, Zencastr). Garante qualidade de audio equivalente a gravacao presencial, com multi-track separado, sync automatico e troubleshooting proativo.

## Uso

```bash
# Gravacao remota via Riverside
*remote-recording --episode S02E03 --guest "Maria Santos" --platform riverside

# Gravacao multi-guest remota
*remote-recording --episode S02E12 --guests "Ana,Pedro,Carla" --platform squadcast

# Tech check pre-gravacao
*remote-recording --tech-check --guest "João Silva" --datetime "2026-03-20 13:50 BRT"
```

## Steps

1. **Enviar tech requirements (7 dias antes)**

   **Email template:**
   ```
   Oi {Nome Guest},

   Animado para nossa gravacao dia {data} as {hora} {fuso}!

   Para garantir melhor qualidade de audio, algumas dicas:

   🎙️ **MICROFONE:**
   - Ideal: Mic USB dedicado (Blue Yeti, Shure MV7, Audio-Technica AT2020)
   - Aceitavel: AirPods ou fone com mic embutido
   - Evitar: Mic interno do laptop (qualidade inferior)

   🎧 **FONE:**
   - ESSENCIAL usar fone/headset (evita eco)
   - Qualquer fone serve (in-ear, over-ear, AirPods)

   📍 **AMBIENTE:**
   - Lugar silencioso (feche janelas, desligue AC/ventilador)
   - Quanto mais "abafado" melhor (cortinas, tapetes, livros ajudam)
   - Evitar: Salas vazias com eco

   📶 **INTERNET:**
   - Wifi forte OU cabo ethernet (ideal)
   - Testar velocidade: https://fast.com (minimo 10 Mbps)
   - Fechar abas/apps que usam banda (streaming, downloads)

   💻 **NAVEGADOR:**
   - Chrome ou Edge (Firefox tem problemas com Riverside)
   - Atualizado para ultima versao

   🧪 **TESTE:**
   - 10min antes da gravacao, vamos fazer teste rapido
   - Se quiser testar sozinho antes: {link teste}

   Qualquer duvida, so gritar!

   Link da gravacao: {riverside/zencastr link}

   Abraco,
   {Produtor/Host}
   ```

2. **Escolher plataforma de gravacao**

   **Comparativo:**

   | Plataforma | Preco | Local Recording | Multi-track | Video | Melhor para |
   |------------|-------|-----------------|-------------|-------|-------------|
   | **Riverside** | $20/mes | ✅ 4K video + lossless audio | ✅ | ✅ 4K | Video podcast, qualidade maxima |
   | **Zencastr** | $20/mes | ✅ Lossless audio | ✅ | ✅ 1080p | Audio-first, budget |
   | **SquadCast** | $20/mes | ✅ Lossless audio | ✅ | ✅ 1080p | Multiplos guests (ate 4) |
   | **Zoom** | $15/mes | ❌ (precisa recorder local) | ❌ Single track | ✅ 1080p | Evitar (qualidade inferior) |

   **Recomendacao:** Riverside.fm para qualidade maxima + video opcional.

3. **Configurar sessao na plataforma**

   **Riverside setup:**
   - Criar novo recording: `S0{N}E0{N} - {titulo}`
   - Convidar guest via email (link unico)
   - Configurar:
     - Audio: WAV 48kHz (lossless)
     - Video: 4K (se precisar) ou OFF (se audio-only)
     - Separate tracks: ON (essencial)
     - Recording mode: Local recording (nao depende de internet)
   - Testar com co-host/produtor antes do guest entrar

4. **Tech check (10min antes da gravacao)**

   **Checklist com guest:**
   - [ ] "Voce consegue me ouvir bem?"
   - [ ] "Consegue se ouvir no retorno?"
   - [ ] "Qual mic voce esta usando?" (validar no Riverside)
   - [ ] "Clica em 'Test Audio' e fala algo..." (verificar levels)
   - [ ] "Feche outras abas/apps que usam internet"
   - [ ] "Esta em lugar silencioso? Janelas fechadas?"
   - [ ] "Agua disponivel?"

   **Validar levels:**
   - Pedir para guest falar em volume normal
   - Observar meter no Riverside (verde = bom, amarelo = cuidado, vermelho = alto demais)
   - Ajustar gain se necessario (Riverside ajusta automaticamente, mas validar)

   **Red flags:**
   - Eco: Guest nao esta usando fone → ESSENCIAL corrigir
   - Ruido de fundo alto: Fechar janelas, desligar AC
   - Latencia >500ms: Internet fraca → testar cabo ethernet

5. **Iniciar gravacao com countdown**
   - "Tudo certo! Vou iniciar a gravacao."
   - Clicar "Start Recording" no Riverside
   - Aguardar indicador vermelho "REC" aparecer
   - Countdown verbal: "Gravando em 3, 2, 1... vai!"
   - Primeiros 5s: silencio (room tone para edicao)

6. **Monitorar durante gravacao**

   **Responsabilidades do engineer/host:**
   - Observar indicadores de conexao (Riverside mostra status)
   - Verificar sync (delay entre audio/video)
   - Tomar notas de timestamps importantes
   - Identificar problemas:
     - Guest muito longe do mic (volume baixo)
     - Ruido de fundo (cachorro, carro, construcao)
     - Internet instavel (Riverside alerta)

   **Intervencoes sutis:**
   - "Aproxima um pouquinho do mic" (se volume baixo)
   - "Vou pausar 30s, tem barulho de fundo" (se ruido)
   - Nao interromper fluxo a menos que critico

7. **Troubleshooting em tempo real**

   **Problema:** Audio cortando (choppy)
   - **Causa:** Internet instavel
   - **Fix:**
     - Pedir guest fechar outras abas/apps
     - Trocar de wifi para cabo ethernet
     - Ultimo recurso: Reduzir qualidade de video (Riverside)

   **Problema:** Eco/feedback
   - **Causa:** Guest sem fone
   - **Fix:** ESSENCIAL guest usar fone

   **Problema:** Latencia alta (delay >1s)
   - **Causa:** Internet lenta ou distancia geografica
   - **Fix:**
     - Reduzir qualidade de transmissao (Riverside ajusta)
     - Aceitar latencia (local recording nao afetado)

   **Problema:** Ruido de fundo constante
   - **Causa:** AC, ventilador, trafego
   - **Fix:** Pedir guest desligar/fechar (se possivel)

8. **Finalizacao da gravacao**
   - "Otimo! Vou finalizar a gravacao."
   - Clicar "Stop Recording"
   - **NAO FECHAR O NAVEGADOR** ainda
   - Aguardar Riverside fazer upload dos arquivos locais (barra de progresso)
   - Tempo de upload: ~5-15min dependendo da duracao

9. **Download multi-track separado**

   **Riverside:**
   - Acessar "Downloads" na dashboard
   - Baixar cada track individualmente:
     - `S02E03_host_audio.wav`
     - `S02E03_maria-santos_audio.wav`
     - `S02E03_host_video.mp4` (se precisar)
     - `S02E03_maria-santos_video.mp4` (se precisar)

   **Naming convention:**
   ```
   S0{N}E0{N}_{participante}_{tipo}_raw.wav

   Exemplo:
   S02E03_host_audio_raw.wav
   S02E03_maria-santos_audio_raw.wav
   ```

10. **Verificar sync entre tracks**
    - Importar ambas tracks no DAW (Logic/Reaper/Audition)
    - Alinhar pela forma de onda (Riverside ja sincroniza, mas validar)
    - Testar: Momento onde ambos falam ao mesmo tempo deve bater perfeitamente
    - Se dessincronizado: Usar clap no inicio da gravacao como referencia

11. **Backup imediato**
    - Upload Google Drive / Dropbox
    - Verificar tamanho dos arquivos (nao corrompidos)
    - Manter backups locais ate edicao finalizada

12. **Documentar tech report**
    - Salvar em `/sessions/S0{N}E0{N}-remote-tech-report.md`
    - Incluir qualidade de conexao, problemas, solucoes

## Output

### S0{N}E0{N}-remote-tech-report.md

```markdown
# Remote Recording Tech Report: S02E03

**Data:** 2026-03-15
**Episodio:** S02E03 - IA e Etica com Maria Santos
**Plataforma:** Riverside.fm
**Duracao:** 52min
**Engineer:** @engineer

---

## Setup Tecnico

### Host (Local)
- **Mic:** Shure SM7B
- **Interface:** Focusrite Scarlett 2i2
- **Internet:** 300 Mbps fibra (cabo ethernet)
- **Browser:** Chrome 120

### Guest (Remota - São Paulo, BR)
- **Mic:** Shure MV7 USB
- **Fone:** Sony WH-1000XM4
- **Internet:** 100 Mbps fibra (wifi)
- **Browser:** Chrome 119
- **Ambiente:** Home office com porta fechada

---

## Qualidade de Conexao

| Participante | Conexao | Latencia | Packet Loss | Qualidade |
|--------------|---------|----------|-------------|-----------|
| Host | Excelente | 15ms | 0% | 10/10 |
| Maria Santos | Boa | 45ms | 1% | 8/10 |

**Sync:** Perfeito (Riverside local recording elimina latencia na gravacao)

---

## Problemas Encontrados

### 1. Leve reverb no ambiente da guest (12:00-25:00)
- **Causa:** Sala com paredes lisas, sem tratamento acustico
- **Impacto:** Baixo (tratavel na pos-producao com iZotope RX)
- **Fix futuro:** Sugerir cobertor/cortina atras do mic

### 2. Cachorro latiu ao fundo (23:10)
- **Causa:** Pet no corredor
- **Impacto:** Minimo (latido distante, 2s de duracao)
- **Fix:** Editavel na pos-producao

### 3. Internet instavel (38:00-38:30)
- **Causa:** Alguem iniciou streaming na casa da guest
- **Impacto:** Zero (local recording nao afetado)
- **Fix:** Pedimos para pausar streaming, resolvido

---

## Niveis de Audio

| Participante | Peak | Average | Clipping? |
|--------------|------|---------|-----------|
| Host | -10 dBFS | -18 dBFS | Nao |
| Maria Santos | -12 dBFS | -20 dBFS | Nao |

**Room tone (guest):** -55 dBFS (aceitavel, reverb presente)

---

## Timestamps Importantes

| Tempo | Nota |
|-------|------|
| 12:30 | GOLD: Quote sobre etica em IA (clip viral) |
| 23:10 | Cachorro latiu (cortar na edicao) |
| 34:50 | Pausa para agua (cortar silencio) |
| 48:20 | Risada espontanea (manter, humaniza) |

---

## Arquivos Baixados

- ✅ `S02E03_host_audio_raw.wav` (2.1GB, 48kHz/24bit)
- ✅ `S02E03_maria-santos_audio_raw.wav` (1.9GB, 48kHz/24bit)
- ✅ `S02E03_sync.json` (metadata Riverside)
- ✅ Backup: Google Drive `/backups/S02E03/`

---

## Qualidade Geral

**8.5/10**

Audio limpo, niveis corretos, sync perfeito. Unico ajuste: reverb reduction na track da guest.

---

## Recomendacoes Futuras

1. Enviar absorption foam para guests recorrentes
2. Pedir para guest testar com cortina/cobertor atras do mic
3. Confirmar que ninguem vai usar internet durante gravacao

---

## Proximos Passos

- [x] Arquivos baixados e verificados
- [x] Backup em Google Drive completo
- [ ] Enviar para @engineer iniciar edicao
- [ ] Enviar thank you email ao guest
```

## Criterios de Qualidade

- [ ] Tech requirements enviados 7 dias antes
- [ ] Tech check realizado 10min antes da gravacao
- [ ] Plataforma configurada para local recording + separate tracks
- [ ] Niveis de audio validados (-16 to -12 dBFS)
- [ ] Guest usando fone (zero eco)
- [ ] Ambiente silencioso validado
- [ ] Sync entre tracks verificado (audio alinhado)
- [ ] Multi-track separado baixado (nao single stereo mix)
- [ ] Backup imediato em cloud
- [ ] Tech report documentado com problemas e solucoes
- [ ] Qualidade geral 7/10 ou superior
- [ ] Nenhum problema tecnico comprometeu conteudo
