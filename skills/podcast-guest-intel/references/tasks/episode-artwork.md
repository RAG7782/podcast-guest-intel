---
task: Episode Artwork
responsavel: "@designer"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - episode-info: Titulo, guest, tema
  - brand-guidelines: Paleta de cores, tipografia, logo
  - platforms: Apple (3000x3000), YouTube (1280x720), Instagram (1080x1080, 1080x1920)
  - guest-photo: Foto do convidado (se aplicavel)
Saida: |
  - cover-apple: 3000x3000px (1:1) para Apple Podcasts
  - thumbnail-youtube: 1280x720px (16:9) para YouTube
  - post-instagram: 1080x1080px (1:1) para feed
  - stories-instagram: 1080x1920px (9:16) para Stories
Checklist:
  - "[ ] Cover 3000x3000px (Apple Podcasts spec)"
  - "[ ] Thumbnail YouTube 1280x720px"
  - "[ ] Post Instagram 1080x1080px"
  - "[ ] Stories Instagram 1080x1920px"
  - "[ ] Manter brand consistency (cores, fonts, logo)"
  - "[ ] Texto legivel em thumbnail pequeno (300x300px)"
  - "[ ] Foto do guest (se entrevista)"
  - "[ ] Export RGB (para digital)"
---

# *episode-artwork

Criacao de arte customizada por episodio: cover Apple Podcasts (3000x3000), thumbnail YouTube (1280x720), posts Instagram (1:1 e 9:16). Brand consistency mantida.

## Uso

```bash
# Arte completa (todos formatos)
*episode-artwork --episode S02E03 --guest "Maria Santos" --all-formats

# Apenas cover para podcast
*episode-artwork --episode S02E05 --format cover-only

# Arte para episodio especial (custom design)
*episode-artwork --episode S02E10 --type special --custom-layout
```

## Steps (Resumido)

1. **Template base**
   - Background com paleta de cores do brand
   - Logo do podcast
   - Typography guidelines

2. **Cover Apple Podcasts (3000x3000px)**
   - Foto do guest (se entrevista)
   - Titulo do episodio (legivel)
   - Numero do episodio (S02E03)

3. **Thumbnail YouTube (1280x720px)**
   - Foto do guest ou imagem tematica
   - Titulo chamativo (grandes, bold)
   - Expressao facial chamativa (se foto)

4. **Instagram Feed (1080x1080px)**
   - Quadrado
   - Foto do guest
   - Quote visual (frase do episodio)

5. **Instagram Stories (1080x1920px)**
   - Vertical 9:16
   - Animacao leve (opcional)
   - Swipe up CTA

6. **Brand consistency**
   - Mesma paleta de cores
   - Mesma tipografia
   - Logo sempre presente

7. **Test legibilidade**
   - Thumbnail 300x300px ainda legivel?
   - Mobile (6" screen) legivel?

## Criterios de Qualidade

- [ ] Cover 3000x3000px (Apple spec)
- [ ] Thumbnail YouTube 1280x720px
- [ ] Instagram 1080x1080px e 1080x1920px
- [ ] Brand consistency (cores, fonts, logo)
- [ ] Texto legivel em 300x300px
- [ ] RGB color space (para digital)
- [ ] Foto do guest em alta resolucao
- [ ] Export em PNG ou JPG (80%+ quality)
