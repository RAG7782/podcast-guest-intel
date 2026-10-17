---
task: Topic Research
responsavel: "@researcher"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - topic: Tema aprovado por Max
  - format: Entrevista, solo, painel ou série
  - deadline: Data de gravação (research fecha 72 h antes, para Sentinel validar)
Saida: |
  - research-doc: Landscape, ângulo único, fontes, story beats, contranarrativa, claims marcados, convidado ideal
  - claims-for-sentinel: Lista de afirmações factuais com fonte e status
Checklist:
  - "[ ] Landscape: quem já cobriu e com que ângulo; o que está saturado"
  - "[ ] Fontes primárias localizadas (estudo original, dado oficial, documento), não só o artigo que as cita"
  - "[ ] Para cada dado: data, metodologia/amostra e se diz o que parece dizer"
  - "[ ] Ângulo único em uma frase"
  - "[ ] Contranarrativa: quem discorda e por quê"
  - "[ ] Story beats (setup, desenvolvimento, virada, resolução)"
  - "[ ] Todo claim factual marcado [FACT-CHECK NEEDED] ou [VERIFIED] com referência completa"
  - "[ ] Dados pessoais de terceiros só se públicos e pertinentes ao tema (LGPD)"
  - "[ ] Entregue a Sentinel 72 h antes da gravação"
---

# *research-topic

Deep dive em um tema pelo framework DIAMOND (`agents/researcher.md`): Discovery, Investigation, Angle, Mapping, Opposition, Narrative. Roteiro só começa com D, I e A completos.

## Uso

```bash
*research-topic --topic "burnout em founders" --format entrevista --recording 2026-04-10
*research-topic --topic "open finance" --format solo
```

## Hierarquia de fontes

| Tier | Tipo | Uso |
|------|------|-----|
| 1 — primária | estudo revisado por pares, dado oficial (IBGE, Banco Central), documento público, depoimento em 1a pessoa | preferência absoluta |
| 2 — secundária confiável | livro de especialista, relatório de instituto de pesquisa, jornalismo de referência, entrevista em veículo estabelecido | com referência completa |
| 3 — complementar | blog de especialista, podcast/entrevista anterior, relatório de empresa (viés de negócio), Wikipedia | contexto, nunca como dado final |
| Nunca | post anônimo, "fonte confiável" sem nome, dado sem metodologia, site sensacionalista | — |

## Protocolo de verificação de um claim

1. Subir até a origem (artigo que cita estudo → o estudo).
2. Conferir a data e buscar versão mais recente.
3. Conferir metodologia e tamanho de amostra.
4. Conferir se o dado diz o que se afirma (não over-reading).
5. Marcar no doc:

```text
[FACT-CHECK NEEDED: "<citação exata>"
 Fonte: <autor, título, ano, n, link>
 Status: PENDENTE validação Sentinel]
```

Sentinel devolve VERIFIED / NEEDS-UPDATE / REMOVE / FLAG-AS-OPINION (`references/tasks/fact-check-review.md`).

## Por formato

- **Entrevista:** trajetória do convidado, 2-3 entrevistas anteriores ouvidas (o que já foi coberto), tema principal com contranarrativa; insumo para `references/tasks/episode-briefing.md` e `references/tasks/interview-prep.md`.
- **Solo:** sem fonte primária, sem episódio; contranarrativa obrigatória.
- **Painel:** pesquisa individual por convidado e mapa de pontos de discordância entre eles.
- **Série:** arco definido com Max antes; cada episódio aprofunda um aspecto; vocabulário consistente.

## Template de saída

```text
RESEARCH DOC — [Título] | Scout | EP [XX] | [data] | [formato]
LANDSCAPE: [o que já existe, quem cobriu, o que está saturado]
ÂNGULO ÚNICO: [1 frase]
FONTES (tier): 1. [autor, título, ano, link] ...
STORY BEATS: 1 setup | 2 desenvolvimento | 3 virada | 4 resolução
CONTRANARRATIVA: [quem discorda, fonte]
FACTS PARA SENTINEL: "[citação]" (fonte, status)
CONVIDADO IDEAL: [perfil + por quê]
```

## Criterios de Qualidade

- [ ] Nenhum claim sem fonte rastreável
- [ ] Contranarrativa presente
- [ ] Ângulo único explícito
