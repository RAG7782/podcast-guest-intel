# Workflow: Crisis Management

## Visao Geral
- **Objetivo:** Responder rapida e adequadamente a incidentes que ameacam reputacao do podcast
- **SLA Total:** 24 horas (do incidente a resposta publica)
- **Owner:** @guardian + @producer

## Etapas

### Hora 0: Identificacao do Incidente
- **Owner:** @guardian
- **SLA:** Imediato
- **Entrada:** Flag de incidente
- **Saida:** Incidente confirmado e equipe notificada
- **Checklist:**
  - [ ] Fontes de Identificacao:
    - [ ] Listener report (email, DM, comentario)
    - [ ] Team member flag
    - [ ] Press/media mention
    - [ ] Social media monitoring
    - [ ] Guest complaint
  - [ ] Confirmar Incidente:
    - [ ] Validar: e um incidente real? (nao e hate infundado)
    - [ ] Identificar episodio/conteudo especifico
    - [ ] Documentar: o que foi dito/feito?
  - [ ] Notificar Equipe:
    - [ ] Alert em canal #crisis (Slack/Discord)
    - [ ] Notificar: @guardian, @producer, @host
    - [ ] Criar thread dedicado para tracking

### Hora 0-2: Reconhecimento Interno
- **Owner:** @guardian + @producer
- **SLA:** 2 horas
- **Entrada:** Incidente identificado
- **Saida:** Severidade classificada + plano de acao inicial
- **Checklist:**
  - [ ] Classificar Severidade:
    - [ ] **Nivel 1 (Baixo):** Erro factual simples, facilmente corrigivel
    - [ ] **Nivel 2 (Medio):** Conteudo controverso, guest insatisfeito, audio issue grave
    - [ ] **Nivel 3 (Alto):** Crise grave (legal issue, conteudo ofensivo, backlash massivo)
  - [ ] Reunir Informacoes:
    - [ ] Transcrever secao problematica
    - [ ] Compilar comentarios/feedback
    - [ ] Avaliar escala (quantas pessoas mencionaram?)
    - [ ] Identificar stakeholders afetados (guest, sponsor, audiencia)
  - [ ] Reconhecimento Interno:
    - [ ] Email/mensagem interna: "Estamos cientes do incidente e investigando"
    - [ ] Nao fazer statement publico ainda
  - [ ] Pausar Promocao:
    - [ ] Cancelar posts agendados sobre o episodio
    - [ ] Pausar ads (se sponsor envolvido)
    - [ ] Considerar: remover episodio temporariamente? (apenas Nivel 3)

### Hora 2-6: Investigacao
- **Owner:** @guardian + especialistas (se necessario)
- **SLA:** 4 horas
- **Entrada:** Incidente reconhecido
- **Saida:** Fact-check completo + decisao sobre acao
- **Checklist:**
  - [ ] Fact-Check Rigoroso:
    - [ ] Verificar claims do episodio (foram precisos?)
    - [ ] Consultar fontes primarias
    - [ ] Consultar experts (se topico tecnico)
  - [ ] Ouvir Envolvidos:
    - [ ] Guest (se aplicavel): qual a versao dele?
    - [ ] Host: contexto da gravacao
    - [ ] Listener: por que ficou ofendido/preocupado?
  - [ ] Avaliar Impacto:
    - [ ] Quantas pessoas afetadas?
    - [ ] Impacto em sponsors? (valores alinhados?)
    - [ ] Impacto em audiencia? (perda de confianca?)
    - [ ] Risco legal? (consultar advogado se necessario)
  - [ ] Consultar Especialistas:
    - [ ] Se topico sensivel (saude, legal, etc): consultar expert externo
    - [ ] Se legal issue: consultar advogado
    - [ ] Se LGPD/privacidade: consultar DPO

### Hora 6-12: Decisao
- **Owner:** @guardian + @producer + @host
- **SLA:** 6 horas
- **Entrada:** Investigacao completa
- **Saida:** Decisao sobre acao + rascunho de comunicacao
- **Checklist:**
  - [ ] Opcoes de Acao:
    - [ ] **Manter:** Conteudo e correto, nao precisa mudar (mas pode esclarecer)
    - [ ] **Corrigir:** Adicionar errata em show notes + mencao no proximo episodio
    - [ ] **Editar:** Re-upload de versao editada (remover secao problematica)
    - [ ] **Remover:** Takedown completo do episodio
  - [ ] Decisao por Nivel:
    - [ ] **Nivel 1:** Corrigir (errata em show notes)
    - [ ] **Nivel 2:** Editar ou Corrigir + statement
    - [ ] **Nivel 3:** Remover + statement formal + consulta juridica
  - [ ] Comunicacao:
    - [ ] Decidir: onde comunicar? (show notes, social, blog, proximo episodio)
    - [ ] Decidir: tom? (desculpas, esclarecimento, posicionamento)
    - [ ] Rascunho de statement (revisar com equipe)
  - [ ] Aprovacao:
    - [ ] @guardian, @producer, @host devem aprovar acao
    - [ ] Se Nivel 3: consultar advogado antes de publicar statement

