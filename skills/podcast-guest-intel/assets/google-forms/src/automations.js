/**
 * automations.js — lado Google, parte 2: gatilho onFormSubmit e lembrete diário (D-1).
 * Cada canal roda isolado (runActions): falha de um não derruba os outros, e o erro
 * vai para a aba "intake", para o e-mail do dono e para o log (console.error) — nunca some.
 * Idempotência: chave "sent:<intake_id>:<canal>:<tipo>" em Script Properties.
 */

function store_() {
  var p = PropertiesService.getScriptProperties();
  return {
    has: function (k) { return p.getProperty('sent:' + k) !== null; },
    set: function (k, v) { p.setProperty('sent:' + k, v); }
  };
}

/** "-0300" → {iso: "-03:00", minutes: -180}, no fuso do script. */
function tzOffset_() {
  var z = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'Z');
  var m = /^([+-])(\d{2})(\d{2})$/.exec(z);
  if (!m) throw new Error('offset de fuso inesperado: ' + JSON.stringify(z) + '; esperado ±HHMM');
  var sign = m[1] === '-' ? -1 : 1;
  return { iso: m[1] + m[2] + ':' + m[3], minutes: sign * (Number(m[2]) * 60 + Number(m[3])) };
}

/** FormResponse → {chave: valor}, com rótulo de escolha traduzido para o `value` do contrato. */
function readAnswers_(response, itemMap) {
  var answers = {};
  response.getItemResponses().forEach(function (ir) {
    var meta = itemMap[String(ir.getItem().getId())];
    if (!meta) return; // item adicionado à mão no Form, fora do contrato: ignorado de propósito
    var raw = ir.getResponse();
    var decode = function (label) { return meta.choices[label] !== undefined ? meta.choices[label] : label; };
    answers[meta.key] = Array.isArray(raw) ? raw.map(decode) : decode(raw);
  });
  return answers;
}

function intakeSheet_() {
  var id = PropertiesService.getScriptProperties().getProperty('SHEET_ID');
  var sheet = id && SpreadsheetApp.openById(id).getSheetByName('intake');
  if (!sheet) throw new Error('aba "intake" não encontrada (SHEET_ID=' + JSON.stringify(id) + '); rode criarFormulario* de novo');
  return sheet;
}

function whatsappCfg_() {
  var p = PropertiesService.getScriptProperties();
  return { provider: p.getProperty('WHATSAPP_PROVIDER') || 'generic', url: p.getProperty('WHATSAPP_URL'),
    token: p.getProperty('WHATSAPP_TOKEN'), instance: p.getProperty('WHATSAPP_INSTANCE'),
    session: p.getProperty('WHATSAPP_SESSION') };
}

function sendWhatsapp_(e164, message) {
  var req = buildWhatsappRequest(whatsappCfg_(), e164, message);
  var resp = UrlFetchApp.fetch(req.url, { method: 'post', contentType: 'application/json',
    payload: JSON.stringify(req.payload), headers: req.headers, muteHttpExceptions: true });
  var code = resp.getResponseCode();
  if (code >= 300) {
    throw new Error('HTTP ' + code + ' de ' + req.url.replace(/^(https?:\/\/[^/]+).*/, '$1') +
      ': ' + resp.getContentText().slice(0, 200) + '; esperado 2xx');
  }
  return 'http-' + code;
}

function createInvite_(show, intake, i18n) {
  var start = new Date(intake.scheduled_at);
  var minutes = show.logistics.recording_duration_minutes || 90;
  var end = new Date(start.getTime() + minutes * 60000);
  var location = intake.recording_mode === 'presencial'
    ? [addressLine(show.logistics.address), show.logistics.gps_hint].filter(Boolean).join(' — ')
    : i18n.messages.calendar_remote_location;
  var event = CalendarApp.getDefaultCalendar().createEvent(renderMessage('calendar_title', show, intake, i18n),
    start, end, { location: location, guests: intake.contacts.email, sendInvites: true,
      description: renderMessage('calendar_description', show, intake, i18n) });
  return event.getId();
}

