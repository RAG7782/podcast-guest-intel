# Política de Diversidade e Inclusão

## Compromisso

Este podcast se compromete com **representatividade, diversidade e inclusão** em todas as dimensões de produção de conteúdo: convidados, temas, perspectivas, linguagem e acessibilidade.

**Objetivo:** Criar um podcast que reflita a diversidade do mundo real e seja acessível a todas as pessoas.

---

## 1. Meta de Convidados

### Representatividade Mínima por Temporada

**Regra de dados (LGPD):** a equipe **nunca infere** atributo de identidade de um
convidado (raça/etnia, gênero, orientação sexual, deficiência, saúde, religião, opinião
política). Inferência sobre dado sensível é tratamento sem base legal (art. 5, II e art. 11).

**Meta (critérios não sensíveis, observáveis no trabalho público):**
- **Geografia:** Vozes do Norte/Nordeste (em podcasts do Sudeste), vozes de países do Sul Global
- **Área e tipo de organização:** setores e instituições variados
- **Trajetória/senioridade:** não só C-level; autodidatas, formação técnica, transição de carreira
- **Estreantes:** pessoas que nunca foram convidadas de podcast

**Representatividade de identidade** (gênero, raça/etnia, orientação sexual, PcD, idade
e background socioeconômico quando declarados): só por **autodeclaração voluntária e
opcional** do próprio convidado no formulário, com aviso de que é dado sensível,
consentimento específico e destacado (art. 11, I), opção "prefiro não responder" e
revogação. Usada só em agregado da temporada; dimensão com < 5 respostas não é reportada.

### Como Medir

**Fórmula:** score de critérios não sensíveis de `references/checklists/diversity-check.md`
(fora do Sudeste, junior/mid, áreas distintas, estreantes). Meta: 75+ pontos.

**Exemplo:**
- Temporada 1: 10 episódios
- 3 fora do Sudeste, 4 junior/mid, 5 áreas, 3 estreantes
- **Resultado:** 100 pontos ✅

### Interseccionalidade e autodeclaração

Uma pessoa pode pertencer a vários grupos — mas só a própria pessoa diz a quais, se
quiser. O agregado de autodeclaração conta cada resposta por dimensão declarada e nunca
completa o que não foi declarado.

**Objetivo:** Diversidade autêntica, não tokenização.

---

## 2. Diversidade de Temas

### Perspectivas Diversas

Ao escolher temas, buscar ativamente:
- **Perspectivas não-mainstream:** Não apenas o que já é amplamente coberto
- **Histórias locais:** Não apenas contexto global, mas também realidades brasileiras/regionais
- **Vozes de campo:** Não apenas acadêmicos/teóricos, mas praticantes, ativistas, comunidades
- **Contra-narrativas:** Questionar narrativas dominantes quando apropriado

### Evitar

- ❌ **Monocultura de temas:** Todos os episódios sobre a mesma perspectiva
- ❌ **"Único representante":** Chamar uma única pessoa de um grupo para "representar" todo o grupo
- ❌ **Temas tokenizados:** Só falar de diversidade em episódios específicos, mas ignorar em outros

**Exemplo do que fazer:**
- Episódio sobre IA: convidar mulher negra que trabalha com ética em IA, não só homens brancos do Vale do Silício

---

## 3. Linguagem Inclusiva

### Princípios

- **Evitar termos depreciativos:** Nunca usar termos ofensivos, mesmo em contexto de citação (use "termo depreciativo" ou censure)
- **Evitar generalizações:** "Todos os [grupo]..." raramente é verdade
- **Linguagem neutra quando possível:** Usar "pessoas" em vez de "homens" em contextos genéricos
- **Respeitar pronomes:** Usar pronomes corretos dos convidados (ele/ela/elu/they)

### Checklist de Linguagem

**Evitar:**
- ❌ "Portador de deficiência" → ✅ "Pessoa com deficiência" ou "PcD"
- ❌ "Homossexualismo" (sufixo -ismo implica doença) → ✅ "Homossexualidade"
- ❌ "Mulata", "moreno" → ✅ "Negra", "parda" (termos IBGE)
- ❌ "Dono de casa" (generalizando) → ✅ "Pessoa que cuida da casa"
- ❌ "Cadeirante preso à cadeira" → ✅ "Usuário de cadeira de rodas"
- ❌ "Bipolar" como metáfora → ✅ Evitar usar condições de saúde mental como metáfora negativa

