## approach-mode.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://podcast-production.invalid/contracts/approach-mode.schema.json",
  "title": "ApproachMode",
  "description": "Um modo de abordagem do roteiro (ortogonal ao formato). Registro extensível em contracts/approach-modes.yaml: adicionar modo = 1 entrada. legal_risk=alto liga as recomendações de gate do guardian e de contraditório (recomendação + alerta; seguir contra exige aceite humano registrado).",
  "type": "object",
  "required": ["id", "label", "hook_style", "pacing", "source_rigor", "requires_counterpoint", "requires_guardian_gate", "legal_risk"],
  "additionalProperties": false,
  "properties": {
    "id": { "type": "string", "pattern": "^[a-z][a-z0-9-]{1,40}$" },
    "label": {
      "type": "object",
      "required": ["pt-BR", "en"],
      "additionalProperties": false,
      "properties": {
        "pt-BR": { "type": "string" },
        "en": { "type": "string" },
        "es": { "type": "string" },
        "zh": { "type": "string" }
      }
    },
    "extends": { "type": "string", "description": "id de outro modo cujos defaults este herda." },
    "description": { "type": "string" },
    "hook_style": { "type": "string" },
    "pacing": { "enum": ["lento", "moderado", "rapido"] },
    "source_rigor": { "enum": ["padrao", "alto", "maximo"], "description": "maximo = afirmação sobre conduta de terceiro só como claim conduct_allegation=true; abaixo de tier 1 ou 2 fontes tier 2 independentes, a claim carrega advisory e o uso exige aceite humano (claim.schema.json, human-decision.schema.json)." },
    "requires_counterpoint": { "type": "boolean" },
    "requires_guardian_gate": { "type": "boolean" },
    "legal_risk": { "enum": ["baixo", "medio", "alto"] },
    "shelf_life": { "enum": ["evergreen", "timely", "misto"] },
    "beats": {
      "type": "array", "minItems": 1, "items": { "type": "string", "pattern": "^[a-z][a-z0-9-]{1,40}$" },
      "description": "Movimentos de cada bloco do roteiro, em ordem (ex.: definicao, distincao, caso-pratico). Ausente: o roteiro usa contexto, desenvolvimento, pergunta."
    },
    "depth": { "enum": ["superficie", "media", "profunda"], "description": "Profundidade: perguntas por bloco (1, 2, 3). Ausente: derivada do pacing." },
    "counterpoint_block": { "type": "boolean", "description": "true = o roteiro ganha um bloco de contraponto mesmo sem requires_counterpoint (opinião assumida como opinião)." }
  },
  "if": { "properties": { "legal_risk": { "const": "alto" } }, "required": ["legal_risk"] },
  "then": {
    "properties": {
      "requires_guardian_gate": { "x-rule": "R-MODE-HIGH-RISK-GATE", "const": true },
      "requires_counterpoint": { "x-rule": "R-MODE-HIGH-RISK-GATE", "const": true },
      "source_rigor": { "x-rule": "R-MODE-HIGH-RISK-GATE", "const": "maximo" }
    }
  }
}

```


## claim.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://podcast-production.invalid/contracts/claim.schema.json",
  "title": "Claim",
  "description": "Uma afirmação sobre uma pessoa ou tema, com status epistêmico e fonte. Regras rígidas: verificado exige >=1 source; inferencia exige basis_claim_ids; sensitive=true só vale se o TITULAR declarou (origin=guest_intake) com consentimento específico (LGPD art. 11, I). Varredura pública/inferência nunca produz dado sensível. Modo denúncia (decisão do dono 2026-10-09, revista na 3ª rodada: a decisão é sempre humana): conduct_allegation=true sem status verificado com >=1 fonte tier 1 OU >=2 fontes tier 2 independentes NÃO invalida a claim; ela carrega `advisory` com o alerta (R-CLAIM-CONDUTA-FONTES / R-CLAIM-CONDUTA-INDEPENDENCIA) e quem a usa como base (roteiro) exige aceite humano registrado (human-decision.schema.json). Conferido em Python: o alerta devido tem de estar no advisory (R-CLAIM-ADVISORY-AUSENTE).",
  "type": "object",
  "required": ["id", "subject", "text", "status", "origin", "purpose", "sensitive"],
  "additionalProperties": false,
  "properties": {
    "id": { "type": "string", "pattern": "^[a-z0-9][a-z0-9_-]{1,63}$" },
    "subject": { "type": "string", "minLength": 1, "description": "Referência ao titular/tema (ex.: intake_id do convidado)." },
    "text": { "type": "string", "minLength": 1 },
    "status": { "enum": ["verificado", "autodeclarado", "inferencia"] },
    "origin": { "enum": ["public_scan", "guest_intake", "guest_material", "manager_material"] },
    "purpose": { "type": "string", "minLength": 1, "description": "Finalidade do tratamento (LGPD art. 6º, I; art. 7º, §3º)." },
    "sources": {
      "type": "array",
      "items": { "$ref": "#/$defs/source" }
    },
    "basis_claim_ids": {
      "type": "array",
      "items": { "type": "string" },
      "uniqueItems": true,
      "description": "Claims das quais a inferência deriva (obrigatório se status=inferencia)."
    },
    "sensitive": { "type": "boolean", "description": "Dado pessoal sensível (LGPD art. 5º, II). Só o titular decide incluir." },
    "sensitive_category": { "$ref": "#/$defs/sensitive_category" },
    "consent_ref": {
      "type": "string",
      "minLength": 1,
      "description": "consent_id de guest-intake.sensitive_declarations[].consent que autoriza ESTE dado sensível."
    },
    "confidence": { "type": "number", "minimum": 0, "maximum": 1 },
    "created_at": { "type": "string", "format": "date-time" },
    "coverage_area": { "type": "string", "pattern": "^[a-z0-9_]{2,40}$", "description": "Área de guest-dossier.coverage.expected que esta claim preenche (ex.: trajetoria, cargo_atual, pronuncia_nome)." },
    "as_of": { "type": "string", "format": "date", "description": "Data a que o fato se refere (cargo ATUAL, fatos datados). Diferente de sources[].accessed_at." },
    "conduct_allegation": { "type": "boolean", "description": "true = afirma conduta de uma pessoa (o que ela fez, sobretudo conduta reprovável). Ativa a recomendação de rigor máximo do modo denúncia: fonte fraca vira advisory, não invalidação." },
    "advisory": {
      "type": "array",
      "items": { "$ref": "human-decision.schema.json#/$defs/alert" },
      "description": "Alertas de responsabilidade calculados pela ferramenta (dossier_tools.py advise). Não invalidam a claim; obrigam aceite humano para usá-la como base."
    }
  },
  "allOf": [
    {
      "if": { "properties": { "status": { "const": "verificado" } }, "required": ["status"] },
      "then": {
        "x-rule": "R-CLAIM-VERIFICADO-SOURCES",
        "required": ["sources"],
        "properties": { "sources": { "x-rule": "R-CLAIM-VERIFICADO-SOURCES", "minItems": 1 } }
      }
    },
    {
      "if": { "properties": { "status": { "const": "inferencia" } }, "required": ["status"] },
      "then": {
        "x-rule": "R-CLAIM-INFERENCIA-BASIS",
        "required": ["basis_claim_ids"],
        "properties": { "basis_claim_ids": { "x-rule": "R-CLAIM-INFERENCIA-BASIS", "minItems": 1 } }
      }
    },
    {
      "if": { "properties": { "sensitive": { "const": true } }, "required": ["sensitive"] },
      "then": {
        "x-rule": "R-CLAIM-SENSITIVE-CONSENT",
        "required": ["consent_ref", "sensitive_category"],
        "properties": {
          "origin": { "x-rule": "R-CLAIM-SENSITIVE-ORIGIN", "const": "guest_intake" },
          "status": { "x-rule": "R-CLAIM-SENSITIVE-ORIGIN", "const": "autodeclarado" }
        }
      }
    }
  ],
  "$defs": {
    "source": {
      "type": "object",
      "required": ["url", "accessed_at"],
      "additionalProperties": false,
      "properties": {
        "url": { "type": "string", "format": "uri" },
        "title": { "type": "string" },
        "accessed_at": { "type": "string", "format": "date-time" },
        "tier": { "type": "integer", "minimum": 1, "maximum": 3, "description": "Hierarquia de fontes do researcher (1 = primária)." },
        "author": { "type": "string", "description": "Autor ou assinatura, quando houver." },
        "outlet": { "type": "string", "description": "Veículo ou órgão que publicou." },
        "agency": { "type": "string", "description": "Agência ou origem do conteúdo replicado, quando houver." }
      }
    },
    "sensitive_category": {
      "description": "Categorias do art. 5º, II da LGPD.",
      "enum": [
        "origem_racial_etnica", "conviccao_religiosa", "opiniao_politica",
        "filiacao_sindical_religiosa_filosofica_politica", "saude", "vida_sexual",
        "genetico", "biometrico"
      ]
    }
  }
}

```


