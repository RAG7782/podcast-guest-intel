# Workflow: Content Lifecycle

## Visao Geral
- **Objetivo:** Gerenciar ciclo completo do conteudo desde publicacao ate arquivo ou remocao
- **SLA Total:** Lifecycle continuo (monitoring ativo primeiros 30 dias)
- **Owner:** @editor + @guardian

## Etapas

### Fase 1: Publicacao (Dia 0)
- **Owner:** @distributor
- **Entrada:** Episodio aprovado e pronto
- **Saida:** Episodio publicado em todas as plataformas
- **Checklist:**
  - [ ] Upload para hosting (RSS feed)
  - [ ] Publicar em Apple Podcasts, Spotify, YouTube, Amazon Music
  - [ ] Publicar show notes no site
  - [ ] Publicar transcript
  - [ ] Ativar monetizacao (ads, V4V)
  - [ ] Tag inicial: [ACTIVE]

### Fase 2: Monitoring Ativo (Dias 1-30)
- **Owner:** @analyst + @guardian
- **Entrada:** Episodio publicado
- **Saida:** Report de performance + classificacao (Evergreen ou Topical)
- **Checklist:**
  - [ ] Dias 1-7: Monitoring intensivo
    - [ ] Acompanhar downloads/plays diarios
    - [ ] Monitorar comentarios (Apple, Spotify, YouTube)
    - [ ] Responder comentarios/reviews
    - [ ] Acompanhar mencoes em social
    - [ ] Detectar issues (audio, fact-check, controversia)
  - [ ] Dias 8-30: Monitoring regular
    - [ ] Analytics semanais
    - [ ] Engagement em social
    - [ ] Listener feedback (emails, DMs)
    - [ ] Identificar trending topics (oportunidade de follow-up)
  - [ ] Dia 30: Classificacao
    - [ ] Evergreen: conteudo atemporal, pode ser repromovido
    - [ ] Topical: conteudo ligado a momento especifico
    - [ ] Update tag: [EVERGREEN] ou [TOPICAL]

### Fase 3: Evergreen Management
- **Owner:** @editor
- **Entrada:** Episodio classificado como Evergreen
- **Saida:** Conteudo mantido ativo e repromovido periodicamente
- **Checklist:**
  - [ ] Manter ativo indefinidamente
  - [ ] Re-promover periodicamente:
    - [ ] A cada 6 meses: post em social
    - [ ] Incluir em "best of" ou playlists tematicas
    - [ ] Mencionar em newsletter (evergreen recommendations)
  - [ ] Atualizar show notes se necessario:
    - [ ] Links quebrados
    - [ ] Informacoes desatualizadas (adicionar nota: "Update: ...")
    - [ ] Novos recursos mencionados
  - [ ] SEO maintenance:
    - [ ] Verificar ranking de keywords (trimestral)
    - [ ] Atualizar meta description se necessario
    - [ ] Internal links de novos episodios relacionados

### Fase 4: Topical Management
- **Owner:** @editor
- **Entrada:** Episodio classificado como Topical
- **Saida:** Conteudo mantido com contexto temporal
- **Checklist:**
  - [ ] Adicionar nota temporal:
    - [ ] No inicio do episodio (audio): "Este episodio foi gravado em [data]"
    - [ ] Em show notes: "Contexto: Este episodio discute [evento] de [data]"
  - [ ] Manter acessivel (nao remover)
  - [ ] Nao re-promover (exceto se virar relevante novamente)
  - [ ] Monitorar comentarios (podem vir anos depois)
  - [ ] Se informacao ficar desatualizada:
    - [ ] Adicionar "Update: [nova info]" em show notes
    - [ ] Considerar episodio follow-up