function executors_(show, intake, i18n) {
  var to = intake.contacts.email;
  return {
    email: function (a) {
      if (a.kind === 'kit') {
        var md = renderKit(BUNDLE.kitTemplate, show, intake, i18n);
        MailApp.sendEmail(to, renderMessage('email_subject', show, intake, i18n), md, { htmlBody: mdToHtml(md), name: show.name });
      } else {
        MailApp.sendEmail(to, renderMessage('reminder_subject', show, intake, i18n),
          renderMessage('reminder_body', show, intake, i18n), { name: show.name });
      }
      return 'mail';
    },
    whatsapp: function (a) {
      return sendWhatsapp_(intake.contacts.whatsapp, renderMessage(a.kind === 'kit' ? 'whatsapp_kit' : 'reminder_body', show, intake, i18n));
    },
    calendar: function () { return createInvite_(show, intake, i18n); },
    owner: function (a) { return notifyOwner_(show, intake, i18n, a.results, a.dropped); }
  };
}

function notifyOwner_(show, intake, i18n, results, dropped) {
  var owner = Session.getEffectiveUser().getEmail();
  if (!owner) throw new Error('e-mail do dono indisponível (Session.getEffectiveUser().getEmail() vazio)');
  var body = 'intake_id: ' + intake.intake_id + '\nconvidado: ' + intake.guest.full_name +
    '\n\nEnvios:\n' + results.map(function (r) { return '- ' + r.key + ': ' + r.status + (r.error ? ' — ' + r.error : r.reason ? ' — ' + r.reason : ''); }).join('\n') +
    '\n\nDescartados (não guardados):\n' + (dropped.length ? dropped.map(function (d) { return '- ' + d.field + ': ' + d.reason; }).join('\n') : '- nenhum') +
    '\n\nJSON completo na aba "intake" da planilha de respostas.';
  MailApp.sendEmail(owner, renderMessage('owner_subject', show, intake, i18n), body);
  return 'owner';
}

function logErrors_(results) {
  results.filter(function (r) { return r.status === 'error'; }).forEach(function (r) {
    console.error('falha no envio ' + r.key + ': ' + r.error);
  });
}

/** Gatilho instalável (Form → ao enviar). e.response = FormResponse. */
function onFormSubmit(e) {
  if (!e || !e.response) {
    throw new Error('onFormSubmit sem e.response (recebido ' + JSON.stringify(e && Object.keys(e)) +
      '); esperado execução pelo gatilho instalado por criarFormulario*, não pelo botão Executar');
  }
  var show = loadShow_(), meta = loadMeta_(), props = PropertiesService.getScriptProperties();
  var i18n = selectLocale(BUNDLE, meta.locale, allowUnreviewed_());
  var answers = readAnswers_(e.response, JSON.parse(props.getProperty('FORM_ITEM_MAP')));
  var res = normalizeIntake(answers, { responseId: e.response.getId(), submittedAt: e.response.getTimestamp().toISOString(),
    variant: meta.variant, locale: meta.locale, jurisdiction: meta.jurisdiction, clauseId: meta.clause_id,
    textVersion: meta.text_version, offset: tzOffset_().iso,
    purposes: { sensitive: i18n.consent.sensitive_purpose, accessibility: i18n.consent.accessibility_purpose,
      voice_replica: i18n.consent.dub_replica_purpose }, localization: show.localization || null });
  var intake = res.intake, store = store_(), policy = guestPolicy_(intake.contacts.email);
  var results = runActions(planSubmitActions(intake, show, policy), executors_(show, intake, i18n), store);
  if (!policy.invited || policy.optedOut) results = [heldResult_(intake, policy)];
  results = results.concat(runActions([{ key: intake.intake_id + ':owner:notify', channel: 'owner', kind: 'notify',
    results: results, dropped: res.dropped }], executors_(show, intake, i18n), store));
  if (!store.has(intake.intake_id + ':record')) {
    intakeSheet_().appendRow([intake.intake_id, intake.submitted_at, JSON.stringify(intake), JSON.stringify(results), JSON.stringify(res.dropped)]);
    store.set(intake.intake_id + ':record', new Date().toISOString());
  }
  logErrors_(results);
  return results;
}