### Termos Técnicos

Quando usar termos técnicos ou de comunidades específicas:
- **Explicar no contexto:** Não assumir que audiência conhece
- **Respeitar autodefinição:** Se uma pessoa se identifica de certa forma, usar aquela forma

---

## 4. Acessibilidade

Acessibilidade É diversidade. Ver detalhes completos em **accessibility-standards.md**.

### Resumo de Obrigações

- ✅ **Transcrição** em todos os episódios
- ✅ **Chapters** para navegação
- ✅ **Content warnings** timestamped
- ✅ **Legendas** em vídeos
- ✅ **Alt text** em imagens
- ✅ **Volume consistente** e voz clara

---

## 5. Representação Visual

### Artwork e Thumbnails

- **Diversidade visual:** Usar imagens que representem diversidade de pessoas
- **Evitar estereótipos:** Não usar apenas representações estereotipadas de grupos
- **Ilustrações inclusivas:** Pessoas de diferentes etnias, corpos, idades

### Vídeo Podcast

- **Cenário neutro ou representativo:** Evitar cenários que excluam culturalmente
- **Enquadramento:** Incluir pessoas com deficiência de forma respeitosa (não focar apenas na deficiência)

---

## 6. Monitoramento — Diversity Check Trimestral

### Checklist Trimestral

**Convidados:**
- [ ] Meta de 40% atingida?
- [ ] Diversidade interseccional presente?
- [ ] Algum grupo está sub-representado demais?

**Temas:**
- [ ] Temas diversos cobertos?
- [ ] Perspectivas não-mainstream incluídas?
- [ ] Evitamos monocultura?

**Linguagem:**
- [ ] Termos inclusivos usados consistentemente?
- [ ] Houve feedback negativo sobre linguagem?
- [ ] Hosts/equipe estão atualizados sobre terminologia?

**Acessibilidade:**
- [ ] 100% dos episódios têm transcrição?
- [ ] Content warnings foram usados quando apropriado?
- [ ] Houve feedback sobre acessibilidade?

**Visual:**
- [ ] Artwork representa diversidade?
- [ ] Thumbnails evitam estereótipos?

### Registro

Documentar resultados em `assets/data/diversity-metrics.yaml`:

```yaml
quarter: 2026-Q1
guests:
  total: 12
  underrepresented: 8
  percentage: 66.7%
  breakdown:          # criterios nao sensiveis
    outside_southeast: 4
    junior_mid: 3
    distinct_areas: 5
    first_time_guests: 4
  self_declared:       # agregado de autodeclaracao voluntaria; nunca inferido
    responses: 6
    reported: false    # nenhuma dimensao com 5+ respostas
themes:
  diverse_perspectives: true
  notes: "Incluímos episódio sobre acessibilidade em tech, perspectiva indígena sobre IA"
language:
  issues: 0
  feedback: "Positivo sobre uso de pronomes neutros"
accessibility:
  transcripts: 100%
  warnings: 3 episódios
```

---

## 7. Ações Corretivas

### Se Abaixo da Meta

**Meta de 40% não atingida:**

1. **Identificar gaps:** Quais grupos estão faltando?
2. **Busca ativa:** Priorizar convites para grupos sub-representados
3. **Expandir rede:** Pedir indicações, buscar em comunidades diversas
4. **Revisar critérios:** Verificar se critérios de seleção têm viés implícito

### Se Feedback Negativo sobre Linguagem

1. **Ouvir e reconhecer:** Não ser defensivo
2. **Corrigir:** Publicar correção/errata se necessário
3. **Aprender:** Atualizar conhecimento sobre terminologia
4. **Prevenir:** Adicionar revisão de linguagem no workflow

### Se Problemas de Acessibilidade

1. **Corrigir imediatamente:** Adicionar transcrição/legenda faltante
2. **Revisar processo:** Identificar onde falha ocorreu
3. **Prevenir:** Tornar acessibilidade obrigatória no checklist pré-publicação

