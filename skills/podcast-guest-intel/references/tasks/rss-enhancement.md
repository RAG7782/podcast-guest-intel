---
task: RSS Enhancement (Podcasting 2.0)
responsavel: "@distributor"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - rss-feed-url: URL do feed RSS atual
  - transcript-files: Transcricoes em JSON/VTT
  - chapter-markers: Chapter markers JSON
  - participant-info: Dados de host/guests
Saida: |
  - enhanced-rss: Feed RSS com Podcasting 2.0 tags
  - transcript-urls: URLs dos transcripts hospedados
  - funding-tag: Tag de financiamento (Value4Value)
  - validation-report: Relatorio de validacao do feed
Checklist:
  - "[ ] Adicionar podcast:transcript tag"
  - "[ ] Adicionar podcast:chapters tag"
  - "[ ] Adicionar podcast:person tag (host, guests)"
  - "[ ] Adicionar podcast:funding (V4V, Patreon)"
  - "[ ] Adicionar podcast:value (Bitcoin Lightning)"
  - "[ ] Adicionar podcast:soundbite (clips)"
  - "[ ] Migrar feed para dominio proprio (nao 3rd party)"
  - "[ ] Configurar redirect 301 (se migrou)"
  - "[ ] Validar com Podbase Validator"
---

# *rss-enhancement

Implementacao completa de Podcasting 2.0 tags no RSS feed: transcript, chapters, person, funding, value (V4V), soundbite. Feed proprio em dominio proprio.

## Uso

```bash
# Adicionar Podcasting 2.0 tags ao feed
*rss-enhancement --feed-url "https://podcast.com/feed.xml" --add-all-tags

# Migrar feed para dominio proprio
*rss-enhancement --migrate-feed --old-url "feeds.libsyn.com/xyz" --new-url "podcast.com/feed"

# Validar feed Podcasting 2.0
*rss-enhancement --validate-only --feed-url "https://podcast.com/feed.xml"
```

## Steps (Resumido)

1. **podcast:transcript**
   ```xml
   <podcast:transcript url="https://podcast.com/transcripts/S02E03.json" type="application/json" />
   ```

2. **podcast:chapters**
   ```xml
   <podcast:chapters url="https://podcast.com/chapters/S02E03.json" type="application/json+chapters" />
   ```

3. **podcast:person**
   ```xml
   <podcast:person role="host" img="https://..." href="https://...">Nome Host</podcast:person>
   <podcast:person role="guest" img="https://..." href="https://...">Maria Santos</podcast:person>
   ```

4. **podcast:funding (V4V)**
   ```xml
   <podcast:funding url="https://patreon.com/xyz">Support via Patreon</podcast:funding>
   <podcast:funding url="https://buymeacoffee.com/xyz">Buy me a coffee</podcast:funding>
   ```

5. **podcast:value (Bitcoin Lightning)**
   ```xml
   <podcast:value type="lightning" method="keysend" suggested="0.00000005000">
     <podcast:valueRecipient type="node" address="...">Host</podcast:valueRecipient>
   </podcast:value>
   ```

6. **podcast:soundbite (clips)**
   ```xml
   <podcast:soundbite startTime="750" duration="60" title="Quote viral sobre IA" />
   ```

7. **Feed proprio em dominio proprio**
   - Migrar de `feeds.libsyn.com/xyz` para `podcast.com/feed`
   - Configurar redirect 301 (importante!)
   - Atualizar URL em Apple/Spotify

8. **Validar feed**
   - Podbase Validator: <https://podbase.org/validate>
   - Cast Feed Validator
   - Zero erros criticos

## Criterios de Qualidade

- [ ] podcast:transcript adicionado
- [ ] podcast:chapters adicionado
- [ ] podcast:person para host + guests
- [ ] podcast:funding configurado
- [ ] podcast:value (V4V) opcional
- [ ] podcast:soundbite para clips virais
- [ ] Feed em dominio proprio (nao 3rd party)
- [ ] Redirect 301 configurado (se migrou)
- [ ] Validado sem erros (Podbase)
