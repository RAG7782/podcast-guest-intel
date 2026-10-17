---
task: Social Clips Creation
responsavel: "@designer"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - final-audio: Arquivo masterizado do episodio
  - gold-moments: Timestamps dos melhores momentos
  - platforms: Reels, TikTok, Shorts, LinkedIn
  - branding-assets: Logo, fonts, cores
Saida: |
  - vertical-clips: 9:16 videos para Reels/TikTok/Shorts (3-5 clips)
  - audiograms: Waveform animado com legendas
  - square-clips: 1:1 videos para feed Instagram
  - virality-scores: Scoring de potencial viral por clip
Checklist:
  - "[ ] Identificar 5-8 gold moments via Opus Clip"
  - "[ ] Criar clips verticais 9:16 (30-60s cada)"
  - "[ ] Adicionar legendas queimadas (97% accuracy)"
  - "[ ] Audiogram com waveform animado"
  - "[ ] Branding sutil (logo, cores)"
  - "[ ] Hook forte nos primeiros 3s"
  - "[ ] Export 1080x1920px (9:16), 1080x1080px (1:1)"
  - "[ ] Validar virality score (Opus Clip)"
---

# *social-clips

Criacao de clips virais verticais (9:16) para Reels/TikTok/Shorts. Uso de Opus Clip para detectar momentos virais, legendas queimadas, audiograms. 3-5 clips por episodio.

## Uso

```bash
# Clips virais automaticos via Opus Clip
*social-clips --episode S02E03 --auto-detect --count 5

# Criar clips de gold moments especificos
*social-clips --episode S02E05 --timestamps "12:30,28:45,48:20" --format vertical

# Audiograms para LinkedIn
*social-clips --episode S02E08 --format audiogram --platform linkedin --square
```

## Steps (Resumido)

1. **Opus Clip (AI virality detection)**
   - Upload episodio completo
   - AI detecta 5-10 momentos com virality scoring
   - Selecionar top 3-5 (score >8/10)

2. **Criar clips verticais 9:16**
   - Duracao: 30-60s cada
   - Formato: 1080x1920px
   - Hook nos primeiros 3s

3. **Legendas queimadas**
   - 97% accuracy (Descript/CapCut)
   - Font grande, legivel
   - Highlight keyword em cor diferente

4. **Audiogram (waveform animado)**
   - Headliner, Wavve, Audiogram
   - Waveform sincronizado com audio
   - Background com branding

5. **Branding sutil**
   - Logo no canto (pequeno)
   - Cores do brand no design
   - Nao overpower o conteudo

6. **Hook strategy**
   - Primeiro 3s: Frase impactante
   - Sem intro longa
   - Direto ao ponto

7. **Export multi-formato**
   - 1080x1920px (Reels/TikTok/Shorts)
   - 1080x1080px (Feed Instagram)
   - 1280x720px (YouTube landscape)

## Output (Template)

```
/clips/S02E03/
├── clip01_viral_9-16.mp4 (Reels/TikTok/Shorts)
├── clip01_square_1-1.mp4 (Instagram feed)
├── clip02_viral_9-16.mp4
├── clip03_viral_9-16.mp4
├── audiogram_linkedin_1-1.mp4
└── virality-scores.json
```

## Criterios de Qualidade

- [ ] 3-5 clips por episodio
- [ ] Virality score >8/10 (Opus Clip)
- [ ] Legendas 97%+ accuracy
- [ ] Hook forte nos primeiros 3s
- [ ] Branding sutil (nao invasivo)
- [ ] Export 1080x1920px (9:16)
- [ ] Duracao 30-60s (algoritmo prefere)
- [ ] Audio limpo (-14 LUFS)
