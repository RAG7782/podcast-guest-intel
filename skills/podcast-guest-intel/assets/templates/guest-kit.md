<!--
Kit do Convidado — template GENÉRICO (produto). Nada de show específico aqui: tudo vem do
show-profile (references/contracts/show-profile.schema.json), do guest-intake e dos textos do locale
(references/contracts/i18n/<locale>.json, chave "kit"). Renderizado por assets/google-forms/src/core.js.

Sintaxe (mustache mínimo): {{caminho}} insere valor · {{#x}}…{{/x}} só se x existir (lista = repete,
item atual em {{.}}) · {{^x}}…{{/x}} só se x NÃO existir. Placeholder sem valor = erro (não some calado).
Tom: acolhedor e tranquilizador (show-profile.kit_tone). Variantes: presencial e remota.
Este bloco de comentário é removido na renderização.
-->
# {{t.title}} · {{show.name}}

{{t.greeting}}

{{t.thanks}}

## {{t.about_heading}}

{{#show.tagline}}
_{{show.tagline}}_

{{/show.tagline}}
{{show.editorial_line}}

**{{t.pillars_heading}}:**

{{#show.pillars}}
- {{.}}
{{/show.pillars}}

## {{t.when_heading}}

{{#scheduled_text}}
{{scheduled_text}}
{{/scheduled_text}}
{{^scheduled_text}}
{{t.when_tbd}}
{{/scheduled_text}}

{{#presencial}}
## {{t.where_heading}}

{{#studio_name}}
**{{studio_name}}**

{{/studio_name}}
- **{{t.address_label}}:** {{address_line}}
{{#landmarks}}
- **{{t.landmarks_label}}:** {{landmarks}}
{{/landmarks}}
{{#gps_hint}}
- **{{t.gps_label}}:** {{gps_hint}}
{{/gps_hint}}
{{#arrival_instructions}}
- {{arrival_instructions}}
{{/arrival_instructions}}
- **{{t.parking_label}}:** {{parking_text}}

{{t.arrive}}

{{/presencial}}
{{#remoto}}
## {{t.remote_heading}}

{{#remote_notes}}
- {{.}}
{{/remote_notes}}

{{/remoto}}
## {{t.conduct_heading}}

{{#conduct_notes}}
- {{.}}
{{/conduct_notes}}

## {{t.materials_heading}}

{{t.materials_text}}

## {{t.privacy_heading}}

{{t.privacy_text}}

{{t.signoff}}
{{show.name}}