## episode-record.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://podcast-production.invalid/contracts/episode-record.schema.json",
  "title": "EpisodeRecord",
  "description": "Registro do episódio na memória/centro de comando: guarda blueprint, pesquisa, pauta, roteiro, gravação, edições e cortes postados. retention permite eliminação real por titular (LGPD art. 18, VI; art. 8º, §5º). Mídia (gravação, transcrição, edições, cortes) é guardada por REFERÊNCIA (caminho/URL + sha256 + duração), nunca o binário. Ferramenta: scripts/memory_tools.py (F6).",
  "type": "object",
  "required": ["episode_id", "show_ref", "status", "artifacts", "retention"],
  "additionalProperties": false,
  "properties": {
    "episode_id": { "type": "string", "pattern": "^[a-z0-9][a-z0-9_-]{1,63}$" },
    "show_ref": { "type": "string" },
    "title": { "type": "string" },
    "status": {
      "description": "EpisodeStatus de docs/prd/podcommand-prd.md §11.5.",
      "enum": [
        "idea", "planning", "briefing", "guest_outreach", "guest_confirmed", "pre_production",
        "ready_to_record", "recording_scheduled", "recorded", "editing", "review",
        "ready_to_publish", "publishing", "published", "repurposing", "archived"
      ]
    },
    "format": { "type": "string" },
    "approach_mode": { "type": "string" },
    "series_ref": { "type": "string" },
    "guest_refs": { "type": "array", "items": { "type": "string" } },
    "themes": { "type": "array", "items": { "type": "string" }, "description": "Temas do episódio (busca, catálogo da pauta, surfacing de temas recorrentes)." },
    "recording_mode": { "enum": ["presencial", "remoto"] },
    "published_at": { "type": "string", "format": "date-time" },
    "published_url": { "type": "string", "format": "uri" },
    "gate": {
      "type": "object",
      "required": ["recommendation"],
      "additionalProperties": false,
      "description": "Recomendação do quality gate (*approve-episode). Avançar para publicação sem APPROVE exige human-decision com R-PUBLICACAO-GATE.",
      "properties": {
        "recommendation": { "enum": ["APPROVE", "REQUEST_CHANGES", "HOLD"] },
        "by": { "type": "string" },
        "at": { "type": "string", "format": "date-time" }
      }
    },
    "history": {
      "type": "array",
      "description": "Transições de status (auditoria sem conteúdo pessoal).",
      "items": {
        "type": "object",
        "required": ["from", "to", "at"],
        "additionalProperties": false,
        "properties": {
          "from": { "type": "string" },
          "to": { "type": "string" },
          "at": { "type": "string", "format": "date-time" },
          "by": { "type": "string" },
          "decision_ref": { "type": "string" }
        }
      }
    },
    "artifacts": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "intake": { "$ref": "#/$defs/refs", "description": "intake_id ou caminho do guest-intake; vários convidados = lista." },
        "dossier": { "$ref": "#/$defs/refs", "description": "Caminho/ref do dossiê (guest-dossier); vários convidados = lista." },
        "research": { "type": "string" },
        "pauta": { "type": "string" },
        "script": {
          "description": "Roteiro (F5): caminho/ref de um documento válido contra script.schema.json, o roteiro embutido, ou lista de refs (modos alternativos).",
          "anyOf": [{ "type": "string" }, { "$ref": "script.schema.json" }, { "type": "array", "items": { "type": "string" } }]
        },
        "decisions": {
          "type": "array",
          "items": { "$ref": "human-decision.schema.json" },
          "description": "Decisões humanas registradas neste episódio (aceites para seguir contra recomendações)."
        },
        "recording": { "$ref": "#/$defs/media" },
        "transcript": { "$ref": "#/$defs/media" },
        "edits": { "type": "array", "items": { "$ref": "#/$defs/media" } },
        "clips": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["platform", "url"],
            "additionalProperties": false,
            "properties": {
              "platform": { "type": "string" },
              "url": { "type": "string", "format": "uri" },
              "posted_at": { "type": "string", "format": "date-time" },
              "metrics": { "type": "object", "additionalProperties": { "type": "number" } },
              "duration_s": { "type": "number", "minimum": 0 },
              "title": { "type": "string" },
              "source_ref": { "type": "string", "description": "Caminho/URL do arquivo do corte (referência, não o binário)." },
              "sha256": { "type": "string", "pattern": "^[0-9a-f]{64}$" }
            }
          }
        }
      }
    },
    "metrics": { "type": "object", "additionalProperties": { "type": "number" } },
    "lessons": { "type": "array", "items": { "type": "string" } },
    "retention": {
      "type": "object",
      "required": ["subject_ids"],
      "additionalProperties": false,
      "properties": {
        "subject_ids": { "type": "array", "items": { "type": "string" }, "description": "Titulares cujos dados (intake, dossiê) estão neste registro." },
        "delete_after": { "type": "string", "format": "date" },
        "keep_consent_record": { "type": "boolean", "default": true, "description": "Guardar só o registro do consentimento (ônus da prova, art. 8º, §2º)." },
        "days_after_publish": { "type": "integer", "minimum": 0, "description": "Elimina intake e dossiê N dias após published_at (vem de show-profile.retention_days_after_publish). delete_after, se presente, prevalece." },
        "applied_at": { "type": "string", "format": "date-time", "description": "Quando a retenção eliminou intake/dossiê deste registro." }
      }
    }
  },
  "$defs": {
    "refs": { "anyOf": [{ "type": "string" }, { "type": "array", "items": { "type": "string" } }] },
    "media": {
      "description": "Mídia por referência: string (legado) ou objeto com ref + integridade. O binário fica onde o usuário já guarda.",
      "anyOf": [
        { "type": "string" },
        {
          "type": "object",
          "required": ["ref"],
          "additionalProperties": false,
          "properties": {
            "ref": { "type": "string", "minLength": 1, "description": "Caminho local ou URL." },
            "sha256": { "type": "string", "pattern": "^[0-9a-f]{64}$" },
            "bytes": { "type": "integer", "minimum": 0 },
            "duration_s": { "type": "number", "minimum": 0 },
            "platform": { "type": "string" },
            "title": { "type": "string" }
          }
        }
      ]
    }
  }
}

```


## guest-dossier.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://podcast-production.invalid/contracts/guest-dossier.schema.json",
  "title": "GuestDossier",
  "description": "Dossiê/Blueprint do convidado. Sempre válido com claims: [] (degrada, não trava). degraded=true sse coverage.gaps não vazio; o consumidor (pauta) TEM de ler degraded. Nenhum mínimo de fontes bloqueia o dossiê: o mínimo só bloqueia o status verificado de cada claim.",
  "type": "object",
  "required": ["dossier_id", "guest_ref", "generated_at", "purpose", "legal_basis", "coverage", "degraded", "claims"],
  "additionalProperties": false,
  "properties": {
    "dossier_id": { "type": "string", "pattern": "^[a-z0-9][a-z0-9_-]{1,63}$" },
    "guest_ref": { "type": "string", "minLength": 1 },
    "intake_ref": { "type": "string", "description": "intake_id, quando houver formulário." },
    "episode_ref": { "type": "string" },
    "generated_at": { "type": "string", "format": "date-time" },
    "locale": { "$ref": "show-profile.schema.json#/$defs/locale" },
    "purpose": { "type": "string", "minLength": 1, "description": "Finalidade registrada (LGPD art. 7º, §3º)." },
    "legal_basis": {
      "type": "object",
      "required": ["public_scan"],
      "additionalProperties": false,
      "properties": {
        "public_scan": { "enum": ["dados_tornados_publicos_pelo_titular", "legitimo_interesse", "consentimento"] },
        "intake": { "const": "consentimento" }
      }
    },
    "coverage": {
      "type": "object",
      "required": ["expected", "found", "gaps"],
      "additionalProperties": false,
      "properties": {
        "expected": { "type": "array", "items": { "type": "string" } },
        "found": { "type": "array", "items": { "type": "string" } },
        "gaps": { "type": "array", "items": { "type": "string" } }
      }
    },
    "degraded": { "type": "boolean" },
    "claims": { "type": "array", "items": { "$ref": "claim.schema.json" } },
    "materials_used": { "type": "array", "items": { "type": "string" } },
    "enriched_by": { "type": "array", "items": { "enum": ["guest", "manager"] } }
  },
  "if": {
    "properties": { "coverage": { "properties": { "gaps": { "minItems": 1 } } } }
  },
  "then": { "properties": { "degraded": { "x-rule": "R-DOSSIER-DEGRADED", "const": true } } },
  "else": { "properties": { "degraded": { "x-rule": "R-DOSSIER-DEGRADED", "const": false } } }
}

```


