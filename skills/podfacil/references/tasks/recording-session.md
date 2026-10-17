---
task: Recording Session
responsavel: "@engineer"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - episode-script: Roteiro/pauta completo
  - recording-type: Solo, entrevista, narrativo, ao vivo
  - participants: Lista de participantes (host, guests, co-hosts)
  - duration-target: Duracao estimada da gravacao
Saida: |
  - raw-audio-files: Arquivos raw multi-track
  - backup-files: Backup redundante (local + cloud)
  - session-notes: Notas tecnicas da gravacao
  - levels-log: Log de niveis de audio
Checklist:
  - "[ ] Executar pre-recording checklist completo"
  - "[ ] Configurar dual recording (primary + backup)"
  - "[ ] Verificar niveis de audio (-16 to -12 dBFS target)"
  - "[ ] Testar monitoramento (fone, retorno)"
  - "[ ] Room check (ruidos, reverb, eco)"
  - "[ ] Gravar safety announcement (pode pausar, agua, etc)"
  - "[ ] Monitorar levels durante gravacao (nao clipar)"
  - "[ ] Verificar backup em tempo real"
  - "[ ] Exportar arquivos com naming convention (S01E01_titulo_raw.wav)"
  - "[ ] Upload backup para cloud (Google Drive/Dropbox)"
---

# *recording-session

Setup completo e execucao de sessao de gravacao de podcast com foco em qualidade tecnica maxima, redundancia de backup e monitoramento ativo. Garante audio profissional e previne perda de conteudo por falhas tecnicas.

## Uso

```bash
# Gravacao solo no estudio
*recording-session --episode S02E05 --type solo --duration 45min

# Gravacao de entrevista presencial
*recording-session --episode S02E03 --type interview --participants "host,guest" --location studio

# Gravacao narrativa multi-narrador
*recording-session --episode S02E10 --type narrative --participants 3 --duration 60min
```

## Steps

1. **Pre-recording checklist (15min antes)**

   **Equipamento:**
   - [ ] Mic conectado e testado (phantom power se condensador)
   - [ ] Audio interface ligada, drivers atualizados
   - [ ] DAW aberta (Logic/Reaper/Audition) com sessao criada
   - [ ] Fones funcionando (retorno claro)
   - [ ] Pop filter posicionado (2-3 dedos de distancia do mic)
   - [ ] Boom arm/pedestal estavel

   **Ambiente:**
   - [ ] Porta fechada, placa "Gravando" na porta
   - [ ] Janelas fechadas (ruido externo)
   - [ ] AC/ventilador desligado (ou silencioso)
   - [ ] Celular no modo aviao
   - [ ] Pets em outro comodo
   - [ ] Agua disponivel (temperatura ambiente, sem gas)

   **Software:**
   - [ ] DAW configurado para 48kHz / 24bit
   - [ ] Track nomeado: `S0{N}E0{N}_{nome-episodio}_host`
   - [ ] Arm track para gravacao
   - [ ] Input monitoring ativado
   - [ ] Metronomo/click desativado

2. **Configurar dual recording (redundancia)**

   **Setup recomendado:**
   - **Primary:** DAW (Logic/Reaper) gravando WAV 48kHz/24bit
   - **Backup:**
     - Opcao A: Zoom H6 gravando em paralelo (SD card)
     - Opcao B: Audacity em segundo computador
     - Opcao C: Riverside/Zencastr com local recording

   **Por que dual recording?**
   - DAW pode crashar
   - Arquivo pode corromper
   - Seguro de vida contra Murphy's Law

3. **Verificar niveis de audio**

   **Target levels:**
   - **Speaking voice:** -16 to -12 dBFS (peaks)
   - **Loudest moments:** -6 dBFS (nunca clipar 0dBFS)
   - **Average:** -18 dBFS

   **Como ajustar:**
   - Pedir para host/guest falar normalmente
   - Observar meters no DAW
   - Ajustar gain no audio interface (nao no software)
   - Testar momento mais alto (risada, enfase)
   - Deixar 6dB de headroom para seguranca

   **Red flags:**
   - Clipping (luz vermelha): MUITO ALTO, reduzir gain
   - Muito baixo (<-30 dBFS): aumentar gain ou aproximar do mic
   - Inconsistente: orientar distancia fixa do mic (1 palmo)

4. **Testar monitoramento**
   - Host/guest usando fones fechados (evitar bleed)
   - Nivel do retorno confortavel (nao muito alto)
   - Latencia imperceptivel (<10ms)
   - Se entrevista remota: testar audio bidirecional

5. **Room check (ruidos indesejaveis)**
   - Gravar 30s de silencio (room tone)
   - Ouvir com fone em volume alto
   - Identificar ruidos:
     - Geladeira/AC/ventilador
     - Trafego externo
     - Computador ventilando
     - Eletricidade (ground loop hum 60Hz)
   - Eliminar ou minimizar antes de comecar

6. **Safety announcement (relaxar participantes)**
   - "Vamos comecar. Lembre: podemos pausar a qualquer momento."
   - "Se precisar de agua, pausa, corrigir algo, so avisar."
   - "Eu vou estar monitorando audio, entao fique tranquilo com a parte tecnica."
   - "Tente manter distancia fixa do mic (1 palmo)."
   - "3, 2, 1... gravando!"

7. **Monitorar durante gravacao**

   **Responsabilidades do engineer:**
   - Olhos no meter (nao clipar, nao ficar muito baixo)
   - Ouvidos no fone (qualidade, ruidos, distorcao)
   - Tomar notas de timestamps:
     - Erros a cortar ("corta isso" do host)
     - Melhores momentos (potenciais clips)
     - Problemas tecnicos (ruido, clipping)
   - Verificar backup gravando em paralelo (glance a cada 5min)

   **Intervencoes necessarias:**
   - Nivel muito baixo: "Aproxima um pouco do mic"
   - Clipping: "Um pouco mais longe, ou fala mais suave"
   - Ruido externo: Pausar, eliminar ruido, retomar