---

## 8. Priorização Ativa vs. Quotas

### Não É Quota

**Esta política NÃO é:**
- Sistema de quota rígido ("exatamente 50% mulheres")
- Priorização baseada APENAS em identidade (qualificação importa)
- Tokenização (chamar alguém só para "cumprir meta")

### É Priorização Ativa

**Esta política É:**
- Busca intencional de vozes diversas
- Combate a viés implícito na seleção
- Reconhecimento de que "meritocracia" pura ignora desigualdades estruturais
- Compromisso de amplificar vozes historicamente excluídas

**Princípio:** Se dois candidatos são igualmente qualificados, priorizar o de grupo sub-representado.

---

## 9. Educação Contínua

### Para a Equipe

- **Treinamento:** Ler artigos, assistir talks sobre diversidade e inclusão
- **Feedback:** Criar canal para audiência dar feedback sobre D&I
- **Sensibilidade:** Entender impacto de linguagem e representação
- **Humildade:** Reconhecer que sempre há mais a aprender

### Recursos Recomendados

- **Livros:** "Como Ser Antirracista" (Ibram X. Kendi), "Lugar de Fala" (Djamila Ribeiro)
- **Guias:** Guia de Comunicação Inclusiva (várias ONGs publicam)
- **Podcasts:** Ouvir podcasts feitos por pessoas de grupos diversos

---

## 10. Responsabilidade

### Responsável Principal

**@guardian (Sentinel)** é o guardião desta política.

**Funções:**
- Conduzir diversity check trimestral
- Revisar linguagem antes de publicação
- Sinalizar quando meta de convidados está em risco
- Sugerir ações corretivas

### Corresponsabilidade

**Toda a equipe** é responsável por D&I:
- **@producer:** Priorizar convidados diversos na curadoria
- **@researcher:** Usar linguagem inclusiva em roteiros
- **@host:** Usar linguagem inclusiva durante gravação
- **@editor:** Incluir content warnings quando necessário
- **@designer:** Usar alt text em todas as imagens

---

## 11. Revisão Anual

Esta política deve ser **revisada anualmente** para:

- Atualizar terminologia (linguagem evolui)
- Ajustar metas se necessário
- Incorporar feedback da audiência
- Refletir mudanças na sociedade e no podcast

**Próxima revisão:** [Data — 1 ano após implementação]

---

## 12. Comunicação com Audiência

### Transparência

**Comunicar publicamente:**
- Compromisso com diversidade
- Metas e progresso (pode ser anual)
- Erros e correções quando ocorrerem

**Exemplo de comunicação anual:**
```
Em 2026, 65% dos nossos convidados foram de vozes sub-representadas,
superando nossa meta de 40%. Continuamos comprometidos com representatividade
autêntica e perspectivas diversas.
```

### Feedback

**Canal aberto:**
- Email para feedback sobre D&I
- Formulário anônimo para reportar problemas
- Resposta a críticas construtivas

---

## 13. Casos Especiais

### Podcast Nicho (ex: "Podcast de CEOs")

Se o podcast tem nicho específico que naturalmente limita diversidade (ex: todos os convidados são CEOs, grupo historicamente homogêneo):

**Ainda assim:**
- Buscar CEOs de grupos sub-representados
- Expandir definição de "CEO" (startups, ONGs, cooperativas, não só corporações)
- Incluir episódios sobre barreiras que grupos enfrentam para chegar a posições de liderança

### Podcast Solo (sem convidados)

Se o podcast é solo:
- Diversidade de **temas** e **perspectivas** se torna ainda mais crítica
- Host deve buscar ativamente fontes diversas para pesquisa
- Convidar colaboradores diversos (co-hosts temporários, especialistas)

---

## 14. Princípio Orientador

**"Diversidade não é checkbox, é compromisso."**

Não basta ter números. É necessário:
- Respeito genuíno
- Amplificação de vozes, não exploração
- Reconhecimento de privilégios e vieses
- Disposição para errar, aprender e melhorar

---

**Responsável:** @guardian (Sentinel)
**Revisão:** Anual
**Última atualização:** 2026-02-11
