# Workflow: Guest Pipeline

## Visao Geral
- **Objetivo:** Identificar, contatar, preparar e gravar com convidados ideais
- **SLA Total:** 14-21 dias (do research ao follow-up pos-gravacao)
- **Owner:** @guest-coordinator (dono unico do fluxo de convidado; demais agentes executam etapas sob a coordenacao dele)
- **Modo de gravacao:** `presencial` ou `remoto`, definido na Etapa 4. Etapas e checklists que so valem para um modo estao marcadas.

## Prazos canonicos (fonte unica)

Esta tabela e a unica fonte de prazos do fluxo. `references/tasks/guest-booking.md` e
`references/checklists/onboarding-convidado.md` referenciam estes numeros e nao os redefinem.
`D` = dia da gravacao; `E` = dia do envio do convite.

| Marco | Prazo | Dono | Executa |
|---|---|---|---|
| Shortlist de convidados | 3 dias | @guest-coordinator | @researcher (apoio de pesquisa) |
| Convite enviado | E | @guest-coordinator | |
| Follow-up 1 | E+3 a E+5 | @guest-coordinator | |
| Follow-up 2 (ultimo) | E+10 | @guest-coordinator | |
| Sem resposta → backup (tier B) | E+11 | @guest-coordinator | |
| Data/hora + modo confirmados | ate 1 dia apos o aceite | @guest-coordinator | |
| Kit de onboarding enviado (inclui termo de autorizacao) | D-14 a D-7 | @guest-coordinator | |
| Pre-entrevista por call (**OPCIONAL**) | D-10 a D-7 | @guest-coordinator | |
| Remoto: tech check | D-5 a D-3 | @guest-coordinator | @engineer |
| Presencial: logistica confirmada (endereco, acesso, estacionamento, chegada) | D-3 | @guest-coordinator | |
| Briefing final ao host | D-2 (48h antes) | @guest-coordinator | |
| Lembretes ao convidado | D-7, D-1 e 2h antes | @guest-coordinator | |
| Gravacao | D | @guest-coordinator | @host + @engineer |
| Agradecimento + data estimada de publicacao | D+1 (24h) | @guest-coordinator | |

**Pre-entrevista por call e opcional.** O formulario do convidado (fatia F2,
`guest-intake`) substitui a call como fonte de bio, topicos, limites e logistica. A
call fica como enriquecimento: convidado desconhecido, tema sensivel, ou quando o
proprio convidado prefere conversar.

## Etapas

### Etapa 1: Research Guest
- **Owner:** @guest-coordinator + @researcher
- **SLA:** 3 dias
- **Entrada:** Content calendar, audience requests, industry trends
- **Saida:** Shortlist de 5-10 guests potenciais
- **Checklist:**
  - [ ] Identificar guests por tema/episodio
  - [ ] Pesquisar background (credenciais, publicacoes, talks)
  - [ ] Avaliar fit com podcast bible (valores, audiencia)
  - [ ] Verificar diversidade por criterios nao sensiveis (checklist diversity-check.md; nunca inferir atributo sensivel)
  - [ ] Buscar contato (email, LinkedIn, agente)
  - [ ] Priorizar shortlist (A, B, C tier)
  - [ ] Documentar em guest database

### Etapa 2: Outreach
- **Owner:** @guest-coordinator
- **SLA:** 2 dias
- **Entrada:** Shortlist aprovada
- **Saida:** Email de convite enviado
- **Checklist:**
  - [ ] Personalizar email template por guest
  - [ ] Incluir: sobre o podcast, por que esse guest, topicos, formato
  - [ ] Anexar: media kit, episodios recentes, listener demographics
  - [ ] Mencionar guests anteriores (social proof)
  - [ ] Sugerir 3 datas possiveis
  - [ ] Enviar para tier A primeiro
  - [ ] Tier B so apos o ciclo de follow-up do tier A (ver prazos canonicos)

### Etapa 3: Follow-up
- **Owner:** @guest-coordinator
- **SLA:** ate E+10 (2 follow-ups)
- **Entrada:** Email inicial enviado
- **Saida:** Resposta do guest ou descarte
- **Checklist:**
  - [ ] Follow-up 1: E+3 a E+5 (gentle reminder)
  - [ ] Follow-up 2: E+10 (last call)
  - [ ] Se sem resposta: mover para "no response" e tentar tier B
  - [ ] Se resposta negativa: agradecer, perguntar quando seria bom
  - [ ] Se resposta positiva: prosseguir para confirmacao

### Etapa 4: Confirm & Schedule
- **Owner:** @guest-coordinator
- **SLA:** 1 dia
- **Entrada:** Guest aceitou convite
- **Saida:** Data/hora confirmada, calendario bloqueado
- **Checklist:**
  - [ ] Confirmar data/hora (timezone!)
  - [ ] Definir modo de gravacao: presencial ou remoto (perguntar ao convidado; nao presumir)
  - [ ] Remoto: enviar invite de calendario com link da plataforma (Zoom/Riverside)
  - [ ] Presencial: enviar invite com endereco, instrucoes de acesso, estacionamento e horario de chegada
  - [ ] Bloquear calendario do host
  - [ ] Bloquear calendario do @engineer (ambos os modos) e do estudio (se presencial)
  - [ ] Adicionar guest ao CRM/database
  - [ ] Atualizar content calendar