### Fase 5: Correcao de Erros
- **Owner:** @guardian + @engineer
- **Entrada:** Erro identificado (fact-check, audio, disclosure)
- **Saida:** Erro corrigido e comunicado
- **Checklist:**
  - [ ] Identificacao do Erro:
    - [ ] Reportado por listener, equipe, press
    - [ ] Erro factual, audio issue, missing disclosure
  - [ ] Avaliar Severidade:
    - [ ] Nivel 1 (Baixo): erro menor (typo, link quebrado)
    - [ ] Nivel 2 (Medio): erro factual, audio issue
    - [ ] Nivel 3 (Alto): conteudo problematico, missing disclosure critico
  - [ ] Correcao Nivel 1:
    - [ ] Corrigir show notes/transcript
    - [ ] Nao precisa comunicar publicamente
  - [ ] Correcao Nivel 2:
    - [ ] Adicionar "Errata" no inicio das show notes
    - [ ] Mencionar correcao em proximo episodio (se relevante)
    - [ ] Re-upload de audio (se audio issue)
  - [ ] Correcao Nivel 3:
    - [ ] Seguir workflow crisis-management.md
    - [ ] Remover episodio temporariamente se necessario
    - [ ] Statement publico (blog, social)

### Fase 6: Takedown (Remocao)
- **Owner:** @guardian + @producer
- **Entrada:** Pedido formal de remocao ou decisao interna
- **Saida:** Episodio removido com comunicacao adequada
- **Checklist:**
  - [ ] Pedido de Remocao:
    - [ ] Quem pediu? (guest, legal, listener, equipe)
    - [ ] Por que? (conteudo problematico, legal issue, request do guest)
  - [ ] Review Interno:
    - [ ] Avaliar se remocao e necessaria
    - [ ] Consultar legal (se aplicavel)
    - [ ] Decisao: manter, editar, ou remover?
  - [ ] Processo de Remocao:
    - [ ] Remover de todas as plataformas (Apple, Spotify, YouTube, etc)
    - [ ] Manter show notes com nota: "Este episodio foi removido em [data]"
    - [ ] Se remocao parcial: re-upload de versao editada
  - [ ] Comunicacao:
    - [ ] Nivel de transparencia (depende do motivo)
    - [ ] Statement publico (se necessario)
    - [ ] Notificar guest (se aplicavel)
    - [ ] Notificar audiencia (se relevante)
  - [ ] Arquivo Interno:
    - [ ] Manter backup do episodio original (legal protection)
    - [ ] Documentar motivo da remocao
    - [ ] Post-mortem interno

## Diagrama

```
[Publicacao] (Dia 0)
      |
      v
[Monitoring Ativo] (Dias 1-30)
      |
      +------------------+
      |                  |
      v                  v
[EVERGREEN]        [TOPICAL]
      |                  |
      v                  v
[Re-promover]    [Adicionar contexto]
[Atualizar]      [Manter acessivel]
      |                  |
      +--------+---------+
               |
               v
      [Correcao de Erros?]
               |
         +-----+-----+
         |           |
         v           v
     [Corrigir]  [Crisis Management]
                     |
                     v
                [Takedown?]
                     |
                     v
            [Remover + Comunicar]
                     |
                     v
            [Arquivo Interno]
```

## Classificacao de Conteudo

| Tipo | Exemplo | Acao |
|------|---------|------|
| Evergreen | "Como comecar um podcast", "Entrevista com expert atemporal" | Re-promover, manter SEO |
| Topical | "Analise das eleicoes 2024", "Reacao ao evento X" | Contexto temporal, nao re-promover |
| Seasonal | "Especial de fim de ano", "Back to school" | Re-promover anualmente |
| Series | Miniseries de 4 episodios | Re-promover como binge |

## Metricas de Sucesso
- **Evergreen Ratio:** 40%+ dos episodios classificados como Evergreen
- **Long-tail Traffic:** 30%+ dos downloads sao de episodios >90 dias
- **Correction Rate:** <5% dos episodios precisam de correcao
- **Takedown Rate:** <1% dos episodios removidos
- **Response Time:** Correcoes feitas em <24h apos identificacao

## Pontos de Falha Comuns
- **Sem Classificacao:** Todos os episodios tratados igual → classificar Evergreen vs. Topical
- **Episodios Esquecidos:** Nunca re-promover Evergreens → criar calendario de re-promocao
- **Erros Ignorados:** Listener reporta erro, ninguem corrige → ter processo de error reporting
- **Takedown Precipitado:** Remover episodio sem review → sempre revisar antes de remover
- **Sem Backup:** Episodio removido, arquivo perdido → manter backup de todos os episodios
- **Comunicacao Ruim:** Remocao sem explicacao → comunicar motivo (quando apropriado)
