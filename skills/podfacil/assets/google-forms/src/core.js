/**
 * core.js — LÓGICA PURA do formulário do convidado (sem serviço Google).
 * Roda igual no Apps Script (V8, escopo global) e no Node (`module.exports` no fim).
 * Tudo que toca Google (FormApp, MailApp, CalendarApp, UrlFetchApp, PropertiesService)
 * fica em forms.js / automations.js e recebe daqui só dados.
 */

// ---------- template (mustache mínimo) ----------

var TPL_STANDALONE_RE = /^[ \t]*(\{\{[#^\/][^}]+\}\})[ \t]*\r?\n/gm;
var TPL_RE = /\{\{([#^])\s*([\w.]+)\s*\}\}([\s\S]*?)\{\{\/\s*\2\s*\}\}|\{\{\s*([\w.]+)\s*\}\}/g;

/** Valor de `path` em `view`. undefined = chave inexistente (erro); null = vazio declarado. */
function lookupPath(view, path) {
  if (path === '.') return view['.'];
  var parts = path.split('.');
  var node = view;
  for (var i = 0; i < parts.length; i++) {
    if (node === null) return null;
    if (typeof node !== 'object' || !(parts[i] in node)) return undefined;
    node = node[parts[i]];
  }
  return node;
}

function isFilled(value) {
  if (Array.isArray(value)) return value.length > 0;
  return value !== null && value !== undefined && value !== false && value !== '';
}

function renderSection(kind, key, inner, view) {
  var value = lookupPath(view, key);
  if (kind === '^') return isFilled(value) ? '' : renderRaw(inner, view);
  if (!isFilled(value)) return '';
  if (!Array.isArray(value)) return renderRaw(inner, view);
  return value.map(function (item) {
    return renderRaw(inner, Object.assign({}, view, { '.': item }));
  }).join('');
}

/** Uma passada só: valor inserido nunca é re-escaneado (dado do convidado não vira placeholder). */
function renderTemplate(template, view) {
  return renderRaw(String(template).replace(TPL_STANDALONE_RE, '$1'), view);
}

function renderRaw(template, view) {
  return template.replace(TPL_RE,
    function (m, kind, key, inner, varKey) {
      if (kind) return renderSection(kind, key, inner, view);
      var value = lookupPath(view, varKey);
      if (value === undefined) {
        throw new Error('placeholder {{' + varKey + '}} sem valor; esperado uma das chaves ' +
          JSON.stringify(Object.keys(view)));
      }
      return value === null ? '' : String(value);
    });
}

function stripDocComment(md) {
  return String(md).replace(/^<!--[\s\S]*?-->\s*/, '');
}

// ---------- locale, cláusula, controlador ----------

function selectLocale(bundle, locale, allowUnreviewed) {
  var i18n = bundle.i18n[locale];
  if (!i18n) {
    throw new Error('locale "' + locale + '" inexistente; esperado um de ' + JSON.stringify(Object.keys(bundle.i18n)));
  }
  if (i18n.needs_native_review && !allowUnreviewed) {
    throw new Error('locale "' + locale + '" tem needs_native_review=true (esqueleto); ' +
      'esperado locale revisado ou ALLOW_UNREVIEWED_LOCALE=true');
  }
  return i18n;
}

function selectClause(i18n, jurisdiction) {
  var clause = i18n.consent.clauses[jurisdiction];
  if (!clause) {
    throw new Error('jurisdição "' + jurisdiction + '" sem cláusula no locale ' + i18n.locale +
      '; esperado uma de ' + JSON.stringify(Object.keys(i18n.consent.clauses)));
  }
  return clause;
}

/** Controlador citado na cláusula. Sem contato válido, recusa (art. 9º, III LGPD). */
function resolveController(show, i18n) {
  var c = show.controller || {};
  var contact;
  if (c.contact_mode === 'reply_to_email') {
    contact = i18n.consent.contact_reply_to_email;
  } else if (c.contact_email) {
    contact = renderTemplate(i18n.consent.contact_email, { email: c.contact_email });
  } else {
    throw new Error('controller sem contato: contact_email=' + JSON.stringify(c.contact_email) +
      ', contact_mode=' + JSON.stringify(c.contact_mode) +
      '; esperado contact_email (e-mail) ou contact_mode="reply_to_email"');
  }
  return { name: c.name, document_id: c.document_id || null, contact: contact };
}

var BASE_PURPOSES = ['preparo_entrevista', 'dossie', 'memoria_episodio'];

function renderClause(i18n, jurisdiction, show) {
  var clause = selectClause(i18n, jurisdiction);
  var purposes = BASE_PURPOSES.map(function (p) { return i18n.consent.purposes[p]; });
  var text = renderTemplate(clause.text, {
    controller: resolveController(show, i18n), show: { name: show.name },
    purposes: purposes.join('; '),
    retention_days: show.retention_days_after_publish === undefined ? 90 : show.retention_days_after_publish
  });
  var draft = isDraftClause(clause);
  return { clause_id: clause.clause_id, text: draft ? i18n.consent.draft_notice + '\n\n' + text : text, draft: draft };
}

/** R-07: cláusula sem `legal_review: aprovado|approved` é rascunho; o aviso some sozinho quando o advogado aprova. */
function isDraftClause(clause) {
  return ['aprovado', 'approved'].indexOf(clause.legal_review) < 0;
}

// ---------- especificação do formulário ----------

var FIELD_TYPES = {
  'guest.full_name': 'text', 'guest.preferred_name': 'text', 'guest.name_pronunciation': 'text',
  'guest.pronouns': 'text', 'guest.role_title': 'text', 'guest.photo_url': 'url',
  'bio.short': 'paragraph', 'bio.long': 'paragraph', links: 'paragraph', social_handles: 'paragraph',
  previous_interviews: 'paragraph', key_ideas: 'paragraph', stories_to_tell: 'paragraph',
  'controversies.accepts': 'paragraph', 'controversies.declines': 'paragraph',
  off_limits_topics: 'paragraph', wants_to_promote: 'paragraph', dream_questions: 'paragraph',
  'conflicts_of_interest.details': 'paragraph', 'companion.name': 'text', materials: 'paragraph',
  recording_mode: 'choice', scheduled_at: 'datetime', wants_prepublication_review: 'choice',
  preferred_channel: 'choice', 'contacts.email': 'email', 'contacts.whatsapp': 'phone',
  automation_consents: 'checkbox'
};

var SECTIONS = [
  ['about', ['guest.full_name', 'guest.preferred_name', 'guest.name_pronunciation', 'guest.pronouns',
    'guest.role_title', 'guest.photo_url', 'bio.short', 'bio.long', 'links', 'social_handles', 'previous_interviews']],
  ['content', ['key_ideas', 'stories_to_tell', 'controversies.accepts', 'controversies.declines',
    'off_limits_topics', 'wants_to_promote', 'dream_questions', 'conflicts_of_interest.details', 'materials']],
  ['logistics', ['recording_mode', 'scheduled_at', 'companion.name', 'wants_prepublication_review']],
  ['channels', ['contacts.email', 'contacts.whatsapp', 'preferred_channel', 'automation_consents']]
];

var REQUIRED = ['guest.full_name', 'guest.preferred_name', 'bio.short', 'links', 'recording_mode', 'contacts.email'];

/**
 * Padrão do WhatsApp no Forms, coerente com o toE164 do intake.js (o que passa aqui o intake aceita): no Brasil,
 * celular (DDD + 9 + 8 dígitos, com +55 ou 0 opcionais) ou número de outro país com +; fora do Brasil, só com + ou 00.
 * ponytail: o DDD inexistente (ex.: 20) passa aqui e cai no toE164, que confere a lista da Anatel.
 */
function phonePattern(jurisdiction) {
  var intl = '(\\+|00)[1-9][0-9 ().-]{6,20}[0-9]';
  if (jurisdiction !== 'BR-LGPD') return '^\\s*' + intl + '\\s*$';
  var br = '(\\+?55[ .-]*)?\\(?0?[1-9]{2}\\)?[ .-]*9[ .-]*[0-9]{4}[ .-]*[0-9]{4}';
  return '^\\s*(' + br + '|' + intl + ')\\s*$';
}

function choicesFor(key, i18n, show) {
  var c = i18n.form.choices;
  var pick = function (map, keys) { return keys.map(function (k) { return { value: k, label: map[k] }; }); };
  if (key === 'recording_mode') return pick(c.recording_mode, show.logistics.recording_modes);
  if (key === 'wants_prepublication_review') return pick(c.yes_no, ['yes', 'no']);
  if (key === 'preferred_channel') return pick(c.preferred_channel, ['email', 'whatsapp', 'phone', 'other']);
  if (key === 'automation_consents') return pick(c.channels, enabledChannels(show));
  if (key === 'sensitive.category') return pick(c.sensitive_category, Object.keys(c.sensitive_category));
  return null;
}

function enabledChannels(show) {
  var ch = show.automations.channels;
  return ['email', 'whatsapp', 'calendar'].filter(function (k) { return ch[k]; });
}

function inVariant(key, variant, variants) {
  if (variant === 'completo') return true;
  var list = variants[variant];
  if (!Array.isArray(list)) throw new Error('variante "' + variant + '" inválida; esperado essencial|completo');
  return list.some(function (v) { return key === v || key.indexOf(v + '.') === 0; });
}

function fieldItem(key, i18n, show) {
  var label = i18n.form.fields[key];
  if (!label) throw new Error('campo "' + key + '" sem rótulo em i18n ' + i18n.locale + '.form.fields');
  var it = { type: FIELD_TYPES[key] || 'paragraph', key: key, title: label.title, help: label.help,
    required: REQUIRED.indexOf(key) >= 0, choices: choicesFor(key, i18n, show) };
  if (it.type === 'phone') it.invalid = i18n.form.validation.phone;   // o Forms mostra ao convidado e não deixa enviar
  return it;
}

function acceptItem(key, i18n, text, required) {
  return { type: 'checkbox', key: key, title: i18n.form.fields[key].title, help: '',
    required: required, choices: [{ value: 'yes', label: text }] };
}

function consentItems(i18n, clause) {
  var c = i18n.consent;
  return [
    { type: 'section', key: 'section.consent', title: i18n.form.sections.consent, help: clause.text },
    acceptItem('consent.general', i18n, c.general_accept, true),
    acceptItem('consent.public_research', i18n, c.public_research_accept, true),
    acceptItem('consent.divulgacao', i18n, c.divulgacao_accept, false),
    acceptItem('image_voice', i18n, c.image_voice_accept, false)
  ];
}

function sensitiveItems(i18n, show) {
  var c = i18n.consent;
  return [
    { type: 'section', key: 'section.sensitive', title: i18n.form.sections.sensitive, help: c.sensitive_intro },
    fieldItem('accessibility.needs', i18n, show),
    acceptItem('accessibility.accept', i18n, c.accessibility_accept, false),
    Object.assign(fieldItem('sensitive.category', i18n, show), { type: 'choice' }),
    fieldItem('sensitive.value', i18n, show),
    acceptItem('sensitive.accept', i18n, c.sensitive_accept, false)
  ];
}

/**
 * Três aceites SEPARADOS de localização (research/06 §3.3), nenhum obrigatório nem pré-marcado.
 * Só aparecem se o show-profile tem localization.target_locales (idiomas nomeados: autorização
 * genérica é nula, LGPD art. 8º, §4º); a réplica de voz só com localization.voice_replica
 * (provedor, país e prazo de apagamento nomeados no texto: art. 11, I e art. 33).
 */
function localizationItems(i18n, show) {
  var loc = show.localization;
  if (!loc || !loc.target_locales || !loc.target_locales.length) return [];
  var c = i18n.consent, names = i18n.localization.language_names;
  var locales = loc.target_locales.map(function (l) { return names[l] || l; }).join(', ');
  var items = [
    { type: 'section', key: 'section.localization', title: i18n.form.sections.localization, help: c.localization_intro },
    acceptItem('localization.translation_text', i18n, renderTemplate(c.translation_accept, { locales: locales }), false),
    acceptItem('localization.dub_generic_voice', i18n, renderTemplate(c.dub_generic_accept, { locales: locales }), false)
  ];
  var vr = loc.voice_replica;
  if (vr) {
    items.push(acceptItem('localization.dub_voice_replica', i18n, renderTemplate(c.dub_replica_accept,
      { locales: locales, provider: vr.provider, country: vr.provider_country, days: vr.model_deletion_days }), false));
  }
  return items;
}

/** Lista ordenada de itens que forms.js materializa com FormApp. */
/** Free: "Preparado com PodFácil" no fim da descrição, em qualquer variante. Só `branded === false`
 *  (pago) tira a marca; o pacote local, que é o Free, não passa a opção (FLUXOS Q7). */
function formBrandLine(i18n, branded) {
  if (branded === false) return '';
  var brand = i18n.invitation && i18n.invitation.footer_brand;
  if (typeof brand !== 'string') {
    throw new Error('i18n ' + i18n.locale + ' invitation.footer_brand=' + JSON.stringify(brand) + '; esperado texto do rodapé do Free');
  }
  return '\n\n' + brand;
}

function buildFormSpec(opts) {
  var i18n = opts.i18n, show = opts.show, variant = opts.variant;
  var clause = renderClause(i18n, opts.jurisdiction, show);
  var items = [];
  SECTIONS.forEach(function (sec) {
    var keys = sec[1].filter(function (k) { return inVariant(k, variant, opts.variants); });
    if (!keys.length) return;
    items.push({ type: 'section', key: 'section.' + sec[0], title: i18n.form.sections[sec[0]], help: '' });
    keys.forEach(function (k) { items.push(fieldItem(k, i18n, show)); });
  });
  // Codex #5: código de uso único do convite, pré-preenchido pelo link do enviarConvite (logo após o e-mail)
  var at = items.map(function (it) { return it.key; }).indexOf('contacts.email');
  items.splice(at + 1, 0, { type: 'text', key: 'invite.token', title: i18n.form.fields['invite.token'].title,
    help: i18n.form.fields['invite.token'].help, required: false });
  items.forEach(function (it) { if (it.type === 'phone') it.pattern = phonePattern(opts.jurisdiction); });
  if (variant === 'completo') items = items.concat(sensitiveItems(i18n, show));
  items = items.concat(consentItems(i18n, clause)).concat(localizationItems(i18n, show));
  return {
    title: renderTemplate(i18n.form.title, { show: { name: show.name } }),
    description: (clause.draft ? i18n.consent.draft_notice + '\n\n' : '') + i18n.form['description_' + variant] + formBrandLine(i18n, opts.branded),
    confirmation: i18n.form.confirmation,
    clause_id: clause.clause_id, text_version: i18n.text_version, items: items
  };
}

if (typeof module !== 'undefined') {
  module.exports = {
    renderTemplate: renderTemplate, lookupPath: lookupPath, stripDocComment: stripDocComment,
    selectLocale: selectLocale, selectClause: selectClause, resolveController: resolveController,
    renderClause: renderClause, isDraftClause: isDraftClause, buildFormSpec: buildFormSpec, enabledChannels: enabledChannels,
    localizationItems: localizationItems, phonePattern: phonePattern,
    BASE_PURPOSES: BASE_PURPOSES
  };
}
