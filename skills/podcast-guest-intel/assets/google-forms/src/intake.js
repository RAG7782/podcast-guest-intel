/**
 * intake.js — LÓGICA PURA: resposta do Form → guest-intake, regras de consentimento,
 * plano de envios, D-1, kit, WhatsApp e orquestração idempotente. Sem serviço Google.
 */
if (typeof module !== 'undefined') {
  var core_ = require('./core.js');
  var renderTemplate = core_.renderTemplate, stripDocComment = core_.stripDocComment;
  var resolveController = core_.resolveController, BASE_PURPOSES = core_.BASE_PURPOSES;
}

// ---------- normalização ----------

var URL_RE = /^https?:\/\/\S+\.\S+$/i;
var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function maskValue(value) {
  var s = String(value);
  return s.length <= 4 ? '***' : '***' + s.slice(-4);
}

function lines(raw) {
  if (raw === undefined || raw === null) return [];
  return String(raw).split(/\r?\n/).map(function (l) { return l.trim(); }).filter(Boolean);
}

function text(raw) {
  var s = raw === undefined || raw === null ? '' : String(raw).trim();
  return s || null;
}

function toUrl(s) {
  var u = /^https?:\/\//i.test(s) ? s : (/^[\w-]+(\.[\w-]+)+/.test(s) ? 'https://' + s : s);
  return URL_RE.test(u) ? u : null;
}

function urlList(raw, field, dropped) {
  return lines(raw).map(function (l) {
    var u = toUrl(l);
    if (!u) dropped.push({ field: field, reason: 'não é URL: ' + JSON.stringify(l) + '; esperado http(s)://…' });
    return u;
  }).filter(Boolean);
}

function toE164(raw) {
  var s = text(raw);
  if (!s) return null;
  var digits = s.replace(/[\s().-]/g, '').replace(/^00/, '+');
  return /^\+[1-9][0-9]{7,14}$/.test(digits) ? digits : undefined;
}

function hasYes(raw) {
  return Array.isArray(raw) ? raw.indexOf('yes') >= 0 : raw === 'yes';
}

function setIf(obj, key, value) {
  if (Array.isArray(value) ? value.length : value !== null && value !== undefined) obj[key] = value;
}

function slugId(prefix, id) {
  return (prefix + String(id).toLowerCase().replace(/[^a-z0-9_-]/g, '-')).slice(0, 64);
}

function pad2(n) { return (n < 10 ? '0' : '') + n; }

/** "YYYY-MM-DD HH:MM" (DateTimeItem) + "-03:00" → ISO; null se vazio; undefined se ilegível. */
function parseFormDateTime(raw, offset) {
  var s = text(raw);
  if (!s) return null;
  var m = /^(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2})/.exec(s);
  return m ? m[1] + '-' + m[2] + '-' + m[3] + 'T' + m[4] + ':' + m[5] + ':00' + offset : undefined;
}

function guestBlock(a) {
  var g = { full_name: text(a['guest.full_name']) };
  if (!g.full_name) throw new Error('guest.full_name vazio; esperado nome completo (campo obrigatório)');
  g.preferred_name = text(a['guest.preferred_name']) || g.full_name.split(/\s+/)[0];
  ['name_pronunciation', 'pronouns', 'role_title'].forEach(function (k) { setIf(g, k, text(a['guest.' + k])); });
  setIf(g, 'photo_url', text(a['guest.photo_url']) && toUrl(text(a['guest.photo_url'])));
  return g;
}

function bioBlock(a) {
  var short = text(a['bio.short']);
  if (!short) throw new Error('bio.short vazio; esperado mini-bio de até 280 caracteres');
  var bio = { short: short.length > 280 ? short.slice(0, 279) + '…' : short };
  setIf(bio, 'long', text(a['bio.long']) || (short.length > 280 ? short : null));
  return bio;
}

