---
task: Guest Booking
responsavel: "@guest-coordinator"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - guest-wishlist: Lista priorizada da season planning
  - episode-schedule: Calendario de gravacoes disponiveis
  - podcast-media-kit: Materiais de apresentacao do show
  - diversity-targets: Metas de diversidade da temporada
Saida: |
  - confirmed-guests: Lista de convidados confirmados com datas
  - outreach-log: Registro de todos os contatos realizados
  - tech-requirements-sent: Confirmacao de envio de specs tecnicas
  - pre-interview-notes: Anotacoes da pre-entrevista (OPCIONAL; so se houve call)
  - recording-mode: presencial | remoto (definido na confirmacao)
Checklist:
  - "[ ] Pesquisar guest (background, trabalho, contatos publicos)"
  - "[ ] Identificar melhor canal de outreach (email, DM, agente, mutual connection)"
  - "[ ] Enviar pitch personalizado (template + customizacao)"
  - "[ ] Follow-ups em E+3 a E+5 e E+10 (prazos canonicos: references/workflows/guest-pipeline.md)"
  - "[ ] Confirmar data/hora com fuso horario explicito e modo (presencial ou remoto)"
  - "[ ] Remoto: enviar tech requirements · Presencial: enviar logistica (endereco, acesso, chegada)"
  - "[ ] OPCIONAL: pre-interview por call (D-10 a D-7) — o formulario do convidado (F2) substitui"
  - "[ ] Enviar calendar invite (link da plataforma ou endereco)"
  - "[ ] Lembretes D-7, D-1 e 2h antes da gravacao"
---

# *guest-booking

Pipeline completo de guest booking, desde research inicial ate confirmacao e onboarding. Dono unico: @guest-coordinator. Prazos: tabela canonica em `references/workflows/guest-pipeline.md` (esta task nao os redefine). Gerencia outreach, follow-ups, scheduling e preparacao tecnica para garantir gravacoes sem fricao.

## Uso

```bash
# Iniciar booking de guest especifico
*guest-booking --guest "Maria Santos" --episode S02E03 --priority high

# Booking em lote para temporada
*guest-booking --season 2 --batch --targets 12

# Follow-up automatizado
*guest-booking --follow-up --guest "João Silva" --attempt 2

# Verificar diversity score da temporada
*guest-booking --diversity-check --season 2
```

## Steps

1. **Research do guest**
   - Google search: `"{nome guest}" + biografia`
   - LinkedIn: trabalho atual, trajetoria, conexoes mutuas
   - Twitter/Instagram: tom, temas que comenta, engajamento
   - Podcast Addict / Apple Podcasts: ja foi guest em outros shows?
   - Website pessoal: contato publico, assessoria, agente
   - Tempo investido: 15-30min por guest

2. **Identificar melhor canal de outreach**

   **Hierarquia de eficacia:**
   1. **Warm intro** (conexao mutua) - 60% response rate
   2. **Email direto** (se publico) - 30% response rate
   3. **DM Instagram/Twitter** - 20% response rate
   4. **LinkedIn InMail** - 15% response rate
   5. **Agente/Assessoria** - 10% response rate (mas mais profissional)

   **Como pedir warm intro:**
   - Identificar conexao mutua no LinkedIn
   - Mensagem curta: "Oi {conexao}, estou produzindo podcast sobre {tema} e adoraria conversar com {guest}. Voce pode fazer uma intro?"

3. **Criar pitch personalizado**

   **Template base:**
   ```
   Assunto: Convite para [Nome do Podcast] - [Topico Especifico]

   Oi {Nome},

   Meu nome e {Host/Produtor}, e produzo o [Nome do Podcast], um show sobre {tema} com {numero} ouvintes mensais.

   Estou preparando um episodio sobre {topico especifico} e voce seria a pessoa PERFEITA para essa conversa por causa de {razao personalizada - trabalho/artigo/fala especifica}.

   Algumas perguntas que adoraria explorar:
   - {Pergunta 1 provocativa}
   - {Pergunta 2 relevante}
   - {Pergunta 3 unica}

   A gravacao e {presencial no nosso estudio em {cidade} | remota pelo {Zoom/Riverside}}, dura {X minutos}, e podemos encaixar na sua agenda entre {datas disponiveis}.

   Guests anteriores: {Nome 1}, {Nome 2}, {Nome 3} [social proof]

   Toparia?

   Abraco,
   {Assinatura}
   ```

   **Customizacao obrigatoria:**
   - Mencionar trabalho/artigo/fala ESPECIFICA do guest
   - Mostrar que voce fez homework (nao e template massivo)
   - Perguntas relevantes ao trabalho atual dele
   - Datas especificas (nao "quando voce puder")

