---
task: Guest Intake
responsavel: "@guest-coordinator"
responsavel_type: agent
atomic_layer: task
elicit: false
input_schema: references/contracts/show-profile.schema.json
output_schema: references/contracts/guest-intake.schema.json
Entrada: |
  - show-profile: perfil do programa (references/contracts/show-profile.schema.json) — linha editorial, logística, controlador, automações
  - variante: essencial (~2 min) | completo — escolhida pelo host na hora do envio
  - locale + jurisdição: definem os rótulos e a cláusula (references/contracts/i18n/<locale>.json)
  - convidado: nome + e-mail + data (convite oficial); nome + 1 link (modo mínimo, se não houver formulário)
  - show-profile.brand (opcional): logo, cores, fonte e assinatura do Convite Oficial
Saida: |
  - convite oficial enviado (assets/templates/guest-invitation-official.md + HTML com a marca), com o link do formulário
  - guest-intake: JSON validado contra references/contracts/guest-intake.schema.json (aba "intake" da planilha)
  - kit do convidado enviado (assets/templates/guest-kit.md), se o convidado consentiu no canal
  - convite de agenda e lembrete D-1, se houver data e consentimento
  - descartados: lista do que NÃO foi guardado e por quê (ex.: dado sensível sem aceite)
Checklist:
  - "[ ] show-profile válido (scripts/validate-contracts.py) e controlador com contato (contact_email ou contact_mode=reply_to_email)"
  - "[ ] Locale revisado (needs_native_review=false) e cláusula da jurisdição existe"
  - "[ ] Formulário criado pelo Apps Script (assets/google-forms), sem pergunta de upload"
  - "[ ] Convite Oficial enviado (enviarConvite) com o link do formulário ativo; brand com contraste AA (R-BRAND-CONTRAST)"
  - "[ ] Rodapé do convite: controlador, finalidade e opt-out; quem pediu SAIR está em OPTOUT_EMAILS (registrarOptOut)"
  - "[ ] Resposta recebida: intake na aba intake; e-mail-resumo do dono sem erro de canal"
  - "[ ] Dados sensíveis: só os com aceite específico; descartados conferidos no resumo"
  - "[ ] Materiais: links no intake; arquivos chegam como resposta ao e-mail do kit"
  - "[ ] Retenção: apagar respostas/dossiê até retention_days_after_publish após publicar"
---

# *guest-intake

Coleta do convidado antes da gravação: formulário curto com consentimento LGPD/GDPR, Kit do
Convidado e automações por canal. Dono único: @guest-coordinator. Fica entre o aceite do convite
(`references/tasks/guest-booking.md`) e a varredura pública/dossiê. Substitui a pré-entrevista por call.

## Entrada

- `show-profile` (input_schema): tudo que é do programa vem daqui; nada de show fixo no código.
- Variante `essencial` ou `completo` (mesmo contrato, só `form_variant` muda; campos da essencial
  em `x-form-variants` do schema).
- `locale`/`jurisdiction`: `references/contracts/i18n/<locale>.json` → rótulos e cláusula
  (`BR-LGPD`, `EU-GDPR`, `other`; `CN-PIPL` só esqueleto em `zh`).

## Saida

`guest-intake` (output_schema). Regras que o contrato e a integração garantem:

| Regra | O que acontece |
|---|---|
| Sem consentimento geral + aviso de pesquisa pública | não existe intake; o dono recebe a falha |
| Dado sensível (art. 11, I) | só entra com aceite específico e destacado; sem aceite é descartado e não guardado |
| Acessibilidade | tratada como sensível (pode revelar saúde): aceite próprio |
| WhatsApp | só com número válido (E.164; em show `BR-LGPD`, também DDD + número) **e** consentimento no canal |
| Agenda / D-1 | só com data combinada **e** consentimento no canal |
| Materiais | links no formulário; arquivos por resposta ao e-mail do kit (upload no Forms exige login Google) |

## Passos

1. Validar o show-profile: `uv run --no-project --with jsonschema --with pyyaml python scripts/validate-contracts.py`.
2. Instalar o formulário: `assets/google-forms/README.md` (copiar e colar no script.google.com).
3. Enviar o **Convite Oficial**, o primeiro contato: `enviarConvite({nome, email, data, modo}, variante)`.
   O e-mail sai com o logo, as cores e a assinatura do `brand` e leva o link do formulário ativo.
   O kit só é enviado depois da resposta. Quem responder SAIR vai para `registrarOptOut`.
4. Conferir o aviso que o dono recebe a cada resposta, em linguagem simples: o que foi enviado, o que precisa
   da atenção dele e o botão para a linha do convidado na aba **Convidados** da planilha.
5. Entregar o intake (aba `intake`, coluna `intake_json`, oculta) à etapa seguinte (varredura pública/dossiê).
   O link do briefing pronto vai na coluna **Briefing** da aba Convidados, na linha cujo **Código do registro**
   é o `intake_id`.
6. Sem formulário: modo mínimo com nome + 1 link; registrar como lacuna no dossiê.

## Uso

```bash
# Prévia do formulário, do kit e do convite oficial (.html/.txt) para um show-profile (sem tocar conta Google)
node integrations/google-forms/build.js (ferramenta de desenvolvimento, fora do pacote) example <show-profile.json> <pasta-de-saida>

# Testes da lógica (mapeamento, consentimento, kit, convite, D-1, WhatsApp)
node --test integrations/google-forms/test/*.test.js (ferramenta de desenvolvimento, fora do pacote)
```

## Limites

- A cláusula é rascunho técnico (`legal_review: pendente`): revisão de advogado antes do uso comercial.
- Revogação de consentimento e eliminação após a retenção ainda são manuais (apagar a linha da planilha).
