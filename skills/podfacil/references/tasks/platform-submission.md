---
task: Platform Submission
responsavel: "@distributor"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - rss-feed-url: URL pública do feed já validado (zero erros)
  - show-metadata: Nome, descrição, categorias, e-mail do owner, capa
  - target-platforms: Plataformas a cadastrar (padrão: Tier 1 + Tier 2)
Saida: |
  - platform-registry: Tabela plataforma → status, link público, data, conta usada
  - verification-log: Confirmação de que o episódio mais recente aparece em cada uma
Checklist:
  - "[ ] Feed validado (Cast Feed Validator ou Podbase) antes de qualquer submissão"
  - "[ ] E-mail de itunes:owner acessível (Apple e Spotify verificam por e-mail)"
  - "[ ] Tier 1 cadastrado: Apple Podcasts, Spotify, YouTube, Amazon Music"
  - "[ ] Tier 2 conferido: Overcast, Pocket Casts, Podcast Addict, Castbox"
  - "[ ] Podcast Index cadastrado (base dos apps Podcasting 2.0)"
  - "[ ] Categorias definidas por plataforma (Apple e Spotify usam taxonomias diferentes)"
  - "[ ] Registro atualizado com link público de cada plataforma"
  - "[ ] Links públicos entregues a Amp (growth) e ao site"
---

# *submit-platforms

Cadastra o podcast em plataformas novas a partir do mesmo RSS e registra onde ele está.

## Uso

```bash
# Lançamento: Tier 1 + Tier 2
*submit-platforms --tiers 1,2

# Expansão trimestral: plataformas específicas
*submit-platforms --platforms "deezer,iheartradio"
```

## Steps

1. **Pré-voo:** feed validado com zero erros, capa na spec (1400–3000 px, quadrada, RGB) e e-mail do owner acessível.
2. **Tier 1 (cadastro manual):** Apple Podcasts Connect, Spotify for Creators, YouTube (RSS ingestion ou upload), Amazon Music for Podcasters.
3. **Tier 2 (descoberta automática):** Overcast, Pocket Casts e Podcast Addict indexam via diretório da Apple/Podcast Index — só conferir que o show aparece; Castbox aceita submissão manual.
4. **Tier 3 / nicho:** Podcast Index, Deezer, iHeartRadio, TuneIn — avaliar retorno antes de cadastrar.
5. **Otimização por plataforma:** categorias corretas em cada uma; no YouTube, capítulos via timestamps na descrição e playlists.
6. **Registro:** atualizar a tabela de plataformas e passar os links para Amp.

Não submeter: Google Podcasts (descontinuado em 2024) e Stitcher (encerrado em 2023).

## Criterios de Qualidade

- [ ] Nenhuma submissão com feed inválido
- [ ] Toda plataforma cadastrada tem link público no registro
- [ ] Episódio mais recente visível em cada plataforma do registro
