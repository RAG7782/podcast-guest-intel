---
task: Crisis Management
responsavel: "@guardian"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - incident: O que aconteceu, onde surgiu, links/prints
  - episode-ref: Episodio(s) envolvido(s)
  - spread-signal: Sinal de alcance (mencoes, canais, imprensa)
Saida: |
  - severity: Nivel 1-4 com justificativa
  - response-decision: Ignorar | correcao | statement | retirar segmento | retirar episodio | consulta juridica
  - public-statement: Texto aprovado (se houver) para @growth distribuir
  - postmortem: assets/templates/episode-postmortem.md preenchido
Checklist:
  - "[ ] Detectar e registrar o incidente (hora, fonte, evidencia)"
  - "[ ] Avaliar: severidade (1-4), validade da critica, alcance, risco juridico"
  - "[ ] Decidir a resposta pela tabela abaixo e registrar o porque"
  - "[ ] Redigir statement com assets/templates/crisis-response.md (rapido, honesto, assume responsabilidade, diz o que muda)"
  - "[ ] Handoff para @growth publicar; @producer comunica o squad"
  - "[ ] Aplicar correcao conforme assets/templates/corrections-policy.md"
  - "[ ] Post-mortem em ate 1 semana: causa raiz, mudanca de processo, responsavel"
---

# *crisis-response

Protocolo de crise editorial/reputacional. Comunicar cedo com informacao parcial e melhor que silencio prolongado.

## Niveis

| Nivel | Exemplo | Resposta |
|---|---|---|
| 1 Menor | Dado errado sem impacto (data, nome) | Correcao nas shownotes + mencao no proximo episodio |
| 2 Moderado | Guest fez afirmacao problematica, audiencia reclama | Statement + correcao + contexto |
| 3 Grave | Desinformacao significativa, backlash amplo | Disclaimer forte ou retirada + statement + post-mortem |
| 4 Critico | Difamacao, violacao legal, risco existencial | Retirada imediata + consulta juridica + statement |

Prazos de resposta por nivel sao definidos pelo show em `assets/templates/crisis-response.md`; este squad nao fixa numero sem lastro.

## Decisao

| Acao | Quando |
|---|---|
| Ignorar | Ataque de ma-fe, critica invalida |
| Correcao simples | Erro factual menor, nao controverso |
| Statement publico | Questao valida; audiencia merece explicacao |
| Retirar segmento | Parte do episodio e problematica |
| Retirar episodio | Episodio inteiro problematico ou risco juridico |
| Consulta juridica | Nivel 4 ou qualquer duvida de difamacao |

## Checklist

Os itens `[ ]` do frontmatter (`Checklist:`) sao o passo a passo desta task; todos precisam estar marcados antes de entregar a saida.
