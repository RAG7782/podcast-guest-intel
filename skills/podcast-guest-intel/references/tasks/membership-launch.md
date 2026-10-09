---
task: Membership Launch
responsavel: "@monetizer"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - audience-segments: Segmento de ouvintes assíduos (Pulse, references/tasks/audience-analysis.md)
  - benefits-capacity: O que a equipe consegue entregar todo mês sem falhar
  - platform-options: Patreon, Memberful, Glow, Buy Me a Coffee ou feed premium próprio
Saida: |
  - tier-structure: Tiers, preços, benefícios
  - launch-plan: Cronograma de 4 semanas com donos
  - success-metrics: Meta de membros, MRR, churn
Checklist:
  - "[ ] Benefícios do 1º mês já produzidos antes de anunciar"
  - "[ ] 2-3 tiers pagos, cada um com benefício que a equipe consegue sustentar"
  - "[ ] Plataforma escolhida com taxas conferidas no site oficial na data da decisão"
  - "[ ] Feed premium/ad-free testado (Cast)"
  - "[ ] Termos de uso e política de privacidade dos membros publicados (LGPD)"
  - "[ ] Incentivo de lançamento com prazo/limite claro"
  - "[ ] Onboarding: e-mail de boas-vindas, convite para comunidade, acesso aos benefícios"
  - "[ ] Revisão trimestral de churn (quem saiu e por quê)"
---

# *create-membership

Lança programa de membership como fonte de receita recorrente e menos dependente de sponsors.

## Uso

```bash
*create-membership --platform patreon --tiers 3
*create-membership --review-churn --quarter Q2
```

## Estrutura de tiers (ponto de partida)

| Tier | Benefícios típicos |
|------|--------------------|
| Free | episódios públicos, show notes, comunidade só leitura |
| Supporter | episódios sem anúncio (feed premium), acesso antecipado 24-48 h, participação na comunidade |
| Insider | + bônus exclusivo mensal, Q&A mensal com host, voto em temas |
| Patron | + crédito de produtor executivo, brindes, contato anual com host |

Preços definidos a partir do segmento de Pulse e de pesquisa com a audiência — não de tabela genérica.

## Steps

1. **Pré-lançamento (2-4 semanas):** tiers, preços, página, conteúdo bônus piloto, assets visuais (Pixel).
2. **Semana de lançamento:** anúncio host-read autêntico no episódio, newsletter (`*send-newsletter`, Amp), campanha social (Amp), incentivo limitado.
3. **Pós-lançamento:** onboarding, entrega pontual dos benefícios, contato mensal (Q&A, bastidores).
4. **Retenção:** entregar o prometido, comunidade ativa, extras não prometidos ocasionais, pesquisa de cancelamento.

## Criterios de Qualidade

- [ ] Nenhum benefício prometido sem capacidade de entrega
- [ ] MRR, membros e churn acompanhados mensalmente em `*revenue-report`
