---
task: Newsletter Edition
responsavel: "@growth"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - episode-highlights: Destaques do episodio
  - behind-scenes: Bastidores da producao
  - community-content: Listener spotlights, polls
  - cta: CTA principal (review, share, join)
Saida: |
  - newsletter-html: Newsletter em HTML
  - subject-line: Subject line otimizado (open rate)
  - preview-text: Preview text (mobile)
  - send-schedule: Horario de envio otimizado
Checklist:
  - "[ ] Subject line chamativo (<50 caracteres)"
  - "[ ] Preview text otimizado"
  - "[ ] Destaques do episodio (bullets)"
  - "[ ] Behind the scenes (humaniza)"
  - "[ ] Links uteis mencionados"
  - "[ ] Listener spotlight (engaja comunidade)"
  - "[ ] CTA claro (review, share, join Discord)"
  - "[ ] Envio em horario otimizado (Terca 10am)"
---

# *newsletter-edition

Criacao de newsletter semanal/quinzenal via Substack ou Beehiiv. Destaques do episodio, behind the scenes, listener spotlight, CTA. Open rate target: 40%+.

## Uso

```bash
# Newsletter semanal
*newsletter-edition --week 12 --episodes "S02E03,S02E04" --frequency weekly

# Newsletter quinzenal
*newsletter-edition --month march --episodes "S02E03-S02E06" --frequency biweekly

# Special edition (announcement)
*newsletter-edition --type special --announcement "Season 3 coming"
```

## Steps (Resumido)

1. **Subject line (<50 char)**
   - Curiosity-driven
   - Exemplo: "O erro de $2M que mudou tudo"

2. **Preview text**
   - Complementa subject
   - Visivel em mobile

3. **Destaques episodio**
   ```
   Neste episodio:
   - Por que 70% das startups falham
   - O framework dos 3Cs
   - Como testar ideias em 48h
   ```

4. **Behind the scenes**
   - Humanizar
   - Exemplo: "Gravamos este episodio as 2am porque..."

5. **Links uteis**
   - Livros, tools, artigos mencionados

6. **Listener spotlight**
   - Destacar membro da comunidade
   - Review da semana

7. **CTA**
   - Avaliar podcast
   - Compartilhar episodio
   - Juntar Discord

8. **Send schedule**
   - Melhor dia: Terca-feira
   - Melhor horario: 10am (fuso local)

## Criterios de Qualidade

- [ ] Subject line <50 caracteres
- [ ] Open rate >40%
- [ ] Click-through rate >10%
- [ ] Destaques claros (bullets)
- [ ] Behind the scenes incluido
- [ ] Listener spotlight (engaja)
- [ ] CTA claro e unico
- [ ] Enviado em horario otimizado
