# PodFácil 2.2.1

Prepara episódios de podcast com convidado: convite, formulário, dossiê com fontes, pauta,
roteiro, memória e localização. Núcleo aberto (Apache-2.0). Repositório: https://github.com/RAG7782/podcast-guest-intel.

- Skill orquestradora: `skills/podfacil/SKILL.md`
- 13 especialistas (subagentes): `agents/`
- Manifestos: `.claude-plugin/` (Claude), `plugin.json` (Agent Plugins: Codex, Hermes, agy),
  `.codex-plugin/` (Codex legado), `.agents/plugins/marketplace.json` (marketplace Codex)

Claude Code, a partir da pasta deste pacote (ou de um repositório GitHub que o contenha):

```text
/plugin marketplace add ./
/plugin install podfacil@guest-intel
```

Grátis × pago: o grátis roda inteiro aqui, sem chave. O pago vem pelo servidor MCP do PodFácil
(pauta em 3 troncos, 7 modos de roteiro, coleta do X, plano de dublagem) ou roda aqui conferindo a
chave de licença (memória do show, formulário completo e automações). Detalhes e como configurar a
chave: `skills/podfacil/SKILL.md` (seção "Grátis × pago") e `INSTALL.md`. Planos: https://antecena.artesanatodigital.com/precos/.
Estúdios, produtoras e redes: fale conosco em contato@artesanatodigital.com.

Instalação passo a passo para cada harness: [`INSTALL.md`](INSTALL.md).