### Hora 12-24: Resposta Publica
- **Owner:** @producer + @editor
- **SLA:** 12 horas
- **Entrada:** Decisao aprovada
- **Saida:** Acao executada + comunicacao publicada
- **Checklist:**
  - [ ] Executar Acao:
    - [ ] Corrigir: atualizar show notes com errata destacada
    - [ ] Editar: re-upload de audio editado (manter numero do episodio)
    - [ ] Remover: seguir processo de takedown (ver content-lifecycle.md)
  - [ ] Comunicacao Publica:
    - [ ] Nivel 1: apenas errata (show notes)
    - [ ] Nivel 2: post em blog/social + mencao no proximo episodio
    - [ ] Nivel 3: statement formal (blog) + posts em social + email para lista
  - [ ] Statement Template (Nivel 2-3):
    ```
    Titulo: Sobre o episodio [X]: [Topico]

    Fomos informados de [issue]. Levamos isso muito a serio.

    Apos investigacao interna, [o que descobrimos].

    [Acao tomada: corrigimos, editamos, removemos].

    [Se erro nosso:] Pedimos desculpas. [O que faremos diferente].

    [Se nao foi erro:] Esclarecemos: [contexto].

    Agradecemos o feedback da audiencia. [Valores do podcast].
    ```
  - [ ] Publicar Statement:
    - [ ] Blog post (se Nivel 2-3)
    - [ ] Pin post em social (24-48h)
    - [ ] Enviar para lista de email (se Nivel 3)
    - [ ] Responder comentarios (primeiras 4h criticas)
  - [ ] Notificar Stakeholders:
    - [ ] Guest (se envolvido)
    - [ ] Sponsor (se relacionado)
    - [ ] Plataformas (se remocao)

### Dia 7: Post-Mortem Interno
- **Owner:** @guardian + toda a equipe
- **SLA:** 7 dias apos incidente
- **Entrada:** Crise resolvida
- **Saida:** Learnings documentados + acoes preventivas
- **Checklist:**
  - [ ] Reuniao de Post-Mortem:
    - [ ] O que aconteceu? (timeline completa)
    - [ ] Por que aconteceu? (root cause)
    - [ ] O que fizemos bem?
    - [ ] O que poderia ter sido melhor?
  - [ ] Documentar Learnings:
    - [ ] Adicionar ao "Crisis Playbook" interno
    - [ ] Atualizar checklists (pre-gravacao, fact-check, etc)
    - [ ] Identificar gaps no processo
  - [ ] Acoes Preventivas:
    - [ ] Treinar equipe (se skill gap)
    - [ ] Atualizar podcast bible (se valores unclear)
    - [ ] Adicionar gate no workflow (ex: fact-check mais rigoroso)
    - [ ] Melhorar monitoring (se detectado tarde)
  - [ ] Comunicar Learnings:
    - [ ] Compartilhar com equipe
    - [ ] Atualizar SOP (Standard Operating Procedures)
    - [ ] Considerar: compartilhar com audiencia? (transparencia)

## Classificacao de Severidade

| Nivel | Exemplo | Acao | SLA |
|-------|---------|------|-----|
| **1 (Baixo)** | Erro factual menor (data errada, nome errado) | Errata em show notes | 24h |
| **2 (Medio)** | Conteudo controverso, guest insatisfeito, claim impreciso | Statement + Edicao ou Correcao | 24h |
| **3 (Alto)** | Legal issue, conteudo ofensivo, backlash massivo, LGPD | Remocao + Statement formal + Juridico | 12h |

## Diagrama

```
[Hora 0: Identificacao]
   (Listener, team, press, social)
          |
          v
[Hora 0-2: Reconhecimento]
   (Classificar severidade: 1, 2, 3)
          |
          v
[Hora 2-6: Investigacao]
   (Fact-check + Ouvir envolvidos)
          |
          v
[Hora 6-12: Decisao]
   (Manter, Corrigir, Editar, Remover)
          |
          v
[Hora 12-24: Resposta Publica]
   (Executar acao + Statement)
          |
          v
[Dia 7: Post-Mortem]
   (Learnings + Prevencao futura)
```

## Metricas de Sucesso
- **Response Time:** 90%+ dos incidentes respondidos em <24h
- **Escalation Rate:** <10% dos incidentes chegam a Nivel 3
- **Resolution Rate:** 95%+ dos incidentes resolvidos sem impacto duradouro
- **Repeat Issues:** <5% dos mesmos tipos de incidente
- **Audience Trust:** Manter 80%+ de confianca apos crise (survey)

## Pontos de Falha Comuns
- **Resposta Tardia:** Demorar dias para responder → ter SLA de 24h
- **Defensividade:** Negar erro obvio → ser transparente e assumir responsabilidade
- **Over-apologizing:** Pedir desculpas por nao-erro → investigar antes de responder
- **Comunicacao Confusa:** Statement vago → ser claro sobre o que aconteceu e o que foi feito
- **Sem Learnings:** Repetir mesmo erro → fazer post-mortem sempre
- **Panic Mode:** Remover episodio sem investigar → seguir processo, nao agir por panico
- **Ignoring Feedback:** "E hate, vamos ignorar" → avaliar TODA critica (pode ser valida)