4. **Follow-up estrategico**

   **Timeline (canonica, `references/workflows/guest-pipeline.md`):**
   - Envio inicial: E
   - Follow-up 1: E+3 a E+5 (se sem resposta)
   - Follow-up 2: E+10 (ultimo follow-up)
   - Apos isso: mover para "nao respondeu" e tentar guest backup

   **Template follow-up:**
   ```
   Oi {Nome},

   Sei que inbox fica cheio. Estava pensando se viu meu email sobre [Topico] no [Nome Podcast].

   Se nao rolar, tudo bem! Mas se voce topar, vai ser uma conversa incrivel.

   Abraco,
   {Assinatura}
   ```

5. **Confirmar scheduling e modo de gravacao**
   - Usar Calendly ou similar para guest escolher horario
   - SEMPRE incluir fuso horario explicito (ex: "14h BRT / 13h EST")
   - Perguntar ao convidado: presencial ou remoto? (nao presumir remoto)
   - Enviar calendar invite com:
     - Remoto: link do Zoom/Riverside · Presencial: endereco, acesso, estacionamento, horario de chegada
     - Duracao estimada
     - Documentos de prep (optional)
   - Confirmar por email: "Confirmado! {Dia} as {hora} {fuso}. Link: {url}"

6. **Enviar tech requirements (remoto) ou logistica (presencial)**

   **Presencial:** endereco completo, como entrar no predio, estacionamento, acessibilidade,
   chegar 15min antes, contato de emergencia no dia. Nao enviar specs de mic/internet.

   **Remoto — email com specs tecnicas:**
   ```
   Oi {Nome},

   Animado para nossa conversa! Algumas dicas tecnicas para melhor qualidade:

   🎙️ MIC: Se tiver mic externo (Blue Yeti, Shure, etc), otimo. Se nao, AirPods funcionam bem.

   🎧 FONE: Use fone/headset para evitar eco.

   📍 AMBIENTE: Lugar silencioso (feche janelas, desligue AC/ventilador se possivel).

   📶 INTERNET: Wifi forte ou cabo ethernet (evite celular).

   💻 PLATAFORMA: Vamos usar {Riverside/Zoom/etc}. Link: {url}

   🧪 TESTE: Podemos fazer teste rapido 10min antes se quiser.

   Qualquer duvida, so gritar!

   Abraco,
   {Assinatura}
   ```

7. **Pre-interview por call — OPCIONAL (D-10 a D-7)**
   - O formulario do convidado (F2, `guest-intake`) substitui a call como fonte de bio,
     topicos, limites e logistica. Fazer a call so quando agrega: convidado desconhecido,
     tema sensivel, ou preferencia do proprio convidado.
   - Se fizer: chamada de 20-30min
   - Objetivos:
     - Alinhar expectativas (duracao, formato, topicos)
     - Remoto: testar setup tecnico (audio, video, conexao)
     - Fazer rapport (deixar guest confortavel)
     - Identificar areas sensiveis (o que evitar)
     - Confirmar data/hora final
   - Tomar notas em `/guests/{nome-guest}/pre-interview-notes.md`

8. **Lembretes automatizados (D-7, D-1, 2h antes)**
   - D-7: "Oi {Nome}, nossa gravacao e em uma semana ({dia} as {hora}). {Link ou endereco}"
   - D-1: "Oi {Nome}, lembrando da nossa gravacao {dia} as {hora}. Link: {url}"
   - 2h antes: remoto "Oi {Nome}, em 2h! Link: {url}. Testou o audio?" · presencial "Oi {Nome}, te esperamos as {hora} em {endereco}. Qualquer imprevisto, me chama."

