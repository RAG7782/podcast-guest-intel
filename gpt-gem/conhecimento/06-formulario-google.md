# Formulário do convidado (Google Forms + Apps Script)

Cria, na **sua** conta Google, um formulário para o convidado do seu podcast, envia o **Convite
Oficial** com a marca do programa e automatiza o que vem depois do envio:

- **Convite Oficial** (primeiro contato): e-mail com o logo, as cores e a fonte do seu programa, data,
  local ou link da sala, o que é o programa, um botão para o formulário e a sua assinatura.

- **Kit do Convidado por e-mail**, com o que é o programa, a linha editorial, o endereço, o que digitar
  no GPS, o estacionamento, a hora de chegar e um texto para tranquilizar o convidado. Na gravação
  remota, o kit traz os requisitos técnicos no lugar do endereço.
- **Convite na sua Agenda**, com o endereço e o convidado como participante.
- **WhatsApp**, opcional, pela sua própria API (Evolution API ou WAHA).
- **Lembrete na véspera (D-1)**, por e-mail e/ou WhatsApp.

**Grátis × plano pago.** O Convite Oficial e o formulário essencial são grátis. O formulário
**completo** e as automações pós-envio (Kit por e-mail, Agenda, WhatsApp e lembrete D-1) são do
**plano pago** e conferem a sua chave de licença antes (passo 4). Sem chave, o formulário segue
recebendo respostas, você recebe o aviso de cada envio e a retenção/`esquecerTitular` (LGPD)
continuam funcionando. Planos: <https://antecena.artesanatodigital.com/precos/>.

Cada envio só acontece se o convidado **consentiu naquele canal**. Os dados sensíveis só são
guardados com **aceite específico** (LGPD, art. 11, I). Sem esse aceite, são descartados, e a
resposta crua também some do Forms e da planilha ligada (o que é lícito fica na aba `intake`).

Não é preciso servidor nem projeto no Google Cloud, e nada é instalado no seu computador.

---

## Passo a passo (uns 10 minutos, sem programar)

### 1. Crie o projeto
1. Abra **<https://script.google.com/home/projects/create>** (já abre um projeto novo; se não abrir, vá em script.google.com → **Novo projeto**).
2. Clique em "Projeto sem título" e dê um nome, por exemplo `Formulário do convidado`.

### 2. Cole os 10 arquivos
No editor, para **cada** arquivo da pasta `src/` deste repositório:
1. Clique no **+** ao lado de "Arquivos" e escolha **Script**.
2. Dê um nome (o nome não importa; sugestão: `bundle`, `core`, `intake`, `actions`, `invitation`, `forms`, `automations`, `admission`, `licenca`, `convidados`).
3. Apague o conteúdo de exemplo e cole o conteúdo do arquivo.

O arquivo `Código.gs` que já vem no projeto pode ser apagado. A ordem dos arquivos não importa.
O 11º arquivo, `drive-logo.js`, é **opcional**: cole só se o logo estiver no seu Google Drive (veja
"Logo e cores do convite").
Clique em 💾 **Salvar**.

### 3. Ajuste o fuso horário
⚙️ **Configurações do projeto** → **Fuso horário**: o da sua cidade (ex.: `(GMT-03:00) São Paulo`).
O lembrete D-1 e a hora da gravação usam esse fuso.

### 4. Cole a configuração do seu programa
Ainda em ⚙️ **Configurações do projeto**, desça até **Propriedades do script** →
**Adicionar propriedade do script**:

