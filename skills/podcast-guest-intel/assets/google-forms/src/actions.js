/**
 * actions.js — LÓGICA PURA: kit, mensagens, plano de envio por consentimento, D-1,
 * requisição de WhatsApp (Evolution API / WAHA / genérico) e orquestração idempotente.
 */
if (typeof module !== 'undefined') {
  var core2_ = require('./core.js');
  var renderTemplate = core2_.renderTemplate, stripDocComment = core2_.stripDocComment;
  var resolveController = core2_.resolveController;
}

// ---------- view do kit ----------

function addressLine(addr) {
  if (!addr) return null;
  var parts = [addr.building_name, addr.street + ', ' + addr.number +
    (addr.number_aliases && addr.number_aliases.length ? ' / ' + addr.number_aliases.join(' / ') : ''),
    addr.complement, addr.district, addr.city + ' - ' + addr.region, addr.postal_code];
  return parts.filter(Boolean).join(' · ');
}

/** "2026-10-20T14:30:00-03:00" → "20/10/2026, 14:30" (pt-BR) ou "2026-10-20, 14:30" (outros). Hora local do ISO. */
function formatScheduled(iso, locale) {
  if (!iso) return null;
  var m = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})/.exec(iso);
  if (!m) throw new Error('scheduled_at=' + JSON.stringify(iso) + '; esperado ISO 8601 com hora');
  var day = locale === 'pt-BR' || locale === 'es' ? m[3] + '/' + m[2] + '/' + m[1] : m[1] + '-' + m[2] + '-' + m[3];
  return day + ', ' + m[4] + ':' + m[5];
}

function baseView(show, intake, i18n) {
  var lg = show.logistics, mode = intake.recording_mode;
  var presencial = mode === 'presencial';
  return {
    show: { name: show.name, tagline: show.tagline || null, editorial_line: show.editorial_line, pillars: show.pillars },
    guest: { preferred_name: intake.guest.preferred_name },
    controller: resolveController(show, i18n),
    presencial: presencial, remoto: mode === 'remoto',
    scheduled_text: formatScheduled(intake.scheduled_at, intake.locale),
    studio_name: presencial ? lg.studio_name || null : null,
    address_line: presencial ? addressLine(lg.address) : null,
    landmarks: presencial && lg.landmarks && lg.landmarks.length ? lg.landmarks.join('; ') : null,
    gps_hint: presencial ? lg.gps_hint || null : null,
    arrival_instructions: presencial ? lg.arrival_instructions || null : null,
    parking_text: lg.parking ? i18n.kit.parking[lg.parking.status] + (lg.parking.details && lg.parking.status !== 'pendente' ? ' (' + lg.parking.details + ')' : '') : i18n.kit.parking.pendente,
    arrive: presencial && lg.arrive_minutes_before ? lg.arrive_minutes_before : null,
    remote_notes: lg.remote_setup_notes && lg.remote_setup_notes.length ? lg.remote_setup_notes : i18n.kit.remote_default,
    conduct_notes: i18n.kit.conduct_default.concat(lg.conduct_notes || [])
  };
}

/** Strings do i18n renderizadas uma vez contra a view (antes do template). */
function renderStrings(map, view) {
  var out = {};
  Object.keys(map).forEach(function (k) {
    out[k] = typeof map[k] === 'string' ? renderTemplate(map[k], view) : map[k];
  });
  return out;
}

function renderKit(template, show, intake, i18n) {
  var view = baseView(show, intake, i18n);
  view.t = renderStrings(i18n.kit, view);
  return renderTemplate(stripDocComment(template), view).replace(/\n{3,}/g, '\n\n').trim() + '\n';
}

function renderMessage(key, show, intake, i18n) {
  var tpl = i18n.messages[key];
  if (tpl === undefined) throw new Error('mensagem "' + key + '" ausente em i18n ' + i18n.locale + '.messages');
  return renderTemplate(tpl, baseView(show, intake, i18n));
}