## guest-intake.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://podcast-production.invalid/contracts/guest-intake.schema.json",
  "title": "GuestIntake",
  "description": "Respostas do formulário do convidado (adaptador: Google Forms, Tally, form próprio). Um único contrato para as duas variantes; só form_variant muda. Sem consentimento geral não existe intake. Dado sensível só entra em sensitive_declarations, cada um com consentimento específico e destacado (LGPD art. 11, I). Materiais são LINKS (Forms sem upload: upload exige login Google).",
  "type": "object",
  "x-form-variants": {
    "essencial": [
      "guest.full_name", "guest.preferred_name", "bio.short", "links", "recording_mode",
      "contacts.email", "contacts.whatsapp", "scheduled_at", "automation_consents", "consent"
    ],
    "completo": "todos os campos de properties; nenhum além da variante essencial é obrigatório (o convidado pode pular)"
  },
  "required": [
    "intake_id", "form_variant", "locale", "jurisdiction", "submitted_at",
    "guest", "bio", "links", "recording_mode", "contacts", "automation_consents", "consent"
  ],
  "additionalProperties": false,
  "properties": {
    "intake_id": { "type": "string", "pattern": "^[a-z0-9][a-z0-9_-]{1,63}$" },
    "episode_ref": { "type": "string" },
    "scheduled_at": { "type": "string", "format": "date-time", "description": "Data/hora da gravação já combinada com o host (opcional). Alimenta o convite de agenda e o lembrete D-1." },
    "form_variant": { "enum": ["essencial", "completo"] },
    "locale": { "$ref": "show-profile.schema.json#/$defs/locale" },
    "jurisdiction": { "enum": ["BR-LGPD", "EU-GDPR", "CN-PIPL", "other"] },
    "submitted_at": { "type": "string", "format": "date-time" },
    "guest": {
      "type": "object",
      "required": ["full_name", "preferred_name"],
      "additionalProperties": false,
      "properties": {
        "full_name": { "type": "string", "minLength": 1 },
        "preferred_name": { "type": "string", "minLength": 1, "description": "Nome de tratamento (como quer ser chamado no ar)." },
        "name_pronunciation": { "type": "string" },
        "pronouns": { "type": "string" },
        "role_title": { "type": "string" },
        "photo_url": { "type": "string", "format": "uri" }
      }
    },
    "bio": {
      "type": "object",
      "required": ["short"],
      "additionalProperties": false,
      "properties": {
        "short": { "type": "string", "minLength": 1, "maxLength": 280, "description": "Mini-bio de até 2 linhas." },
        "long": { "type": "string" }
      }
    },
    "links": { "type": "array", "minItems": 1, "items": { "type": "string", "format": "uri" }, "description": "Site, perfis, portfólio. Modo mínimo sem formulário = nome + 1 link." },
    "social_handles": {
      "type": "array",
      "description": "@ das redes para marcar na divulgação.",
      "items": {
        "type": "object",
        "required": ["platform", "handle"],
        "additionalProperties": false,
        "properties": { "platform": { "type": "string" }, "handle": { "type": "string" } }
      }
    },
    "previous_interviews": { "type": "array", "items": { "type": "string", "format": "uri" } },
    "key_ideas": { "type": "array", "maxItems": 3, "items": { "type": "string" }, "description": "3 ideias que quer deixar ao público." },
    "stories_to_tell": { "type": "array", "items": { "type": "string" } },
    "controversies": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "accepts": { "type": "array", "items": { "type": "string" } },
        "declines": { "type": "array", "items": { "type": "string" } }
      }
    },
    "off_limits_topics": { "type": "array", "items": { "type": "string" }, "description": "Assuntos proibidos." },
    "wants_to_promote": { "type": "array", "items": { "type": "string" } },
    "dream_questions": { "type": "array", "items": { "type": "string" }, "description": "Perguntas que adoraria receber." },
    "conflicts_of_interest": {
      "type": "object",
      "required": ["declared"],
      "additionalProperties": false,
      "properties": {
        "declared": { "type": "boolean" },
        "details": { "type": "string" },
        "sponsorships": { "type": "array", "items": { "type": "string" } }
      }
    },
    "accessibility": {
      "type": "object",
      "description": "Necessidade de acessibilidade pode revelar saúde (dado sensível): exige consentimento específico.",
      "required": ["needs", "consent"],
      "additionalProperties": false,
      "properties": {
        "needs": { "type": "string", "minLength": 1 },
        "consent": { "$ref": "#/$defs/specific_consent" }
      }
    },
    "companion": {
      "type": "object",
      "required": ["bringing"],
      "additionalProperties": false,
      "properties": { "bringing": { "type": "boolean" }, "name": { "type": "string" } }
    },
    "recording_mode": { "enum": ["presencial", "remoto"] },
    "image_voice_authorization": {
      "type": "object",
      "required": ["granted", "text_version", "granted_at"],
      "additionalProperties": false,
      "properties": {
        "granted": { "type": "boolean" },
        "text_version": { "type": "string" },
        "granted_at": { "type": "string", "format": "date-time" }
      }
    },
    "wants_prepublication_review": { "type": "boolean" },
    "preferred_channel": { "enum": ["email", "whatsapp", "phone", "other"] },
    "materials": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["kind", "url"],
        "additionalProperties": false,
        "properties": {
          "kind": { "enum": ["palestra", "livro", "artigo", "video", "podcast", "apresentacao", "outro"] },
          "title": { "type": "string" },
          "url": { "type": "string", "format": "uri" }
        }
      }
    },
    "contacts": {
      "type": "object",
      "required": ["email"],
      "additionalProperties": false,
      "properties": {
        "email": { "type": "string", "format": "email" },
        "whatsapp": { "type": "string", "pattern": "^\\+[1-9][0-9]{7,14}$", "description": "E.164." }
      }
    },
    "automation_consents": {
      "type": "object",
      "description": "Consentimento por canal para automações (kit por e-mail, WhatsApp, convite de agenda, lembrete D-1).",
      "required": ["email", "whatsapp", "calendar"],
      "additionalProperties": false,
      "properties": {
        "email": { "$ref": "#/$defs/channel_consent" },
        "whatsapp": { "$ref": "#/$defs/channel_consent" },
        "calendar": { "$ref": "#/$defs/channel_consent" }
      }
    },
    "consent": { "$ref": "#/$defs/general_consent" },
    "sensitive_declarations": {
      "type": "array",
      "description": "Únicos campos sensíveis. Cada um marcado e com aceite próprio, separado do geral.",
      "items": { "$ref": "#/$defs/sensitive_declaration" }
    },
    "localization_consents": {
      "type": "object",
      "description": "Três aceites SEPARADOS e destacados para levar o episódio a outros idiomas (research/06 §3.3). Nenhum pré-marcado, nenhum condiciona a participação. Ausência do bloco ou de um aceite = não autorizado. (a) tradução/legendas; (b) dublagem com voz sintética genérica; (c) réplica da própria voz = dado sensível (LGPD art. 11, I), específico, revogável.",
      "additionalProperties": false,
      "properties": {
        "translation_text": { "$ref": "#/$defs/localization_consent" },
        "dub_generic_voice": { "$ref": "#/$defs/localization_consent" },
        "dub_voice_replica": { "$ref": "#/$defs/voice_replica_consent" }
      }
    }
  },
  "allOf": [
    {
      "if": {
        "properties": { "automation_consents": { "properties": { "whatsapp": { "properties": { "granted": { "const": true } } } } } }
      },
      "then": {
        "properties": { "contacts": { "x-rule": "R-INTAKE-WHATSAPP-NUMBER", "required": ["whatsapp"] } }
      }
    }
  ],
  "$defs": {
    "general_consent": {
      "type": "object",
      "description": "Cláusula destacada (art. 8º, §1º), finalidades específicas (art. 8º, §4º), revogável (art. 8º, §5º).",
      "x-rule": "R-INTAKE-CONSENT",
      "required": ["consent_id", "granted", "granted_at", "text_version", "clause_id", "purposes", "public_research_notice"],
      "additionalProperties": false,
      "properties": {
        "consent_id": { "type": "string", "minLength": 1 },
        "granted": { "const": true, "x-rule": "R-INTAKE-CONSENT" },
        "granted_at": { "type": "string", "format": "date-time" },
        "text_version": { "type": "string", "minLength": 1 },
        "clause_id": { "type": "string", "minLength": 1, "description": "Cláusula por jurisdição (ex.: BR-LGPD/v1, EU-GDPR/v1)." },
        "purposes": {
          "type": "array",
          "minItems": 1,
          "uniqueItems": true,
          "items": { "enum": ["preparo_entrevista", "dossie", "memoria_episodio", "divulgacao"] }
        },
        "public_research_notice": { "const": true, "description": "Titular informado de que haverá pesquisa em fontes públicas (LGPD art. 9º; GDPR art. 14)." },
        "channel": { "type": "string" },
        "revoked_at": { "type": "string", "format": "date-time" }
      }
    },
    "specific_consent": {
      "type": "object",
      "description": "Aceite específico e destacado para UMA finalidade (art. 11, I). Caixa desmarcada por padrão.",
      "x-rule": "R-INTAKE-SENSITIVE-SPECIFIC-CONSENT",
      "required": ["consent_id", "specific", "highlighted", "purpose", "granted_at", "text_version"],
      "additionalProperties": false,
      "properties": {
        "consent_id": { "type": "string", "minLength": 1 },
        "specific": { "const": true, "x-rule": "R-INTAKE-SENSITIVE-SPECIFIC-CONSENT" },
        "highlighted": { "const": true, "x-rule": "R-INTAKE-SENSITIVE-SPECIFIC-CONSENT" },
        "purpose": { "type": "string", "minLength": 1 },
        "granted_at": { "type": "string", "format": "date-time" },
        "text_version": { "type": "string", "minLength": 1 },
        "revoked_at": { "type": "string", "format": "date-time" }
      }
    },
    "sensitive_declaration": {
      "type": "object",
      "required": ["field_id", "sensitive", "category", "value", "consent"],
      "additionalProperties": false,
      "properties": {
        "field_id": { "type": "string", "minLength": 1 },
        "sensitive": { "const": true },
        "category": { "$ref": "claim.schema.json#/$defs/sensitive_category" },
        "value": { "type": "string", "minLength": 1 },
        "consent": { "$ref": "#/$defs/specific_consent" }
      }
    },
    "localization_consent": {
      "type": "object",
      "description": "Aceite de localização (texto ou voz genérica): idiomas nomeados (autorização genérica é nula, art. 8º, §4º).",
      "required": ["granted"],
      "additionalProperties": false,
      "properties": {
        "consent_id": { "type": "string", "minLength": 1 },
        "granted": { "type": "boolean" },
        "granted_at": { "type": "string", "format": "date-time" },
        "text_version": { "type": "string", "minLength": 1 },
        "target_locales": { "type": "array", "minItems": 1, "uniqueItems": true, "items": { "$ref": "show-profile.schema.json#/$defs/locale" } },
        "revoked_at": { "type": "string", "format": "date-time" }
      },
      "if": { "properties": { "granted": { "const": true } } },
      "then": { "x-rule": "R-INTAKE-LOCALIZATION-CONSENT", "required": ["consent_id", "granted_at", "text_version", "target_locales"] }
    },
    "voice_replica_consent": {
      "type": "object",
      "description": "Réplica artificial da voz do titular: dado sensível (LGPD art. 5º, II e art. 11, I; CF art. 5º, XXVIII, a). Específico (episódio, idiomas, provedor e país, prazo de apagamento do modelo), destacado, revogável (art. 8º, §5º). Sem este aceite concedido e não revogado, a dublagem com réplica é RECUSADA (regra rígida).",
      "required": ["granted"],
      "additionalProperties": false,
      "properties": {
        "consent_id": { "type": "string", "minLength": 1 },
        "granted": { "type": "boolean" },
        "sensitive": { "const": true },
        "specific": { "const": true },
        "highlighted": { "const": true },
        "purpose": { "type": "string", "minLength": 1 },
        "episode_ref": { "type": "string" },
        "granted_at": { "type": "string", "format": "date-time" },
        "text_version": { "type": "string", "minLength": 1 },
        "target_locales": { "type": "array", "minItems": 1, "uniqueItems": true, "items": { "$ref": "show-profile.schema.json#/$defs/locale" } },
        "provider": {
          "type": "object",
          "required": ["name", "country"],
          "additionalProperties": false,
          "properties": { "name": { "type": "string", "minLength": 1 }, "country": { "type": "string", "minLength": 2 } },
          "description": "Transferência internacional nomeada (LGPD art. 33)."
        },
        "model_deletion_days": { "type": "integer", "minimum": 0, "maximum": 365 },
        "revoked_at": { "type": "string", "format": "date-time" }
      },
      "if": { "properties": { "granted": { "const": true } } },
      "then": {
        "x-rule": "R-INTAKE-VOICE-REPLICA-CONSENT",
        "required": ["consent_id", "sensitive", "specific", "highlighted", "purpose", "granted_at", "text_version", "target_locales", "provider", "model_deletion_days"]
      }
    },
    "channel_consent": {
      "type": "object",
      "required": ["granted"],
      "additionalProperties": false,
      "properties": {
        "granted": { "type": "boolean" },
        "granted_at": { "type": "string", "format": "date-time" }
      },
      "if": { "properties": { "granted": { "const": true } } },
      "then": { "required": ["granted_at"] }
    }
  }
}

