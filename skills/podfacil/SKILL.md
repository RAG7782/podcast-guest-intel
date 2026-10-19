---
name: podfacil
description: "Prepara episódios de podcast com convidado, do convite ao roteiro: convite oficial e formulário do convidado (Google Forms), dossiê com fontes (VERIFICADO / AUTODECLARADO / INFERÊNCIA), pauta ranqueada, roteiro por modo de abordagem, memória do show e localização (legendas, tradução). Use quando o usuário pedir para preparar entrevista, pesquisar convidado, montar pauta ou roteiro de podcast, convidar alguém para o programa ou legendar um episódio. EN: prepares podcast guest episodes end to end — invite, guest form, sourced guest dossier, ranked topic plan, approach-mode script, show memory, localization. Use for podcast guest research, interview prep, episode outline or script, guest invitation, subtitles."
license: Apache-2.0
compatibility: "Python 3.10+ com PyYAML (roteiro e check da pauta) e jsonschema (validação); recomendado uv (uv run --with pyyaml --with jsonschema python scripts/...). Busca web do harness para o dossiê e a pauta. Plano pago: chave de licença (scripts/licenca.py) e o conector MCP do PodFácil."
metadata:
  version: "2.1.0"
  source: "https://github.com/RAG7782/podcast-guest-intel"
---

# PodFácil — orquestração

Você conduz a preparação de um episódio com convidado. Responda no idioma do usuário (ou no
`locale` do show-profile). Explique em palavras simples: o usuário pode ser leigo em IA e em podcast.

**Antes de tudo, leia `references/principios.md`.** Resumo: você recomenda e alerta; quem decide
é o humano, e seguir contra a recomendação exige aceite registrado. Dado sensível só se o titular declarou.

## Onde estão os arquivos (caminhos relativos a esta pasta)

- Tasks (o passo a passo de cada etapa): `references/tasks/`
- Manifestos (contrato de entrada e saída de cada etapa): `references/manifests/`
- Contratos JSON Schema, modos de abordagem, fontes de tendência e textos i18n: `references/contracts/`
- Ferramentas Python: `scripts/` (rode com `python3 scripts/<arquivo>.py --help`)
- Templates, configuração e dados: `assets/templates/`, `assets/config/`, `assets/data/`
- Formulário do convidado (Google Apps Script, sem servidor): `assets/google-forms/README.md`
- Agentes especialistas (se o harness carregar subagentes): `references/agents.md`
- O que é grátis e o que é pago: `references/capabilities.json`

## Primeiro uso

1. Peça (ou ajude a preencher) o `show-profile` e o `host-profile` do usuário
   (`references/contracts/show-profile.schema.json`, `references/contracts/host-profile.schema.json`).
   Nunca invente dados do programa.
2. Pergunte o que ele já tem: nome do convidado, um link, data, formulário respondido.
   Com só o nome + 1 link o fluxo já funciona (degrada, não trava).

## Fluxo

Siga a ordem. Cada etapa tem uma task; leia a task inteira antes de executar a etapa.

| # | Etapa | Task | Especialista | Comando |
|---|---|---|---|---|
| 1 | Convite + formulário | `references/tasks/guest-intake.md` | @guest-coordinator | `*guest-intake` |
| 2 | Dossiê do convidado | `references/tasks/guest-dossier.md` | @researcher | `*guest-dossier` |
| 3 | Pauta (3 troncos) | `references/tasks/pauta.md` | @researcher | `*pauta` |
| 4 | Roteiro por modo | `references/tasks/roteiro.md` | @researcher | `*roteiro` |
| 5 | Memória do show | `references/tasks/memoria.md` | @producer | `*memoria` |
| 6 | Localização | `references/tasks/localizacao.md` | @editor | `*localizacao` |

Regras do fluxo:

- Valide cada artefato antes de seguir (a task diz o comando `check`). Inválido = corrigir, não pular.
- Lote acima de 20 chamadas a fonte externa: avise o volume e peça confirmação antes.
- Ao fim de cada etapa, mostre ao usuário o resumo legível (`render`) e os alertas em linguagem clara.
- Se o usuário quiser pular uma etapa, pule e registre a lacuna; a etapa seguinte degrada.

## Especialistas

13 especialistas (HPF v1). Mandato de cada um em `references/agents/<id>.md`; índice em `references/agents.md`. No Claude Code também são subagentes `podfacil:<id>`.

## Grátis × pago

O pacote é o núcleo aberto (Apache-2.0). Tudo o que é `free` roda aqui, sem servidor e sem chave.
O `paid` chega de dois jeitos:

- **No servidor (MCP):** o código não vem neste pacote. Chame a tool indicada pelo conector MCP do
  PodFácil, com a chave. Aqui, a pauta sai só com o tronco editorial e o roteiro só no modo grátis.
- **Neste pacote, com a chave:** roda no computador ou na conta Google do usuário (os dados são dele)
  e confere a chave de licença antes. Sem chave, para com a mensagem de como assinar.

Não imite um recurso pago, não contorne a checagem e não diga que ele está ativo sem a confirmação.
Esquecer um titular, a retenção e exportar a memória em Markdown funcionam sem chave (LGPD).

| Capacidade | Tier | Onde roda | O que é |
|---|---|---|---|
| `convite-e-formulario-essencial` | free | neste pacote, grátis | Convite oficial + formulário variante essencial (Apps Script), kit do convidado com rodapé de marca |
| `formulario-completo-e-automacoes` | paid | neste pacote, com a chave de licença | Variante completa sem marca; automações pós-envio no Apps Script da sua conta Google (e-mail com kit, WhatsApp, agenda, lembrete D-1), liberadas pela chave de licença |
| `dossie` | free | neste pacote, grátis | Dossiê completo, cada afirmação VERIFICADO / AUTODECLARADO / INFERÊNCIA + fonte |
| `pauta-1-tronco` | free | neste pacote, grátis | Perfil do convidado × linha editorial + Google Trends/News RSS rodado pelo próprio harness |
| `pauta-3-troncos` | paid | servidor (MCP): `pauta_completa`, `trends_collect` | Tendências BYOK do X (chave do usuário, verificada) agregadas no servidor + continuidade com o catálogo; sem chave, Google Trends/News RSS |
| `roteiro-modo-informativo` | free | neste pacote, grátis | Roteiro no modo informativo, com versões completo, teleprompter e cartão |
| `roteiro-7-modos` | paid | servidor (MCP): `roteiro_modos` | Os 7 modos de abordagem e modos extensíveis por nicho, servidos pelo MCP |
| `memoria-centro-de-comando` | paid | neste pacote, com a chave de licença | Catálogo, busca, perfil do host gerado dos episódios, lições e cortes; roda no seu computador (os dados ficam com você), liberado pela chave de licença |
| `localizacao-local` | free | neste pacote, grátis | Transcrição, tradução, legendas e checks de QA locais (BYOK) |
| `localizacao-servidor` | paid | servidor (MCP): `localizacao_plano` | Plano de dublagem por idioma com gate auditável de consentimento de voz (LGPD art. 11), no servidor |
| `exportacao-markdown` | free | neste pacote, grátis | Saída em Markdown |
| `exportacao-pdf-docx` | paid | servidor (MCP): `exportar_documento` | PDF/DOCX com a marca do show |

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

## Se o servidor não responder

As tools do servidor do produto podem falhar por tempo esgotado, erro de conexão, HTTP 5xx ou a
mensagem "temporariamente indisponível". Isso não é recusa de licença (recusa vem com código, como
`quota_free` ou `paid_only`). Nesse caso:

1. Tente de novo no máximo 1 vez, depois de cerca de 1 minuto. Não repita em laço.
2. Avise o usuário em uma frase: "O servidor do PodFácil não respondeu agora; sigo com a versão
   grátis local desta etapa, e você pode refazer com o recurso pago quando ele voltar."
3. Siga com o fallback grátis da tabela abaixo. Ele roda inteiro neste pacote, sem servidor.
4. Registre a lacuna no artefato (alertas ou lacunas): a etapa saiu na versão grátis por indisponibilidade.
5. Nunca simule o resultado pago nem diga que a licença caiu.

| Capacidade paga | Fallback grátis local | O que o fallback entrega |
|---|---|---|
| `formulario-completo-e-automacoes` | `convite-e-formulario-essencial` | Convite oficial + formulário variante essencial (Apps Script), kit do convidado com rodapé de marca |
| `pauta-3-troncos` | `pauta-1-tronco` | Perfil do convidado × linha editorial + Google Trends/News RSS rodado pelo próprio harness |
| `roteiro-7-modos` | `roteiro-modo-informativo` | Roteiro no modo informativo, com versões completo, teleprompter e cartão |
| `memoria-centro-de-comando` | `exportacao-markdown` | Saída em Markdown |
| `localizacao-servidor` | `localizacao-local` | Transcrição, tradução, legendas e checks de QA locais (BYOK) |
| `exportacao-pdf-docx` | `exportacao-markdown` | Saída em Markdown |
