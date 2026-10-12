# Como criar o Gem (sem programar)

Este pacote é a versão "sem plugin" do PodFácil, para quem usa o Gemini (Gem). Ele traz só o
núcleo grátis: convite, dossiê, pauta de 1 tronco e roteiro no modo informativo. Sem scripts: os
checks automáticos ficam na versão plugin.

## Arquivos

- `INSTRUCOES.txt`: cole no campo de instruções (cabe no limite de 8000 caracteres).
- `conhecimento/`: envie os 8 arquivos como conhecimento.

## ChatGPT

Segundo a OpenAI, contas pessoais do ChatGPT (Free, Go, Plus e Pro) não podem mais criar GPTs; a
criação ficou para workspaces Business, Enterprise e Edu
(<https://help.openai.com/en/articles/8554397-creating-and-editing-gpts>).

- Conta pessoal: use o Gem do Gemini abaixo (grátis) ou o Claude: no plano grátis, o arquivo
  `podfacil-skill-<versão>.zip` em **Personalizar > Skills > + > Criar skill > Carregar um skill**;
  nos planos pagos, o plugin. Passo a passo em <https://antecena.artesanatodigital.com/instalar/>.
- Workspace Business, Enterprise ou Edu que permite criar GPTs: em <https://chatgpt.com/gpts/editor>,
  cole `INSTRUCOES.txt` nas instruções, envie os arquivos de `conhecimento/` e deixe a pesquisa na
  web ligada.

## Gemini — Gem (ou Skill)

1. Abra <https://gemini.google.com/gems/create>.
2. **Nome**: PodFácil. **Instruções**: cole `INSTRUCOES.txt`.
3. Em **Conhecimento**, envie os arquivos de `conhecimento/` (o Gem aceita até 10).
4. **Salvar** e, se quiser, **Compartilhar** para gerar o link.

O Google está trocando Gems por Skills (contas pessoais a partir de novembro de 2026). Os Gems
viram Skills automaticamente; se preferir já usar Skills, a versão plugin traz o `SKILL.md`
pronto para importar no app do Gemini (web ou Mac).