| Propriedade | Valor | Obrigatória? |
|---|---|---|
| `SHOW_PROFILE_JSON` | o conteúdo inteiro do seu `show-profile.json` (formato em `references/contracts/show-profile.schema.json`) | **sim** |
| `LOCALE` | `pt-BR` ou `en` (padrão: o `locale` do show-profile) | não |
| `JURISDICTION` | `BR-LGPD`, `EU-GDPR` ou `other` (padrão: o do show-profile, senão `BR-LGPD`) | não |
| `REMINDER_HOUR` | hora do lembrete diário, de 0 a 23 (padrão `9`) | não |
| `WHATSAPP_PROVIDER` | `evolution`, `waha` ou `generic` | só com WhatsApp |
| `WHATSAPP_URL` | endereço da sua API (ex.: `https://minha-evolution.exemplo.com`) | só com WhatsApp |
| `WHATSAPP_TOKEN` | a chave da sua API | só com WhatsApp |
| `WHATSAPP_INSTANCE` | nome da instância (Evolution) | só Evolution |
| `WHATSAPP_SESSION` | nome da sessão (WAHA; padrão `default`) | não |
| `PODFACIL_LICENSE_KEY` | a chave de licença do e-mail de compra (**nunca** cole no código) | só no plano pago |
| `PODFACIL_DEVICE_ID` | só se o seu conector usa `X-Device-Id` (Claude Code): o mesmo valor do conector / de `~/.podfacil/dispositivo`. **No claude.ai, deixe sem**: sem ela, o formulário não conta como dispositivo | não |

> **O valor de cada propriedade aceita até 9 KB.** Se o seu show-profile for maior, crie mais um
> arquivo de script chamado `config` e cole nele `var SHOW_PROFILE = { …seu JSON… };`.

**O controlador dos dados precisa de contato**, senão o formulário não é criado. Há dois jeitos:
- **Produtora ou empresa:** `"controller": { "name": "…", "contact_email": "privacidade@…" }`.
- **Podcast pessoal (você é o controlador):** `"controller": { "name": "Seu Nome", "kind": "personal", "contact_mode": "reply_to_email" }`.
  A cláusula vai orientar o convidado a responder a qualquer e-mail do programa. Não precisa de CPF nem CNPJ.

### 5. Crie o formulário
1. No topo do editor, escolha a função **`criarFormularioEssencial`** (cerca de 2 min para o convidado)
   ou **`criarFormularioCompleto`**. Depois clique em ▶ **Executar**.
2. Na primeira vez o Google pede autorização: **Revisar permissões** → escolha sua conta. Se aparecer
   o aviso de app não verificado, clique em **Avançado** → **Acessar (projeto)** → **Permitir**.
   O script é seu e roda na sua conta.
3. Abra o **Registro de execução** (embaixo). Lá aparecem 3 links:
   - **Link para o convidado**: é o que você envia.
   - **Editar**: o formulário, caso queira mudar algum texto.
   - **Respostas**: a planilha. Ela abre na aba **Convidados**: uma linha por convidado, em linguagem simples,
     com a coluna **Briefing** para o link do dossiê e da pauta. A aba `intake` é o registro técnico (JSON) e
     fica oculta; não apague nem edite. Se a aba Convidados sumir ou for editada à mão, rode
     `reconstruirAbaConvidados` (os links de briefing já gravados são mantidos).

A cada resposta você recebe um **aviso por e-mail** com a marca do programa: o que já foi enviado ao convidado,
o que precisa da sua atenção (por exemplo, WhatsApp não reconhecido ou data ilegível), um resumo e o botão
**Ver as respostas completas**, que abre direto a linha do convidado. Para reenviar um aviso, rode
`reenviarAviso` (sem argumento, o do último convidado). Em show brasileiro (`BR-LGPD`), o WhatsApp é aceito do
jeito que se digita (`11 91234-5678`, com ou sem o `+55`).

Os dois gatilhos (envio do formulário e lembrete diário) são instalados sozinhos. Para conferir, use o
menu ⏰ **Acionadores**. Se você rodar `criarFormulario…` de novo, ele cria **outro** formulário e
passa a usar esse (os gatilhos antigos são trocados, não duplicados).

### 6. Envie o Convite Oficial (primeiro contato com o convidado)
O convite leva o link do formulário **ativo** (o último criado no passo 5) e sai com a marca do seu
programa. O kit do convidado continua indo **depois** que ele responde ao formulário.

1. Crie mais um arquivo de script chamado `convites` e cole, trocando os dados do convidado:

   ```javascript
   function convidarAna() {
     enviarConvite({
       nome: 'Ana Souza',
       email: 'ana@exemplo.com',
       data: '2026-10-20T14:30:00-03:00', // data e hora com fuso; omita se ainda não houver data
       modo: 'presencial'                // ou 'remoto', com link_remoto: 'https://…'
     }, 'essencial');                    // a variante do formulário ativo
   }
   ```

