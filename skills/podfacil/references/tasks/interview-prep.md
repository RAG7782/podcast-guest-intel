---
task: Interview Prep
responsavel: "@guest-coordinator"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - guest-info: Dados do convidado (bio, trabalho, social media)
  - episode-brief: Research completo do topico
  - pre-interview-notes: Anotacoes da pre-entrevista (OPCIONAL; a call deixou de ser obrigatoria)
  - host-style: Tom e estilo do host conforme podcast-bible
Saida: |
  - host-briefing: Documento de prep para o host (1-2 paginas)
  - question-bank: 20-25 perguntas estrategicas
  - red-flags: Lista de areas a evitar
  - guest-review-protocol: Documento enviado ao guest sobre edicao
Checklist:
  - "[ ] Compilar bio detalhada do guest (trajetoria, conquistas)"
  - "[ ] Listar trabalhos relevantes (livros, artigos, palestras, projetos)"
  - "[ ] Criar question bank com 20-25 perguntas abertas"
  - "[ ] Marcar 5-7 perguntas essenciais (nao podem ficar de fora)"
  - "[ ] Identificar red flags (topicos sensiveis, NDAs, controversias)"
  - "[ ] Preparar perguntas provocativas (2-3) para depth"
  - "[ ] Criar follow-up questions para respostas previsiveis"
  - "[ ] Enviar guest-review-protocol explicando edicao"
  - "[ ] Briefing final ao host 48h antes da gravacao"
  - "[ ] Tech check 10min antes da gravacao"
---

# *interview-prep

Preparacao completa do host para entrevista de alta qualidade. Transforma research e pre-interview em briefing acionavel com perguntas estrategicas, red flags mapeadas e protocolos de edicao alinhados com o guest.

## Uso

```bash
# Prep para entrevista confirmada
*interview-prep --episode S02E03 --guest "Maria Santos" --date "2026-03-15"

# Prep urgente (guest confirmado last minute)
*interview-prep --episode S02E08 --guest "João Silva" --fast-track --deadline "24h"

# Prep para mesa-redonda (multiplos guests)
*interview-prep --episode S02E12 --format roundtable --guests "Ana,Pedro,Carla"
```

## Steps

1. **Compilar contexto completo do guest**
   - Ler pre-interview notes
   - Revisar episode-brief
   - Pesquisar trabalho recente do guest (ultimos 6 meses):
     - Livros/artigos publicados
     - Palestras/entrevistas em outros shows
     - Projetos atuais
     - Premios/reconhecimentos
   - Identificar unique angle: o que NINGUEM perguntou ainda?

2. **Criar bio executiva (1 paragrafo)**
   - Trajetoria resumida (origem → presente)
   - Principais conquistas
   - Por que essa pessoa importa para o topico
   - Credibilidade (titulos, empresas, reconhecimentos)

3. **Desenvolver question bank (20-25 perguntas)**

   **Estrutura estrategica:**

   **WARMUP (3-5 perguntas):**
   - Perguntas faceis para relaxar
   - Exemplo: "Como voce chegou ate aqui?" / "Conte-me sobre sua trajetoria"
   - Objetivo: criar rapport, deixar guest confortavel

   **CORE (12-15 perguntas):**
   - Perguntas abertas sobre o topico principal
   - Usar "como", "por que", "conte-me sobre" (evitar sim/nao)
   - Sequencia logica (do geral ao especifico)
   - Exemplo: "Como voce identifica que uma ideia vale a pena?" em vez de "Voce testa ideias?"

   **PROVOCATIVE (2-3 perguntas):**
   - Perguntas desconfortaveis/controversas
   - Desafiar consenso
   - Exemplo: "Muita gente diz X, mas voce defende Y. Por que eles estao errados?"
   - Marcar com ⚠️ no briefing

   **CLOSING (2-3 perguntas):**
   - Perguntas sobre futuro/visao
   - Lightning round (respostas rapidas)
   - Exemplo: "Se voce pudesse dar um conselho ao seu eu de 10 anos atras?"

4. **Marcar perguntas essenciais**
   - Identificar 5-7 perguntas que NAO PODEM ficar de fora
   - Marcar com ⭐ no briefing
   - Orientar host: "Se o tempo apertar, priorize essas"

5. **Preparar follow-up questions**
   - Para cada pergunta core, criar 2-3 follow-ups
   - Antecipar respostas genericas
   - Exemplo:
     - Pergunta: "Como voce lida com fracasso?"
     - Resposta generica: "Aprendo com os erros"
     - Follow-up: "Me conta um erro especifico e o que exatamente voce aprendeu"

