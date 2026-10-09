---
task: Community Building
responsavel: "@growth"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - platform-choice: Discord, Telegram, Circle, Slack
  - community-goals: Engagement, feedback, loyalty
  - moderation-team: Moderadores designados
  - gamification: Pontos, badges, leaderboard
Saida: |
  - community-setup: Servidor Discord/Telegram configurado
  - channels-structure: Canais organizados por topico
  - roles-permissions: Roles e permissoes configuradas
  - engagement-plan: Plano de engajamento 30 dias
Checklist:
  - "[ ] Criar servidor Discord ou grupo Telegram"
  - "[ ] Configurar canais (#geral, #episodios, #off-topic)"
  - "[ ] Definir roles (membro, VIP, moderador)"
  - "[ ] Gamification (pontos, badges, leaderboard MEE6)"
  - "[ ] Listener polls para proximos temas"
  - "[ ] Voicemail submission (perguntas audio)"
  - "[ ] Fan episodes (featuring listeners)"
  - "[ ] Moderation guidelines (toxicidade zero)"
---

# *community-building

Criacao de comunidade em Discord/Telegram. Channels, roles, gamification, listener polls, voicemail, fan episodes. Objetivo: Loyalty e feedback loop.

## Uso

```bash
# Setup Discord completo
*community-building --platform discord --setup full --gamification enabled

# Setup Telegram simples
*community-building --platform telegram --type simple --channels 3

# Launch community (invite blast)
*community-building --launch --invite-blast --target 500-members
```

## Steps (Resumido)

1. **Plataforma**
   - Discord (feature-rich, gamification)
   - Telegram (simples, mobile-first)
   - Circle (paid, premium)

2. **Channels structure (Discord)**
   ```
   #welcome - Boas-vindas
   #anuncios - Novos episodios
   #geral - Chat livre
   #episodios - Discuss episodios
   #sugestoes - Temas futuros
   #off-topic - Diversao
   #voicemail - Enviar audio
   ```

3. **Roles**
   - @Membro (todos)
   - @VIP (supporters, Patreon)
   - @Moderador (equipe)

4. **Gamification (MEE6)**
   - XP por mensagem
   - Levels (level 5 = role especial)
   - Leaderboard
   - Badges

5. **Listener polls**
   - "Qual tema proximo episodio?"
   - "Quem voce quer de guest?"

6. **Voicemail submission**
   - Canal para enviar perguntas audio
   - Melhores vao para episodio

7. **Fan episodes**
   - Featuring listeners
   - Ex: "Best of listener questions"

8. **Moderation**
   - Guidelines: Respeito, sem spam, sem toxicidade
   - Ban se violar

## Criterios de Qualidade

- [ ] Servidor configurado (Discord/Telegram)
- [ ] 5-8 canais organizados
- [ ] Roles e permissoes definidas
- [ ] Gamification ativa (MEE6)
- [ ] Polls mensais para temas
- [ ] Voicemail submission funcionando
- [ ] Moderation guidelines publicadas
- [ ] 500+ membros em 90 dias