```


## host-profile.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://podcast-production.invalid/contracts/host-profile.schema.json",
  "title": "HostProfile",
  "description": "Perfil do host derivado de episódios publicados + memória do usuário, depois confirmado por questionário curto. Os 5 elementos vêm de agents/host.md (Vocabulary Signature, Opinion Stance, Curiosity Signature, Vulnerability Pattern, Energy Range).",
  "type": "object",
  "required": ["host_id", "show_ref", "name", "locale", "status", "elements", "derived_from"],
  "additionalProperties": false,
  "properties": {
    "host_id": { "type": "string", "pattern": "^[a-z0-9][a-z0-9_-]{1,63}$" },
    "show_ref": { "type": "string" },
    "name": { "type": "string", "minLength": 1 },
    "locale": { "$ref": "show-profile.schema.json#/$defs/locale" },
    "status": { "enum": ["draft", "confirmed"] },
    "elements": {
      "type": "object",
      "required": ["vocabulary_signature", "opinion_stance", "curiosity_signature", "vulnerability_pattern", "energy_range"],
      "additionalProperties": false,
      "properties": {
        "vocabulary_signature": { "$ref": "#/$defs/element" },
        "opinion_stance": { "$ref": "#/$defs/element" },
        "curiosity_signature": { "$ref": "#/$defs/element" },
        "vulnerability_pattern": { "$ref": "#/$defs/element" },
        "energy_range": { "$ref": "#/$defs/element" }
      }
    },
    "question_style": { "$ref": "#/$defs/element" },
    "recurring_themes": { "type": "array", "items": { "type": "string" } },
    "open_gaps": { "type": "array", "items": { "type": "string" }, "description": "Temas na linha editorial ainda não tratados (alimenta o tronco editorial da pauta)." },
    "pending": { "type": "array", "items": { "type": "string" }, "description": "O que falta confirmar no questionário." },
    "derived_from": {
      "type": "object",
      "required": ["episodes"],
      "additionalProperties": false,
      "properties": {
        "episodes": { "type": "array", "items": { "type": "string" }, "description": "episode_refs analisados." },
        "catalog_ref": { "type": "string" },
        "memory_refs": { "type": "array", "items": { "type": "string" } },
        "method_note": { "type": "string" }
      }
    },
    "questionnaire": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "answers": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["element", "question", "answer"],
            "additionalProperties": false,
            "properties": {
              "element": { "type": "string" },
              "question": { "type": "string" },
              "answer": { "type": "string" }
            }
          }
        },
        "confirmed_at": { "type": "string", "format": "date-time" }
      }
    }
  },
  "if": { "properties": { "status": { "const": "confirmed" } }, "required": ["status"] },
  "then": {
    "x-rule": "R-HOST-CONFIRMED-QUESTIONNAIRE",
    "required": ["questionnaire"],
    "properties": { "questionnaire": { "x-rule": "R-HOST-CONFIRMED-QUESTIONNAIRE", "required": ["answers", "confirmed_at"] } }
  },
  "$defs": {
    "element": {
      "type": "object",
      "required": ["summary"],
      "additionalProperties": false,
      "properties": {
        "summary": { "type": "string", "minLength": 1 },
        "markers": { "type": "array", "items": { "type": "string" } },
        "evidence": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["episode_ref"],
            "additionalProperties": false,
            "properties": {
              "episode_ref": { "type": "string" },
              "at": { "type": "string", "pattern": "^[0-9]{1,3}:[0-5][0-9]$" },
              "quote": { "type": "string" },
              "kind": { "enum": ["observado", "metadado", "inferencia"] }
            }
          }
        }
      }
    }
  }
}

```


## human-decision.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://podcast-production.invalid/contracts/human-decision.schema.json",
  "title": "HumanDecision",
  "description": "Registro de uma decisão HUMANA sobre uma recomendação do plugin (research/00-escopo.md, 'a decisão é sempre humana'). O plugin recomenda e alerta; quem decide é o usuário. Seguir contra a recomendação exige este registro: quem decidiu, quando, quais alertas viu e qual versão do texto de responsabilidade aceitou. Os textos dos alertas e do aceite vivem em contracts/i18n/<locale>.json (decision.*); a chave tem de existir em pt-BR e en (conferido em Python: R-DECISION-I18N-KEY). Não se aplica a regra rígida (dado sensível só autodeclarado, credencial fora do repo, validade de schema): essas não aceitam decisão contra.",
  "type": "object",
  "required": ["decision_id", "subject_ref", "recommendation", "alerts", "decided_by", "decided_at", "decision", "acknowledgment_text_version"],
  "additionalProperties": false,
  "properties": {
    "decision_id": { "type": "string", "pattern": "^[a-z0-9][a-z0-9_-]{1,63}$" },
    "subject_ref": { "type": "string", "minLength": 1, "description": "O que foi decidido: script_id, claim id, episode_id." },
    "recommendation": {
      "type": "object",
      "required": ["by", "verdict"],
      "additionalProperties": false,
      "properties": {
        "by": { "type": "string", "minLength": 1, "description": "Agente ou ferramenta que recomendou (ex.: @guardian, roteiro_tools check)." },
        "verdict": { "type": "string", "minLength": 1, "description": "A recomendação em si (ex.: vetado, nao_gravar_ainda, reforcar_fontes)." },
        "summary": { "type": "string" }
      }
    },
    "alerts": {
      "type": "array",
      "minItems": 1,
      "items": { "$ref": "#/$defs/alert" },
      "description": "Os alertas de responsabilidade que o humano VIU antes de decidir."
    },
    "decided_by": { "type": "string", "minLength": 1, "description": "Pessoa que decidiu (nome ou id do usuário). Nunca um agente." },
    "decided_at": { "type": "string", "format": "date-time" },
    "decision": { "enum": ["seguir_recomendacao", "seguir_contra"] },
    "acknowledgment_text_version": {
      "type": "string",
      "pattern": "^decision\\.ack\\.v[0-9]+$",
      "description": "Chave do texto de aceite em contracts/i18n (ex.: decision.ack.v1). Texto novo = versão nova; a antiga não é reescrita."
    },
    "rationale": { "type": "string", "description": "Motivo do humano (opcional)." }
  },
  "$defs": {
    "alert": {
      "type": "object",
      "required": ["code", "severity", "text_i18n_key"],
      "additionalProperties": false,
      "properties": {
        "code": { "type": "string", "pattern": "^R-[A-Z0-9-]+$" },
        "severity": { "enum": ["info", "atencao", "alta"], "description": "info não exige aceite; atencao e alta exigem aceite explícito para seguir contra." },
        "text_i18n_key": { "type": "string", "pattern": "^decision\\.alerts\\.R-[A-Z0-9-]+$" },
        "evidence": { "type": "string", "description": "O que o humano precisa ver para julgar (ex.: domínios, autores, veículos, agências das fontes)." }
      }
    }
  }
}