8. **Gestao de pausas**
   - Pausas naturais a cada 20-30min (beber agua, respirar)
   - Se erro grande: pausar, respirar, retomar do inicio do paragrafo
   - Nao deletar takes ruins (manter tudo, decisao na edicao)
   - Mark/flag no DAW para facilitar edicao depois

9. **Finalizacao da gravacao**
   - "Gravacao finalizada! Vou verificar os arquivos."
   - Parar gravacao no DAW E no backup
   - Ouvir ultimos 30s para confirmar gravou ate o fim
   - Salvar projeto do DAW
   - Nao desligar nada ate verificar arquivos

10. **Exportar e backup**

    **Naming convention:**
    ```
    S0{N}E0{N}_{titulo-episodio}_{participante}_raw.wav

    Exemplo:
    S02E03_IA-Etica_host_raw.wav
    S02E03_IA-Etica_maria-santos_raw.wav
    S02E03_IA-Etica_backup-zoom_raw.wav
    ```

    **Export settings:**
    - Formato: WAV (nao MP3, precisa de fidelidade)
    - Sample rate: 48kHz
    - Bit depth: 24bit
    - Interleaved: Mono (cada participante em arquivo separado)

    **Backup imediato:**
    - Upload para Google Drive / Dropbox / Backblaze
    - Verificar upload completo (tamanho do arquivo)
    - Nao deletar arquivos locais ate edicao finalizada

11. **Documentar session notes**
    - Salvar em `/sessions/S0{N}E0{N}-session-notes.md`
    - Incluir:
      - Equipamento usado
      - Niveis de audio (peak, average)
      - Problemas encontrados
      - Timestamps de momentos importantes
      - Qualidade geral (1-10)

## Output

### S0{N}E0{N}-session-notes.md

```markdown
# Recording Session Notes: S02E03

**Data:** 2026-03-15
**Episodio:** S02E03 - IA e Etica com Maria Santos
**Formato:** Entrevista remota
**Duracao:** 52min
**Engineer:** @engineer

---

## Equipamento

### Host (Local)
- **Mic:** Shure SM7B
- **Interface:** Focusrite Scarlett 2i2
- **DAW:** Logic Pro X
- **Fone:** Audio-Technica ATH-M50x

### Guest (Remota)
- **Mic:** Shure MV7
- **Plataforma:** Riverside.fm (local recording)
- **Fone:** Sony WH-1000XM4

---

## Niveis de Audio

| Participante | Peak | Average | Clipping? | Qualidade |
|--------------|------|---------|-----------|-----------|
| Host | -10 dBFS | -18 dBFS | Nao | 9/10 |
| Maria Santos | -12 dBFS | -20 dBFS | Nao | 8/10 (leve room reverb) |

**Room tone:** Limpo, ruido de fundo minimo (<-60 dBFS)

---

## Timestamps Importantes

| Tempo | Nota |
|-------|------|
| 03:45 | Host pediu para recomecar frase (ja cortado no take 2) |
| 12:30 | GOLD: Fala incrivel sobre etica em IA (potencial clip viral) |
| 23:10 | Cachorro latiu ao fundo (guest side), mas baixo |
| 34:50 | Pausa para agua |
| 48:20 | Risada espontanea otima (humaniza) |

---

## Problemas Encontrados

1. **Leve reverb no ambiente da guest:**
   - Nao critico, facilmente tratavel com iZotope RX
   - Orientacao para proxima: usar cobertor/cortina

2. **Clipping breve aos 18:32:**
   - Guest falou MUITO alto por 2 segundos
   - Nao comprometeu, mas atencao na mixagem

---

## Backup

- ✅ Primary: Logic Pro X → `S02E03_IA-Etica_host_raw.wav` (2.1GB)
- ✅ Backup: Riverside local → `S02E03_IA-Etica_maria-santos_raw.wav` (1.8GB)
- ✅ Cloud: Upload Google Drive completo (verified)

---

## Qualidade Geral

**9/10**

Audio limpo, niveis corretos, conteudo excelente. Unico ajuste necessario: leve reverb reduction na track da guest.

---

## Proximos Passos

- [ ] Enviar arquivos raw para @engineer (edicao)
- [ ] Agendar pre-interview com proximo guest (orientar sobre ambiente)
- [ ] Considerar enviar absorption foam para guests recorrentes

---

**Arquivos:**
- `/audio/raw/S02E03_IA-Etica_host_raw.wav`
- `/audio/raw/S02E03_IA-Etica_maria-santos_raw.wav`
- `/backups/S02E03_backup.zip` (uploaded to Google Drive)
```

## Criterios de Qualidade

- [ ] Pre-recording checklist 100% completado
- [ ] Dual recording configurado (primary + backup)
- [ ] Niveis de audio corretos (-16 to -12 dBFS peaks)
- [ ] Room tone limpo (<-60 dBFS noise floor)
- [ ] Zero clipping durante gravacao (ou minimo e documentado)
- [ ] Backup verificado em tempo real durante gravacao
- [ ] Arquivos exportados com naming convention correto
- [ ] Upload de backup para cloud completado
- [ ] Session notes documentadas com timestamps importantes
- [ ] Qualidade geral 7/10 ou superior
- [ ] Nenhum arquivo perdido ou corrompido
- [ ] Participantes confortaveis (pausas oferecidas, agua disponivel)
