## guest-invitation-official.md

<!--
Convite Oficial — template GENÉRICO (produto). É o PRIMEIRO envio ao convidado: leva o link do
formulário (variante escolhida pelo host). O kit (assets/templates/guest-kit.md) só vai depois da resposta.
Este arquivo é a versão TEXTO PURO do e-mail. A versão HTML (logo, cores, fonte e assinatura do bloco
`brand` do show-profile) é montada por assets/google-forms/src/invitation.js com os MESMOS
textos (references/contracts/i18n/<locale>.json, chave "invitation"). Nada de show específico aqui.

Sintaxe (mustache mínimo): {{caminho}} insere valor · {{#x}}…{{/x}} só se x existir (lista = repete,
item atual em {{.}}) · {{^x}}…{{/x}} só se x NÃO existir. Placeholder sem valor = erro.
Este bloco de comentário é removido na renderização.
-->
{{brand.display_name}}
{{t.title}}

{{t.greeting}}

{{t.intro}}

{{t.when_label}}: {{#scheduled_text}}{{scheduled_text}}{{/scheduled_text}}{{^scheduled_text}}{{t.when_tbd}}{{/scheduled_text}}
{{#presencial}}
{{t.where_label}}: {{#studio_name}}{{studio_name}} · {{/studio_name}}{{address_line}}
{{#gps_hint}}
{{t.gps_label}}: {{gps_hint}}
{{/gps_hint}}
{{#arrival_instructions}}
{{t.arrival_label}}: {{arrival_instructions}}
{{/arrival_instructions}}
{{#arrive}}
{{t.arrive}}
{{/arrive}}
{{/presencial}}
{{#remoto}}
{{t.remote_label}}: {{#remote_link}}{{remote_link}}{{/remote_link}}{{^remote_link}}{{t.remote_link_tbd}}{{/remote_link}}
{{/remoto}}

{{t.about_heading}}
{{#show.tagline}}
{{show.tagline}}
{{/show.tagline}}
{{show.editorial_line}}

{{t.cta_intro}}
{{t.cta_button}}: {{form_url}}

{{t.signoff}}
{{signature.name}}
{{#signature.role}}{{signature.role}} · {{/signature.role}}{{brand.display_name}}
{{#links_text}}
{{.}}
{{/links_text}}

--
{{t.footer_controller}}
{{t.footer_purpose}}
{{t.footer_optout}}


## guest-kit.md

<!--
Kit do Convidado — template GENÉRICO (produto). Nada de show específico aqui: tudo vem do
show-profile (references/contracts/show-profile.schema.json), do guest-intake e dos textos do locale
(references/contracts/i18n/<locale>.json, chave "kit"). Renderizado por assets/google-forms/src/core.js.

Sintaxe (mustache mínimo): {{caminho}} insere valor · {{#x}}…{{/x}} só se x existir (lista = repete,
item atual em {{.}}) · {{^x}}…{{/x}} só se x NÃO existir. Placeholder sem valor = erro (não some calado).
Tom: acolhedor e tranquilizador (show-profile.kit_tone). Variantes: presencial e remota.
Este bloco de comentário é removido na renderização.
-->
# {{t.title}} · {{show.name}}

{{t.greeting}}

{{t.thanks}}

## {{t.about_heading}}

{{#show.tagline}}
_{{show.tagline}}_

{{/show.tagline}}
{{show.editorial_line}}

**{{t.pillars_heading}}:**

{{#show.pillars}}
- {{.}}
{{/show.pillars}}

## {{t.when_heading}}

{{#scheduled_text}}
{{scheduled_text}}
{{/scheduled_text}}
{{^scheduled_text}}
{{t.when_tbd}}
{{/scheduled_text}}

{{#presencial}}
## {{t.where_heading}}

{{#studio_name}}
**{{studio_name}}**

{{/studio_name}}
- **{{t.address_label}}:** {{address_line}}
{{#landmarks}}
- **{{t.landmarks_label}}:** {{landmarks}}
{{/landmarks}}
{{#gps_hint}}
- **{{t.gps_label}}:** {{gps_hint}}
{{/gps_hint}}
{{#arrival_instructions}}
- {{arrival_instructions}}
{{/arrival_instructions}}
- **{{t.parking_label}}:** {{parking_text}}

{{t.arrive}}

{{/presencial}}
{{#remoto}}
## {{t.remote_heading}}

{{#remote_notes}}
- {{.}}
{{/remote_notes}}

{{/remoto}}
## {{t.conduct_heading}}

{{#conduct_notes}}
- {{.}}
{{/conduct_notes}}

## {{t.materials_heading}}

{{t.materials_text}}

## {{t.privacy_heading}}

{{t.privacy_text}}

{{t.signoff}}
{{show.name}}


## interview-guide.md

# Interview Guide
## Guia de Perguntas para Entrevista

---

## Informacoes do Episodio

**Episodio:** S{X}E{XX}
**Convidado:** {Nome Completo}
**Data de gravacao:** {YYYY-MM-DD}
**Horario:** {HH:MM timezone}
**Duracao prevista:** {X} minutos

---

## Bio Resumida do Convidado

{3-4 linhas sobre quem e o convidado, o que faz, por que e relevante}

**Credenciais principais:**
- {Credencial 1}
- {Credencial 2}
- {Credencial 3}

**Trabalho mais conhecido:** {Nome do livro/projeto/empresa}

---

## Topicos Aprovados

✅ {Topico 1: ex: trajetoria profissional}
✅ {Topico 2: ex: metodologia X que desenvolveu}
✅ {Topico 3: ex: fracassos e aprendizados}
✅ {Topico 4: ex: controversia Y (abordagem respeitosa)}
✅ {Topico 5: ex: visao de futuro da industria}

---

## Topicos Sensiveis / A Evitar

❌ {Topico 1 + razao: ex: processo judicial em andamento}
❌ {Topico 2 + razao: ex: pedido explicito do convidado}
⚠️ {Topico 3: ex: fracasso anterior - apenas se convidado trouxer primeiro}

**Notas do pre-interview:**
{Cole aqui qualquer pedido especifico do convidado sobre o que evitar ou priorizar}

---

## Estrutura da Entrevista

### Aquecimento (off-record, antes de gravar)

**Perguntar antes de apertar REC:**
1. "Como voce prefere ser apresentado?"
2. "Algum topico que voce NAO quer abordar hoje?"
3. "Tem algo que voce QUER garantir que vamos falar?"
4. "Primeira vez em podcast? (Se sim, explicar o processo)"

**Small talk (2-3 min):**
- {Comentario pessoal para deixar convidado confortavel}
- {Pergunta leve sobre o dia dele, viagem, clima, etc}

---

## Bloco 1: Contexto e Fundacao [0:00-15:00]

**Objetivo:** Estabelecer credibilidade, construir rapport, dar contexto ao ouvinte

### Pergunta 1: Abertura (warmup)
**Pergunta:** {Pergunta facil e aberta para o convidado se soltar}

**Exemplo:** "Conta pra gente: como voce chegou a trabalhar com {area}?"

**Objetivo:** Deixar convidado confortavel, estabelecer narrativa

**Follow-ups possiveis:**
- Se mencionar momento decisivo: "O que te fez perceber que era isso?"
- Se mencionar influencia: "Que papel {pessoa/livro} teve nisso?"

---

### Pergunta 2: Credenciais
**Pergunta:** {Pergunta que destaca expertise do convidado}

**Exemplo:** "Voce {credencial impressionante}. O que a maioria das pessoas nao entende sobre {area}?"

**Objetivo:** Estabelecer autoridade, dar ao ouvinte razao para continuar escutando

**Follow-ups possiveis:**
- "Isso e contraintuitivo. Por que as pessoas erram tanto nisso?"
- "Qual foi o momento em que VOCE entendeu isso?"

---

### Pergunta 3: Fundamentos
**Pergunta:** {Pergunta que explora conceito basico necessario para entender o resto}

**Exemplo:** "Antes de irmos fundo, explica pra gente: o que e {conceito X} de um jeito que minha avó entenderia?"

**Objetivo:** Nivelar audiencia, garantir que todos entendem o basico

**Follow-ups possiveis:**
- "E por que isso importa no dia a dia?"
- "De um exemplo concreto disso acontecendo"

---

### Pergunta 4: Contexto atual
**Pergunta:** {Pergunta que conecta o trabalho do convidado com momento presente}

**Exemplo:** "Estamos em {ano}, {contexto de tendencia/crise}. Como isso muda {area do convidado}?"

**Objetivo:** Relevancia, criar urgencia

**Follow-ups possiveis:**
- "O que voce diria pra alguem que acha que isso e so hype?"
- "Onde voce acha que estaremos em 5 anos?"

---

### Pergunta 5: Transicao para profundidade
**Pergunta:** {Pergunta que abre para o proximo bloco}

**Exemplo:** "Ok, agora que entendemos o contexto, vamos pro que realmente interessa: {topico profundo}. Me conta sobre {case especifico}."

**Objetivo:** Sinalizar mudanca de ritmo, entrar em material mais substantivo

---

## Bloco 2: Profundidade [15:00-35:00]

**Objetivo:** Explorar controversias, nuances, fracassos, insights unicos

### Pergunta 6: Controversia ou desafio ao status quo
**Pergunta:** {Pergunta que provoca ou desafia visao dominante}

**Exemplo:** "Tem uma crenca comum na sua area de que {crenca X}. Voce discorda. Por que?"

**Objetivo:** Gerar momento memoravel, posicionar convidado como pensador independente

**Follow-ups possiveis:**
- "O que voce diz pra quem argumenta {contrargumento}?"
- "Qual foi o momento que te fez mudar de ideia sobre isso?"

**Nota:** Deixar espaco para resposta longa. Nao interromper.

---

### Pergunta 7: Fracasso ou vulnerabilidade
**Pergunta:** {Pergunta que pede ao convidado para compartilhar erro ou desafio}

**Exemplo:** "Me conta sobre uma vez que voce errou feio em {area}. O que aconteceu?"

**Objetivo:** Humanizar convidado, criar conexao emocional

**Follow-ups possiveis:**
- "O que voce aprendeu que nao teria aprendido de outra forma?"
- "Se pudesse voltar, faria diferente ou era necessario errar?"

**Nota:** Se convidado resistir, nao forcar. Oferecer saida: "Ou se preferir, um momento dificil..."

---

### Pergunta 8: Metodologia ou framework
**Pergunta:** {Pergunta que pede ao convidado para ensinar algo acionavel}

**Exemplo:** "Voce desenvolveu {metodologia/framework X}. Walk us through: como alguem aplicaria isso segunda-feira de manha?"

**Objetivo:** Dar valor pratico, tornar episodio acionavel

**Follow-ups possiveis:**
- "Qual e o erro mais comum que voce ve ao implementar isso?"
- "Tem um caso de sucesso que ilustra isso na pratica?"

---

### Pergunta 9: Behind the scenes
**Pergunta:** {Pergunta que revela processo ou bastidor}

**Exemplo:** "Quando voce {conquista especifica}, o que estava acontecendo nos bastidores que ninguem viu?"

**Objetivo:** Satisfazer curiosidade, revelar trabalho oculto

**Follow-ups possiveis:**
- "Quanto tempo realmente levou?"
- "Quem te ajudou que nao recebe credito?"

---

### Pergunta 10: Opiniao impopular ou ousada
**Pergunta:** {Pergunta que convida convidado a ser provocativo}

**Exemplo:** "Ok, opiniao controversa: {tema}. Onde voce se posiciona?"

**Objetivo:** Criar momento clippable, gerar debate

**Follow-ups possiveis:**
- "Voce ja levou hate por essa opiniao?"
- "O que te daria certeza de que voce esta errado nisso?"

**Nota:** Apenas fazer essa pergunta se convidado ja demonstrou conforto em ser ousado.

---

### Pergunta 11: Transicao para lightning round
**Pergunta:** {Pergunta que fecha o bloco de profundidade}

**Exemplo:** "Ultima pergunta longa antes de irmos pro lightning round: se voce pudesse mudar uma coisa em {industria/campo}, o que seria?"

**Objetivo:** Dar espaco para ultima reflexao importante

---

## Lightning Round [35:00-40:00]

**Instrucoes ao convidado:**
"Agora vamos fazer um lightning round. Perguntas rapidas, respostas em 30-60 segundos. Primeira coisa que vem na cabeca. Pronto?"

### Pergunta 12
**Pergunta:** {Pergunta rapida sobre livro/conteudo}

**Exemplo:** "Livro que mudou sua vida?"

---

### Pergunta 13
**Pergunta:** {Pergunta rapida sobre conselho}

**Exemplo:** "Conselho que voce daria pro seu eu de 10 anos atras?"

---

### Pergunta 14
**Pergunta:** {Pergunta rapida sobre tecnologia/tendencia}

**Exemplo:** "Tecnologia que voce acha superestimada?"

---

### Pergunta 15
**Pergunta:** {Pergunta rapida sobre habito}

**Exemplo:** "Um habito que te torna melhor no que faz?"

---

### Pergunta 16
**Pergunta:** {Pergunta rapida sobre futuro}

**Exemplo:** "Onde voce ve {area} em 5 anos?"

---

### Pergunta 17
**Pergunta:** {Pergunta rapida inusitada}

**Exemplo:** "Se {area do convidado} fosse uma comida, seria o que?"

**Nota:** Pergunta leve para fechar com bom humor

---

### Pergunta 18: Encerramento
**Pergunta:** {Pergunta final, geralmente aberta}

**Exemplo:** "Ultima pergunta: o que voce gostaria que mais pessoas soubessem sobre {topico/trabalho}?"

**Objetivo:** Dar ao convidado espaco para mensagem final

---

## Encerramento (ainda gravando)

**Agradecer:**
"(Nome), muito obrigado pela conversa. Onde as pessoas podem te encontrar e saber mais do seu trabalho?"

**Convidado responde com links/redes**

**CTA para ouvintes:**
"Pessoal, links para tudo que o {Nome} mencionou estao nas show notes. Se voce gostou deste episodio, deixa um review e compartilha com alguem que precisa ouvir isso."

**Preview proximo episodio:**
"Semana que vem, {preview do proximo episodio}."

**Despedida:**
"Ate la!"

---

## Pos-gravacao (off-record)

- Agradecer novamente
- Perguntar como foi a experiencia
- Explicar timeline: edicao, data de publicacao
- Confirmar: "Tudo ok se publicarmos como esta, ou voce quer revisar algum trecho?"
- Informar sobre assets (audiograms, quote cards) que enviaremos
- Pedir para compartilhar quando publicar

---

## Notas de Edicao para @engineer

**Momentos para o cold open:**
- {Timestamp} - {Descricao da frase/momento impactante}
- {Timestamp} - {Alternativa 2}

**Trechos para cortar:**
- {Timestamp} - {Razao: ex: convidado pediu, off-topic demais, qualidade audio ruim}

**Trechos para clipes sociais:**
- {Timestamp} - {Tema do clip: ex: controversia sobre X}
- {Timestamp} - {Tema do clip: ex: framework acionavel}

---

## Checklist Pre-gravacao

No dia anterior:
- [ ] Enviar perguntas ao convidado (opcional, alguns preferem surpresa)
- [ ] Confirmar horario e link Riverside
- [ ] Revisar bio e trabalho recente do convidado
- [ ] Preparar introducao (2-3 linhas para ler ao vivo)

1 hora antes:
- [ ] Testar setup de audio/video
- [ ] Abrir Riverside e criar sala
- [ ] Ter agua por perto
- [ ] Silenciar notificacoes

15 min antes:
- [ ] Entrar na sala Riverside
- [ ] Testar audio do convidado
- [ ] Fazer small talk, deixar convidado confortavel

---

## Checklist Durante a Gravacao

- [ ] REC ligado (checar luz vermelha)
- [ ] Backup recording ligado
- [ ] Monitorar niveis de audio
- [ ] Tomar notas de timestamps importantes
- [ ] Observar linguagem corporal (se video)
- [ ] Dar pausas se convidado parecer cansado

---

## Licoes de Entrevistas Anteriores

**O que funciona:**
- {Exemplo: Perguntas sobre fracasso sempre geram melhores historias}
- {Exemplo: Deixar silencio apos pergunta profunda - convidado preenche com gold}

**O que evitar:**
- {Exemplo: Nao interromper quando convidado esta contando historia}
- {Exemplo: Perguntas duplas confundem - fazer uma de cada vez}

**Convidados que travam:**
- Se convidado der resposta curta, usar: "Conta mais sobre isso"
- Se convidado desviar, redirecionar: "Voltando ao que voce disse sobre X..."

**Convidados que falam demais:**
- Usar sinalizacao: "Antes de irmos pra frente, quero explorar..."
- Interromper educadamente: "Isso e fascinante, e conecta com..."

---

**Versao:** 1.0
**Criado por:** @researcher + @host
**Ultima atualizacao:** {data}

---

*Este guia e um GPS, nao uma prisao. Use como base, mas deixe a conversa fluir naturalmente.*


## script-template.md

# Script Template
## Modelo de Roteiro para Episodio Padrao (Entrevista/Solo)

> Tempos de bloco sao referencia para um episodio de ~40 min; ajuste a duracao alvo.
> Exemplos entre aspas ilustram tom, nao sao texto para copiar.

---

## Informacoes do Episodio

**Episodio:** S{X}E{XX}
**Titulo:** {Titulo Final do Episodio}
**Formato:** [ ] Entrevista [ ] Solo
**Convidado:** {Nome - se aplicavel}
**Duracao alvo:** {X} minutos
**Data de gravacao:** {YYYY-MM-DD}
**Data de publicacao:** {YYYY-MM-DD}

---

## [0:00-0:15] COLD OPEN

**Instrucao de edicao:** Trecho mais impactante do episodio. Corte abrupto, sem contexto.

**Trecho selecionado:**
```
[TIMESTAMP DO ORIGINAL: XX:XX]

{Transcreva aqui a frase/momento exato que sera o cold open}

Ex (entrevista): "...e foi ai que eu percebi: eu tinha perdido tudo fazendo exatamente o que os experts mandavam fazer."
Ex (solo): "Se voce acredita que [mito comum], esta jogando dinheiro fora. Deixa eu te mostrar por que."
```

**SFX:** {Opcional: som de impacto, musica cortando abrupto}

---

## [0:15-0:30] VALUE PROMISE

**Instrucao:** Host falando direto para o ouvinte. Tom energetico e promissor.

```
Neste episodio, voce vai descobrir:
- {Takeaway 1 em 5-7 palavras}
- {Takeaway 2 em 5-7 palavras}
- {Takeaway 3 em 5-7 palavras}
```

Estatistica usada aqui precisa de fonte citavel nas show notes; sem fonte, nao entra.

---

## [0:30-0:45] VINHETA

**Instrucao de edicao:** Inserir vinheta do podcast (sonic logo) + {opcional: "Apresenta: {Patrocinador}"}.

---

## [0:45-1:30] INTRO

### Para ENTREVISTA:

```
[Tom: acolhedor, contextualizador]

Ola, eu sou {Nome do Host} e este e o {Nome do Podcast}.

{Contexto: por que este episodio, por que agora}
Ex: "Na semana passada, falamos sobre [topico anterior]. Hoje vamos fundo em [topico atual], e pra isso eu trouxe a pessoa que [credencial]."

{Apresentacao do convidado - usar a bio que o convidado aprovou}
Ex: "{Nome} e {titulo/ocupacao}. {Credencial 1}, {Credencial 2} e [trabalho mais conhecido]."

"{Nome}, muito obrigado por estar aqui."
[Convidado responde com cumprimento]
```

**Nota de edicao:** Manter a resposta do convidado se for calorosa/interessante; cortar se for generica.

### Para SOLO:

```
[Tom: direto, pessoal]

Ola, eu sou {Nome do Host} e este e o {Nome do Podcast}.

{Hook pessoal ou anedota curta}
Ex: "Semana passada, um ouvinte me mandou: '[pergunta]'. E eu pensei: essa e a pergunta central. Porque [razao]."

{Roadmap do episodio}
Ex: "Nos proximos [X] minutos, vou te mostrar [entrega]. Vamos falar de [topico 1], [topico 2] e [topico 3]. Bora?"
```

---

## [1:30-15:00] BLOCO 1: Contexto e Fundacao

### ENTREVISTA - Perguntas e Respostas

**Objetivo do bloco:** {Ex: Estabelecer credibilidade do convidado e dar fundamentos ao ouvinte}

Formato de cada pergunta: **Host** (pergunta preparada) → **Convidado** (espaco para resposta, preenchido na gravacao/transcricao) → **Host follow-up** (se a resposta vier curta).

**[1:30] Pergunta 1: Warmup**
```
Host: {Pergunta facil, que solta o convidado}
Ex: "Como voce chegou a trabalhar com [area]?"
Convidado: {Resposta}
Follow-up: "E quando voce percebeu: 'e isso que eu quero fazer'?"
```

**[~5:00] Pergunta 2: Credenciais**
```
Host: {Pergunta que destaca expertise}
Ex: "O que a maioria das pessoas NAO entende sobre [area]?"
Convidado: {Resposta}
```

**[~8:00] Pergunta 3: Fundamentos**
```
Host: {Conceito basico explicado para qualquer pessoa}
Ex: "Antes de irmos fundo: o que exatamente e [conceito]?"
Convidado: {Resposta}
Host (transicao): "Ok, entao [reformular em 1 frase]. Agora..."
```

**[~12:00] Pergunta 4: Conexao com o presente**
```
Host: {Conectar com contexto atual}
Ex: "Estamos em [ano/contexto]. Como isso muda [area]?"
Convidado: {Resposta}
```

### SOLO - Script corrido

**Objetivo:** {Ex: Dar fundamentos do topico e mostrar por que importa}

```
[Tom: didatico, use analogias]

{Introducao ao problema/topico}
Ex: "Voce ja ouviu falar de [topico]. Mas aqui esta o que ninguem te conta: [insight]."

{Contexto/historia - o que se acreditava antes e o que mudou}

{Explicacao do conceito fundamental com analogia + exemplo do dia a dia}

{Por que isso importa para o ouvinte - consequencia de agir e de nao agir}

{Dados (se relevante) - sempre com fonte nomeada}
Ex: "Segundo [fonte], [dado]."

{Transicao para Bloco 2}
Ex: "Agora que voce entende o basico, deixa eu te mostrar como isso funciona na pratica..."
```

---

## [15:00-15:30] BREAK

**Instrucao de edicao:** Inserir um dos seguintes:

- **CTA parcial:** "A gente ja volta. Se voce esta gostando, tira 5 segundos pra deixar um review. Ok, voltando..."
- **Patrocinio:** {Leitura de patrocinio - ~30 s, identificada como publicidade}
- **Transicao musical:** {Trilha instrumental curta com fade in/out}

---

## [15:30-35:00] BLOCO 2: Profundidade

### ENTREVISTA

**Objetivo do bloco:** {Ex: Ir fundo, explorar controversias, ouvir aprendizados}

**[15:30] Pergunta 5: Provocacao/Controversia**
```
Host: {Pergunta que desafia o status quo}
Ex: "Tem uma crenca comum de que [X]. Voce discorda. Por que?"
Convidado: {Resposta - deixar espaco para resposta longa}
```

**[~20:00] Pergunta 6: Fracasso/Aprendizado**
```
Host: {Pergunta sobre erro ou desafio - combinada antes com o convidado; ele pode recusar}
Ex: "Me conta sobre uma vez que voce errou. O que aconteceu?"
Convidado: {Resposta}
Host (empatia + follow-up): "O que voce aprendeu que nao teria aprendido de outra forma?"
```

Se o tema tocar sofrimento real (luto, violencia, saude), seguir `assets/templates/trauma-informed-interview.md`.

**[~25:00] Pergunta 7: Metodologia acionavel**
```
Host: {Pedir framework pratico}
Ex: "Voce desenvolveu [metodologia]. Como alguem aplicaria isso na segunda de manha?"
Convidado: {Resposta - deixar dar o passo a passo}
```

**[~30:00] Pergunta 8: Bastidores**
```
Host: "Quando voce [conquista], o que estava rolando nos bastidores que ninguem viu?"
Convidado: {Resposta}
```

### SOLO

```
[Tom: mais profundo, pode desacelerar]

{Nuances e complexidade - onde a coisa complica}

{Caso de estudo 1 - acao, resultado, explicacao}

{Contrargumento e resposta}
Ex: "Tem gente que argumenta: '[contrargumento]'. E um ponto valido. Mas nao considera [resposta]."

{Caso de estudo 2 - acao oposta, resultado diferente, o insight da diferenca}

{Framework ou passo a passo}
Passo 1: [Acao especifica]
Passo 2: [Acao especifica]
Passo 3: [Acao especifica]
E o mais importante: [erro comum a evitar].

{Transicao: lightning round (entrevista) ou recap (solo)}
```

---

## [35:00-40:00] LIGHTNING ROUND (apenas entrevista)

```
Host: "Lightning round. Perguntas rapidas, primeira coisa que vem na cabeca. Pronto?"

1. "Livro que mudou sua vida?"
2. "Conselho pro seu eu de 10 anos atras?"
3. "Tecnologia superestimada?"
4. "Um habito que te torna melhor?"
5. "Onde voce ve [area] em 5 anos?"

Convidado: {Respostas}
```

---

## [40:00-40:45] CTA (Call-to-Action)

### ENTREVISTA:

```
Host: "{Nome}, muito obrigado. Onde as pessoas podem te encontrar?"
Convidado: {Redes, website, livro etc.}

Host: "Pessoal, todos os links estao nas show notes.
Se voce gostou deste episodio:
1. Deixa um review
2. Compartilha com alguem que precisa ouvir isso
3. Se inscreve na newsletter em {website}

Semana que vem, {preview curto e intrigante}. Ate la!"
```

### SOLO:

```
Host: "Recapitulando: hoje voce aprendeu [takeaway 1], [takeaway 2] e [takeaway 3].
Se fez sentido, deixa um review e compartilha com alguem que esta lutando com [problema].
Links e recursos nas show notes.
Proximo episodio, {preview}. Ate la!"
```

---

## [40:45-41:00] OUTRO

**Instrucao de edicao:** Vinheta final + creditos falados ("Producao: {Nome}. Edicao: {Nome}. Musica: {Nome}.") OU apenas vinheta com fade out.

---

## Notas de Producao

**Audio:** (alvos de loudness em `assets/templates/audio-specs.md`)
- Voz do host e do convidado no mesmo alvo de loudness (normalizar se necessario)
- Trilha de fundo (se usar) bem abaixo da voz
- Remover: respiracoes ruidosas, cliques de boca, hesitacoes excessivas

**Edicao:**
- Cortar: silencios longos, tangentes irrelevantes, trechos que o convidado pediu para retirar
- Manter: pausas dramaticas intencionais, autenticidade (pequenos tropecos ok)
- Adicionar: chapter markers a cada mudanca de topico

**Chapter Markers:**
1. [0:00] Cold Open
2. [0:15] Intro
3. [1:30] {Topico do Bloco 1}
4. [15:30] {Topico do Bloco 2}
5. [35:00] Lightning Round (se aplicavel)
6. [40:00] Onde encontrar {convidado}

---

**Versao do script:** 1.0
**Criado por:** @researcher
**Aprovado por:** @host
**Ultima atualizacao:** {data}

*Este script e um guia. A conversa real pode (e deve) fluir naturalmente. Use como estrutura, nao como prisao.*
