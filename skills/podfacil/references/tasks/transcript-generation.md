---
task: Transcript Generation
responsavel: "@editor"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - final-audio: Arquivo masterizado final
  - participant-names: Lista de participantes (host, guests)
  - accuracy-target: 97%+ accuracy
  - format-type: Clean (sem fillers) ou Verbatim (com fillers)
Saida: |
  - transcript-clean: Transcricao limpa para leitura
  - transcript-srt: Legendas SRT com timecodes
  - transcript-vtt: WebVTT para players web
  - transcript-json: JSON estruturado (Podcasting 2.0)
Checklist:
  - "[ ] Transcricao AI via Whisper/Descript (primeira passada)"
  - "[ ] Revisao humana para accuracy 97%+"
  - "[ ] Speaker labeling (host, guest 1, guest 2)"
  - "[ ] Adicionar timestamps a cada 2-5min"
  - "[ ] Formatar para screen readers (semantica HTML)"
  - "[ ] Gerar versao clean (sem fillers) e verbatim"
  - "[ ] Exportar SRT/VTT para legendas
"
  - "[ ] Criar chapter markers (Podcasting 2.0)"
---

# *transcript-generation

Geracao de transcricao profissional com AI + revisao humana. Speaker labeling, timestamps, chapter markers. Multiplos formatos (clean, verbatim, SRT, VTT, JSON) para acessibilidade e SEO.

## Uso

```bash
# Transcricao standard (clean)
*transcript-generation --episode S02E03 --format clean --accuracy 97

# Transcricao verbatim (com fillers)
*transcript-generation --episode S02E05 --format verbatim --include-fillers

# Gerar apenas SRT/VTT para video
*transcript-generation --episode S02E08 --output srt,vtt --for-youtube
```

## Steps (Resumido)

1. **Transcricao AI (Whisper/Descript)**
   - Upload audio
   - Configurar: Language PT-BR, speaker diarization
   - Export transcript raw

2. **Revisao humana**
   - Corrigir erros (nomes proprios, termos tecnicos)
   - Validar speaker labeling
   - Target: 97%+ accuracy

3. **Speaker labeling**
   ```
   HOST: Bem-vindos ao episodio...
   MARIA SANTOS: Obrigada por me receber.
   HOST: Vamos falar sobre IA...
   ```

4. **Timestamps a cada 2-5min**
   ```
   [00:00:00] Introducao
   [00:02:30] Trajetoria de Maria em IA
   [00:08:15] Projeto atual: SentimentAI
   ```

5. **Formatar para acessibilidade**
   - Semantica HTML (headings, paragrafos)
   - Alt text para elementos visuais
   - Keyboard navigable

6. **Chapter markers (Podcasting 2.0)**
   ```json
   {
     "chapters": [
       {"start": 0, "title": "Introducao"},
       {"start": 150, "title": "Trajetoria de Maria"},
       {"start": 495, "title": "SentimentAI"}
     ]
   }
   ```

## Criterios de Qualidade

- [ ] Accuracy 97%+ validado
- [ ] Speaker labeling 100% correto
- [ ] Timestamps a cada 2-5min
- [ ] Formatado para screen readers
- [ ] Versoes clean e verbatim disponiveis
- [ ] SRT/VTT exportado sem erros
- [ ] Chapter markers sincronizados