/** Gatilho diário: lembrete na véspera (D-1) para quem consentiu no canal. */
function lembreteDiario() {
  var show = loadShow_(), meta = loadMeta_(), store = store_(), tz = tzOffset_(), now = Date.now();
  var i18n = selectLocale(BUNDLE, meta.locale, allowUnreviewed_());
  var rows = intakeSheet_().getDataRange().getValues().slice(1);
  var all = [];
  rows.forEach(function (row) {
    var intake;
    try {
      intake = JSON.parse(row[2]);
    } catch (err) {
      console.error('linha da aba intake com JSON inválido (intake_id=' + JSON.stringify(row[0]) + '): ' + err.message);
      return;
    }
    var acts = planReminderActions(intake, show, now, tz.minutes, guestPolicy_(intake.contacts && intake.contacts.email));
    all = all.concat(runActions(acts, executors_(show, intake, i18n), store));
  });
  logErrors_(all);
  if (props_().getProperty('RETENCAO_AUTOMATICA') === 'true') aplicarRetencao(now);
  return all;
}

/** Quem o host convidou (enviarConvite) ou aprovou (confirmarIntake), e quem pediu SAIR. */
function guestPolicy_(email) {
  var e = String(email || '').trim().toLowerCase();
  return { invited: props_().getProperty('invited:' + e) !== null, optedOut: optOutList_().indexOf(e) >= 0 };
}

function markInvited_(email, how) {
  props_().setProperty('invited:' + String(email).trim().toLowerCase(), JSON.stringify({ by: how, at: new Date().toISOString() }));
}

function heldResult_(intake, policy) {
  return { key: intake.intake_id + ':guest', status: policy.optedOut ? 'skipped' : 'held',
    reason: policy.optedOut ? 'opt-out (OPTOUT_EMAILS)' : 'e-mail não convidado por enviarConvite; nada foi enviado ao' +
      ' convidado. Se for legítimo, rode confirmarIntake(' + JSON.stringify(intake.intake_id) + ')' };
}

/** Decisão do host para um intake retido: marca o e-mail como convidado e roda os envios dele. */
function confirmarIntake(intakeId) {
  var row = intakeSheet_().getDataRange().getValues().slice(1).filter(function (r) { return r[0] === intakeId; })[0];
  if (!row) throw new Error('confirmarIntake(' + JSON.stringify(intakeId) + '): intake não está na aba "intake"; esperado o intake_id do e-mail ao dono');
  var show = loadShow_(), meta = loadMeta_(), intake = JSON.parse(row[2]);
  var i18n = selectLocale(BUNDLE, meta.locale, allowUnreviewed_());
  markInvited_(intake.contacts.email, 'confirmarIntake');
  var results = runActions(planSubmitActions(intake, show, guestPolicy_(intake.contacts.email)), executors_(show, intake, i18n), store_());
  logErrors_(results);
  return results;
}

// ---------- Convite Oficial (primeiro envio; leva o link do formulário) ----------

function optOutList_() {
  var raw = PropertiesService.getScriptProperties().getProperty('OPTOUT_EMAILS');
  try {
    return raw ? JSON.parse(raw) : [];
  } catch (e) {
    throw new Error('OPTOUT_EMAILS não é JSON (' + e.message + '); início: ' + JSON.stringify(raw.slice(0, 40)) + '; esperado ["a@b.c", …]');
  }
}

/** Quem respondeu SAIR: o host roda registrarOptOut('email') e nenhum convite novo sai para ele. */
function registrarOptOut(email) {
  var e = String(email || '').trim().toLowerCase();
  if (!EMAIL_RE.test(e)) throw new Error('registrarOptOut(' + JSON.stringify(email) + '); esperado e-mail');
  var list = optOutList_();
  if (list.indexOf(e) < 0) list.push(e);
  PropertiesService.getScriptProperties().setProperty('OPTOUT_EMAILS', JSON.stringify(list));
  return list.length;
}

