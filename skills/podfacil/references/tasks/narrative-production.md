---
task: Narrative Production
responsavel: "@engineer"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - narrative-script: Roteiro dramaturgico (3 atos)
  - character-list: Lista de personagens/narradores
  - scene-descriptions: Descricoes de cenas com ambientes
  - production-budget: Orcamento para voiceovers/foley
Saida: |
  - narrative-audio: Episodio narrativo completo
  - multi-narrator-tracks: Tracks separadas por narrador
  - scene-foley: Foley sincronizado por cena
  - production-notes: Notas de producao dramaturgica
Checklist:
  - "[ ] Escrever roteiro dramaturgico completo (3 atos)"
  - "[ ] Casting de voiceovers (narradores, personagens)"
  - "[ ] Gravar cenas com direcao dramatica"
  - "[ ] Montagem nao-linear (pacing cinematico)"
  - "[ ] Sound design cenico (foley, ambientes, SFX)"
  - "[ ] Mix dramatico (espacializacao, profundidade)"
  - "[ ] Music score original (se budget)"
  - "[ ] Masterizar para -16 LUFS (Apple Podcasts spec)"
---

# *narrative-production

Producao de podcast narrativo estilo Serial, Radiolab, This American Life. Workflow completamente diferente de entrevista: roteiro dramaturgico, multi-narrador, montagem nao-linear, sound design cenico.

## Uso

```bash
# Producao narrativa completa
*narrative-production --episode S02E10 --acts 3 --narrators 3 --duration 45min

# Investigativo true crime
*narrative-production --episode S02E12 --genre true-crime --tone suspense
```

## Steps (Resumido)

1. **Roteiro dramaturgico (3 atos)**
   - Ato 1: Setup (personagens, contexto, conflito)
   - Ato 2: Confrontation (desenvolvimento, obstaculos)
   - Ato 3: Resolution (climax, desfecho)

2. **Casting voiceovers**
   - Narrador principal (voz authoritative)
   - Personagens (actors profissionais ou amadores)
   - Considerar diversidade de vozes

3. **Gravacao de cenas**
   - Direcao dramatica (emocao, pacing, enfase)
   - Multiplos takes (escolher melhor performance)

4. **Montagem nao-linear**
   - Cortar entre cenas, narradores, entrevistas
   - Pacing cinematico (variar ritmo)

5. **Sound design cenico**
   - Foley sincronizado (passos, portas, objetos)
   - Ambientes (escritorio, rua, natureza)
   - SFX dramaticos (tensao, impacto)

6. **Mix dramatico**
   - Espacializacao (vozes em diferentes posicoes)
   - Profundidade (reverb para distancia)
   - Music score (trilha original)

## Criterios de Qualidade

- [ ] Arco narrativo claro (inicio, meio, fim)
- [ ] Performances emocionais convincentes
- [ ] Sound design imersivo (foley, ambientes)
- [ ] Pacing cinematico (nao monotono)
- [ ] Mix espacial (depth, positioning)
- [ ] Retencao alta (>70% completion rate)
