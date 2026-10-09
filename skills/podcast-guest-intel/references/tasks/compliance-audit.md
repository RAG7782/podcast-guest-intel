---
task: Compliance Audit
responsavel: "@guardian"
responsavel_type: agent
atomic_layer: task
elicit: false
Entrada: |
  - scope: Episodio unico (quick check) ou periodo (auditoria periodica)
  - sponsor-reads: Ad reads e integracoes do periodo
  - music-and-media: Inventario de musicas, imagens e trechos de terceiros (references/legal/music-license-tracker.md)
  - data-practices: Politica de privacidade, newsletter, cookies, formularios de convidado
Saida: |
  - compliance-report: Status por area (OK / AJUSTAR / RISCO) com evidencia
  - remediation-plan: Acoes com responsavel e prazo
Checklist:
  - "[ ] LGPD: dados pessoais citados com base legal ou anonimizados; politica de privacidade atual; newsletter com opt-in; cookies com aviso"
  - "[ ] LGPD art. 11: nenhum dado sensivel inferido; so autodeclaracao voluntaria com aceite especifico e destacado"
  - "[ ] CONAR: publicidade identificada como tal; claims do sponsor verificaveis; cuidado com publico infantil"
  - "[ ] Direito autoral: musica com licenca registrada; citacoes curtas e creditadas; trechos de video licenciados"
  - "[ ] Difamacao: nenhuma acusacao grave sem evidencia publica e fonte"
  - "[ ] Sorteios/promocoes: regras publicadas e conformes a legislacao aplicavel"
  - "[ ] Listar achados e plano de remediacao; reportar a @producer"
---

# *compliance-audit

Auditoria de conformidade legal. Dois modos: **quick check** por episodio (antes da publicacao, junto de `references/tasks/fact-check-review.md` e `references/tasks/ethics-review.md`) e **auditoria periodica** do show inteiro.

Nao substitui parecer juridico: em duvida de difamacao, direito autoral ou regra de promocao, a recomendacao e consultar advogado. Normas citadas em relatorio devem ser conferidas na fonte oficial vigente.

## Formato de saida

```
COMPLIANCE AUDIT — [episodio | periodo]
LGPD:          [OK | AJUSTAR | RISCO] — [evidencia]
CONAR:         [...]
Direito autoral: [...]
Difamacao:     [...]
Promocoes:     [...]
Remediacao: [acao — responsavel — prazo]
```

## Checklist

Os itens `[ ]` do frontmatter (`Checklist:`) sao o passo a passo desta task; todos precisam estar marcados antes de entregar a saida.
