---
task: Show Notes Writing
responsavel: "@editor"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - transcript-clean: Transcricao limpa do episodio
  - episode-brief: Briefing original com key takeaways
  - links-mentioned: Lista de links mencionados no episodio
  - guest-info: Bio e links do convidado
Saida: |
  - show-notes-md: Show notes em Markdown
  - show-notes-html: Show notes em HTML (para web)
  - chapter-markers: Chapter markers com timestamps
  - seo-metadata: Title, description, keywords
Checklist:
  - "[ ] Titulo otimizado para SEO (H1 com keyword)"
  - "[ ] Descricao curta (160 caracteres para meta description)"
  - "[ ] Key takeaways em bullet points (3-5)"
  - "[ ] Timestamps clicaveis com chapter markers"
  - "[ ] Links mencionados no episodio"
  - "[ ] Bio do guest com links sociais"
  - "[ ] CTAs claros (avaliar, inscrever, compartilhar)"
  - "[ ] Keywords para SEO (5-8 keywords)"
---

# *show-notes

Criacao de show notes otimizadas para SEO e UX. H1 com keyword, timestamps clicaveis, key takeaways, links, bio do guest, chapter markers para Podcasting 2.0.

## Uso

```bash
# Show notes standard
*show-notes --episode S02E03 --seo-optimized

# Show notes minimalistas
*show-notes --episode S02E05 --format minimal

# Show notes com transcript embedded
*show-notes --episode S02E08 --include-transcript
```

## Steps (Resumido)

1. **Titulo SEO (H1)**
   - Formato: `{Topico} com {Guest} | {Nome Podcast} S0{N}E0{N}`
   - Exemplo: "IA e Etica com Maria Santos | TechTalks S02E03"
   - Incluir keyword principal

2. **Descricao curta (160 char)**
   - Para meta description e iTunes
   - Incluir hook + value promise

3. **Key takeaways (3-5 bullets)**
   - Principais insights do episodio
   - Formato scannable

4. **Timestamps clicaveis**
   ```
   00:00 - Introducao
   02:30 - Trajetoria de Maria em IA
   08:15 - Projeto SentimentAI
   ```

5. **Links mencionados**
   - Livros, artigos, tools, pessoas citadas
   - Formato: `[Texto do link](url)`

6. **Bio do guest**
   - 2-3 frases
   - Links: Twitter, LinkedIn, site

7. **CTAs**
   - Avaliar no Apple Podcasts
   - Inscrever no feed
   - Compartilhar episodio

## Output (Template)

```markdown
# IA e Etica com Maria Santos | TechTalks S02E03

Neste episodio, conversamos com Maria Santos, cientista de dados e fundadora da SentimentAI, sobre os desafios eticos de usar IA para analisar saude mental em redes sociais.

## Key Takeaways

- IA pode detectar sinais de depressao com 85% de accuracy, mas levanta questoes de privacidade
- Regulacao de IA precisa equilibrar inovacao e protecao de dados
- Bias em modelos de NLP e um problema sistematico que requer diversidade nas equipes

## Timestamps

- [00:00](link) Introducao
- [02:30](link) Trajetoria de Maria
- [08:15](link) SentimentAI
- [18:40](link) Etica em IA
- [28:00](link) Proximos passos

## Sobre Maria Santos

Maria Santos e cientista de dados com PhD pela USP e 12 anos de experiencia em NLP. Fundadora da SentimentAI, startup que usa IA para prevenir crises de saude mental.

- Twitter: [@mariasantos](url)
- LinkedIn: [Maria Santos](url)
- Site: [sentimentai.com](url)

## Links Mencionados

- [Paper: "Ethics in AI"](url)
- [Livro: "Weapons of Math Destruction"](url)
- [Tool: Hugging Face](url)

## Inscreva-se

- [Apple Podcasts](link)
- [Spotify](link)
- [YouTube](link)

---

Gostou? Avalie 5 estrelas no Apple Podcasts!
```

## Criterios de Qualidade

- [ ] Titulo com keyword principal (SEO)
- [ ] Descricao <160 caracteres
- [ ] 3-5 key takeaways claros
- [ ] Timestamps clicaveis (chapter markers)
- [ ] Links funcionando (verificar 404)
- [ ] Bio do guest com links sociais
- [ ] CTAs claros e acionaveis
- [ ] Keywords para SEO incluidas naturalmente
