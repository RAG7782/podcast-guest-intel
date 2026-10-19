# Como instalar o PodFácil

O PodFácil ajuda a preparar episódios com convidado: convite, formulário, pesquisa
sobre o convidado (dossiê com fontes), pauta e roteiro. Este guia é para quem **não é
programador**. Escolha a ferramenta de IA que você já usa e siga só a seção dela.

> **Onde está o plugin.** No repositório público
> [`RAG7782/podcast-guest-intel`](https://github.com/RAG7782/podcast-guest-intel). As opções
> **"a partir da pasta"** usam uma cópia local dele (`git clone` ou o `.zip` do GitHub). No
> repositório de desenvolvimento, a mesma pasta é `dist/plugin`, gerada por
> `python3 scripts/build_plugin.py`.

## Qual opção escolher

| Você usa | Melhor caminho | Esforço |
|---|---|---|
| Claude no navegador ou no app (Pro, Max, Team, Enterprise) | Plugin (adicionar marketplace ou enviar `.zip`) | 1 clique + colar um endereço |
| Claude grátis | Skill em `.zip` (`podfacil-skill-<versão>.zip`) | 3 cliques, sem terminal |
| Claude Code (terminal) | Plugin | 1 comando |
| ChatGPT (Codex ou app com plugins) | Plugin | 2 comandos |
| ChatGPT, conta pessoal (Free, Go, Plus, Pro) | Codex (terminal) ou Gem/Claude | contas pessoais não criam GPTs |
| Gemini | Gem (ou Skill) | 5 minutos, sem programar |
| Hermes Agent | Plugin portátil ou só a skill | 1 comando |
| OpenClaw | Plugin do marketplace do Claude | 1 comando |
| Antigravity (`agy`) | Plugin | 1 comando |

## Claude

### No navegador ou no app (claude.ai, Desktop, Cowork)

1. Abra **Personalizar** (Customize) → **Plugins**.
2. Clique em **Adicionar marketplace** e cole `RAG7782/podcast-guest-intel`.
3. Instale **PodFácil** (`podfacil`).

Os plugins são dos planos pagos do Claude (Pro, Max, Team e Enterprise).

A partir da pasta: compacte o **conteúdo** da pasta do plugin num `.zip` e use **Enviar plugin**
(Upload plugin) na mesma tela. No Mac, abra o Terminal dentro da pasta do plugin e rode:

```bash
zip -r ../podfacil.zip .
```

### Claude grátis: a skill em `.zip`, sem terminal

No plano grátis não há plugins, mas dá para enviar a skill. Baixe `podfacil-skill-<versão>.zip` na
página de releases do repositório (<https://github.com/RAG7782/podcast-guest-intel/releases>) e:

1. Em **Configurações → Capacidades**, ligue **Execução de código e criação de arquivos**.
2. Em **Personalizar → Skills**, clique em **+ → Criar skill → Carregar um skill** e escolha o `.zip`.
3. Ative a skill na lista e peça: “prepare o episódio com <nome do convidado>”.

O zip tem a pasta `podfacil/` no topo, como o claude.ai exige
(<https://claude.com/docs/skills/how-to#package-your-skill>). No repositório de desenvolvimento ele sai
em `dist/podfacil-skill-<versão>.zip`, gerado por `python3 scripts/build_plugin.py`.

### Claude Code

```bash
claude plugin marketplace add RAG7782/podcast-guest-intel
claude plugin install podfacil@guest-intel
```

A partir da pasta (dentro da pasta do plugin):

```bash
claude plugin marketplace add ./
claude plugin install podfacil@guest-intel
```

Para usar: peça "prepare o episódio com <nome do convidado>". Os especialistas aparecem como
`podfacil:researcher`, `podfacil:guest-coordinator` e assim por diante.

## Atualizar

Quando sai uma versão nova, o PodFácil avisa no chat (se o conector do PodFácil estiver ligado). A
sincronização automática do marketplace do Claude pode demorar ou não acontecer; para atualizar na hora:

- **Claude no navegador ou no app:** **Personalizar → Plugins → Adicionar → Gerenciar marketplaces**. No ⋮
  ao lado de `podcast-guest-intel`, clique em **Verificar atualizações**. Depois abra o **PodFácil** na lista
  de plugins e, se aparecer o botão **Adicionar**, clique nele. A versão aparece ao lado do nome.
- **Claude grátis (skill em `.zip`):** baixe o `podfacil-skill-<versão>.zip` mais novo em
  <https://github.com/RAG7782/podcast-guest-intel/releases/latest> e carregue de novo em **Personalizar → Skills**.
- **Claude Code:**

  ```bash
  claude plugin marketplace update guest-intel
  claude plugin update podfacil@guest-intel
  ```

- **ChatGPT e Codex, Hermes, OpenClaw e Antigravity:** rode de novo o comando de instalação da seção da sua
  ferramenta, abaixo; ele traz a versão mais nova do repositório.

## ChatGPT e Codex

O ChatGPT e o Codex usam o mesmo diretório de plugins.

```bash
codex plugin marketplace add RAG7782/podcast-guest-intel
codex plugin add podfacil@guest-intel
```

A partir da pasta: `codex plugin marketplace add ./dist/plugin` e depois o mesmo
`codex plugin add`. No app do ChatGPT, o plugin aparece em **Plugins** depois de instalado pela
conta. Contas pessoais do ChatGPT (Free, Go, Plus e Pro) não criam mais GPTs
(<https://help.openai.com/en/articles/8554397-creating-and-editing-gpts>): nelas, use o Codex, o Gem
ou o Claude.

## Gem (Gemini) e GPT personalizado (só workspaces Business, Enterprise e Edu)

É a versão sem instalação: você cria um assistente e cola as instruções. Os arquivos ficam em
`dist/gpt-gem/`, e o passo a passo, com os links das telas, está em `dist/gpt-gem/GUIA.md`.
Resumo:

1. Abra o criador: Gem em <https://gemini.google.com/gems/create>, GPT em
   <https://chatgpt.com/gpts/editor>.
2. Cole o conteúdo de `INSTRUCOES.txt` no campo de instruções.
3. Envie os arquivos da pasta `conhecimento/` (são 8; o Gem aceita até 10).
4. No GPT, deixe a **pesquisa na web** ligada.

Essa versão traz só o núcleo grátis e não roda os checks automáticos.

O Google vai trocar os Gems por **Skills** (contas pessoais a partir de novembro de 2026). No app
do Gemini (web ou Mac) você já pode importar o arquivo
`dist/plugin/skills/podfacil/SKILL.md` como Skill.

## Hermes Agent

Plugin completo (pacote portátil; o Hermes instala desligado e pede para ligar):

```bash
hermes plugins install RAG7782/podcast-guest-intel --enable
```

Só a skill:

```bash
hermes skills install RAG7782/podcast-guest-intel/skills/podfacil
```

## OpenClaw

O OpenClaw lê o marketplace do Claude:

```bash
openclaw plugins install podfacil --marketplace RAG7782/podcast-guest-intel
```

A partir da pasta, troque o endereço por `./dist/plugin`.

## Antigravity (`agy`)

```bash
agy plugin install ./dist/plugin
```

Se o plugin já estiver no Claude Code, `agy plugin import claude` traz de lá.

## O que é grátis e o que é pago

O núcleo aberto (licença Apache-2.0) funciona sem servidor e sem conta nossa. A lista completa está
em `dist/plugin/skills/podfacil/references/capabilities.json`.

| Grátis | Pago (chave de licença) |
|---|---|
| Convite oficial e formulário essencial, com rodapé "Preparado com PodFácil" | Formulário completo sem marca e automações (e-mail com kit, WhatsApp, agenda, lembrete na véspera), que rodam no Apps Script da sua conta Google |
| Dossiê completo, cada afirmação com status e fonte | Memória do show (centro de comando): catálogo, busca, lições e cortes |
| Pauta com 1 tronco (perfil × linha editorial, Google Trends/News) | Pauta com 3 troncos: tendências do X com a sua chave e continuidade com o catálogo |
| Roteiro no modo informativo | Os 7 modos de abordagem do roteiro |
| Legendas e tradução locais, com checks de qualidade | Plano de localização com gate de consentimento de voz |
| Saída em Markdown | PDF e DOCX com a marca do show |

## Plano pago: chave de licença

Depois da compra, a chave (começa com `pgi_`) chega por e-mail. O passo a passo com exemplos para
cada assistente está na página de instalação do site, em `/instalar/`. São dois lugares:

1. **Servidor MCP**, para as funções que rodam no servidor. Endereço:
   `https://api.antecena.artesanatodigital.com/mcp`. No conector, adicione os headers
   `Authorization: Bearer <sua chave>` e `X-Device-Id: <um nome fixo para este dispositivo>`.
   No Claude Code:

   ```bash
   claude mcp add --transport http podfacil https://api.antecena.artesanatodigital.com/mcp \
     --header "Authorization: Bearer $PODFACIL_LICENSE_KEY" --header "X-Device-Id: notebook"
   ```

2. **Pacote local**, a partir da versão 1.1.0. Os 7 modos de roteiro e a pauta de 3 troncos com X
   vêm do servidor, pelo conector do passo 1. A memória e o formulário completo com automações rodam
   no seu computador e na sua conta Google e pedem a chave. Use uma das formas (ou
   `python3 scripts/licenca.py configurar`, que lê a chave sem mostrá-la):

   ```bash
   # variável de ambiente (ponha no ~/.zshrc ou ~/.bashrc)
   export PODFACIL_LICENSE_KEY='pgi_...'

   # ou arquivo, legível só por você
   mkdir -p ~/.podfacil && printf '%s\n' 'pgi_...' > ~/.podfacil/licenca && chmod 600 ~/.podfacil/licenca
   ```

Na primeira checagem o pacote cria `~/.podfacil/dispositivo`. Use esse mesmo valor no `X-Device-Id`
do conector e nas propriedades do script do formulário (`PODFACIL_LICENSE_KEY`, `PODFACIL_DEVICE_ID`);
com valores diferentes, o Solo conta dois dispositivos. Confira com `python3 scripts/licenca.py status`.
**No claude.ai** o conector não envia `X-Device-Id`: no formulário, crie só `PODFACIL_LICENSE_KEY` e deixe
`PODFACIL_DEVICE_ID` sem valor. Sem `X-Device-Id`, conector e formulário não contam como dispositivo.

Sem chave, o pacote continua funcionando no plano grátis. Detalhes técnicos do servidor e da
licença: `docs/LICENSING.md`.

## Confirmado × inferido

| Ferramenta | Formato usado | Situação |
|---|---|---|
| Claude Code | `.claude-plugin/plugin.json` + `marketplace.json` | **Confirmado**: `claude plugin validate` passou |
| Antigravity | `plugin.json` na raiz | **Confirmado**: `agy plugin validate` passou (1 skill, 13 agentes) |
| Hermes | `plugin.json` na raiz (Agent Plugins v1) | **Confirmado**: `hermes plugins validate` passou |
| OpenClaw | marketplace do Claude | **Confirmado**: `openclaw plugins marketplace list` leu o plugin |
| Codex / ChatGPT | `plugin.json` com `extensions.com.openai` + `.codex-plugin/` + `.agents/plugins/marketplace.json` | **Inferido** da documentação; não instalado nesta máquina |
| claude.ai (marketplace + conector) | mesmo plugin do Claude Code + conector personalizado | **Confirmado** em 2026-10-17 pelo dono: plugin instalado pelo marketplace, conector "Sem login" com só `Authorization`, `licenca_status` devolveu `tier: paid`. O claude.ai recusa header de nome não aprovado (`X-Device-Id`) e não deixa editar header depois de criar o conector (só excluir e criar de novo) |
| Gem / GPT | instruções + 8 arquivos | Limite de 8.000 caracteres do GPT **relatado pela comunidade** (a página oficial respondeu 403) |

## Fontes consultadas

- Agent Skills, especificação: <https://agentskills.io/specification>
- Claude Code, manifesto de plugin: <https://code.claude.com/docs/en/plugins-reference>
- Claude Code, marketplaces: <https://code.claude.com/docs/en/plugin-marketplaces>
- Claude Code, subagentes: <https://code.claude.com/docs/en/sub-agents>
- Codex, criar plugins: <https://developers.openai.com/codex/plugins/build>
- Agent Plugins, schema do `plugin.json`: <https://agent-plugins.org/schemas/1.0.0/plugin.schema.json>
- Hermes, skills: <https://hermes-agent.nousresearch.com/docs/user-guide/features/skills>
- OpenClaw, skills e manifesto: <https://docs.openclaw.ai/tools/skills> · <https://docs.openclaw.ai/plugins/manifest>
- Gemini, de Gems para Skills: <https://support.google.com/gemini/answer/18560919>
- Gems com até 10 arquivos: <https://workspace.google.com/blog/product-announcements/new-gemini-gems-deeper-knowledge-and-business-context>
- Limite de instruções do GPT (comunidade): <https://community.openai.com/t/how-can-i-increase-the-ceiling-for-gpt-instructions-beyond-8000-characters/801867>

## Plano pago: chave de licença (gerado pelo build do pacote)

O grátis roda inteiro neste pacote, sem servidor e sem chave. O pago chega de dois jeitos: tools do servidor MCP (o código não vem no pacote) e recursos locais que conferem a chave antes de rodar.

Configurar a chave do plano pago (vem no e-mail de compra):

1. **Neste computador (memória do show):** `python3 scripts/licenca.py configurar` grava a chave em
   `~/.podfacil/licenca` (permissão 600), sem mostrar na tela; ou exporte `PODFACIL_LICENSE_KEY`.
   Confira com `python3 scripts/licenca.py status`. A confirmação vale 1 h sem nova consulta e até 72 h
   se o servidor não responder.
2. **Conector MCP (pauta em 3 troncos, 7 modos, coleta do X):** URL `https://api.antecena.artesanatodigital.com/mcp`, headers
   `Authorization: Bearer <chave>` e `X-Device-Id: <conteúdo de ~/.podfacil/dispositivo>`. Use o mesmo
   X-Device-Id em todo lugar: o plano conta dispositivos por ele.
3. **Formulário (Apps Script):** em Configurações do projeto → Propriedades do script, crie
   `PODFACIL_LICENSE_KEY` (nunca no código) e `PODFACIL_DEVICE_ID` com o mesmo valor do item 2.

Sem chave, o recurso pago para e mostra onde assinar: https://antecena.artesanatodigital.com/precos/

Estúdios, produtoras e redes: fale conosco em contato@artesanatodigital.com (proposta para vários programas
ou vários hosts; não há plano de equipe em autosserviço).
