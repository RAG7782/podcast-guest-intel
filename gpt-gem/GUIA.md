# Como criar o Gem ou o GPT (sem programar)

Este pacote é a versão "sem plugin" do Podcast Guest Intel, para quem usa o Gemini (Gem) ou o
ChatGPT (GPT personalizado). Ele traz só o núcleo grátis: convite, dossiê, pauta de 1 tronco e
roteiro no modo informativo. Sem scripts: os checks automáticos ficam na versão plugin.

## Arquivos

- `INSTRUCOES.txt`: cole no campo de instruções (cabe no limite de 8000 caracteres).
- `conhecimento/`: envie os 8 arquivos como conhecimento.

## ChatGPT — GPT personalizado

1. Abra <https://chatgpt.com/gpts/editor> e vá na aba **Configurar**.
2. **Nome**: Podcast Guest Intel. **Instruções**: cole o conteúdo de `INSTRUCOES.txt`.
3. Em **Conhecimento**, clique em **Carregar arquivos** e envie os arquivos de `conhecimento/`.
4. Em **Recursos**, deixe **Pesquisa na web** ligada (o dossiê precisa dela).
5. **Criar** → escolha quem pode usar (só você, quem tiver o link, ou a GPT Store).

## Gemini — Gem (ou Skill)

1. Abra <https://gemini.google.com/gems/create>.
2. **Nome**: Podcast Guest Intel. **Instruções**: cole `INSTRUCOES.txt`.
3. Em **Conhecimento**, envie os arquivos de `conhecimento/` (o Gem aceita até 10).
4. **Salvar** e, se quiser, **Compartilhar** para gerar o link.

O Google está trocando Gems por Skills (contas pessoais a partir de novembro de 2026). Os Gems
viram Skills automaticamente; se preferir já usar Skills, a versão plugin traz o `SKILL.md`
pronto para importar no app do Gemini (web ou Mac).
