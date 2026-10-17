---
task: Video Editing
responsavel: "@engineer"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - video-sources: Multicam (presencial) ou gravação de vídeo por participante (remota), B-roll
  - edited-audio: Áudio já editado/masterizado (a edição de vídeo segue os cortes do áudio)
  - destinations: Episódio completo no YouTube e/ou cortes verticais (Shorts, Reels, LinkedIn)
  - assets: Lower thirds, logos, thumbnail (Pixel)
Saida: |
  - video-full: Episódio completo em MP4 (H.264)
  - video-clips: Cortes verticais 9:16 por destino
  - captions: Legendas revisadas (.srt)
Checklist:
  - "[ ] Multicam sincronizado pelo áudio; sync conferido no início, meio e fim"
  - "[ ] Cortes idênticos aos da edição de áudio (mesmo conteúdo em todas as versões)"
  - "[ ] Lower thirds com nome e função do convidado conforme autorizado no intake"
  - "[ ] Legendas geradas automaticamente e revisadas à mão (nomes, jargões)"
  - "[ ] .srt exportado separado (acessibilidade e Cast/Clip)"
  - "[ ] Duração máxima e proporção de cada destino conferidas no site da plataforma na data"
  - "[ ] Loudness do vídeo completo medido (-14 LUFS integrado, true peak <= -1 dBTP)"
  - "[ ] Capítulos do YouTube via timestamps na descrição (Clip)"
  - "[ ] Thumbnail com Pixel"
---

# *edit-video

Edição de vídeo para YouTube e redes, a partir do áudio já aprovado.

## Uso

```bash
*edit-video --episode EP06 --full --clips 3
```

## Steps

1. **Captura (planejada na gravação):** 2-3 ângulos presenciais (host, convidado, plano aberto) ou vídeo local de cada participante na remota (mínimo 1080p).
2. **Sync e corte:** multicam alinhado pelo áudio; replicar a decisão editorial do áudio.
3. **Gráficos:** lower thirds, logos e overlays simples (assets de Pixel).
4. **Legendas:** auto (Descript, Premiere, CapCut) + revisão manual; `.srt` separado.
5. **Export por destino:**

| Destino | Resolução | Formato | Observação |
|---------|-----------|---------|------------|
| YouTube (completo) | 1080p ou 4K | MP4 H.264 | capítulos via timestamps |
| YouTube Shorts | 1080×1920 (9:16) | MP4 | conferir duração máxima vigente |
| Instagram Reels | 1080×1920 | MP4 | conferir duração máxima vigente |
| LinkedIn | 1080×1920 ou 1080p | MP4 | conferir duração máxima vigente |

Bitrate: o preset de upload recomendado pela plataforma; limites de duração mudam com frequência e não ficam fixos aqui.

## Criterios de Qualidade

- [ ] Nenhum trecho cortado no áudio aparece no vídeo
- [ ] Legenda sem erro em nome próprio
- [ ] Entregue a Max para revisão
