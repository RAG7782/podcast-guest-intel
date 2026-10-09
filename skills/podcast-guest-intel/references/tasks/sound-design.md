---
task: Sound Design
responsavel: "@composer"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - episode-script: Roteiro com marcacoes de sound design
  - brand-sonic-identity: Guidelines de identidade sonora
  - production-level: Standard, elevated, cinematic
  - music-style: Genero/vibe da trilha
  - deliverables: full | music-only (trilha/score) | jingle (audio logo/vinheta) | narrative (ambientes + foley)
Saida: |
  - custom-music: Trilhas originais (intro, outro, beds, stingers, scores de episodio especial)
  - audio-logo: Audio logo / vinheta (3-10s) em versoes full, short e stinger
  - sfx-library: Biblioteca de SFX customizados
  - transitions: Transicoes sonoras entre blocos
  - sonic-branding-guide: Guia de identidade sonora atualizado
Checklist:
  - "[ ] Criar tema principal do podcast (intro/outro)"
  - "[ ] Criar audio logo / vinheta (3-10s) quando pedido via *make-jingle"
  - "[ ] Compor score de episodio especial quando pedido via *compose-score"
  - "[ ] Produzir music beds (background durante fala)"
  - "[ ] Criar stingers (pontuacoes curtas 2-5s)"
  - "[ ] Produzir transicoes entre blocos"
  - "[ ] Adicionar ambientes sonoros (se narrativo)"
  - "[ ] Gravar foley artesanal (passos, portas, objetos)"
  - "[ ] Garantir consistencia de sonic branding"
  - "[ ] Masterizar todos elementos para -16 LUFS"
  - "[ ] Organizar biblioteca de assets"
  - "[ ] Documentar guia de uso dos elementos"
---

# *sound-design

Criacao de identidade sonora completa do podcast: trilhas originais, audio logo, transicoes, stingers, ambientes, foley. Eleva producao de conversacional para cinematico, mantendo consistencia de brand.

Esta task atende tres comandos do @composer: `*design-sound` (pacote completo ou narrativo), `*compose-score` (`--deliverables music-only`) e `*make-jingle` (`--deliverables jingle`). Spatial audio e outra task: `references/tasks/spatial-audio-production.md`.

## Uso

```bash
# Sound design completo para novo podcast
*sound-design --podcast "Nome Show" --style cinematic --deliverables full

# Apenas trilhas (intro/outro/beds ou score de episodio especial) — *compose-score
*sound-design --episode S02E03 --deliverables music-only

# Audio logo / vinheta — *make-jingle
*sound-design --podcast "Nome Show" --deliverables jingle

# Sound design narrativo (ambientes + foley)
*sound-design --episode S02E10 --format narrative --sfx heavy
```

## Steps

1. **Entender o sonic brand do podcast** — revisar `podcast-bible`: audiencia, brand adjectives (profissional, intimista, energetico...), podcasts de referencia (o que gostam/nao gostam sonoramente), genero musical.

2. **Criar tema principal (intro/outro)**
   - Intro 15-30s: hook melodico memoravel, build → drop para a voz, espaco para voiceover opcional, fade in curto.
   - Instrumentacao alinhada ao brand (ex.: corporativo = piano/strings; tech = synths/arpeggios; intimista = violao/piano solo; energetico = drums/guitarras).
   - Versoes: full (30s, trailers/estreia), short (15s, episodios regulares), outro (versao conclusiva do tema).

3. **Audio logo / vinheta (`*make-jingle`)**
   - 3-10s, derivado do motif do tema principal (mesma paleta).
   - Workshop curto com @producer e @designer: personalidade, 3-5 referencias, emocao alvo.
   - 3-5 esbocos (vocal × instrumental, organico × sintetico) → @producer escolhe → versoes full, short e stinger (~1s).
   - Entregar timing de cada evento sonoro para o @designer sincronizar o logo animado.

4. **Score de episodio especial (`*compose-score`)**
   - Para series tematicas, episodios narrativos ou marcos (ex.: Ep 100).
   - Briefing com @producer/@researcher: tom, arco emocional por segmento, referencias.
   - Esboco 2-3 direcoes → aprovacao → arranjo completo → stems separados para o @engineer.

5. **Music beds** — textura emocional sem competir com a voz.
   - Evitar a faixa da voz (aprox. 300 Hz-4 kHz) com EQ; movimento sutil; loop seamless de 2-3 min.
   - Tipos: tension, contemplative, upbeat, neutral. Sem drums fortes, melodias chamativas ou vocals.

6. **Stingers (2-5s)** — transition, emphasis, question, humor. Simples, iconicos, mesma paleta do tema, varias versoes de pitch.

7. **Transicoes** — whoosh + impact (1-2s), musical bridge (8-15s) ou ambient (mudanca de cenario, para narrativos). 5-8 variacoes, naming `transition_01_whoosh_impact.wav`.