function contentBlock(a, out, dropped) {
  setIf(out, 'social_handles', lines(a.social_handles).map(function (l) {
    var m = /^([^:]+):\s*(.+)$/.exec(l);
    return m ? { platform: m[1].trim().toLowerCase(), handle: m[2].trim() } : { platform: 'outro', handle: l };
  }));
  setIf(out, 'previous_interviews', urlList(a.previous_interviews, 'previous_interviews', dropped));
  var ideas = lines(a.key_ideas);
  if (ideas.length > 3) dropped.push({ field: 'key_ideas', reason: 'mais de 3 ideias (' + ideas.length + '); mantidas as 3 primeiras' });
  setIf(out, 'key_ideas', ideas.slice(0, 3));
  ['stories_to_tell', 'off_limits_topics', 'wants_to_promote', 'dream_questions'].forEach(function (k) {
    setIf(out, k, lines(a[k]));
  });
  var acc = lines(a['controversies.accepts']), dec = lines(a['controversies.declines']);
  if (acc.length || dec.length) out.controversies = { accepts: acc, declines: dec };
  var coi = text(a['conflicts_of_interest.details']);
  out.conflicts_of_interest = coi ? { declared: true, details: coi } : { declared: false };
  setIf(out, 'materials', urlList(a.materials, 'materials', dropped).map(function (u) { return { kind: 'outro', url: u }; }));
}

function consentRecord(id, at, ctx, purposes) {
  return { consent_id: id, granted: true, granted_at: at, text_version: ctx.textVersion,
    clause_id: ctx.clauseId, purposes: purposes, public_research_notice: true, channel: 'google-forms' };
}

function specificConsent(id, purpose, ctx) {
  return { consent_id: id, specific: true, highlighted: true, purpose: purpose,
    granted_at: ctx.submittedAt, text_version: ctx.textVersion + '/sensitive' };
}

/** Art. 11, I: sensível só entra com aceite próprio; sem ele, descartado (não guardado). */
function sensitiveBlock(a, out, ctx, dropped) {
  var needs = text(a['accessibility.needs']);
  if (needs && hasYes(a['accessibility.accept'])) {
    out.accessibility = { needs: needs, consent: specificConsent('cs-' + ctx.idBase + '-acess', ctx.purposes.accessibility, ctx) };
  } else if (needs) {
    dropped.push({ field: 'accessibility', reason: 'DADO SENSÍVEL sem aceite específico; descartado' });
  }
  var value = text(a['sensitive.value']), category = text(a['sensitive.category']);
  if (!value) return;
  if (!hasYes(a['sensitive.accept']) || !category) {
    dropped.push({ field: 'sensitive', reason: 'DADO SENSÍVEL sem aceite específico ou sem categoria (categoria=' +
      JSON.stringify(category) + '); descartado' });
    return;
  }
  out.sensitive_declarations = [{ field_id: 'sensivel_1', sensitive: true, category: category, value: value,
    consent: specificConsent('cs-' + ctx.idBase + '-sens', ctx.purposes.sensitive, ctx) }];
}

var LOC_KEYS = ['translation_text', 'dub_generic_voice', 'dub_voice_replica'];

function replicaConsent(base, loc, ctx) {
  var vr = loc.voice_replica;
  if (!vr) throw new Error('aceite de réplica de voz sem show.localization.voice_replica (recebido ' + JSON.stringify(vr) + '); esperado {provider, provider_country, model_deletion_days}');
  var rec = { consent_id: base.consent_id, granted: true, sensitive: true, specific: true, highlighted: true,
    purpose: ctx.purposes.voice_replica };
  if (ctx.episodeRef) rec.episode_ref = ctx.episodeRef;
  return Object.assign(rec, { granted_at: base.granted_at, text_version: base.text_version, target_locales: base.target_locales,
    provider: { name: vr.provider, country: vr.provider_country }, model_deletion_days: vr.model_deletion_days });
}

/** Três aceites separados (research/06 §3.3). Nenhum marcado = bloco ausente = nada autorizado. */
function localizationBlock(a, out, ctx) {
  var granted = LOC_KEYS.filter(function (k) { return hasYes(a['localization.' + k]); });
  if (!granted.length) return;
  var loc = ctx.localization;
  if (!loc || !Array.isArray(loc.target_locales) || !loc.target_locales.length) {
    throw new Error('aceite de localização sem ctx.localization.target_locales (recebido ' + JSON.stringify(loc) + '); esperado show.localization do show-profile');
  }
  out.localization_consents = {};
  LOC_KEYS.forEach(function (k) {
    if (granted.indexOf(k) < 0) { out.localization_consents[k] = { granted: false }; return; }
    var base = { consent_id: 'cl-' + ctx.idBase + '-' + k.replace(/_/g, '-'), granted: true, granted_at: ctx.submittedAt,
      text_version: ctx.textVersion + '/' + k, target_locales: loc.target_locales.slice() };
    out.localization_consents[k] = k === 'dub_voice_replica' ? replicaConsent(base, loc, ctx) : base;
  });
}

