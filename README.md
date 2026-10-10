# Podcast Guest Intel 1.0.1

Prepara episódios de podcast com convidado: convite, formulário, dossiê com fontes, pauta,
roteiro, memória e localização. Núcleo aberto (Apache-2.0). Repositório: https://github.com/RAG7782/podcast-guest-intel.

- Skill orquestradora: `skills/podcast-guest-intel/SKILL.md`
- 13 especialistas (subagentes): `agents/`
- Manifestos: `.claude-plugin/` (Claude), `plugin.json` (Agent Plugins: Codex, Hermes, agy),
  `.codex-plugin/` (Codex legado), `.agents/plugins/marketplace.json` (marketplace Codex)

Claude Code, a partir da pasta deste pacote (ou de um repositório GitHub que o contenha):

```text
/plugin marketplace add ./
/plugin install podcast-guest-intel@guest-intel
```

Instalação passo a passo para cada harness: [`INSTALL.md`](INSTALL.md).