8. **Ambientes (se narrativo)** — field recording (gravador portatil) ou biblioteca licenciada; EQ cortando <80 Hz; loop continuo; fade in/out 3-5s.

9. **Foley (se narrativo)** — passos, portas, papel, objetos; varios takes; sync no DAW; reverb compativel com a cena; volume proporcional a distancia.

10. **Consistencia de sonic branding** — mesma paleta (instrumentos, key, faixa de BPM) em tema, beds, stingers e transicoes. Qualquer mudanca de paleta exige aprovacao do @producer.

11. **Masterizar** — -16 LUFS integrado (recomendacao Apple Podcasts para fala), true peak -1 dBFS, 48 kHz/24-bit WAV; dither se exportar 16-bit.

12. **Organizar biblioteca e documentar** — estrutura de pastas abaixo + `sonic-branding-guide.md`.

```
/sound-design/
├── themes/       intro_full_30s.wav, intro_short_15s.wav, outro_30s.wav
├── logo/         audio_logo_full.wav, audio_logo_short.wav, audio_logo_stinger.wav
├── beds/         tension_bed_2min.wav, contemplative_bed_2min.wav, upbeat_bed_2min.wav
├── stingers/     transition_01.wav, emphasis_01.wav, question_01.wav
├── transitions/  whoosh_impact_01.wav, musical_transition_01.wav
├── ambiences/    office_loop.wav, cafe_loop.wav, street_loop.wav
└── foley/        footsteps_wood_01.wav, door_open_01.wav
```

## Output

### sonic-branding-guide.md (estrutura)

```markdown
# Sonic Branding Guide: {Nome Podcast}

**Compositor:** @composer · **Data:** {AAAA-MM-DD} · **Versao:** 1.0

## Identidade Sonora
- Brand adjectives: {3-4 adjetivos}
- Paleta: {instrumentos}, key {X}, BPM {faixa}, genero {X}
- Reference tracks: {2-3 faixas e o que cada uma inspira}

## Elementos e Uso
| Elemento | Arquivo | Duracao | Quando usar |
|----------|---------|---------|-------------|
| Intro (short) | themes/intro_short_15s.wav | 15s | Inicio de todo episodio |
| Intro (full) | themes/intro_full_30s.wav | 30s | Trailers, especiais |
| Outro | themes/outro_30s.wav | 30s | Final de todo episodio |
| Audio logo | logo/audio_logo_full.wav | 3-5s | Abertura, final de clips |
| Beds | beds/*.wav | loop 2min | Momentos dramaticos/reflexivos/energeticos |
| Stingers | stingers/*.wav | 2-5s | Entre blocos, apos frase de impacto |
| Transicoes | transitions/*.wav | 1-15s | Mudanca de topico ou de convidado |
| Ambiences | ambiences/*.wav | loop | So narrativo: localizar a cena |

## Don'ts
- {generos/efeitos fora do brand}
```

### Niveis de referencia na mixagem

Ponto de partida para o @engineer, nao regra: o nivel final e decidido no mix contra a voz.

| Elemento | Nivel relativo | Quando |
|----------|----------------|--------|
| Intro/Outro sem voz | 0 dB | Sem fala |
| Intro sob voz | aprox. -18 dB (duck) | Voz entra |
| Music beds | aprox. -28 dB | Durante fala |
| Stingers / transicoes | aprox. -6 dB | Pontuacoes |
| Ambiences | aprox. -38 dB | Background sutil |
| Foley | -10 a -30 dB | Conforme distancia |

### Uso correto × incorreto

```
CORRETO
0:00-0:15  Intro (fade para voz)
0:15-2:00  Fala sem musica
2:00-5:00  Historia tensa [tension bed]
5:00-5:02  [whoosh_impact_01]
...        Outro

INCORRETO
- Musica tocando o episodio inteiro (compete com a voz)
- Stinger a cada frase (diluir a pontuacao; usar com parcimonia)
```

## Criterios de Qualidade

- [ ] Tema intro/outro memoravel e alinhado com brand
- [ ] Audio logo reconhecivel e coerente com o tema (se pedido)
- [ ] Music beds sutis, sem competir com a voz
- [ ] Stingers iconicos e reconheciveis (2-5s)
- [ ] Transicoes suaves e profissionais
- [ ] Ambientes e foley sincronizados (se narrativo)
- [ ] Consistencia de sonic branding (mesma paleta sonora)
- [ ] Todos elementos masterizados para -16 LUFS / true peak -1 dBFS
- [ ] Biblioteca organizada com naming claro
- [ ] Sonic branding guide documentado
- [ ] Licenca de qualquer material de terceiros registrada em references/legal/music-license-tracker.md
- [ ] Stems e assets em WAV 48kHz/24bit (lossless)