### Etapa 5: Onboarding Brief
- **Owner:** @guest-coordinator + @researcher
- **SLA:** D-14 a D-7
- **Entrada:** Guest confirmado
- **Saida:** Brief enviado ao guest
- **Checklist:**
  - [ ] Executar checklist onboarding-convidado.md
  - [ ] Enviar podcast bible (resumo)
  - [ ] Enviar topicos e perguntas principais
  - [ ] Explicar formato e duracao
  - [ ] Remoto: compartilhar tech requirements · Presencial: enviar logistica (endereco, acesso, chegada)
  - [ ] Pre-entrevista por call: OPCIONAL (ver prazos canonicos)
  - [ ] Enviar termo de autorizacao (assinatura obrigatoria)
  - [ ] Perguntar: bio, foto, links para promover
  - [ ] Confirmar: guest pode promover episodio?

### Etapa 6: Tech Check (remoto) / Logistica (presencial)
- **Owner:** @guest-coordinator + @engineer
- **SLA:** remoto D-5 a D-3 · presencial D-3
- **Entrada:** Guest confirmado
- **Saida:** Tech setup validado
- **Checklist:**
  - [ ] Agendar 15min tech check call
  - [ ] Testar mic/audio do guest
  - [ ] Validar internet (minimo 10 Mbps upload)
  - [ ] Validar ambiente (silencioso, sem eco)
  - [ ] Explicar dual recording (local + cloud)
  - [ ] Testar screen share (se necessario)
  - [ ] Enviar backup plan (celular, outro mic)
  - [ ] Confirmar: guest testou setup antes do dia?
  - [ ] **Presencial (substitui os itens acima):** confirmar endereco, acesso ao predio, estacionamento, acessibilidade, horario de chegada (15min antes) e contato de emergencia

**GATE 1: Diversity Check** - Avaliar a temporada por criterios nao sensiveis (area, regiao, trajetoria) e, quando houver, autodeclaracao voluntaria. Nunca inferir atributo sensivel do convidado.

### Etapa 7: Recording Day
- **Owner:** @guest-coordinator + @host + @engineer
- **SLA:** 1 dia
- **Entrada:** Guest preparado, tech validado
- **Saida:** Episodio gravado
- **Checklist:**
  - [ ] Executar checklist pre-gravacao.md
  - [ ] Equipe pronta 15min antes (warm-up com guest)
  - [ ] Re-testar audio/video (remoto: plataforma; presencial: mics e posicionamento no estudio)
  - [ ] Gravar intro (apresentar guest)
  - [ ] Gravar corpo (seguir script flexivel)
  - [ ] Gravar conclusao (CTA, onde encontrar guest)
  - [ ] Agradecer guest (on e off air)
  - [ ] Foto/video BTS (se presencial)

### Etapa 8: Post-Recording Follow-up
- **Owner:** @guest-coordinator
- **SLA:** D+1 (agradecimento em 24h); demais itens ate D+2
- **Entrada:** Gravacao concluida
- **Saida:** Guest satisfeito, pronto para promover
- **Checklist:**
  - [ ] Enviar thank you note (24h apos gravacao)
  - [ ] Informar: data estimada de publicacao
  - [ ] Pedir: review do episodio antes do publish (opcional)
  - [ ] Confirmar: bio, foto, links para show notes
  - [ ] Enviar: promo assets quando publicar
  - [ ] Pedir: guest pode compartilhar episodio?
  - [ ] Solicitar feedback (guest review protocol)
  - [ ] Adicionar guest ao "network" (futuros eventos, colaboracoes)

## Diagrama

```
[Research Guest] (3d)
      |
      v
[Outreach] (2d)
      |
      v
[Follow-up] (ate E+10) --[No Response]--> [Try Tier B]
      |
   [Accept]
      |
      v
[Confirm & Schedule] (1d)
      |
      +------------------+
      |                  |
      v                  v
[Onboarding] (D-14..D-7)  [Tech Check remoto / Logistica presencial] (D-5..D-3)
      |                  |
      +--------+---------+
               |
               v
        GATE 1: Diversity Check
               |
               v
      [Recording Day] (1d)
               |
               v
    [Post-Recording Follow-up] (2d)
               |
               v
      [Guest Ready to Promote]
```

## Metricas de Sucesso
- **Booking Rate:** 40%+ dos guests tier A aceitam convite
- **Response Rate:** 60%+ respondem ao outreach
- **Guest Satisfaction:** 4.5+ (5.0 scale) em post-recording survey
- **Diversity Score:** 75+ pontos (criterios nao sensiveis, `references/checklists/diversity-check.md`)
- **No-Show Rate:** <5% dos guests confirmados
- **Promotion Rate:** 80%+ dos guests promovem episodio

## Pontos de Falha Comuns
- **Low Response Rate:** Email generico → personalizar MUITO o outreach
- **Guest Ghosting:** Sem follow-up → criar sistema automatizado de reminders
- **Tech Issues on Recording Day:** Sem tech check → remoto: SEMPRE tech check D-5 a D-3; presencial: confirmar logistica D-3
- **Guest Unprepared:** Brief nao lido → enviar video curto explicando formato
- **No-Show:** Guest esqueceu → enviar 3 lembretes (D-7, D-1, 2h antes)
- **Diversity Gap:** Booking sempre os mesmos perfis → priorizar variedade de area, regiao e trajetoria desde o research
- **Guest Won't Promote:** Nao perguntou antes → confirmar promocao ANTES da gravacao
