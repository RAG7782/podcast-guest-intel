---
task: Episode Publishing
responsavel: "@distributor"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - mastered-audio: Arquivos masterizados por plataforma
  - show-notes: Show notes completas
  - artwork: Cover art 3000x3000px
  - metadata: Titulo, descricao, keywords, chapter markers
Saida: |
  - published-episode: Episodio publicado em todas plataformas
  - rss-feed-updated: Feed RSS atualizado
  - chapter-markers-added: Podcasting 2.0 tags
  - distribution-report: Relatorio de publicacao
Checklist:
  - "[ ] Upload audio para host (Libsyn/Buzzsprout/Transistor)"
  - "[ ] Adicionar metadata completo (titulo, descricao, tags)"
  - "[ ] Upload cover art 3000x3000px"
  - "[ ] Configurar chapter markers (podcast:chapters)"
  - "[ ] Adicionar Podcasting 2.0 tags (transcript, person, soundbite)"
  - "[ ] Schedule publishing (ou publish imediato)"
  - "[ ] Validar RSS feed atualizado"
  - "[ ] Verificar em Spotify, Apple, YouTube"
  - "[ ] Submit para Apple Podcasts editorial (se especial)"
---

# *episode-publishing

Publicacao completa de episodio em todas plataformas com metadata otimizado, chapter markers, Podcasting 2.0 tags. Validacao em Spotify, Apple, YouTube.

## Uso

```bash
# Publicar episodio standard
*episode-publishing --episode S02E03 --schedule "2026-03-15 06:00 BRT"

# Publicar episodio especial (submit editorial)
*episode-publishing --episode S02E10 --type special --submit-apple-editorial

# Validar RSS feed apos publicacao
*episode-publishing --episode S02E03 --validate-rss-only
```

## Steps (Resumido)

1. **Upload audio para host**
   - Libsyn, Buzzsprout, Transistor, ou similar
   - Usar arquivo masterizado correto por plataforma

2. **Metadata completo**
   - Titulo (SEO optimized)
   - Descricao (160 char + longa)
   - Keywords/tags
   - Categoria/subcategoria
   - Explicit: Yes/No

3. **Cover art**
   - 3000x3000px
   - RGB
   - <500KB

4. **Chapter markers (Podcasting 2.0)**
   ```xml
   <podcast:chapters url="https://.../chapters.json" type="application/json+chapters" />
   ```

5. **Podcasting 2.0 tags**
   - `<podcast:transcript>`
   - `<podcast:person>` (host, guests)
   - `<podcast:soundbite>` (clips)

6. **Schedule/Publish**
   - Agendar para horario especifico
   - Ou publicar imediatamente

7. **Validar RSS feed**
   - Verificar feed atualizado
   - Testar em validator (Podbase, Cast Feed Validator)

8. **Verificar plataformas**
   - Spotify: Episodio apareceu?
   - Apple Podcasts: Metadata correto?
   - YouTube: Se fizer upload la tambem

9. **Submit Apple editorial** (se episodio especial)
   - Apple Podcasts Connect
   - Pitch: Por que e especial

## Verificacao pos-publicacao

- **T+30 min:** feed reflete o episodio (forcar refresh de cache se preciso); audio toca em 2-3 apps; Spotify e Apple podem levar de minutos a horas.
- **T+24 h:** todas as plataformas Tier 1 mostram o episodio; analytics registrando downloads; nenhum erro reportado.

| Problema | Causa provavel | Correcao |
|----------|----------------|----------|
| Nao aparece no Apple | atraso de cache ou erro no RSS | aguardar ~6 h; se persistir, validar o feed |
| Audio nao toca | URL inacessivel, CORS, Content-Type | testar URL direto, conferir CDN e `audio/mpeg` |
| Capa errada | cache do app | refresh manual ou aguardar propagacao |
| Downloads zerados | prefixo de medicao ausente | conferir prefixos no enclosure |

## Criterios de Qualidade

- [ ] Audio masterizado correto
- [ ] Metadata completo e correto
- [ ] Cover art 3000x3000px
- [ ] Chapter markers adicionados
- [ ] Podcasting 2.0 tags (transcript, person)
- [ ] RSS feed validado (zero erros)
- [ ] Apareceu em Spotify dentro de 2h
- [ ] Apareceu em Apple dentro de 6h
- [ ] Show notes linkadas corretamente
