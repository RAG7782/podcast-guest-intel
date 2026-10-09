---
task: Brand Refresh
responsavel: "@designer"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - brand-guidelines: Guia atual (assets/templates/brand-guidelines.md)
  - visual-performance: Dados de CTR/engajamento dos assets (do @analyst)
  - feedback: Feedback de audiencia, host e squad sobre a identidade
  - scope: refresh (ajuste de cores/templates) | rebrand (logo e identidade)
Saida: |
  - brand-guidelines-v2: Guia atualizado com changelog da versao
  - updated-templates: Templates de artwork, thumbnail e quote card atualizados
  - rollout-plan: Plano de transicao (o que muda, quando, em quais plataformas)
Checklist:
  - "[ ] Levantar o que nao funciona hoje com dados (@analyst), nao com gosto pessoal"
  - "[ ] Definir escopo: refresh ou rebrand (rebrand exige aprovacao do @producer antes de comecar)"
  - "[ ] Propor 2-3 direcoes e testar em mockup no contexto real (feed, app, miniatura)"
  - "[ ] Validar contraste WCAG AA e leitura por daltonicos"
  - "[ ] Conferir licenca comercial de fontes e imagens"
  - "[ ] Aprovar direcao final com @producer"
  - "[ ] Atualizar assets/templates/brand-guidelines.md com versao e changelog"
  - "[ ] Atualizar templates de producao e avisar @growth, @editor e @engineer"
  - "[ ] Trocar cover art no feed via @distributor (nas specs atuais do diretorio)"
---

# *brand-refresh

Evolucao da identidade visual do podcast com base em dados de performance e feedback, documentada no guia de marca. Aciona-se pelo comando `*update-brand` do @designer.

## Quando usar

- Assets com engajamento caindo de forma consistente (dado do @analyst)
- Mudanca de posicionamento, formato ou publico do show
- Identidade inconsistente entre plataformas, ou templates que nao escalam

## Passos

1. **Diagnostico.** Reunir os dados de performance visual e o feedback. Registrar o problema em uma frase: "o que esta errado e como sabemos".
2. **Escopo.** *Refresh* ajusta paleta, tipografia secundaria e templates, e preserva o reconhecimento. *Rebrand* mexe em logo e identidade, e exige aprovacao previa do @producer, porque reinicia o reconhecimento de marca.
3. **Exploracao.** Montar 2-3 direcoes, cada uma testada em mockup no contexto real: miniatura no app, grid do YouTube e feed do Instagram.
4. **Validacao.** Contraste WCAG AA, simulador de daltonismo, licencas, legibilidade em miniatura.
5. **Aprovacao** do @producer.
6. **Documentacao.** Atualizar `assets/templates/brand-guidelines.md` com o numero da versao, o changelog e exemplos.
7. **Rollout.** Atualizar os templates, avisar o squad e trocar a cover no feed com o @distributor. Rebrand ganha uma data de virada unica, comunicada pelo @growth.

## Criterio de pronto

- Guia versionado, com changelog
- Templates de producao refletindo a nova versao
- Nenhum asset novo publicado com a identidade antiga depois da data de virada
