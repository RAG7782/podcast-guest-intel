<!--
Convite Oficial — template GENÉRICO (produto). É o PRIMEIRO envio ao convidado: leva o link do
formulário (variante escolhida pelo host). O kit (assets/templates/guest-kit.md) só vai depois da resposta.
Este arquivo é a versão TEXTO PURO do e-mail. A versão HTML (logo, cores, fonte e assinatura do bloco
`brand` do show-profile) é montada por assets/google-forms/src/invitation.js com os MESMOS
textos (references/contracts/i18n/<locale>.json, chave "invitation"). Nada de show específico aqui.

Sintaxe (mustache mínimo): {{caminho}} insere valor · {{#x}}…{{/x}} só se x existir (lista = repete,
item atual em {{.}}) · {{^x}}…{{/x}} só se x NÃO existir. Placeholder sem valor = erro.
Este bloco de comentário é removido na renderização.
-->
{{brand.display_name}}
{{t.title}}

{{t.greeting}}

{{t.intro}}

{{t.when_label}}: {{#scheduled_text}}{{scheduled_text}}{{/scheduled_text}}{{^scheduled_text}}{{t.when_tbd}}{{/scheduled_text}}
{{#presencial}}
{{t.where_label}}: {{#studio_name}}{{studio_name}} · {{/studio_name}}{{address_line}}
{{#gps_hint}}
{{t.gps_label}}: {{gps_hint}}
{{/gps_hint}}
{{#arrival_instructions}}
{{t.arrival_label}}: {{arrival_instructions}}
{{/arrival_instructions}}
{{#arrive}}
{{t.arrive}}
{{/arrive}}
{{/presencial}}
{{#remoto}}
{{t.remote_label}}: {{#remote_link}}{{remote_link}}{{/remote_link}}{{^remote_link}}{{t.remote_link_tbd}}{{/remote_link}}
{{/remoto}}

{{t.about_heading}}
{{#show.tagline}}
{{show.tagline}}
{{/show.tagline}}
{{show.editorial_line}}

{{t.cta_intro}}
{{t.cta_button}}: {{form_url}}

{{t.signoff}}
{{signature.name}}
{{#signature.role}}{{signature.role}} · {{/signature.role}}{{brand.display_name}}
{{#links_text}}
{{.}}
{{/links_text}}

--
{{t.footer_controller}}
{{t.footer_purpose}}
{{t.footer_optout}}
{{#t.footer_brand}}
{{t.footer_brand}}
{{/t.footer_brand}}