9. **Diversity check**
   - Ao final de cada onda de booking, validar por criterios nao sensiveis
     (`references/checklists/diversity-check.md`):
     - Geografia: nao concentrar em 1 cidade/pais
     - Area e tipo de organizacao: variedade de setores
     - Senioridade/trajetoria: nao so C-level
     - Estreantes: convidados que nunca foram a podcast
     - Pensamento: variedade de perspectivas (evitar echo chamber)
   - **Nunca inferir** raca/etnia, genero, orientacao sexual, deficiencia ou outro atributo
     sensivel do convidado (LGPD art. 5, II e art. 11). Representatividade de identidade so
     por autodeclaracao voluntaria e opcional no formulario do convidado, com aviso de dado
     sensivel, e so em agregado da temporada
   - Se fora dos targets, ajustar proxima onda

## Output

### outreach-log.md

```markdown
# Guest Booking Log - Season 2

## Confirmed (6/12)

| Guest | Episodio | Data Gravacao | Status | Notes |
|-------|----------|---------------|--------|-------|
| Maria Santos | S02E03 | 2026-03-15 14h BRT | ✅ Confirmed | Pre-interview: 2026-03-08 |
| João Silva | S02E05 | 2026-03-22 16h BRT | ✅ Confirmed | Warm intro via Ana Costa |

## Awaiting Response (3/12)

| Guest | Outreach Date | Last Follow-up | Next Action | Channel |
|-------|---------------|----------------|-------------|---------|
| Pedro Lima | 2026-02-10 | 2026-02-13 | Follow-up 2 em 2026-02-20 | Email |
| Carla Rocha | 2026-02-11 | - | Follow-up 1 em 2026-02-16 | LinkedIn |

## Declined / No Response (3/12)

| Guest | Status | Reason | Backup |
|-------|--------|--------|--------|
| Paulo Mendes | Declined | Sem tempo Q1/2026 | Tentar Q3 |
| Ana Costa | No response | 2 follow-ups sem retorno | Mover para Tier B |

## Diversity Scorecard

| Metric (nao sensivel) | Current | Target | Status |
|--------|---------|--------|--------|
| Fora do Sudeste | 4/12 (33%) | 20%+ | ✅ |
| Junior/Mid-level | 3/12 (25%) | 30%+ | ⚠️ Ajustar |
| Areas distintas | 5 | 4+ | ✅ |
| Estreantes em podcast | 4/12 (33%) | 25%+ | ✅ |
| Internacional | 2/12 (17%) | 20%+ | ⚠️ Ajustar |

Autodeclaracao voluntaria (agregado, so se coletada; dimensao com <5 respostas nao e reportada).
```

### guests/{nome-guest}/pre-interview-notes.md

```markdown
# Pre-Interview: Maria Santos

**Data:** 2026-03-08
**Duracao:** 25min
**Condutor:** @guest-coordinator

## Setup Tecnico
- ✅ Mic: Shure MV7
- ✅ Fone: Sony WH-1000XM4
- ✅ Internet: 100Mbps fibra
- ✅ Ambiente: Home office silencioso
- ✅ Plataforma: Riverside testado, tudo OK

## Expectativas Alinhadas
- Duracao: 45-50min
- Formato: Conversacional, nao entrevista formal
- Edicao: Pode cortar se falar algo errado
- Lancamento: ~10 dias apos gravacao

## Topicos Confirmados
1. ✅ Trajetoria em IA
2. ✅ Projeto atual em NLP
3. ✅ Etica em modelos generativos
4. ⚠️ Evitar: Empresa anterior (NDA)

## Vibe Check
- Comunicativa, energetica
- Gosta de contar historias pessoais
- Pode precisar de nudge para ser mais sucinta (tende a divagar)

## Proximos Passos
- ✅ Enviar briefing final 48h antes
- ✅ Reminder 2h antes da gravacao
```

## Criterios de Qualidade

- [ ] Research de 15-30min por guest antes de outreach
- [ ] Pitch 100% personalizado (menciona trabalho especifico do guest)
- [ ] Follow-up timeline respeitado (E+3 a E+5, E+10)
- [ ] Modo de gravacao (presencial/remoto) confirmado com o convidado
- [ ] Remoto: tech requirements no kit (D-14 a D-7) · Presencial: logistica confirmada D-3
- [ ] Calendar invite com fuso horario explicito
- [ ] Lembretes automatizados (D-7, D-1, 2h antes)
- [ ] Pre-interview notes documentadas (so se houve call)
- [ ] Diversity check validado ao final de cada onda de booking (criterios nao sensiveis; nada inferido)
- [ ] Outreach log atualizado em tempo real
- [ ] Response rate > 25% (benchmark industria)
- [ ] No-show rate < 5% (sinal de bom processo)