/** Escapa texto para HTML, inclusive dentro de atributo entre aspas. */
function escapeHtml(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

/** Markdown do kit → HTML simples (títulos, negrito, itálico, listas, parágrafos). */
function mdToHtml(md) {
  return escapeHtml(md).split(/\n{2,}/).map(function (block) {
    var b = block.replace(/\*\*(.+?)\*\*/g, '<b>$1</b>').replace(/(^|\s)_(.+?)_(?=\s|$)/g, '$1<i>$2</i>');
    var h = /^(#{1,3}) (.*)$/.exec(b);
    if (h) return '<h' + (h[1].length + 1) + '>' + h[2] + '</h' + (h[1].length + 1) + '>';
    if (/^- /.test(b)) return '<ul>' + b.split('\n').map(function (l) { return '<li>' + l.replace(/^- /, '') + '</li>'; }).join('') + '</ul>';
    return '<p>' + b.replace(/\n/g, '<br>') + '</p>';
  }).join('\n');
}

// ---------- plano de envio ----------

function consented(intake, ch) {
  return !!(intake.automation_consents[ch] && intake.automation_consents[ch].granted);
}

/** Envio só se o show liga o canal E o convidado consentiu naquele canal. */
function planSubmitActions(intake, show) {
  var on = show.automations.channels, id = intake.intake_id, acts = [];
  if (on.email && consented(intake, 'email')) acts.push({ key: id + ':email:kit', channel: 'email', kind: 'kit' });
  if (on.whatsapp && consented(intake, 'whatsapp') && intake.contacts.whatsapp) {
    acts.push({ key: id + ':whatsapp:kit', channel: 'whatsapp', kind: 'kit' });
  }
  if (on.calendar && consented(intake, 'calendar') && intake.scheduled_at) {
    acts.push({ key: id + ':calendar:invite', channel: 'calendar', kind: 'invite' });
  }
  return acts;
}

function dayKey(ms, offsetMinutes) {
  return new Date(ms + offsetMinutes * 60000).toISOString().slice(0, 10);
}

/** true se a gravação cai no dia seguinte a `nowMs`, no fuso (offset em minutos) do script. */
function isDMinus1(scheduledIso, nowMs, offsetMinutes) {
  var t = Date.parse(scheduledIso);
  if (isNaN(t)) throw new Error('scheduled_at=' + JSON.stringify(scheduledIso) + '; esperado ISO 8601');
  return dayKey(t, offsetMinutes) === dayKey(nowMs + 86400000, offsetMinutes);
}

function planReminderActions(intake, show, nowMs, offsetMinutes) {
  var r = show.automations.reminder_d_minus_1, on = show.automations.channels;
  if (!r.enabled || !intake.scheduled_at || !isDMinus1(intake.scheduled_at, nowMs, offsetMinutes)) return [];
  return (r.channels || ['email']).filter(function (ch) {
    return ch !== 'calendar' && on[ch] && consented(intake, ch) && (ch !== 'whatsapp' || intake.contacts.whatsapp);
  }).map(function (ch) {
    return { key: intake.intake_id + ':' + ch + ':d-1', channel: ch, kind: 'reminder' };
  });
}

// ---------- WhatsApp (webhook genérico) ----------

/**
 * cfg: {provider: evolution|waha|generic, url, token, instance?, session?}
 * evolution: POST {url}/message/sendText/{instance}, header apikey, {number, text}
 * waha:      POST {url}/api/sendText, header X-Api-Key, {chatId: "<dígitos>@c.us", text, session}
 * generic:   POST {url}, Authorization: Bearer, {to: "+E164", text}
 */
function buildWhatsappRequest(cfg, e164, message) {
  if (!cfg || !cfg.url || !cfg.token) {
    throw new Error('WhatsApp sem configuração: url=' + JSON.stringify(cfg && cfg.url) +
      ', token=' + (cfg && cfg.token ? '[definido]' : 'ausente') + '; esperado WHATSAPP_URL e WHATSAPP_TOKEN');
  }
  var base = String(cfg.url).replace(/\/+$/, ''), digits = e164.replace(/^\+/, '');
  var p = cfg.provider || 'generic';
  if (p === 'evolution') {
    if (!cfg.instance) throw new Error('evolution exige WHATSAPP_INSTANCE (nome da instância); recebido vazio');
    return { url: base + '/message/sendText/' + encodeURIComponent(cfg.instance),
      headers: { apikey: cfg.token }, payload: { number: digits, text: message } };
  }
  if (p === 'waha') {
    return { url: base + '/api/sendText', headers: { 'X-Api-Key': cfg.token },
      payload: { chatId: digits + '@c.us', text: message, session: cfg.session || 'default' } };
  }
  if (p === 'generic') {
    return { url: base, headers: { Authorization: 'Bearer ' + cfg.token }, payload: { to: e164, text: message } };
  }
  throw new Error('WHATSAPP_PROVIDER=' + JSON.stringify(p) + '; esperado evolution|waha|generic');
}

// ---------- orquestração ----------

/**
 * Executa cada ação isolada: falha de um canal não derruba os outros.
 * store: {has(key), set(key, value)} — idempotência (reexecução não reenvia).
 * executors: {email|whatsapp|calendar: function(action) → ref}
 */
function runActions(actions, executors, store) {
  return actions.map(function (a) {
    if (store.has(a.key)) return { key: a.key, status: 'skipped', reason: 'já enviado' };
    try {
      var exec = executors[a.channel];
      if (!exec) throw new Error('canal sem executor: ' + JSON.stringify(a.channel) + '; esperado um de ' + JSON.stringify(Object.keys(executors)));
      var ref = exec(a);
      store.set(a.key, String(ref || new Date().toISOString()));
      return { key: a.key, status: 'sent' };
    } catch (e) {
      return { key: a.key, status: 'error', error: a.channel + ': ' + (e && e.message ? e.message : String(e)) };
    }
  });
}

if (typeof module !== 'undefined') {
  module.exports = { renderKit: renderKit, renderMessage: renderMessage, mdToHtml: mdToHtml, escapeHtml: escapeHtml,
    addressLine: addressLine, formatScheduled: formatScheduled, planSubmitActions: planSubmitActions,
    planReminderActions: planReminderActions, isDMinus1: isDMinus1,
    buildWhatsappRequest: buildWhatsappRequest, runActions: runActions };
}
