---
task: SEO Content Page
responsavel: "@editor"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - transcript-clean: Transcricao editada do episodio
  - show-notes: Show notes completas
  - target-keywords: 5-8 keywords principais
  - internal-links: Episodios relacionados para linkagem
Saida: |
  - seo-page-html: Pagina HTML completa (2000+ palavras)
  - schema-markup: JSON-LD schema para podcasts
  - sitemap-entry: Entrada para sitemap.xml
  - meta-tags: Title, description, OG tags
Checklist:
  - "[ ] Transcript editado com keywords (2000+ palavras)"
  - "[ ] H1/H2/H3 semanticos com keywords"
  - "[ ] Internal links para 3-5 episodios relacionados"
  - "[ ] Embed player do episodio"
  - "[ ] Schema markup (PodcastEpisode)"
  - "[ ] Meta tags (title, description, OG image)"
  - "[ ] Sitemap.xml atualizado"
  - "[ ] Publicar ANTES de distribuir (pre-indexing)"
---

# *seo-content-page

Criacao de pagina web SEO-optimized com transcript completo (2000+ palavras), schema markup, internal links, embed player. Publicar ANTES de distribuir episodio para pre-indexing no Google.

## Uso

```bash
# Pagina SEO completa
*seo-content-page --episode S02E03 --keywords "ia,etica,nlp" --word-count 2500

# Pre-indexing (publicar antes de distribuir)
*seo-content-page --episode S02E05 --publish-early --index-date "2026-03-20"
```

## Steps (Resumido)

1. **Editar transcript com keywords**
   - Inserir keywords naturalmente
   - 2000+ palavras (Google prefere conteudo longo)

2. **Estrutura semantica (H1/H2/H3)**
   ```
   H1: {Titulo com keyword}
   H2: Introducao
   H2: Key Takeaways
   H2: Transcript Completo
     H3: Trajetoria de Maria
     H3: Projeto SentimentAI
     H3: Etica em IA
   H2: Episodios Relacionados
   ```

3. **Internal links**
   - Linkar para 3-5 episodios relacionados
   - Anchor text com keywords

4. **Embed player**
   - Player HTML5 ou iframe
   - Permitir play direto na pagina

5. **Schema markup (JSON-LD)**
   ```json
   {
     "@context": "https://schema.org",
     "@type": "PodcastEpisode",
     "name": "IA e Etica com Maria Santos",
     "description": "...",
     "datePublished": "2026-03-15",
     "duration": "PT52M",
     "associatedMedia": {
       "@type": "MediaObject",
       "contentUrl": "https://..."
     }
   }
   ```

6. **Meta tags**
   ```html
   <title>IA e Etica com Maria Santos | TechTalks</title>
   <meta name="description" content="...">
   <meta property="og:image" content="cover.jpg">
   ```

7. **Publicar PRE-lancamento**
   - Publicar pagina 24-48h antes de distribuir episodio
   - Google indexa antes do lancamento
   - Quando episodio sai, pagina ja rankeia

## Criterios de Qualidade

- [ ] 2000+ palavras (transcript editado)
- [ ] H1/H2/H3 semanticos
- [ ] 5-8 keywords inseridas naturalmente
- [ ] 3-5 internal links para episodios relacionados
- [ ] Player embed funcionando
- [ ] Schema markup PodcastEpisode
- [ ] Meta tags completos (title, description, OG)
- [ ] Sitemap.xml atualizado
- [ ] Publicado 24-48h ANTES do lancamento
- [ ] Mobile-friendly (responsive)