2. Escolha `convidarAna` no topo do editor e clique em ▶ **Executar**.

O que você precisa saber:

- **Não reenvia.** Rodar de novo para a mesma pessoa e a mesma data devolve `skipped`.
- **Variante errada é recusada.** Se o formulário ativo é o `essencial` e você pede `completo`, o
  script explica e não envia. Para trocar, rode `criarFormularioCompleto` antes.
- **Com data marcada**, o e-mail leva um anexo `convite.ics` para o convidado pôr na agenda dele.
- **Opt-out.** O rodapé diz quem é o controlador, para que o contato é usado e que o convidado
  pode responder **SAIR**. Quando isso acontecer, rode uma vez `registrarOptOut('email@dele')`:
  nenhum convite, kit, convite de agenda, WhatsApp ou lembrete D-1 sai mais para esse endereço.
- **Só quem você convidou recebe as automações.** O formulário é público e quem responde digita o
  e-mail, então o kit (com o endereço do estúdio), o convite de agenda, o WhatsApp e o lembrete só
  saem para quem respondeu pelo **link do convite**: o `enviarConvite` gera um código de uso único
  para cada convidado (vale 30 dias, só com o e-mail convidado) e o põe no campo "Código do convite",
  já preenchido pelo link. Conhecer o e-mail de um convidado não basta (Codex Security #5). Resposta
  sem código válido (outro e-mail, código já usado, vencido ou apagado) fica **retida**: nada
  sai para o convidado nem para você na hora. Os retidos vão num **resumo único** no gatilho diário,
  com o comando `confirmarIntake("<id>")` ao lado de cada um, que você roda se a pessoa for legítima.
  Para um envio em massa pelo link não esgotar cota nem armazenamento (ALQERA SEC-004, Codex Security
  #2), ficam no máximo **50 retidos abertos**; acima disso a resposta é apagada do Forms e da planilha
  sem gerar linha, e o resumo só conta quantas foram. A linha retida que você não confirmar some em
  **7 dias**, mesmo com `RETENCAO_AUTOMATICA=false`.
- Cada convite gasta **1 destinatário** da cota diária de e-mail.

### 7. Teste antes de enviar
Mande um convite para você mesmo e responda ao formulário com o seu e-mail e uma data de amanhã.
Você deve receber o convite oficial, o kit, o evento na agenda e um e-mail-resumo ("Novo formulário de convidado"). Esse resumo lista cada canal
(`sent`/`error`) e o que foi descartado. **Se um canal falhar, os outros seguem**, e o erro aparece
no resumo, na aba `intake` e no registro de execução.

### Como o convidado manda arquivos
O formulário **não tem upload**, de propósito: no Google Forms, o upload obriga o convidado a entrar
com uma conta Google. Ele cola **links** no formulário e, para PDFs, slides ou fotos, **responde ao
e-mail do kit com os anexos**.

---

## Logo e cores do convite (bloco `brand` do show-profile)

Tudo fica no `brand` do seu `show-profile.json` (formato em `references/contracts/show-profile.schema.json`).
Sem `brand`, o convite sai em cores neutras e com o nome do programa em texto.

```json
"brand": {
  "display_name": "Meu Podcast",
  "logo": { "url": "https://meusite.com/logo.png", "alt": "Logo do Meu Podcast", "width": 120 },
  "colors": { "primary": "#1F6F5C", "secondary": "#7A3E9D", "background": "#FFFDF8", "text": "#1E1E24" },
  "font": { "family": "Georgia", "fallback": "serif" },
  "host_signature": { "name": "Seu Nome", "role": "Host" },
  "links": [{ "label": "YouTube", "url": "https://www.youtube.com/@meupodcast" }],
  "invitation_tone": "cordial"
}
```

- **Trocar o logo:** troque `logo.url` por outro endereço `https://` público. Prefira **PNG com
  fundo transparente**, que se comporta melhor no modo escuro. O `alt` é obrigatório: é o texto que
  aparece quando o programa de e-mail bloqueia imagens.
- **Logo no seu Drive**, em vez de link público: use `"logo": { "drive_file_id": "<id do arquivo>", "alt": "…" }`
  e cole também o arquivo `src/drive-logo.js`. O logo vai **embutido** no e-mail. Esse arquivo faz o
  Google pedir acesso ao seu Drive na autorização, e por isso é opcional.
- **Sem logo:** apague o `logo`. O topo mostra o nome do programa em texto, nunca uma imagem quebrada.
- **Trocar as cores:** `primary` pinta a faixa do topo e o botão (o texto do botão fica preto ou
  branco, o que der mais contraste). `secondary` vai nos títulos e links, e só é usada se for
  legível sobre o fundo. `text` sobre `background` precisa de contraste **≥ 4.5:1** (WCAG AA):
  abaixo disso, o validador (`scripts/validate-contracts.py`, regra `R-BRAND-CONTRAST`) e o script
  recusam, mostrando as duas cores e a razão calculada.
- **Fonte:** só fontes instaladas nos sistemas (Arial, Helvetica, Verdana, Tahoma, Trebuchet MS,
  Georgia, Times New Roman, Courier New) com um fallback genérico. Fonte da web não carrega na
  maioria dos programas de e-mail.
- **Tom:** `formal`, `cordial` ou `descontraido` mudam a frase de abertura.
- **Prévia sem conta Google:** `node integrations/google-forms/build.js (ferramenta de desenvolvimento, fora do pacote) example <show-profile.json> <pasta>`
  gera `convite-oficial.<locale>.html` e `.txt`. Abra o `.html` no navegador.

Como o e-mail é montado (boas práticas de e-mail HTML):

- O layout é feito com **tabelas e CSS inline**, porque muitos programas de e-mail descartam `<style>`
  e o Outlook não entende flex nem grid.
- O botão é uma **célula colorida com link**, e não uma imagem. Por isso funciona com as imagens
  bloqueadas, e o endereço do formulário também vai escrito por extenso logo abaixo.
- O e-mail declara `color-scheme: light` para diminuir a inversão de cores no modo escuro.
  Alguns aplicativos invertem mesmo assim, e é por isso que o logo em PNG transparente é o mais seguro.
- Vai sempre a versão **texto puro** junto (multipart). Ela vem de
  `assets/templates/guest-invitation-official.md`.
- Todo texto que vem do convidado ou do show-profile é **escapado** antes de entrar no HTML.

---

## Outros idiomas: legendas e dublagem (bloco `localization` do show-profile)

Se o programa pretende publicar em outros idiomas, preencha `localization` no show-profile
(formato em `references/contracts/show-profile.schema.json`). Aí o formulário ganha uma seção opcional com
**três aceites separados**, nenhum marcado e nenhum obrigatório:

1. **Legendas e textos traduzidos** do episódio nos idiomas de `target_locales`.
2. **Dublagem com voz sintética genérica** (não é a voz do convidado).
3. **Réplica artificial da própria voz**: marcada como **DADO SENSÍVEL** (LGPD, art. 11, I). O
   texto nomeia o episódio, os idiomas, o provedor e o país e o prazo de apagamento do modelo de
   voz. Só aparece se você preencher `localization.voice_replica`.

```json
"localization": {
  "target_locales": ["en", "es"],
  "voice_replica": { "provider": "Nome do provedor", "provider_country": "US", "model_deletion_days": 30 },
  "glossary": [{ "term": "Nome do Programa", "do_not_translate": true }]
}
```

O aceite vai para `localization_consents` do intake. Nada marcado = nada autorizado. Sem o
aceite 3 registrado, `scripts/localization_tools.py` **recusa** o plano de dublagem com réplica
daquele convidado (regra rígida, não é recomendação). Fluxo completo:
`references/tasks/localizacao.md`.

## WhatsApp (opcional): Evolution API ou WAHA

O script só faz um `POST` na **sua** API de WhatsApp. Nenhum provedor é obrigatório.

| `WHATSAPP_PROVIDER` | Requisição montada | Fonte |
|---|---|---|
| `evolution` | `POST {URL}/message/sendText/{INSTANCE}` · cabeçalho `apikey: {TOKEN}` · corpo `{"number":"5511…","text":"…"}` | [VERIFICADO no código-fonte da Evolution API: rota `/message` + `routerPath('sendText')` com `/:instanceName`, guard lendo `apikey`, schema `number`+`text`](https://github.com/EvolutionAPI/evolution-api/blob/main/src/api/routes/sendMessage.router.ts). A página da doc (doc.evolution-api.com) devolveu 404 na consulta. |
| `waha` | `POST {URL}/api/sendText` · cabeçalho `X-Api-Key: {TOKEN}` · corpo `{"chatId":"5511…@c.us","text":"…","session":"default"}` | [VERIFICADO: waha.devlike.pro/docs/how-to/send-messages](https://waha.devlike.pro/docs/how-to/send-messages/) |
| `generic` | `POST {URL}` · `Authorization: Bearer {TOKEN}` · corpo `{"to":"+5511…","text":"…"}` | formato próprio, para n8n, Make ou um webhook seu |

Uma resposta HTTP fora de 2xx vira erro registrado, com o código e o início da resposta, e os outros
canais continuam.

---

## Limites e cotas (oficiais, conta gratuita × Google Workspace)

Fonte: [Quotas for Google Services](https://developers.google.com/apps-script/guides/services/quotas) [VERIFICADO 2026-10-09].

| Item | Gmail gratuito | Workspace |
|---|---|---|
| **Destinatários de e-mail por dia** (MailApp) | **100** | 1.500 |
| Eventos de agenda criados por dia | 5.000 | 10.000 |
| Chamadas UrlFetch por dia (WhatsApp) | 20.000 | 100.000 |
| Tempo total de gatilhos por dia | 90 min | 6 h |
| Tempo por execução | 6 min | 6 min |
| Gatilhos por usuário por script | 20 | 20 |
| Tamanho de cada propriedade / total | 9 KB / 500 KB | 9 KB / 500 KB |

Cada convidado gasta cerca de **3 a 5 destinatários de e-mail**: o convite, o kit, o resumo para você e o lembrete D-1.
Com conta gratuita, isso dá folga para dezenas de convidados por dia. Os lembretes usam **um único
gatilho diário**, que varre a aba `intake`, e não um gatilho por convidado (o limite é de 20).

---

## Para quem mantém o código

- **Lógica pura** (sem Google, testável em Node): `src/core.js` (template, locale, cláusula, controlador,
  especificação do formulário), `src/intake.js` (resposta → guest-intake, regras de consentimento) e
  `src/actions.js` (kit, mensagens, plano por consentimento, D-1, WhatsApp, `runActions` idempotente) e
  `src/invitation.js` (convite oficial: marca, contraste, visual Cartão, HTML, texto puro, `.ics`) e a parte pura de
  `src/convidados.js` (aviso ao dono e linha da aba Convidados).
- **Lado Google**: `src/forms.js` (criação do Form e gatilhos), `src/automations.js` (`onFormSubmit`, `lembreteDiario`,
  `enviarConvite`, `registrarOptOut`, `confirmarIntake`), `src/admission.js` (lock das chaves de envio e
  admissão por código de convite), `src/licenca.js` (chave do plano pago conferida na tool `licenca_status`
  do servidor; endereço em `references/contracts/produto.json`, empacotado no bundle), o lado Google de `src/convidados.js`
  (aba Convidados por `intake_id`, `reconstruirAbaConvidados`, `reenviarAviso`, briefing na lixeira ao esquecer) e o
  opcional `src/drive-logo.js`. O HTML do convite tem porta Python em `mcp-server/convite_html.py`, com paridade
  byte a byte (`mcp-server/tests/test_convite_paridade.py`): mude os dois juntos.
- `src/bundle.gen.js` é **gerado** a partir de `references/contracts/i18n/*.json`, `assets/templates/guest-kit.md`,
  `assets/templates/guest-invitation-official.md`
  e de `x-form-variants` do schema. Depois de editar textos ou o template, rode:
  ```bash
  node integrations/google-forms/build.js (ferramenta de desenvolvimento, fora do pacote)          # regenera
  node --test integrations/google-forms/test/*.test.js (ferramenta de desenvolvimento, fora do pacote)
  ```
  Um teste falha se o bundle estiver desatualizado.
- Prévia sem conta Google: `node integrations/google-forms/build.js (ferramenta de desenvolvimento, fora do pacote) example <show-profile.json> <pasta>`.
- Idempotência: `sent:<intake_id>:<canal>:<tipo>` e `sent:convite:<email>:<data>` em Script Properties. Rodar de novo não reenvia.
- Segredos: só em Script Properties, nunca no código. **Quem for editor do projeto Apps Script vê as
  propriedades**, então não compartilhe o projeto.

### Simplificações conhecidas
- `ponytail:` só **1** declaração de dado sensível por resposta (um bloco categoria + texto + aceite).
  Se os convidados pedirem mais, acrescente blocos em `sensitiveItems` (core.js) e `sensitiveBlock` (intake.js).
- `ponytail:` um canal que falhou **não é reenviado automaticamente**. O erro fica no resumo e na
  planilha, e o reenvio é manual. Se isso ficar frequente, crie uma função `reprocessar` que leia a aba `intake`.
- `ponytail:` não há trava (LockService) entre dois envios simultâneos da **mesma** resposta. O risco é
  baixo, porque o gatilho dispara uma vez por resposta.
- `ponytail:` só **um** formulário fica ativo por vez, porque os gatilhos apontam para o último criado.
  Por isso o convite recusa uma variante diferente da ativa. Para ter as duas variantes ao mesmo tempo,
  guarde `FORM_ID`/`FORM_URL` por variante e instale um gatilho por formulário.
- `ponytail:` o opt-out é uma lista em `OPTOUT_EMAILS`, alimentada à mão (`registrarOptOut`). Se o volume
  crescer, leia as respostas "SAIR" da caixa de entrada com GmailApp, que pede um escopo maior.
- Revogação e eliminação: `esquecerTitular('in-…')` apaga a linha da aba `intake`, a resposta no Forms
  (`Form.deleteResponse`), a linha da aba de respostas ligada ao Form (casada pelo e-mail, porque apagar a
  resposta não apaga essa linha [INFERÊNCIA: a doc do `deleteResponse` não diz]) e as chaves `sent:`/`invited:`
  do titular, o evento da agenda criado pelo envio, a linha da aba **Convidados** e o **briefing** ligado a ela
  (o Google Docs vai para a lixeira do Drive, que se esvazia em 30 dias; se não puder, vira pendência); devolve o relatório com as contagens e
  `pendencias_manuais` (Gmail do host, histórico do WhatsApp no provedor, logs antigos), que a API deste
  script não apaga (ALQERA PRV-002). Nenhuma linha de log leva e-mail. `OPTOUT_EMAILS` fica, porque é o
  registro da oposição.
  Rode junto com `memory forget` no workspace local.
- `ponytail:` retenção automática **ligada por padrão** (ALQERA PRV-001; `RETENCAO_AUTOMATICA=false` em
  Script Properties desliga): o gatilho diário roda `aplicarRetencao`, que conta `retention_days_after_publish` a partir da **gravação** (a planilha não
  sabe a data de publicação), então apaga mais cedo que o prazo declarado, nunca mais tarde. Para o prazo
  exato, grave `published_at` na aba `intake` e conte dele.
- Locales `es` e `zh` são **esqueletos** (`needs_native_review: true`). O script recusa usá-los, a menos
  que `ALLOW_UNREVIEWED_LOCALE=true`.
- As cláusulas (`legal_review: pendente`) são um **rascunho técnico, não um parecer**. Precisam de
  revisão de advogado antes do uso comercial. Enquanto a cláusula não tiver `legal_review: aprovado`
  (ou `approved`), o formulário mostra ao convidado, na descrição e no topo da cláusula, o aviso
  `consent.draft_notice` ("RASCUNHO (v0) em revisão jurídica"). Mitigação R-07, aceita pelo dono em
  2026-10-10 só para o beta; o aviso some sozinho quando o advogado aprova e a flag muda.

---

## APIs usadas: verificado × inferência

Conferidas na documentação oficial em **2026-10-09**:

| API | Uso | Status | Fonte |
|---|---|---|---|
| `FormApp.create(title)` | cria o Form | [VERIFICADO] | <https://developers.google.com/apps-script/reference/forms/form-app> |
| `Form.addTextItem/ParagraphTextItem/MultipleChoiceItem/CheckboxItem/DateTimeItem/SectionHeaderItem/PageBreakItem`, `setDescription`, `setConfirmationMessage`, `getId`, `getPublishedUrl`, `getEditUrl` | monta o Form | [VERIFICADO] | <https://developers.google.com/apps-script/reference/forms/form> |
| `Form.setDestination(FormApp.DestinationType.SPREADSHEET, id)` | vincula a planilha | [VERIFICADO] | <https://developers.google.com/apps-script/reference/forms/form> · <https://developers.google.com/apps-script/reference/forms/destination-type> |
| `Form.setPublished`, `isPublished`, `supportsAdvancedResponderPermissions` | publica, se for preciso ("default for new forms is true") | [VERIFICADO] | <https://developers.google.com/apps-script/reference/forms/form> |
| `CheckboxItem.setChoiceValues/setRequired/setHelpText` | caixas de consentimento | [VERIFICADO] | <https://developers.google.com/apps-script/reference/forms/checkbox-item> |
| `FormApp.createTextValidation().requireTextIsEmail()/requireTextIsUrl()` + `setValidation` | valida e-mail/URL | [VERIFICADO] (os métodos) · [INFERÊNCIA] (trocar a regra do exemplo por estas) | <https://developers.google.com/apps-script/reference/forms/text-validation-builder> |
| `ScriptApp.newTrigger(fn).forForm(form).onFormSubmit().create()` | gatilho instalável de envio | [VERIFICADO] | <https://developers.google.com/apps-script/reference/script/form-trigger-builder> |
| Evento do Forms: `e.response` (FormResponse), `e.source`, `e.triggerUid` | lê a resposta | [VERIFICADO] | <https://developers.google.com/apps-script/guides/triggers/events> |
| `FormResponse.getItemResponses/getId/getTimestamp`; `ItemResponse.getResponse()` (CheckboxItem → `String[]`) | normaliza | [VERIFICADO] | <https://developers.google.com/apps-script/reference/forms/form-response> · <https://developers.google.com/apps-script/reference/forms/item-response> |
| Formato da resposta de `DateTimeItem` (`"YYYY-MM-DD HH:MM"`) | data combinada | **[INFERÊNCIA]**: a doc não fixa o formato; o parser aceita `YYYY-MM-DD HH:MM` e `YYYY-MM-DDTHH:MM`, e o que vier fora disso é descartado e registrado | <https://developers.google.com/apps-script/reference/forms/date-time-item> |
| `ScriptApp.newTrigger(fn).timeBased().everyDays(1).atHour(h).create()` | lembrete diário | [VERIFICADO] | <https://developers.google.com/apps-script/reference/script/clock-trigger-builder> |
| `ScriptApp.getProjectTriggers/deleteTrigger`, `Trigger.getHandlerFunction` | evita gatilho duplicado | [INFERÊNCIA] (não abri a página nesta sessão) | <https://developers.google.com/apps-script/reference/script/script-app> |
| `MailApp.sendEmail(to, subject, body, {htmlBody, name})` | kit, lembrete, resumo | [VERIFICADO] | <https://developers.google.com/apps-script/reference/mail/mail-app> |
| `MailApp.sendEmail` com `body` (texto) + `htmlBody`: quem lê HTML usa o `htmlBody`, os outros o texto | convite multipart | [VERIFICADO] (2026-10-09) | <https://developers.google.com/apps-script/reference/mail/mail-app> |
| `inlineImages: {chave: Blob}` + `<img src="cid:chave">` no `htmlBody`; `attachments: BlobSource[]` | logo do Drive embutido; `.ics` | [VERIFICADO] (2026-10-09) | <https://developers.google.com/apps-script/reference/mail/mail-app> |
| Limites por mensagem: corpo 200 KB (gratuito) / 400 KB (Workspace); anexos 25 MB | o convite tem ~6 KB | [VERIFICADO] (2026-10-09) | <https://developers.google.com/apps-script/guides/services/quotas> |
| `DriveApp.getFileById(id)` · `File.getBlob()` | logo no Drive (opcional) | [VERIFICADO] (2026-10-09) | <https://developers.google.com/apps-script/reference/drive/drive-app> · <https://developers.google.com/apps-script/reference/drive/file> |
| `Utilities.newBlob(data, contentType, name)` | anexo `.ics` | [VERIFICADO] (2026-10-09) | <https://developers.google.com/apps-script/reference/utilities/utilities> |
| `MailApp` em vez de `GmailApp` | escopo menor (`GmailApp` exige `https://mail.google.com/`) | [VERIFICADO] (2026-10-09) | <https://developers.google.com/apps-script/reference/gmail/gmail-app> |
| Contraste WCAG 2.2 SC 1.4.3: 4.5:1 (texto normal); luminância relativa com limiar 0.04045 | `R-BRAND-CONTRAST` (Python e JS) | [VERIFICADO] (2026-10-09) | <https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html> |
| `color-scheme` suportado em Apple Mail, Gmail e Outlook.com | menos inversão no modo escuro | [VERIFICADO] (2026-10-09) · a meta `supported-color-schemes` é [INFERÊNCIA] (prática da comunidade) | <https://www.caniemail.com/features/css-color-scheme/> |
| Tabelas + CSS inline, alt text, sem texto essencial em imagem, evitar branco/preto puros no modo escuro | layout do convite | [VERIFICADO em guias da comunidade, não em norma] | <https://glockapps.com/blog/html-email-best-practices/> · <https://prospeo.io/s/html-emails> |
| `.ics` (RFC 5545): CRLF, linhas dobradas em 75 octetos, datas UTC (`…Z`) | anexo do convite | [INFERÊNCIA] (não reabri a RFC nesta sessão; testado o formato) | <https://www.rfc-editor.org/rfc/rfc5545> |
| `CalendarApp.getDefaultCalendar().createEvent(title, start, end, {location, guests, sendInvites, description})` | convite | [VERIFICADO] | <https://developers.google.com/apps-script/reference/calendar/calendar-app> |
| `UrlFetchApp.fetch(url, {method, contentType, payload, headers, muteHttpExceptions})` | WhatsApp | [VERIFICADO] · `getResponseCode/getContentText` [INFERÊNCIA] (estão na página HTTPResponse, que não abri) | <https://developers.google.com/apps-script/reference/url-fetch/url-fetch-app> |
| `PropertiesService.getScriptProperties()`; `getProperty/setProperty/getProperties` | config, segredos, idempotência | [VERIFICADO] · `setProperties(obj)` [INFERÊNCIA] | <https://developers.google.com/apps-script/reference/properties/properties-service> · <https://developers.google.com/apps-script/reference/properties/properties> |
| `SpreadsheetApp.create/openById`; `Spreadsheet.insertSheet/getSheetByName/getId/getUrl`; `Sheet.appendRow/getDataRange` | planilha | [VERIFICADO] · `Range.getValues` [INFERÊNCIA] | <https://developers.google.com/apps-script/reference/spreadsheet/spreadsheet-app> · <https://developers.google.com/apps-script/reference/spreadsheet/spreadsheet> · <https://developers.google.com/apps-script/reference/spreadsheet/sheet> |
| `Session.getEffectiveUser()` (no gatilho instalável = quem criou o gatilho), `getScriptTimeZone()` | e-mail do dono, fuso | [VERIFICADO] | <https://developers.google.com/apps-script/reference/base/session> |
| `Utilities.formatDate(date, tz, 'Z')` → `-0300` | offset do fuso | [VERIFICADO] (usa o padrão SimpleDateFormat) · [INFERÊNCIA] (`'Z'` → `±HHMM`) | <https://developers.google.com/apps-script/reference/utilities/utilities> |
| Cotas | tabela acima | [VERIFICADO] | <https://developers.google.com/apps-script/guides/services/quotas> |
| Upload no Forms exige login Google | motivo de não haver upload | [VERIFICADO] em `research/01` | <https://support.google.com/docs/answer/7322334> |

**Nota sobre publicação:** a `research/01` registrou que formulários criados pela **Forms API** depois
de 30/06/2026 nascem não publicados. A página do **Apps Script** diz que o padrão de `setPublished` é
`true`. Por segurança, o script chama `setPublished(true)` quando o formulário suporta publicação e não
está publicado.

Os testes (`test/google.test.js`) rodam os arquivos de `src/` num contexto `vm` com **mocks** dos
serviços Google. Eles provam o encadeamento, **não** o comportamento real da API. A prova real é o
passo 6 ("Teste antes de enviar").