```


## license.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://podcast-production.invalid/contracts/license.schema.json",
  "title": "License",
  "description": "Licença do servidor MCP remoto (F9) como sai do store para admin, suporte e export (mcp-server/admin.py `list --json`). A chave NUNCA aparece: o banco guarda só sha256(chave) e `key_hint` (8 primeiros caracteres, para o suporte reconhecer a chave que o cliente lê). Dados pessoais mínimos (LGPD): e-mail e plano. Ver docs/LICENSING.md.",
  "type": "object",
  "required": ["license_id", "key_hint", "plan", "status", "created_at"],
  "additionalProperties": false,
  "properties": {
    "license_id": { "type": "string", "pattern": "^lic_[0-9a-f]{16}$" },
    "key_hint": { "type": "string", "pattern": "^pgi_[A-Za-z0-9_-]{4}$", "description": "Prefixo de 8 caracteres; nunca a chave inteira." },
    "plan": { "enum": ["free", "individual_solo", "individual_duo", "enterprise_10", "enterprise_20"], "description": "Chave de pricing/plans.yaml." },
    "status": { "enum": ["active", "suspended", "revoked"] },
    "email": { "type": "string", "format": "email" },
    "parent_id": { "type": "string", "pattern": "^lic_[0-9a-f]{16}$", "description": "Presente só em assento de Enterprise: a licença do dono." },
    "provider": { "enum": ["admin", "paddle", "polar", "lemonsqueezy", "hotmart"] },
    "subscription_ref": { "type": "string", "minLength": 1, "description": "Id da assinatura no provedor (ex.: sub_...). Não é segredo." },
    "expires_at": { "type": "string", "format": "date-time", "description": "Fim do reverse trial; depois cai para o Free (não é recusa)." },
    "revoked_reason": { "type": "string", "minLength": 1, "description": "refund, chargeback, canceled, seat_removed, admin." },
    "extra_seats": { "type": "integer", "minimum": 0, "description": "Expansão +5/+10 sobre Enterprise." },
    "created_at": { "type": "string", "format": "date-time" },
    "updated_at": { "type": "string", "format": "date-time" }
  }
}

```


## localization.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://podcast-production.invalid/contracts/localization.schema.json",
  "title": "LocalizationJob",
  "description": "Job de localização de UM episódio (research/06): transcrição → tradução com glossário → legendas SRT/VTT, show notes traduzidas e, opcionalmente, PLANO de dublagem. A decisão é humana: revisão registrada (human-decision) antes de aprovar ou publicar. Regra rígida (é lei, não recomendação): dublagem com réplica da voz exige consent_ref para um aceite dub_voice_replica concedido e não revogado (conferido por scripts/localization_tools.py check). Ferramenta: scripts/localization_tools.py.",
  "type": "object",
  "required": ["localization_id", "episode_ref", "source_locale", "target_locales", "transcript_ref", "subtitles", "review", "status"],
  "additionalProperties": false,
  "properties": {
    "localization_id": { "type": "string", "pattern": "^[a-z0-9][a-z0-9_-]{1,63}$" },
    "episode_ref": { "type": "string", "minLength": 1 },
    "show_ref": { "type": "string" },
    "source_locale": { "$ref": "show-profile.schema.json#/$defs/locale" },
    "target_locales": { "type": "array", "minItems": 1, "uniqueItems": true, "items": { "$ref": "show-profile.schema.json#/$defs/locale" } },
    "transcript_ref": { "type": "string", "minLength": 1, "description": "Transcrição na língua de origem (formato de localization_tools.py: {locale, source, segments[{id,start,end,speaker,text}]})." },
    "transcript_source": { "enum": ["assemblyai", "elevenlabs_scribe", "from_file", "manual"] },
    "glossary_ref": { "type": "string", "description": "show-profile (localization.glossary) ou arquivo próprio {glossary: [...]}." },
    "speakers": {
      "type": "array",
      "description": "Mapa rótulo do STT → pessoa. Proposto pela ferramenta, confirmado pelo humano.",
      "items": {
        "type": "object",
        "required": ["label", "role"],
        "additionalProperties": false,
        "properties": {
          "label": { "type": "string", "minLength": 1 },
          "display_name": { "type": "string" },
          "role": { "enum": ["host", "guest", "other"] },
          "intake_ref": { "type": "string", "description": "intake_id do convidado (onde estão os aceites de localização)." }
        }
      }
    },
    "translations": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["locale", "path", "translated_by"],
        "additionalProperties": false,
        "properties": {
          "locale": { "$ref": "show-profile.schema.json#/$defs/locale" },
          "path": { "type": "string", "minLength": 1 },
          "translated_by": { "enum": ["harness_agent", "deepl", "google", "openai", "assemblyai", "human"], "description": "harness_agent = o LLM do harness traduziu via task (não é BYOK)." }
        }
      }
    },
    "subtitles": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["locale", "format", "path", "max_chars_per_line", "max_lines"],
        "additionalProperties": false,
        "properties": {
          "locale": { "$ref": "show-profile.schema.json#/$defs/locale" },
          "format": { "enum": ["srt", "vtt"] },
          "path": { "type": "string", "minLength": 1 },
          "max_chars_per_line": { "type": "integer", "minimum": 10, "maximum": 80 },
          "max_lines": { "type": "integer", "minimum": 1, "maximum": 3 },
          "max_cps": { "type": "number", "minimum": 5, "maximum": 40 }
        }
      }
    },
    "show_notes_translated": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["locale", "path"],
        "additionalProperties": false,
        "properties": {
          "locale": { "$ref": "show-profile.schema.json#/$defs/locale" },
          "path": { "type": "string", "minLength": 1 },
          "source_path": { "type": "string" }
        }
      }
    },
    "dubbing": {
      "type": "array",
      "description": "Só PLANO no MVP (dub-plan): nenhum provedor de voz é chamado.",
      "items": { "$ref": "#/$defs/dubbing_item" }
    },
    "political_exposure": {
      "type": "object",
      "description": "Convidado candidato ou agente político: alerta extra (Res. TSE 23.732/2024, fonte secundária). Não bloqueia; o humano decide.",
      "required": ["is_political_agent"],
      "additionalProperties": false,
      "properties": {
        "is_political_agent": { "type": "boolean" },
        "basis": { "type": "string", "description": "De onde veio a marcação (dossiê, @guardian, humano)." }
      }
    },
    "review": {
      "type": "object",
      "required": ["alertas"],
      "additionalProperties": false,
      "properties": {
        "alertas": { "type": "array", "items": { "$ref": "human-decision.schema.json#/$defs/alert" }, "description": "Recalculados por localization_tools.py check." },
        "human_decision": { "$ref": "human-decision.schema.json" },
        "reviewed_by_guest": { "type": "boolean" }
      }
    },
    "status": { "enum": ["rascunho", "em_revisao", "aprovado", "publicado"] },
    "published": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["locale", "platform"],
        "additionalProperties": false,
        "properties": {
          "locale": { "$ref": "show-profile.schema.json#/$defs/locale" },
          "platform": { "type": "string" },
          "url": { "type": "string", "format": "uri" },
          "published_at": { "type": "string", "format": "date-time" }
        }
      }
    }
  },
  "allOf": [
    {
      "if": { "properties": { "status": { "enum": ["aprovado", "publicado"] } } },
      "then": { "properties": { "review": { "x-rule": "R-LOC-REVIEW-REQUIRED", "required": ["human_decision"] } } }
    }
  ],
  "$defs": {
    "dubbing_item": {
      "type": "object",
      "required": ["locale", "voice_mode", "provider", "speaker_label", "disclosure_text_key"],
      "additionalProperties": false,
      "properties": {
        "locale": { "$ref": "show-profile.schema.json#/$defs/locale" },
        "voice_mode": { "enum": ["generic", "guest_replica"] },
        "provider": { "type": "string", "minLength": 1 },
        "speaker_label": { "type": "string", "minLength": 1 },
        "consent_ref": { "type": "string", "pattern": "^[a-z0-9][a-z0-9_-]{1,63}#localization_consents/(dub_generic_voice|dub_voice_replica)$", "description": "<intake_id>#localization_consents/<aceite>." },
        "disclosure_text_key": { "type": "string", "pattern": "^localization\\.disclosure\\.(dub_generic|dub_replica)$", "description": "Aviso de IA ao ouvinte (contracts/i18n). Ligado por padrão." }
      },
      "if": { "properties": { "voice_mode": { "const": "guest_replica" } } },
      "then": { "x-rule": "R-LOC-REPLICA-CONSENT", "required": ["consent_ref"] }
    }
  }
}

