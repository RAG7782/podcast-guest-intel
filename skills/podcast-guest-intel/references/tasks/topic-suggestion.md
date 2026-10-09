---
task: Topic Suggestion
responsavel: "@researcher"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - pillars: Content pillars vigentes (assets/templates/podcast-bible.md)
  - calendar: Calendário editorial e lacunas (Max)
  - signals: Perguntas da audiência (Amp), temas em alta, expertise de convidados (Link), dados de tema (Pulse)
Saida: |
  - topic-list: 5-10 temas com ângulo, urgência, pillar, convidado ideal, viabilidade e risco Sentinel
  - priority: Ordem recomendada para Max decidir
Checklist:
  - "[ ] Cada tema tem ângulo único (tema sem ângulo é assunto, não episódio)"
  - "[ ] Urgência classificada: timely, sazonal, evergreen ou trend"
  - "[ ] Mapeado a um pillar; pillar saturado sinalizado"
  - "[ ] Convidado ideal descrito por expertise, não por atributo pessoal"
  - "[ ] Viabilidade (convidado disponível? pesquisa complexa?) e risco Sentinel estimados"
  - "[ ] Prioridade proposta, decisão final de Max"
---

# *suggest-topics

Alimenta o backlog de temas para Max priorizar.

## Uso

```bash
*suggest-topics --pillar P3 --count 5 --mix "timely,evergreen"
```

## Fontes de tema

| Fonte | Cadência | Método |
|-------|----------|--------|
| Tendências em redes e notícias | contínua | monitoramento |
| Perguntas da audiência (Amp, Host) | semanal | DMs, comentários, comunidade |
| Lacunas do calendário (Max) | quinzenal | revisão conjunta |
| Expertise descoberta por Link | quando ocorre | booking |
| Desempenho de temas (Pulse) | mensal | `references/tasks/audience-analysis.md` |
| Evergreens nunca cobertos | trimestral | auditoria do backlog |

## Classificação de urgência

- **Timely:** atrelado a evento/notícia; janela curta.
- **Sazonal:** relevante em período específico (ex.: impostos, planejamento de fim de ano).
- **Evergreen:** sem perda de valor no tempo.
- **Trend:** interesse crescente; janela variável.

Mix por temporada é decisão de Max. Ponto de partida heurístico (não medido): maioria evergreen, com timely/sazonal suficiente para manter o show atual.

## Criterios de Qualidade

- [ ] Nenhum tema sem ângulo e pillar
- [ ] Prioridade justificada