function sendInvitation_(mail) {
  var opts = { htmlBody: mail.html, name: mail.sender };
  if (mail.logo) {
    if (typeof logoBlobFromDrive_ !== 'function') {
      throw new Error('brand.logo.drive_file_id=' + JSON.stringify(mail.logo.drive_file_id) +
        ' exige o arquivo src/drive-logo.js (pede o escopo do Drive); esperado colar drive-logo.js ou usar brand.logo.url');
    }
    opts.inlineImages = {};
    opts.inlineImages[mail.logo.cid] = logoBlobFromDrive_(mail.logo.drive_file_id);
  }
  if (mail.ics) opts.attachments = [Utilities.newBlob(mail.ics, 'text/calendar', 'convite.ics')];
  MailApp.sendEmail(mail.to, mail.subject, mail.text, opts);
  return 'mail';
}

/**
 * O host chama (de uma função sua, ex.: em config.gs):
 *   enviarConvite({nome: 'Ana', email: 'ana@…', data: '2026-10-20T14:30:00-03:00', modo: 'presencial'}, 'essencial')
 * modo: 'presencial' | 'remoto' (+ link_remoto https). variante: a do formulário ativo (padrão).
 * Idempotente por convidado+data; respeita OPTOUT_EMAILS. Devolve {key, status, error?}.
 */
function enviarConvite(convidado, variante) {
  var show = loadShow_(), meta = loadMeta_(), formUrl = props_().getProperty('FORM_URL');
  var variant = variante || meta.variant;
  if (variant !== meta.variant) {
    throw new Error('variante ' + JSON.stringify(variant) + ' não é a do formulário ativo (' + JSON.stringify(meta.variant) +
      '); esperado ' + JSON.stringify(meta.variant) + ' ou rodar criarFormulario' + (variant === 'completo' ? 'Completo' : 'Essencial') + ' antes');
  }
  if (!formUrl) throw new Error('FORM_URL ausente; esperado rodar criarFormulario* (grava o link publicado)');
  var invitee = normalizeInvitee(convidado, show), key = invitationKey(invitee);
  if (optOutList_().indexOf(invitee.email.toLowerCase()) >= 0) return { key: key, status: 'skipped', reason: 'opt-out' };
  var i18n = selectLocale(BUNDLE, meta.locale, allowUnreviewed_());
  var mail = buildInvitationEmail(BUNDLE.invitationTemplate, show, invitee, i18n, { formUrl: formUrl, variant: variant });
  var res = runActions([{ key: key, channel: 'email', kind: 'convite' }], { email: function () { return sendInvitation_(mail); } }, store_())[0];
  if (res.status !== 'error') markInvited_(invitee.email, 'enviarConvite');   // libera o pós-formulário dele
  logErrors_([res]);
  console.log('convite ' + key + ': ' + res.status + (res.error ? ' — ' + res.error : ''));
  return res;
}

// ---------- Esquecer o titular (LGPD art. 18, VI) e retenção (CRITIC M5, DEBT-067, DEBT-075) ----------

/** Linhas (1-based, de baixo para cima) de `sheet` em que `match(row)` é verdadeiro; pula o cabeçalho. */
function rowsWhere_(sheet, match) {
  var rows = sheet.getDataRange().getValues(), out = [];
  for (var i = rows.length - 1; i >= 1; i--) if (match(rows[i])) out.push(i + 1);
  return out;
}

function deleteRows_(sheet, positions) {
  positions.forEach(function (p) { sheet.deleteRow(p); });   // já vêm de baixo para cima
  return positions.length;
}

/** Respostas do Form cujo intake_id é este (o id é derivado do responseId, sem volta: compara pelo slug). */
function deleteFormResponses_(intakeId) {
  var formId = props_().getProperty('FORM_ID');
  if (!formId) return { deleted: 0, note: 'FORM_ID ausente; apague a resposta à mão no Forms' };
  var form = FormApp.openById(formId), n = 0;
  form.getResponses().forEach(function (r) {
    if (slugId('in-', r.getId()) === intakeId) { form.deleteResponse(r.getId()); n++; }
  });
  return { deleted: n };
}