```


## pauta.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://podcast-production.invalid/contracts/pauta.schema.json",
  "title": "Pauta",
  "description": "Pauta ranqueada em 3 troncos: trend (tendência x perfil), continuity (catálogo/memória), editorial (linha do host). Cada item aponta para claims, episódios ou tendências que o sustentam. dossier_degraded copia guest-dossier.degraded para baixar a confiança. Cada tronco tem no máximo max_items_per_trunk itens (default 5, faixa 1-10; conferido em Python: R-PAUTA-MAX-ITEMS).",
  "type": "object",
  "required": ["pauta_id", "episode_ref", "show_ref", "approach_mode", "format", "dossier_degraded", "trunks"],
  "additionalProperties": false,
  "properties": {
    "pauta_id": { "type": "string", "pattern": "^[a-z0-9][a-z0-9_-]{1,63}$" },
    "episode_ref": { "type": "string" },
    "show_ref": { "type": "string" },
    "host_profile_ref": { "type": "string" },
    "dossier_ref": { "type": "string" },
    "approach_mode": { "type": "string", "description": "id em contracts/approach-modes.yaml." },
    "format": { "type": "string", "description": "id em config/formats.yaml do squad." },
    "dossier_degraded": { "type": "boolean" },
    "max_items_per_trunk": {
      "type": "integer", "minimum": 1, "maximum": 10, "default": 5, "x-rule": "R-PAUTA-MAX-RANGE",
      "description": "Teto de itens por tronco aplicado nesta pauta. Vem de show-profile.pauta_max_items_per_trunk ou de parâmetro do usuário; ausente = 5."
    },
    "locale": { "$ref": "show-profile.schema.json#/$defs/locale" },
    "trunks": {
      "type": "object",
      "required": ["trend", "continuity", "editorial"],
      "additionalProperties": false,
      "properties": {
        "trend": { "type": "array", "maxItems": 10, "items": { "$ref": "#/$defs/item" } },
        "continuity": { "type": "array", "maxItems": 10, "items": { "$ref": "#/$defs/item" } },
        "editorial": { "type": "array", "maxItems": 10, "items": { "$ref": "#/$defs/item" } }
      }
    },
    "generated_at": { "type": "string", "format": "date-time" }
  },
  "$defs": {
    "item": {
      "type": "object",
      "required": ["id", "title", "rationale", "rank"],
      "additionalProperties": false,
      "properties": {
        "id": { "type": "string" },
        "title": { "type": "string", "minLength": 1 },
        "rationale": { "type": "string", "minLength": 1 },
        "rank": { "type": "integer", "minimum": 1 },
        "score": { "type": "number", "minimum": 0, "maximum": 1 },
        "questions": { "type": "array", "items": { "type": "string" } },
        "claim_ids": { "type": "array", "items": { "type": "string" } },
        "episode_refs": { "type": "array", "items": { "type": "string" } },
        "trend_refs": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["source_id", "observed_at"],
            "additionalProperties": false,
            "properties": {
              "source_id": { "type": "string" },
              "url": { "type": "string", "format": "uri" },
              "observed_at": { "type": "string", "format": "date-time" }
            }
          }
        }
      }
    }
  }
}

```


## script.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://podcast-production.invalid/contracts/script.schema.json",
  "title": "Script",
  "description": "Roteiro do episódio por modo de abordagem (manifesto HPF-3 squads/podcast-production/manifests/roteiro.md). Chaves, nesta ordem: meta, modo, roteiro, rastreabilidade, contraditorio, gate, status. O plugin recomenda e alerta; a decisão é humana: status pronto_para_gravar com recomendação desfavorável do @guardian (gate exigido e veredito diferente de aprovado) só vale com gate.human_decision em seguir_contra (R-SCRIPT-HUMAN-ACK). Em Python (scripts/roteiro_tools.py check): alertas calculados = gate.alertas; todo alerta de severidade atencao/alta coberto pelo aceite humano para pronto_para_gravar; refs a itens da pauta e a claims existem; rastreabilidade bate com o texto; modo e flags batem com contracts/approach-modes.yaml. pronto_para_gravar corresponde a episode-record.status ready_to_record.",
  "type": "object",
  "required": ["meta", "modo", "roteiro", "rastreabilidade", "contraditorio", "gate", "status"],
  "additionalProperties": false,
  "properties": {
    "meta": {
      "type": "object",
      "required": ["script_id", "pauta_ref", "episode_ref", "duracao_alvo_min", "generated_at"],
      "additionalProperties": false,
      "properties": {
        "script_id": { "type": "string", "pattern": "^[a-z0-9][a-z0-9_-]{1,63}$" },
        "pauta_ref": { "type": "string", "minLength": 1 },
        "episode_ref": { "type": "string", "minLength": 1 },
        "dossier_ref": { "type": "string" },
        "host_profile_ref": { "type": "string" },
        "format": { "type": "string", "description": "id em config/formats.yaml do squad." },
        "locale": { "$ref": "show-profile.schema.json#/$defs/locale" },
        "dossier_degraded": { "type": "boolean" },
        "duracao_alvo_min": { "type": "integer", "minimum": 5, "maximum": 300 },
        "modo_escolhido_pelo_humano": { "type": "boolean", "description": "true = o humano trocou o modo da pauta (o agente nunca troca)." },
        "generated_at": { "type": "string", "format": "date-time" }
      }
    },
    "modo": {
      "type": "object",
      "required": ["id", "extends_resolvido", "source_rigor", "requires_counterpoint", "requires_guardian_gate", "legal_risk", "hook_style", "pacing"],
      "additionalProperties": false,
      "properties": {
        "id": { "type": "string", "pattern": "^[a-z][a-z0-9-]{1,40}$" },
        "extends_resolvido": { "type": "array", "items": { "type": "string" }, "description": "Cadeia de extends resolvida (vazia = sem herança)." },
        "source_rigor": { "enum": ["padrao", "alto", "maximo"] },
        "requires_counterpoint": { "type": "boolean" },
        "requires_guardian_gate": { "type": "boolean" },
        "legal_risk": { "enum": ["baixo", "medio", "alto"] },
        "hook_style": { "type": "string" },
        "pacing": { "enum": ["lento", "moderado", "rapido"] },
        "beats": { "type": "array", "items": { "type": "string" } },
        "depth": { "enum": ["superficie", "media", "profunda"] }
      }
    },
    "roteiro": {
      "type": "array",
      "minItems": 2,
      "items": { "$ref": "#/$defs/bloco" },
      "description": "Blocos em ordem: o primeiro é abertura e o último é encerramento."
    },
    "rastreabilidade": {
      "type": "object",
      "required": ["afirmacoes_total", "com_lastro", "cortadas"],
      "additionalProperties": false,
      "properties": {
        "afirmacoes_total": { "type": "integer", "minimum": 0, "description": "Afirmações de natureza fato." },
        "com_lastro": { "type": "integer", "minimum": 0 },
        "cortadas": { "type": "integer", "minimum": 0, "description": "Afirmações cortadas na autoauditoria (declarado pelo agente)." }
      }
    },
    "contraditorio": {
      "type": ["array", "null"],
      "items": { "$ref": "#/$defs/pedido_contraditorio" },
      "description": "null quando o modo não recomenda contraditório."
    },
    "gate": {
      "type": "object",
      "required": ["exigido", "task", "veredito", "revisao_juridica", "alertas"],
      "additionalProperties": false,
      "properties": {
        "exigido": { "type": "boolean", "description": "Espelha requires_guardian_gate do modo: a revisão é RECOMENDADA antes de gravar." },
        "task": { "const": "fact-check-review" },
        "veredito": { "enum": ["nao_aplicavel", "pendente", "aprovado", "aprovado_com_ajustes", "vetado"], "description": "Recomendação do @guardian (não é decisão)." },
        "revisao_juridica": { "enum": ["nao_aplicavel", "pendente", "feita"] },
        "alertas": { "type": "array", "items": { "$ref": "human-decision.schema.json#/$defs/alert" }, "description": "Alertas de responsabilidade calculados por roteiro_tools (refresh)." },
        "human_decision": { "$ref": "human-decision.schema.json" }
      }
    },
    "status": { "enum": ["rascunho", "aguardando_gate", "pronto_para_gravar"] }
  },
  "allOf": [
    {
      "if": {
        "required": ["status", "gate"],
        "properties": {
          "status": { "const": "pronto_para_gravar" },
          "gate": {
            "required": ["exigido", "veredito"],
            "properties": { "exigido": { "const": true }, "veredito": { "not": { "const": "aprovado" } } }
          }
        }
      },
      "then": {
        "properties": {
          "gate": {
            "x-rule": "R-SCRIPT-HUMAN-ACK",
            "required": ["human_decision"],
            "properties": {
              "human_decision": {
                "x-rule": "R-SCRIPT-HUMAN-ACK",
                "required": ["decision"],
                "properties": { "decision": { "x-rule": "R-SCRIPT-HUMAN-ACK", "const": "seguir_contra" } }
              }
            }
          }
        }
      }
    }
  ],
  "$defs": {
    "bloco": {
      "type": "object",
      "required": ["ordem", "tipo", "titulo", "texto", "duracao_seg", "perguntas", "afirmacoes", "ressalvas"],
      "additionalProperties": false,
      "properties": {
        "ordem": { "type": "integer", "minimum": 1 },
        "tipo": { "enum": ["abertura", "bloco", "transicao", "contraponto", "encerramento"] },
        "titulo": { "type": "string", "minLength": 1 },
        "beat": { "type": "string", "description": "Movimento do modo que este bloco cumpre (approach-mode.beats)." },
        "texto": { "type": "string", "minLength": 1, "description": "O que o host diz (fala de referência, não teatro)." },
        "duracao_seg": { "type": "integer", "minimum": 5 },
        "pauta_item_refs": { "type": "array", "items": { "type": "string" }, "description": "ids de itens da pauta (t1, c3, e1...)." },
        "perguntas": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["texto", "tipo"],
            "additionalProperties": false,
            "properties": {
              "texto": { "type": "string", "minLength": 1 },
              "tipo": { "enum": ["ancora", "aprofundamento", "confirmacao", "contraponto"] },
              "claim_ids": { "type": "array", "items": { "type": "string" } }
            }
          }
        },
        "afirmacoes": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["texto", "natureza"],
            "additionalProperties": false,
            "properties": {
              "texto": { "type": "string", "minLength": 1 },
              "natureza": { "enum": ["fato", "opiniao", "hipotese"], "description": "fato exige lastro; opiniao é assumida como opinião; hipotese vira pergunta." },
              "claim_ids": { "type": "array", "items": { "type": "string" } },
              "fontes": { "type": "array", "items": { "type": "string", "format": "uri" } }
            }
          }
        },
        "ressalvas": { "type": "array", "items": { "type": "string" } }
      }
    },
    "pedido_contraditorio": {
      "type": "object",
      "required": ["parte", "canal", "prazo", "pedido_texto", "situacao"],
      "additionalProperties": false,
      "properties": {
        "parte": { "type": "string", "minLength": 1 },
        "canal": { "type": "string", "minLength": 1 },
        "prazo": { "type": "string", "format": "date" },
        "pedido_texto": { "type": "string", "minLength": 1, "description": "Pedido REDIGIDO pelo agente; quem envia é o humano (o agente nunca contata a parte)." },
        "situacao": { "enum": ["redigido", "enviado", "respondido", "sem_resposta"] },
        "enviado_por": { "type": "string", "description": "Humano que enviou (obrigatório fora de redigido)." },
        "pedido_em": { "type": "string", "format": "date" },
        "resposta": { "type": "string" }
      },
      "if": { "properties": { "situacao": { "enum": ["enviado", "respondido", "sem_resposta"] } }, "required": ["situacao"] },
      "then": { "x-rule": "R-SCRIPT-CONTRADITORIO-ENVIO", "required": ["enviado_por", "pedido_em"] }
    }
  }
}