function channelBlock(a, out, ctx, dropped) {
  var email = text(a['contacts.email']);
  if (!email || !EMAIL_RE.test(email)) {
    throw new Error('contacts.email inválido: ' + JSON.stringify(email && maskValue(email)) + '; esperado e-mail');
  }
  out.contacts = { email: email };
  var phone = toE164(a['contacts.whatsapp']);
  if (phone === undefined) {
    dropped.push({ field: 'contacts.whatsapp', reason: 'número fora do E.164: ' + maskValue(a['contacts.whatsapp']) + '; esperado +<país><número>' });
  } else if (phone) out.contacts.whatsapp = phone;
  var chosen = Array.isArray(a.automation_consents) ? a.automation_consents : [];
  out.automation_consents = {};
  ['email', 'whatsapp', 'calendar'].forEach(function (k) {
    var granted = chosen.indexOf(k) >= 0 && (k !== 'whatsapp' || !!out.contacts.whatsapp);
    if (k === 'whatsapp' && chosen.indexOf(k) >= 0 && !granted) {
      dropped.push({ field: 'automation_consents.whatsapp', reason: 'consentiu WhatsApp sem número válido; canal desligado' });
    }
    out.automation_consents[k] = granted ? { granted: true, granted_at: ctx.submittedAt } : { granted: false };
  });
}

function logisticsBlock(a, out, ctx, dropped) {
  out.recording_mode = text(a.recording_mode);
  if (['presencial', 'remoto'].indexOf(out.recording_mode) < 0) {
    throw new Error('recording_mode=' + JSON.stringify(out.recording_mode) + '; esperado presencial|remoto');
  }
  var when = parseFormDateTime(a.scheduled_at, ctx.offset);
  if (when === undefined) dropped.push({ field: 'scheduled_at', reason: 'data ilegível: ' + JSON.stringify(a.scheduled_at) + '; esperado YYYY-MM-DD HH:MM' });
  else setIf(out, 'scheduled_at', when);
  var comp = text(a['companion.name']);
  if (comp) out.companion = { bringing: true, name: comp };
  if (a.wants_prepublication_review) out.wants_prepublication_review = a.wants_prepublication_review === 'yes';
  setIf(out, 'preferred_channel', text(a.preferred_channel));
  if (hasYes(a.image_voice)) out.image_voice_authorization = { granted: true, text_version: ctx.textVersion, granted_at: ctx.submittedAt };
}

/**
 * answers: {chave_do_campo: string|string[]} (valores de escolha já decodificados para o `value`).
 * ctx: {responseId, submittedAt, variant, locale, jurisdiction, clauseId, textVersion, offset, purposes:{sensitive, accessibility, voice_replica}, localization: show.localization|null}
 * → {intake, dropped}. Sem consentimento geral lança erro: não existe intake.
 */
function normalizeIntake(a, ctx) {
  if (!hasYes(a['consent.general']) || !hasYes(a['consent.public_research'])) {
    throw new Error('consentimento geral ausente (general=' + JSON.stringify(a['consent.general']) +
      ', public_research=' + JSON.stringify(a['consent.public_research']) + '); esperado "yes" nos dois. Resposta descartada.');
  }
  var dropped = [];
  var c = Object.assign({ idBase: slugId('', ctx.responseId).slice(0, 40) }, ctx);
  var out = { intake_id: slugId('in-', ctx.responseId), form_variant: ctx.variant, locale: ctx.locale,
    jurisdiction: ctx.jurisdiction, submitted_at: ctx.submittedAt };
  setIf(out, 'episode_ref', ctx.episodeRef || null);
  out.guest = guestBlock(a);
  out.bio = bioBlock(a);
  out.links = urlList(a.links, 'links', dropped);
  if (!out.links.length) throw new Error('links sem nenhuma URL válida: ' + JSON.stringify(lines(a.links)) + '; esperado ao menos 1 link');
  contentBlock(a, out, dropped);
  logisticsBlock(a, out, c, dropped);
  channelBlock(a, out, c, dropped);
  var purposes = BASE_PURPOSES.concat(hasYes(a['consent.divulgacao']) ? ['divulgacao'] : []);
  out.consent = consentRecord('cg-' + c.idBase, ctx.submittedAt, ctx, purposes);
  sensitiveBlock(a, out, c, dropped);
  localizationBlock(a, out, c);
  return { intake: out, dropped: dropped };
}

if (typeof module !== 'undefined') {
  module.exports = { normalizeIntake: normalizeIntake, parseFormDateTime: parseFormDateTime,
    toE164: toE164, maskValue: maskValue, lines: lines, EMAIL_RE: EMAIL_RE };
}