/** A aba de respostas ligada ao Form NÃO perde a linha quando a resposta é apagada: casa pelo e-mail. */
function deleteLinkedRows_(email) {
  var ss = SpreadsheetApp.openById(props_().getProperty('SHEET_ID')), n = 0;
  var e = String(email || '').trim().toLowerCase();
  if (!e) return { deleted: 0, note: 'intake sem e-mail; revise a aba de respostas do Form à mão' };
  ss.getSheets().filter(function (s) { return s.getFormUrl && s.getFormUrl(); }).forEach(function (s) {
    n += deleteRows_(s, rowsWhere_(s, function (row) {
      return row.some(function (c) { return String(c).trim().toLowerCase() === e; });
    }));
  });
  return { deleted: n };
}

/** Chaves de Script Properties do titular: sent:<intake_id>:*, sent:convite:<email>:*, invited:<email>. */
function deleteGuestKeys_(intakeId, email) {
  var p = props_(), e = String(email || '').trim().toLowerCase();
  var mine = p.getKeys().filter(function (k) {
    return k.indexOf('sent:' + intakeId + ':') === 0 || (e && (k === 'invited:' + e || k.indexOf('sent:convite:' + e + ':') === 0));
  });
  mine.forEach(function (k) { p.deleteProperty(k); });
  return mine.length;
}

/**
 * esquecerTitular('in-…'): apaga a linha da aba intake, a resposta no Forms, a linha da aba de
 * respostas ligada e as chaves do titular. OPTOUT_EMAILS fica (é o registro da oposição dele).
 * Rode junto com `memory forget` no workspace local. Devolve o relatório com o denominador.
 */
function esquecerTitular(intakeId) {
  var sheet = intakeSheet_(), email = null;
  var hit = rowsWhere_(sheet, function (r) { return r[0] === intakeId; });
  if (!hit.length) throw new Error('esquecerTitular(' + JSON.stringify(intakeId) + '): intake não está na aba "intake"; esperado o intake_id do e-mail ao dono');
  try { email = JSON.parse(sheet.getDataRange().getValues()[hit[0] - 1][2]).contacts.email; } catch (err) {
    console.error('intake ' + intakeId + ' com JSON ilegível (' + err.message + '); apagando só pelo intake_id');
  }
  var report = { intake_id: intakeId, form_responses: deleteFormResponses_(intakeId), linked_rows: deleteLinkedRows_(email),
    intake_rows: deleteRows_(sheet, hit), keys: deleteGuestKeys_(intakeId, email) };
  console.log('esquecerTitular: ' + JSON.stringify(report));
  return report;
}

/**
 * Retenção: esquece todo intake cuja gravação (ou envio, sem data) passou de retention_days_after_publish.
 * ponytail: conta da data de GRAVAÇÃO, não da publicação (a planilha não sabe quando publicou), então
 * apaga mais cedo que o prazo declarado, nunca mais tarde. Se o host precisar do prazo exato, gravar
 * published_at na aba intake e contar dele. Só roda no gatilho diário com RETENCAO_AUTOMATICA=true.
 */
function aplicarRetencao(nowMs) {
  var show = loadShow_(), days = show.retention_days_after_publish === undefined ? 90 : show.retention_days_after_publish;
  var limit = (nowMs || Date.now()) - days * 86400000, expired = [];
  intakeSheet_().getDataRange().getValues().slice(1).forEach(function (row) {
    var when = NaN;
    try { var it = JSON.parse(row[2]); when = Date.parse(it.scheduled_at || it.submitted_at); } catch (err) {
      console.error('retenção: linha ' + JSON.stringify(row[0]) + ' com JSON inválido (' + err.message + '); usando submitted_at da coluna B');
    }
    if (isNaN(when)) when = Date.parse(row[1]);
    if (when < limit) expired.push(row[0]);
  });
  return expired.map(esquecerTitular);
}
