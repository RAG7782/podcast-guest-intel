# Como instalar o Podcast Guest Intel

O Podcast Guest Intel ajuda a preparar episódios com convidado: convite, formulário, pesquisa
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
| Claude no navegador ou no app | Plugin (adicionar marketplace ou enviar `.zip`) | 1 clique + colar um endereço |
| Claude Code (terminal) | Plugin | 1 comando |
| ChatGPT (Codex ou app com plugins) | Plugin | 2 comandos |
| ChatGPT sem plugins (plano Plus) | GPT personalizado | 5 minutos, sem programar |
| Gemini | Gem (ou Skill) | 5 minutos, sem programar |
| Hermes Agent | Plugin portátil ou só a skill | 1 comando |
| OpenClaw | Plugin do marketplace do Claude | 1 comando |
| Antigravity (`agy`) | Plugin | 1 comando |

## Claude

### No navegador ou no app (claude.ai, Desktop, Cowork)

1. Abra **Personalizar** (Customize) → **Plugins**.
2. Clique em **Adicionar marketplace** e cole `RAG7782/podcast-guest-intel`.
3. Instale **podcast-guest-intel**.

A partir da pasta: compacte o **conteúdo** da pasta do plugin num `.zip` e use **Enviar plugin**
(Upload plugin) na mesma tela. No Mac, abra o Terminal dentro da pasta do plugin e rode:

```bash
zip -r ../podcast-guest-intel.zip .
```

### Claude Code

```bash
claude plugin marketplace add RAG7782/podcast-guest-intel
claude plugin install podcast-guest-intel@guest-intel
```

A partir da pasta (dentro da pasta do plugin):

```bash
claude plugin marketplace add ./
claude plugin install podcast-guest-intel@guest-intel
```

Para usar: peça "prepare o episódio com <nome do convidado>". Os especialistas aparecem como
`podcast-guest-intel:researcher`, `podcast-guest-intel:guest-coordinator` e assim por diante.

## ChatGPT e Codex

O ChatGPT e o Codex usam o mesmo diretório de plugins.

```bash
codex plugin marketplace add RAG7782/podcast-guest-intel
codex plugin add podcast-guest-intel@guest-intel
```

A partir da pasta: `codex plugin marketplace add ./dist/plugin` e depois o mesmo
`codex plugin add`. No app do ChatGPT, o plugin aparece em **Plugins** depois de instalado pela
conta. Se o seu plano não tiver plugins (por exemplo, Plus), use o **GPT personalizado** abaixo.

## Gem (Gemini) e GPT personalizado (ChatGPT)

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
`dist/plugin/skills/podcast-guest-intel/SKILL.md` como Skill.

## Hermes Agent

Plugin completo (pacote portátil; o Hermes instala desligado e pede para ligar):

```bash
hermes plugins install RAG7782/podcast-guest-intel --enable
```

Só a skill:

```bash
hermes skills install RAG7782/podcast-guest-intel/skills/podcast-guest-intel
```

## OpenClaw

O OpenClaw lê o marketplace do Claude:

```bash
openclaw plugins install podcast-guest-intel --marketplace RAG7782/podcast-guest-intel
```

A partir da pasta, troque o endereço por `./dist/plugin`.

## Antigravity (`agy`)

```bash
agy plugin install ./dist/plugin
```

Se o plugin já estiver no Claude Code, `agy plugin import claude` traz de lá.

## O que é grátis e o que é pago

Tudo neste pacote é o **núcleo aberto** (licença Apache-2.0) e funciona sem servidor e sem
conta nossa. A lista completa está em
`dist/plugin/skills/podcast-guest-intel/references/capabilities.json`.

| Grátis (neste pacote) | Pago (servidor, a lançar) |
|---|---|
| Convite oficial e formulário essencial, com rodapé "Preparado com…" | Formulário completo sem marca e automações: e-mail com kit, WhatsApp, agenda, lembrete na véspera |
| Dossiê completo, cada afirmação com status e fonte | Enriquecimento pelo gestor, histórico do convidado, relatório de auditoria |
| Pauta com 1 tronco (perfil × linha editorial, Google Trends/News) | Pauta com 3 troncos: tendências das redes (X, TikTok, Reddit, LinkedIn) e continuidade com o catálogo |
| Roteiro no modo informativo | Os 7 modos de abordagem e modos por nicho |
| Legendas e tradução locais, com checks de qualidade | Feed por idioma, consentimento de voz auditável, fila de revisão |
| Saída em Markdown | Memória do show (centro de comando) e exportação PDF/DOCX com a marca |

A cobrança e a chave de licença ainda não existem. Nada no pacote liga ou desliga recurso pago.

## Confirmado × inferido

| Ferramenta | Formato usado | Situação |
|---|---|---|
| Claude Code | `.claude-plugin/plugin.json` + `marketplace.json` | **Confirmado**: `claude plugin validate` passou |
| Antigravity | `plugin.json` na raiz | **Confirmado**: `agy plugin validate` passou (1 skill, 13 agentes) |
| Hermes | `plugin.json` na raiz (Agent Plugins v1) | **Confirmado**: `hermes plugins validate` passou |
| OpenClaw | marketplace do Claude | **Confirmado**: `openclaw plugins marketplace list` leu o plugin |
| Codex / ChatGPT | `plugin.json` com `extensions.com.openai` + `.codex-plugin/` + `.agents/plugins/marketplace.json` | **Inferido** da documentação; não instalado nesta máquina |
| claude.ai (upload `.zip`) | mesmo plugin do Claude Code | **Inferido** da documentação; não testado |
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