6. **Mapear red flags**
   - Topicos a evitar (NDAs, processos legais, traumas pessoais)
   - Controversias conhecidas
   - Areas onde guest pode ter vies forte
   - Vieses do proprio host (confirmar neutralidade)
   - Documentar em secao RED FLAGS ⚠️

7. **Preparar guest-review-protocol**
   - Documento explicando processo de edicao
   - Enviar 48h antes da gravacao
   - Conteudo:
     - Como funciona edicao (cortes de fillers, hesitacoes, erros)
     - Guest pode pedir cortes de trechos especificos
     - Timeline de review (48h para aprovar ou pedir ajustes)
     - Lancamento so acontece apos aprovacao
   - Objetivo: deixar guest tranquilo e evitar surpresas

8. **Criar briefing final para o host**
   - Documento de 1-2 paginas, maximo 1000 palavras
   - Formato scannable (bullets, negrito, headings)
   - Incluir:
     - Bio executiva do guest
     - Question bank completa
     - Red flags ⚠️
     - Perguntas essenciais ⭐
     - Vibe check da pre-interview
     - Timecodes sugeridos
   - Enviar 48h antes para o host absorver

9. **Tech check pre-gravacao**
   - 10 minutos antes da gravacao:
   - Confirmar guest online
   - Testar audio (pedir para falar, checar levels)
   - Testar video (se aplicavel)
   - Confirmar ambiente silencioso
   - Relembrar duracao estimada
   - Deixar guest confortavel: "Pode interromper se precisar de agua, pausa, etc"

## Output

### host-briefing-S0{N}E0{N}.md

```markdown
# Host Briefing: S02E03 - Maria Santos

**Data Gravacao:** 2026-03-15 14h BRT
**Duracao Target:** 50min
**Formato:** Entrevista conversacional

---

## Bio Executiva (READ THIS FIRST)

Maria Santos e cientista de dados especializada em NLP (processamento de linguagem natural) com 12 anos de experiencia. PhD pela USP, trabalhou no Google AI por 5 anos liderando equipe de 20 pesquisadores. Atualmente fundadora da SentimentAI, startup que usa IA para analise de saude mental em redes sociais (Series A de $8M em 2025). Autora de 30+ papers citados 2.000+ vezes. Conhecida por defender etica rigorosa em IA.

**Por que ela importa:** Intersecao unica de pesquisa academica, experiencia Big Tech e empreendedorismo de impacto social.

---

## Vibe Check (Pre-Interview)

- Comunicativa, energetica, gosta de contar historias
- Tende a divagar → pode precisar de nudge gentil para voltar ao ponto
- MUITO apaixonada por etica em IA (traz isso naturalmente)
- Tranquila com pausas/cortes na edicao

---

## RED FLAGS ⚠️

1. **Empresa anterior (Google):** Nao pode detalhar projetos especificos (NDA)
2. **Politica partidaria:** Evitar perguntas sobre partidos (ela e vocal em questoes sociais, mas nao partidaria)
3. **Co-fundador:** Separacao nao foi amigavel, nao mencionar

---

## Question Bank

### WARMUP (3 perguntas - 5min)

1. **Como voce foi parar em IA?**
   - Deixar ela contar a historia (origem → presente)

2. **O que te fascina em NLP especificamente?**
   - Rapport, aquecimento

3. **Como foi a transicao de Google para startup?**
   - Ultimas perguntas antes de entrar no core

---

### CORE (12 perguntas - 35min)

⭐ = Essencial (nao pode ficar de fora)

4. ⭐ **Voce analisa textos de redes sociais para detectar sinais de depressao/ansiedade. Como voce equilibra utilidade vs invasao de privacidade?**
   - Follow-up se resposta generica: "Me da um exemplo concreto de uma decisao dificil que voce teve que tomar"

5. ⭐ **Seu modelo detectou 10.000 usuarios com risco de suicidio. O que voce FAZ com essa informacao?**
   - Pergunta provocativa, mas essencial

6. **Modelos de linguagem como GPT-4 estao ficando incrivelmente bons. Qual o risco que ninguem esta falando?**

7. **Voce defendeu publicamente regulacao mais forte de IA. Por que?**
   - Follow-up: "Empresas de IA dizem que regulacao vai matar inovacao. O que voce responde?"

8. ⭐ **Conte-me sobre um erro grande que voce cometeu no Google e o que aprendeu.**
   - Depth, vulnerabilidade

9. **SentimentAI levantou $8M. Como voce usa esse dinheiro?**
   - Context de startup

10. **Se amanha GPT-5 resolve NLP completamente, o que voce faz?**
    - Visao de futuro

11. ⚠️ **Muita gente acha que IA vai substituir terapeutas. Voce concorda?**
    - Provocativa, desafia consenso

12. **Qual metrica voce acompanha diariamente na SentimentAI?**
    - Pragmatica, operacional

13. **Voce tem 3 filhos pequenos. Como equilibra startup founder com maternidade?**
    - Humaniza, relatable (ela e aberta sobre isso publicamente)

14. ⭐ **O que voce gostaria que pesquisadores de IA entendessem sobre saude mental?**
    - Bridge entre as duas areas

15. **Bias em modelos de IA: como voce detecta e corrige?**
    - Tecnica, mas acessivel

---

### CLOSING (3 perguntas - 10min)

16. **Daqui 10 anos, como a IA vai ter mudado saude mental?**
    - Visao de futuro

17. **Lightning round (resposta rapida):**
    - Livro que mudou sua vida?
    - Conselho para alguem entrando em IA hoje?
    - Uma coisa que voce gostaria de desaprender?

18. ⭐ **Onde as pessoas podem encontrar seu trabalho?**
    - CTA, links

---

## Timecodes Sugeridos

| Bloco | Tempo | Perguntas |
|-------|-------|-----------|
| Warmup | 0-5min | 1-3 |
| Core | 5-40min | 4-15 |
| Closing | 40-50min | 16-18 |

**IMPORTANTE:** Se passar dos 50min, cortar perguntas nao-essenciais (sem ⭐).

---

## Guest Review Protocol

✅ ENVIADO em 2026-03-13 (confirmado recebido)

Maria vai receber edicao inicial 48h apos gravacao. Ela pode pedir cortes de trechos especificos. Timeline: 48h para review.

---

## Tech Checklist (10min antes)

- [ ] Guest online?
- [ ] Audio clear? (pedir para falar)
- [ ] Video OK? (se aplicavel)
- [ ] Ambiente silencioso?
- [ ] Relembrar duracao (50min)
- [ ] "Pode interromper se precisar de agua/pausa"

---

**Preparado por:** @guest-coordinator
**Data:** 2026-03-13
**Versao:** 1.0
```