```


## show-profile.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://podcast-production.invalid/contracts/show-profile.schema.json",
  "title": "ShowProfile",
  "description": "Perfil do programa: linha editorial, logística do estúdio (alimenta o Kit do Convidado) e automações. Genérico: todo dado do show é preenchido pelo usuário do plugin.",
  "type": "object",
  "required": ["show_id", "name", "locale", "editorial_line", "pillars", "controller", "logistics", "automations"],
  "additionalProperties": false,
  "properties": {
    "show_id": { "type": "string", "pattern": "^[a-z0-9][a-z0-9_-]{1,63}$" },
    "name": { "type": "string", "minLength": 1 },
    "tagline": { "type": "string" },
    "locale": { "$ref": "#/$defs/locale" },
    "jurisdiction": { "enum": ["BR-LGPD", "EU-GDPR", "CN-PIPL", "other"], "default": "BR-LGPD", "description": "Seleciona a cláusula de consentimento em contracts/i18n/<locale>.json." },
    "editorial_line": { "type": "string", "minLength": 1 },
    "pillars": { "type": "array", "minItems": 1, "items": { "type": "string" } },
    "covers": { "type": "array", "items": { "type": "string" } },
    "does_not_cover": { "type": "array", "items": { "type": "string" } },
    "series": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "name"],
        "additionalProperties": false,
        "properties": {
          "id": { "type": "string" },
          "name": { "type": "string" },
          "description": { "type": "string" },
          "cadence": { "type": "string" }
        }
      }
    },
    "cadence": { "type": "string" },
    "formats": { "type": "array", "items": { "type": "string" }, "description": "Ids de config/formats.yaml do squad." },
    "kit_tone": { "type": "string", "description": "Tom do kit do convidado (ex.: acolhedor, tranquilizador)." },
    "brand": { "$ref": "#/$defs/brand" },
    "controller": {
      "type": "object",
      "description": "Controlador LGPD (art. 5º, VI) citado na cláusula de consentimento. Contato obrigatório: contact_email OU contact_mode=reply_to_email (instância pessoal: o próprio host é o controlador e o titular fala com ele respondendo ao e-mail do programa; CPF/CNPJ não é exigido). Sem nenhum dos dois a cláusula não é emitida (integrations/google-forms recusa).",
      "required": ["name"],
      "additionalProperties": false,
      "properties": {
        "name": { "type": "string", "minLength": 1 },
        "kind": { "enum": ["personal", "organization"], "description": "personal = o próprio host (pessoa natural); organization = produtora/empresa." },
        "document_id": { "type": "string" },
        "contact_email": { "type": "string", "format": "email" },
        "contact_mode": { "enum": ["email", "reply_to_email"], "default": "email", "description": "reply_to_email: a cláusula orienta o titular a responder a qualquer e-mail do programa." }
      }
    },
    "pending": { "type": "array", "items": { "type": "string" }, "description": "Campos que o dono ainda precisa confirmar (lacuna declarada, não inventada)." },
    "pauta_max_items_per_trunk": { "type": "integer", "minimum": 1, "maximum": 10, "default": 5, "x-rule": "R-PAUTA-MAX-RANGE", "description": "Preferência do usuário: teto de itens por tronco da pauta (default 5)." },
    "retention_days_after_publish": { "type": "integer", "minimum": 0, "default": 90 },
    "localization": { "$ref": "#/$defs/localization" },
    "logistics": { "$ref": "#/$defs/logistics" },
    "automations": { "$ref": "#/$defs/automations" }
  },
  "$defs": {
    "brand": {
      "type": "object",
      "description": "Identidade visual do programa no Convite Oficial (integrations/google-forms/src/invitation.js). Opcional: sem brand, o convite sai com cores neutras e o nome do show em texto. Regra cruzada R-BRAND-CONTRAST (scripts/validate-contracts.py e invitation.js): colors.text sobre colors.background >= 4.5:1 (WCAG 2.2, SC 1.4.3, AA).",
      "required": ["colors"],
      "additionalProperties": false,
      "properties": {
        "display_name": { "type": "string", "minLength": 1, "description": "Nome do show como aparece na marca (padrão: name)." },
        "logo": {
          "type": "object",
          "description": "Logo: URL https pública OU id de arquivo no Google Drive (exatamente um). alt é obrigatório (aparece quando o cliente bloqueia imagens). Sem logo, o convite usa o nome do show em texto, nunca imagem quebrada.",
          "required": ["alt"],
          "additionalProperties": false,
          "properties": {
            "url": {
              "type": "string",
              "pattern": "^https://\\S+$",
              "x-rule": "R-BRAND-HTTPS",
              "description": "PNG/JPG público em https (PNG com fundo transparente funciona melhor no modo escuro)."
            },
            "drive_file_id": {
              "type": "string",
              "pattern": "^[A-Za-z0-9_-]{20,}$",
              "description": "Id de um arquivo no Google Drive guardado pelo PodFácil (PodFácil > Enviar logo). Com o acesso reduzido (drive.file), o PodFácil só abre o arquivo que ele mesmo guardou; outro id faz o convite sair com o nome do programa no lugar do logo."
            },
            "alt": { "type": "string", "minLength": 1, "x-rule": "R-BRAND-LOGO-ALT" },
            "width": { "type": "integer", "minimum": 40, "maximum": 600, "default": 120, "description": "Largura em px no e-mail." }
          },
          "allOf": [
            {
              "x-rule": "R-BRAND-LOGO-SOURCE",
              "oneOf": [
                { "required": ["url"], "not": { "required": ["drive_file_id"] } },
                { "required": ["drive_file_id"], "not": { "required": ["url"] } }
              ]
            }
          ]
        },
        "colors": {
          "type": "object",
          "required": ["primary", "background", "text"],
          "additionalProperties": false,
          "properties": {
            "primary": {
              "$ref": "#/$defs/hex_color",
              "description": "Cor principal: faixa do topo e botão. O texto do botão é preto ou branco, o que contrastar mais."
            },
            "secondary": { "$ref": "#/$defs/hex_color", "description": "Cor de destaque: títulos e links." },
            "background": { "$ref": "#/$defs/hex_color", "description": "Fundo do corpo do e-mail." },
            "text": { "$ref": "#/$defs/hex_color", "description": "Texto do corpo; >= 4.5:1 sobre background (R-BRAND-CONTRAST)." }
          }
        },
        "font": {
          "type": "object",
          "description": "Fonte segura para e-mail (instalada nos sistemas) + família genérica de fallback.",
          "required": ["family", "fallback"],
          "additionalProperties": false,
          "properties": {
            "family": { "enum": ["Arial", "Helvetica", "Verdana", "Tahoma", "Trebuchet MS", "Georgia", "Times New Roman", "Courier New"] },
            "fallback": { "enum": ["sans-serif", "serif", "monospace"] }
          }
        },
        "host_signature": {
          "type": "object",
          "required": ["name", "role"],
          "additionalProperties": false,
          "properties": {
            "name": { "type": "string", "minLength": 1 },
            "role": { "type": "string", "minLength": 1 },
            "photo_url": {
              "type": "string",
              "pattern": "^https://\\S+$",
              "x-rule": "R-BRAND-HTTPS",
              "description": "Foto opcional do host (https)."
            },
            "photo_alt": { "type": "string", "minLength": 1 }
          },
          "dependentRequired": { "photo_url": ["photo_alt"] }
        },
        "links": {
          "type": "array",
          "maxItems": 6,
          "items": {
            "type": "object",
            "required": ["label", "url"],
            "additionalProperties": false,
            "properties": {
              "label": { "type": "string", "minLength": 1 },
              "url": { "type": "string", "pattern": "^https://\\S+$", "x-rule": "R-BRAND-HTTPS" }
            }
          },
          "description": "Redes e links no rodapé do convite."
        },
        "invitation_tone": {
          "enum": ["formal", "cordial", "descontraido"],
          "default": "cordial",
          "description": "Tom da abertura do convite (textos em contracts/i18n/<locale>.json, invitation.intro)."
        }
      }
    },
    "hex_color": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$", "x-rule": "R-BRAND-HEX", "description": "Cor em hex #RRGGBB." },
    "locale": { "enum": ["pt-BR", "en", "es", "zh"] },
    "localization": {
      "type": "object",
      "description": "Legendas, tradução e dublagem (research/06). Sem target_locales, o formulário não pergunta os aceites de localização; sem voice_replica, não oferece o aceite de réplica de voz.",
      "required": ["target_locales"],
      "additionalProperties": false,
      "properties": {
        "target_locales": { "type": "array", "minItems": 1, "uniqueItems": true, "items": { "$ref": "#/$defs/locale" } },
        "subtitle_profile": {
          "type": "object",
          "additionalProperties": false,
          "description": "Diagramação (Netflix: 42 car./linha, 2 linhas, 17 car./s adulto). zh exige valor próprio (guia zh não lido).",
          "properties": {
            "max_chars_per_line": { "type": "integer", "minimum": 10, "maximum": 80, "default": 42 },
            "max_lines": { "type": "integer", "minimum": 1, "maximum": 3, "default": 2 },
            "max_cps": { "type": "number", "minimum": 5, "maximum": 40, "default": 17 }
          }
        },
        "voice_replica": {
          "type": "object",
          "required": ["provider", "provider_country", "model_deletion_days"],
          "additionalProperties": false,
          "description": "Só preencher se o programa pretende oferecer réplica de voz. Vai nomeado no aceite (LGPD art. 11, I e art. 33).",
          "properties": {
            "provider": { "type": "string", "minLength": 1 },
            "provider_country": { "type": "string", "minLength": 2 },
            "model_deletion_days": { "type": "integer", "minimum": 0, "maximum": 365 }
          }
        },
        "glossary": { "type": "array", "items": { "$ref": "#/$defs/glossary_term" } }
      }
    },
    "glossary_term": {
      "type": "object",
      "description": "Termo do glossário do show: nome próprio, jargão, sigla. do_not_translate = aparece igual na tradução; translations[locale] = forma obrigatória.",
      "required": ["term"],
      "additionalProperties": false,
      "properties": {
        "term": { "type": "string", "minLength": 1 },
        "do_not_translate": { "type": "boolean", "default": false },
        "translations": { "type": "object", "propertyNames": { "enum": ["pt-BR", "en", "es", "zh"] }, "additionalProperties": { "type": "string", "minLength": 1 } },
        "note": { "type": "string" }
      }
    },
    "logistics": {
      "type": "object",
      "required": ["recording_modes"],
      "additionalProperties": false,
      "properties": {
        "recording_modes": { "type": "array", "minItems": 1, "items": { "enum": ["presencial", "remoto"] } },
        "studio_name": { "type": "string" },
        "address": { "$ref": "#/$defs/address" },
        "landmarks": { "type": "array", "items": { "type": "string" }, "description": "Pontos de referência." },
        "arrival_instructions": { "type": "string" },
        "gps_hint": { "type": "string", "description": "O que digitar no GPS/app de transporte." },
        "parking": {
          "type": "object",
          "required": ["status"],
          "additionalProperties": false,
          "properties": {
            "status": { "enum": ["disponivel", "indisponivel", "pago_proximo", "pendente"] },
            "details": { "type": "string" }
          }
        },
        "arrive_minutes_before": {
          "type": "object",
          "required": ["min", "max"],
          "additionalProperties": false,
          "properties": {
            "min": { "type": "integer", "minimum": 0 },
            "max": { "type": "integer", "minimum": 0 }
          }
        },
        "conduct_notes": { "type": "array", "items": { "type": "string" } },
        "remote_setup_notes": { "type": "array", "items": { "type": "string" } },
        "recording_duration_minutes": { "type": "integer", "minimum": 15, "default": 90, "description": "Duração do bloco no convite de agenda." }
      },
      "if": { "properties": { "recording_modes": { "contains": { "const": "presencial" } } } },
      "then": { "x-rule": "R-SHOW-PRESENCIAL-ADDRESS", "required": ["address", "arrive_minutes_before"] }
    },
    "address": {
      "type": "object",
      "required": ["street", "number", "city", "region", "country"],
      "additionalProperties": false,
      "properties": {
        "building_name": { "type": "string" },
        "street": { "type": "string" },
        "number": { "type": "string" },
        "number_aliases": { "type": "array", "items": { "type": "string" }, "description": "Numeração antiga/alternativa." },
        "complement": { "type": "string" },
        "district": { "type": "string" },
        "city": { "type": "string" },
        "region": { "type": "string" },
        "postal_code": { "type": "string" },
        "country": { "type": "string", "pattern": "^[A-Z]{2}$" }
      }
    },
    "automations": {
      "type": "object",
      "required": ["channels", "reminder_d_minus_1"],
      "additionalProperties": false,
      "properties": {
        "channels": {
          "type": "object",
          "required": ["email", "whatsapp", "calendar"],
          "additionalProperties": false,
          "properties": {
            "email": { "type": "boolean" },
            "whatsapp": { "type": "boolean" },
            "calendar": { "type": "boolean" }
          }
        },
        "reminder_d_minus_1": {
          "type": "object",
          "required": ["enabled"],
          "additionalProperties": false,
          "properties": {
            "enabled": { "type": "boolean" },
            "channels": { "type": "array", "items": { "enum": ["email", "whatsapp", "calendar"] } }
          }
        },
        "note": { "type": "string", "description": "Envio por canal só ocorre se o convidado consentiu naquele canal (guest-intake.automation_consents)." }
      }
    }
  }
}

```