### guest-review-protocol.md

```markdown
# Guest Review Protocol

Oi {Nome Guest},

Animado para nossa gravacao! Queria alinhar como funciona nosso processo de edicao para voce ficar tranquilo:

## Como Funciona a Edicao

1. **Apos a gravacao**, nossa equipe vai:
   - Cortar hesitacoes, fillers ("ahh", "humm", repeticoes)
   - Remover erros tecnicos (ruidos, interrupcoes)
   - Ajustar niveis de audio para clareza

2. **Voce recebe um DRAFT** 48h apos a gravacao:
   - Link privado para ouvir
   - Pode pedir cortes de trechos especificos
   - Pode pedir ajustes de contexto

3. **Voce tem 48h para revisar** e pedir ajustes:
   - Responda com timestamp do que quer ajustar
   - Ex: "Cortar 12:30-13:15 (falei informacao errada)"

4. **Lancamento so acontece apos sua aprovacao final.**

## O Que Cortamos vs O Que Mantemos

✅ **Cortamos:**
- Fillers excessivos ("ahh", "tipo", "sabe")
- Erros factuais que voce pede para cortar
- Informacoes sensiveis (NDAs, etc)

❌ **Nao cortamos (a menos que voce peça):**
- Opinioes controversas (desde que nao sejam difamatorias)
- Pausas naturais de pensamento
- "Erros" que humanizam (contanto que nao sejam constrangedores)

## Por Que Fazemos Isso

Queremos que voce soe como a MELHOR versao de voce mesmo, nao uma versao falsa. A edicao remove friccoes tecnicas, mas mantem sua autenticidade.

## Duvidas?

Qualquer duvida, so me chamar: {email} ou {telefone}

Abraco,
{Produtor}
```

## Criterios de Qualidade

- [ ] Bio executiva do guest em 1 paragrafo (clara e impactante)
- [ ] Question bank com 20-25 perguntas abertas
- [ ] 5-7 perguntas essenciais marcadas com ⭐
- [ ] 2-3 perguntas provocativas marcadas com ⚠️
- [ ] Follow-ups preparados para respostas genericas
- [ ] Red flags mapeadas e documentadas
- [ ] Vibe check da pre-interview incluido
- [ ] Timecodes sugeridos para blocos (warmup, core, closing)
- [ ] Guest-review-protocol enviado 48h antes
- [ ] Briefing entregue ao host 48h antes da gravacao
- [ ] Tech checklist preparado para 10min pre-gravacao
- [ ] Formato scannable (maximo 2 paginas, bullets, negrito)