## trend-sources.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://podcast-production.invalid/contracts/trend-sources.schema.json",
  "title": "TrendSources",
  "description": "Registro de fontes de tendência. keyless funciona sem chave (fallback). byok usa chave do próprio usuário, verificada ao ser fornecida. O contrato NUNCA guarda o valor da chave: só a referência (variável de ambiente ou caminho no cofre) e o resultado da verificação.",
  "type": "object",
  "required": ["version", "sources"],
  "additionalProperties": false,
  "properties": {
    "version": { "type": "integer", "minimum": 1 },
    "sources": { "type": "array", "minItems": 1, "items": { "$ref": "#/$defs/source" } }
  },
  "$defs": {
    "source": {
      "type": "object",
      "required": ["id", "kind", "provider", "priority", "enabled"],
      "additionalProperties": false,
      "properties": {
        "id": { "type": "string", "pattern": "^[a-z][a-z0-9_]{0,40}$" },
        "kind": { "enum": ["keyless", "byok"] },
        "provider": { "type": "string" },
        "priority": { "type": "integer", "minimum": 1, "description": "1 = consultar primeiro." },
        "enabled": { "type": "boolean" },
        "endpoint_template": { "type": "string", "description": "URL com placeholders {geo}, {query}, {hl}." },
        "notes": { "type": "string" },
        "credential": { "$ref": "#/$defs/credential" }
      },
      "allOf": [
        {
          "if": { "properties": { "kind": { "const": "byok" } } },
          "then": { "x-rule": "R-TREND-BYOK-CREDENTIAL", "required": ["credential"] }
        },
        {
          "if": { "properties": { "kind": { "const": "keyless" } } },
          "then": { "x-rule": "R-TREND-KEYLESS-NO-CREDENTIAL", "not": { "required": ["credential"] }, "required": ["endpoint_template"] }
        }
      ]
    },
    "credential": {
      "type": "object",
      "x-rule": "R-TREND-NO-SECRET-VALUE",
      "description": "Somente referência + verificação. Qualquer outra chave (api_key, token, value, secret...) é recusada.",
      "required": ["ref", "status"],
      "additionalProperties": false,
      "properties": {
        "ref": {
          "type": "object",
          "required": ["store", "name"],
          "additionalProperties": false,
          "properties": {
            "store": { "enum": ["env", "vault"] },
            "name": { "type": "string", "pattern": "^[A-Za-z0-9_./:-]{1,128}$", "description": "Nome da variável de ambiente ou caminho no cofre — nunca o valor." }
          }
        },
        "status": { "enum": ["not_provided", "unverified", "valid", "invalid", "expired", "revoked"] },
        "verified_at": { "type": "string", "format": "date-time" },
        "verification_note": { "type": "string", "maxLength": 200 }
      },
      "if": { "properties": { "status": { "enum": ["valid", "invalid", "expired", "revoked"] } } },
      "then": { "x-rule": "R-TREND-VERIFIED-AT", "required": ["verified_at"] }
    }
  }
}

```
