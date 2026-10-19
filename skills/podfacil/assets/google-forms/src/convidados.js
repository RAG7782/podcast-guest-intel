/**
 * convidados.js — o lado legível para o dono do programa (leigo):
 *   1. o aviso por e-mail quando um convidado responde (HTML com a marca, em linguagem simples);
 *   2. a aba "Convidados" da planilha: uma linha por convidado, sem JSON, com o link do briefing.
 * A aba "intake" continua sendo o registro técnico (fica oculta). As linhas se ligam pela última coluna,
 * "Código do registro" (intake_id), nunca pela posição: retenção, retidos e exclusões mudam a ordem.
 * Parte pura (sem Google) no topo, exportada para os testes; parte Google embaixo.
 */

if (typeof module !== 'undefined') {
  var actions4_ = require('./actions.js'), invitation4_ = require('./invitation.js');
  var escapeHtml = actions4_.escapeHtml, formatScheduled = actions4_.formatScheduled;
  var resolveBrand = invitation4_.resolveBrand;
}

// ---------- puro ----------

/** Texto digitado pelo convidado nunca vira fórmula na planilha (=, +, -, @ no início ficam como texto). */
function cellText(v) {
  return typeof v === 'string' && /^[=+\-@]/.test(v) ? "'" + v : v;
}

function fillOwner_(tpl, view) {
  return String(tpl).replace(/\{\{\s*(\w+)\s*\}\}/g, function (m, k) {
    if (!(k in view)) throw new Error('placeholder {{' + k + '}} sem valor em texto do aviso; esperado ' + JSON.stringify(Object.keys(view)));
    return view[k] === null || view[k] === undefined ? '' : String(view[k]);
  });
}

/** Rótulo de um envio pela chave "<intake>:<canal>:<tipo>" (ou "<intake>:automacoes"). */
function sendLabel(key, t) {
  var parts = String(key || '').split(':'), last = parts.slice(-2).join(':');
  if (parts[parts.length - 1] === 'automacoes') return t.sends.automations;
  if (parts[parts.length - 1] === 'guest') return t.sends.guest;
  var map = { 'email:kit': t.sends.kit_email, 'whatsapp:kit': t.sends.kit_whatsapp, 'calendar:invite': t.sends.calendar };
  return map[last] || fillOwner_(t.sends.other, { key: parts.slice(-2).join(' ') });
}

/** Envios em frases simples: [{ok: true|false|null, text}]. O aviso ao dono não entra (é o próprio aviso). */
function ownerSendLines(results, i18n) {
  var t = i18n.owner;
  return (results || []).filter(function (r) { return !/:owner:/.test(r.key || ''); }).map(function (r) {
    var label = sendLabel(r.key, t);
    if (r.status === 'sent') return { ok: true, text: fillOwner_(t.status.sent, { label: label }) };
    if (r.status === 'held') return { ok: null, text: fillOwner_(t.status.held, { label: label }) };
    if (r.status === 'skipped') return { ok: null, text: fillOwner_(t.status.skipped, { label: label }) };
    return { ok: false, text: fillOwner_(t.status.error, { label: label }) };
  });
}

/** Descartes em linguagem leiga: [{action: bool, text}]. action = o dono precisa fazer algo. */
function ownerAttention(dropped, i18n) {
  var t = i18n.owner.drops, out = [];
  (dropped || []).forEach(function (d) {
    var f = d.field;
    if (f === 'contacts.whatsapp') {
      var end = (/\*+(\d{2,4})/.exec(String(d.reason)) || [])[1];
      out.push({ action: true, text: fillOwner_(t.whatsapp, { end: end ? fillOwner_(t.whatsapp_end, { digits: end }) : '' }) });
    } else if (f === 'automation_consents.whatsapp') {
      // já coberto pelo item do número
    } else if (f === 'accessibility' || f === 'scheduled_at') {
      out.push({ action: true, text: t[f] });
    } else if (f.indexOf('check.') === 0 && t[f]) {   // revisarIntake: nada foi descartado, mas o dono confere
      out.push({ action: true, text: fillOwner_(t[f], checkVars(d, i18n.locale)) });
    } else if (t[f] && ['sensitive', 'previous_interviews', 'links', 'key_ideas'].indexOf(f) >= 0) {
      out.push({ action: false, text: t[f] });
    } else {
      out.push({ action: false, text: fillOwner_(t.other, { field: f }) });
    }
  });
  return out;
}

/** Variáveis das checagens (check.*): sempre as quatro, para o texto de qualquer idioma achar a sua. */
function checkVars(d, locale) {
  var v = d.vars || {};
  return { hora: v.hora || '', data: v.data ? formatScheduled(v.data, locale) : '', agora: v.agora || '', antes: v.antes || '' };
}

function ownerDate(iso, locale, t) {
  return iso ? formatScheduled(iso, locale) : t.date_tbd;
}

/** [[rótulo, valor]] do resumo do convidado; só o que veio preenchido. */
function ownerSummary(intake, i18n) {
  var t = i18n.owner, l = t.labels, g = intake.guest || {}, name = g.full_name || g.preferred_name || '';
  var first = String(name).split(/\s+/)[0];
  var nameCell = name + (g.preferred_name && g.preferred_name !== name && g.preferred_name !== first
    ? ' (' + fillOwner_(l.prefers, { name: g.preferred_name }) + ')' : '');
  return [
    [l.name, nameCell],
    [l.role, g.role_title],
    [l.bio, intake.bio && intake.bio.short],
    [l.ideas, (intake.key_ideas || []).join(' · ')],
    [l.recording, (t.mode[intake.recording_mode] || intake.recording_mode) + ' · ' + ownerDate(intake.scheduled_at, i18n.locale, t)],
    [l.email, intake.contacts && intake.contacts.email],
    [l.whatsapp, intake.contacts && intake.contacts.whatsapp]
  ].filter(function (p) { return p[1]; });
}

/**
 * Aviso ao dono: {html, text}. link = endereço da linha do convidado na aba Convidados (ou da planilha).
 * Todo dado do convidado entra escapado no HTML.
 */
function buildOwnerEmail(show, intake, i18n, results, dropped, link) {
  var t = i18n.owner, g = intake.guest || {}, name = g.preferred_name || g.full_name || '';
  var sends = ownerSendLines(results, i18n), att = ownerAttention(dropped, i18n);
  var acts = att.filter(function (a) { return a.action; }), notes = att.filter(function (a) { return !a.action; });
  var summary = ownerSummary(intake, i18n);
  var c, e = escapeHtml, font = 'Georgia, serif';
  try { c = resolveBrand(show).colors; } catch (err) {   // marca inválida não pode calar o aviso: cores neutras
    c = resolveBrand({ name: show.name, controller: show.controller }).colors;
  }
  var mark = function (ok) { return ok === true ? '✅' : ok === null ? '➖' : '⚠️'; };
  var li = function (ok, text) { return '<li style="margin:0 0 8px;list-style:none;font-size:15px;">' + mark(ok) + '&nbsp; ' + e(text) + '</li>'; };
  var cap = function (text) {
    return '<p style="font-size:13px;letter-spacing:1px;text-transform:uppercase;color:' + c.accent + ';margin:0 0 8px;">' + e(text) + '</p>';
  };
  var html = '<div style="background:' + c.background + ';padding:24px 12px;font-family:' + font + ';color:' + c.text + ';">' +
    '<table role="presentation" width="100%" style="max-width:600px;margin:0 auto;background:#ffffff;border-collapse:collapse;">' +
    '<tr><td style="background:' + c.primary + ';color:' + c.on_primary + ';padding:20px 24px;font-size:20px;">' + e(show.name) + '</td></tr>' +
    '<tr><td style="padding:24px;">' +
    '<p style="font-size:20px;margin:0 0 6px;color:' + c.primary + ';"><strong>' + e(fillOwner_(t.headline, { name: name })) + '</strong></p>' +
    '<p style="font-size:15px;margin:0 0 20px;">' + e(t.lead) + '</p>' + cap(t.happened) +
    '<ul style="padding:0;margin:0 0 20px;">' + li(true, t.form_received) +
    sends.map(function (s) { return li(s.ok, s.text); }).join('') + '</ul>' +
    (acts.length ? '<div style="background:#FFF4E5;border-left:3px solid #B26A00;padding:12px 16px;margin:0 0 20px;">' +
      '<p style="margin:0 0 8px;font-size:15px;"><strong>' + e(t.attention) + '</strong></p>' +
      acts.map(function (a) { return '<p style="margin:0 0 6px;font-size:15px;">• ' + e(a.text) + '</p>'; }).join('') +
      '<p style="margin:10px 0 0;font-size:13px;">' + e(t.confirm_hint) + '</p></div>' : '') +
    cap(t.summary) + '<table role="presentation" style="border-collapse:collapse;margin:0 0 24px;">' +
    summary.map(function (p) {
      return '<tr><td style="padding:6px 12px 6px 0;color:' + c.accent + ';font-size:13px;vertical-align:top;white-space:nowrap;">' + e(p[0]) +
        '</td><td style="padding:6px 0;font-size:15px;color:' + c.text + ';">' + e(p[1]) + '</td></tr>';
    }).join('') + '</table>' +
    (link ? '<table role="presentation" align="center" style="margin:0 auto 12px;"><tr><td style="background:' + c.primary + ';border-radius:4px;">' +
      '<a href="' + e(link) + '" style="display:inline-block;padding:12px 22px;color:' + c.on_primary + ';text-decoration:none;font-size:15px;">' +
      e(t.button) + '</a></td></tr></table>' : '') +
    '<p style="font-size:14px;text-align:center;margin:0 0 20px;">' + e(fillOwner_(t.next_step, { name: name })) + '</p>' +
    (notes.length ? '<p style="font-size:12px;color:#6b6257;margin:0 0 4px;">' + e(t.notes) + ':</p>' +
      notes.map(function (a) { return '<p style="font-size:12px;color:#6b6257;margin:0 0 4px;">• ' + e(a.text) + '</p>'; }).join('') : '') +
    '<p style="font-size:11px;color:#8a8178;margin:16px 0 0;">' + e(fillOwner_(t.record_code, { id: intake.intake_id })) + '</p>' +
    '</td></tr></table></div>';
  var text = fillOwner_(t.headline, { name: name }) + '\n\n' + t.happened + ':\n- ' + t.form_received + '\n' +
    sends.map(function (s) { return '- ' + s.text; }).join('\n') +
    (acts.length ? '\n\n' + t.attention + ':\n' + acts.map(function (a) { return '- ' + a.text; }).join('\n') + '\n' + t.confirm_hint : '') +
    '\n\n' + t.summary + ':\n' + summary.map(function (p) { return p[0] + ': ' + p[1]; }).join('\n') +
    (link ? '\n\n' + fillOwner_(t.full_answers, { url: link }) : '') + '\n\n' + fillOwner_(t.next_step, { name: name }) +
    (notes.length ? '\n\n' + t.notes + ':\n' + notes.map(function (a) { return '- ' + a.text; }).join('\n') : '') +
    '\n\n' + fillOwner_(t.record_code, { id: intake.intake_id });
  return { html: html, text: text };
}

// ---------- confirmação ao convidado (decisão 3.1: e-mail pronto pelo MailApp, sem acesso ao Gmail) ----------

/** O que o convidado pode corrigir. O que é só do dono (link ignorado, 4ª ideia) e o dado sensível ficam de fora. */
var GUEST_CONFIRM_FIELDS = ['scheduled_at', 'check.past', 'check.time_odd', 'contacts.whatsapp', 'check.whatsapp_mismatch',
  'accessibility'];

/** Pontos a confirmar, na ordem acima, sem repetir: [texto]. */
function guestConfirmItems(dropped, i18n) {
  var g = i18n.guest_confirm, by = {};
  (dropped || []).forEach(function (d) { if (GUEST_CONFIRM_FIELDS.indexOf(d.field) >= 0 && !by[d.field]) by[d.field] = d; });
  return GUEST_CONFIRM_FIELDS.filter(function (f) { return by[f]; }).map(function (f) {
    var d = by[f], vars = checkVars(d, i18n.locale), end = (/\*+(\d{2,4})/.exec(String(d.reason)) || [])[1];
    vars.end = f === 'contacts.whatsapp' && end ? fillOwner_(g.end, { digits: end }) : '';
    return fillOwner_(g.items[f], vars);
  });
}

/**
 * E-mail ao convidado pedindo para confirmar o que veio com problema (ou, sem problema, os dados principais).
 * -> {subject, text, html, itens}. Todo dado do convidado entra escapado no HTML; do WhatsApp, só o final.
 */
function buildGuestConfirmation(show, intake, dropped, i18n) {
  var g = i18n.guest_confirm, t = i18n.owner, items = guestConfirmItems(dropped, i18n), e = escapeHtml;
  var gu = intake.guest || {}, ct = intake.contacts || {}, v = { show: show.name, nome: gu.preferred_name || gu.full_name || '' };
  var resumo = [[g.labels.recording, (t.mode[intake.recording_mode] || intake.recording_mode || '') + ' · ' +
    ownerDate(intake.scheduled_at, i18n.locale, t)]];
  if (ct.whatsapp) resumo.push([g.labels.whatsapp, fillOwner_(g.whatsapp_end, { digits: ct.whatsapp.slice(-4) })]);
  var intro = fillOwner_(items.length ? g.intro : g.intro_none, v), c;
  try { c = resolveBrand(show).colors; } catch (err) { c = resolveBrand({ name: show.name, controller: show.controller }).colors; }
  var text = fillOwner_(g.greeting, v) + '\n\n' + intro + '\n\n' +
    (items.length ? items.map(function (x, i) { return (i + 1) + '. ' + x; }).join('\n') + '\n\n' : '') +
    g.summary + ':\n' + resumo.map(function (p) { return '- ' + p[0] + ': ' + p[1]; }).join('\n') + '\n\n' +
    g.closing + '\n\n' + fillOwner_(g.signature, v);
  var html = '<div style="background:' + c.background + ';padding:24px 12px;font-family:Georgia, serif;color:' + c.text + ';">' +
    '<table role="presentation" width="100%" style="max-width:600px;margin:0 auto;background:#ffffff;border-collapse:collapse;">' +
    '<tr><td style="background:' + c.primary + ';color:' + c.on_primary + ';padding:20px 24px;font-size:20px;">' + e(show.name) + '</td></tr>' +
    '<tr><td style="padding:24px;font-size:15px;line-height:1.5;">' +
    '<p style="margin:0 0 12px;">' + e(fillOwner_(g.greeting, v)) + '</p><p style="margin:0 0 16px;">' + e(intro) + '</p>' +
    (items.length ? '<ol style="margin:0 0 20px;padding-left:20px;">' +
      items.map(function (x) { return '<li style="margin:0 0 8px;">' + e(x) + '</li>'; }).join('') + '</ol>' : '') +
    '<p style="font-size:13px;letter-spacing:1px;text-transform:uppercase;color:' + c.accent + ';margin:0 0 8px;">' + e(g.summary) + '</p>' +
    '<table role="presentation" style="border-collapse:collapse;margin:0 0 20px;">' + resumo.map(function (p) {
      return '<tr><td style="padding:4px 12px 4px 0;color:' + c.accent + ';font-size:13px;white-space:nowrap;">' + e(p[0]) +
        '</td><td style="padding:4px 0;">' + e(p[1]) + '</td></tr>';
    }).join('') + '</table>' +
    '<p style="margin:0 0 16px;">' + e(g.closing) + '</p><p style="margin:0;">' + e(fillOwner_(g.signature, v)) + '</p>' +
    '</td></tr></table></div>';
  return { subject: fillOwner_(g.subject, v), text: text, html: html, itens: items };
}

/** Linha da aba Convidados (sem a coluna Briefing preenchida; o intake_id vai na última). held = retido. */
function convidadoRow(intake, results, dropped, i18n, held) {
  var t = i18n.owner, s = i18n.sheet, ch = (i18n.form.choices && i18n.form.choices.preferred_channel) || {};
  var yn = (i18n.form.choices && i18n.form.choices.yes_no) || { yes: 'yes', no: 'no' };
  var g = intake.guest || {}, c = intake.contacts || {}, ctr = intake.controversies || {};
  var list = function (a) { return (a || []).join('\n'); };
  var att = ownerAttention(dropped, i18n).filter(function (a) { return a.action; }).map(function (a) { return '• ' + a.text; });
  if (held) att.unshift('• ' + t.held);
  return [
    intake.submitted_at ? formatScheduled(isoLocal(intake.submitted_at, intake), i18n.locale) : '',
    g.full_name || '', g.preferred_name || '', g.role_title || '', (intake.bio && intake.bio.short) || '',
    list(intake.key_ideas), list(intake.wants_to_promote), list(ctr.accepts),
    list((ctr.declines || []).concat(intake.off_limits_topics || [])),
    ownerDate(intake.scheduled_at, i18n.locale, t), t.mode[intake.recording_mode] || intake.recording_mode || '',
    c.email || '', c.whatsapp || s.not_informed, ch[intake.preferred_channel] || intake.preferred_channel || '',
    intake.wants_prepublication_review ? yn.yes : yn.no,
    ownerSendLines(results, i18n).map(function (l) { return (l.ok === true ? '✅ ' : l.ok === null ? '➖ ' : '⚠️ ') + l.text; }).join('\n'),
    att.join('\n') || s.none, '', intake.intake_id
  ].map(cellText);
}

/** submitted_at vem em UTC ("…Z"); passa para o fuso do scheduled_at (ou -03:00) antes de formatar. */
function isoLocal(utcIso, intake) {
  var off = (/([+-]\d{2}):?(\d{2})$/.exec(intake.scheduled_at || '') || [null, '-03', '00']);
  var mins = (off[1][0] === '-' ? -1 : 1) * (Math.abs(Number(off[1])) * 60 + Number(off[2]));
  var d = new Date(Date.parse(utcIso) + mins * 60000).toISOString();
  return d.slice(0, 19) + off[1] + ':' + off[2];
}

/** Id do Google Docs dentro de um link ou de uma fórmula =HYPERLINK(...). */
function docIdFromLink(value) {
  return (/docs\.google\.com\/document\/d\/([\w-]{20,})/.exec(String(value || '')) || [])[1] || null;
}

// ---------- Google ----------

/** Aba Convidados existente (pelo id gravado, ou pelo nome com o cabeçalho do PodFácil), ou null. */
function convidadosSheetExistente_(i18n) {
  var ss = intakeSheet_().getParent(), id = props_().getProperty('CONVIDADOS_SHEET_ID');
  var found = id && ss.getSheets().filter(function (sh) { return String(sh.getSheetId()) === id; })[0];
  if (found) return found;
  var t = (i18n || selectLocale(BUNDLE, loadMeta_().locale, allowUnreviewed_())).sheet;
  var byName = ss.getSheetByName(t.tab);
  if (byName && byName.getLastColumn() >= t.columns.length &&
      byName.getRange(1, 1, 1, t.columns.length).getValues()[0][t.columns.length - 1] === t.columns[t.columns.length - 1]) {
    props_().setProperty('CONVIDADOS_SHEET_ID', String(byName.getSheetId()));   // id perdido: adota a aba certa
    return byName;
  }
  return null;
}

/** Aba Convidados (cria na primeira vez, como 1ª aba; o id fica em CONVIDADOS_SHEET_ID). */
function convidadosSheet_(i18n) {
  var t = (i18n || selectLocale(BUNDLE, loadMeta_().locale, allowUnreviewed_())).sheet;
  var found = convidadosSheetExistente_(i18n);
  if (found) return found;
  var ss = intakeSheet_().getParent(), cols = t.columns;
  var name = ss.getSheetByName(t.tab) ? t.tab + ' (PodFácil)' : t.tab;   // não briga com uma aba do dono de mesmo nome
  var sh = ss.insertSheet(name, 0), brand;
  try { brand = resolveBrand(loadShow_()).colors; } catch (err) { brand = { primary: '#1F2937', on_primary: '#FFFFFF' }; }
  sh.getRange(1, 1, 1, cols.length).setValues([cols]).setFontWeight('bold').setBackground(brand.primary)
    .setFontColor(brand.on_primary).setWrap(true).setVerticalAlignment('middle');
  sh.setFrozenRows(1);
  sh.setFrozenColumns(2);
  sh.setColumnWidths(1, cols.length, 200);
  sh.setColumnWidth(1, 140);
  sh.setColumnWidth(5, 340);
  sh.setColumnWidth(16, 260);
  sh.setColumnWidth(17, 320);
  sh.setColumnWidth(cols.length, 120);
  props_().setProperty('CONVIDADOS_SHEET_ID', String(sh.getSheetId()));
  return sh;
}

/**
 * Colunas do Código do registro e do Briefing, achadas pelo CABEÇALHO (o dono pode acrescentar colunas à direita
 * ou reordenar); sem o cabeçalho, as posições do PodFácil (penúltima e última das colunas dele).
 */
function convidadosCols_(sh, i18n) {
  var cols = i18n.sheet.columns, n = cols.length, width = Math.max(sh.getLastColumn(), n);
  var head = sh.getRange(1, 1, 1, width).getValues()[0];
  var id = head.indexOf(cols[n - 1]) + 1, briefing = head.indexOf(cols[n - 2]) + 1;
  return { n: n, id: id || n, briefing: briefing || n - 1 };
}

/** Linhas (1-based) do convidado, pelo intake_id. [] = não está. */
function convidadoRows_(sh, cc, intakeId) {
  var last = sh.getLastRow(), out = [];
  if (last < 2) return out;
  sh.getRange(2, cc.id, last - 1, 1).getValues().forEach(function (r, i) { if (r[0] === intakeId) out.push(i + 2); });
  return out;
}

/** Link da célula do briefing: fórmula =HYPERLINK, link de texto (Ctrl+K), ou o próprio texto. */
function briefingLink_(range) {
  var f = range.getFormula();
  if (f) return f;
  try {
    var rt = range.getRichTextValue();
    if (rt) {
      if (rt.getLinkUrl()) return rt.getLinkUrl();
      var runs = rt.getRuns ? rt.getRuns() : [];
      for (var i = 0; i < runs.length; i++) if (runs[i].getLinkUrl()) return runs[i].getLinkUrl();
    }
  } catch (err) { /* célula sem texto rico */ }
  return String(range.getValue() || '');
}

/** Escreve a linha SEM tocar na célula do briefing (preserva link, fórmula ou chip que o dono pôs lá). */
function writeConvidadoRow_(sh, cc, at, row) {
  var n = cc.n;
  sh.getRange(at, 1, 1, n - 2).setValues([row.slice(0, n - 2)]);
  sh.getRange(at, cc.id).setValues([[row[n - 1]]]);
  if (cc.briefing !== n - 1) sh.getRange(at, n - 1).setValues([['']]);   // coluna movida: a posição padrão fica vazia
  sh.getRange(at, 1, 1, n).setWrap(true).setVerticalAlignment('top');
}

/** Grava (ou atualiza) a linha do convidado, sob o lock do script. Devolve o nº da linha. */
function registrarConvidado_(intake, results, dropped, i18n, held) {
  return withScriptLock_(function () {
    var sh = convidadosSheet_(i18n), cc = convidadosCols_(sh, i18n);
    var row = convidadoRow(intake, results, dropped, i18n, held), at = convidadoRows_(sh, cc, intake.intake_id)[0];
    if (!at) at = sh.getLastRow() + 1;
    writeConvidadoRow_(sh, cc, at, row);
    return at;
  });
}

/** Endereço da linha do convidado (para o botão do aviso). */
function convidadoLink_(row) {
  var sh = convidadosSheet_();
  return sh.getParent().getUrl() + '#gid=' + sh.getSheetId() + '&range=A' + row;
}

/** Nunca derruba o fluxo do envio: a aba legível é conveniência; o registro técnico é a aba intake. */
function registrarConvidadoSeguro_(intake, results, dropped, i18n, held) {
  try {
    return registrarConvidado_(intake, results, dropped, i18n, held);
  } catch (err) {
    console.error('aba Convidados: ' + maskEmails_(err.message));
    return 0;
  }
}

/**
 * Esquecer: tira a(s) linha(s) do convidado da aba Convidados e manda o briefing para a lixeira se o PodFácil o criou,
 * se for da conta que roda o script e se não estiver ligado a outro convidado; senão, pendência com o link (decisão 4.1).
 * Não cria a aba. {linhas, briefing_docs, pendencias}.
 */
function removerConvidado_(intakeId) {
  var out = { linhas: 0, briefing_docs: 0, pendencias: [] };
  var meta = loadMeta_(), i18n = selectLocale(BUNDLE, meta.locale, allowUnreviewed_()), sh = convidadosSheetExistente_(i18n);
  if (!sh) return out;
  var cc = convidadosCols_(sh, i18n), rows = convidadoRows_(sh, cc, intakeId);
  if (!rows.length) {
    out.pendencias.push('Aba ' + i18n.sheet.tab + ': nenhuma linha com o código ' + intakeId + '; confira se sobrou algo dele à mão');
    return out;
  }
  rows.slice().reverse().forEach(function (at) {   // de baixo para cima: apagar não desloca as próximas
    var link = briefingLink_(sh.getRange(at, cc.briefing)), docId = docIdFromLink(link);
    if (docId) {
      try {   // Drive só com drive.file (drive.js): o PodFácil apaga o que ele criou; o resto vira pendência com link
        var doc = 'https://docs.google.com/document/d/' + docId + '/edit';
        var trash = convidadoOutrasLinhasComDoc_(sh, cc, docId, intakeId) ? 'shared' : driveTrash_(docId);
        if (trash === 'trashed') out.briefing_docs++;
        else if (trash === 'shared') out.pendencias.push('Briefing ' + docId + ' também está ligado a outro convidado; não foi para a lixeira');
        else if (trash === 'not_mine') out.pendencias.push('Briefing ' + docId + ' é de outra conta; peça ao dono para apagar');
        else out.pendencias.push('Briefing: mande para a lixeira à mão (Arquivo > Mover para a lixeira), o PodFácil só apaga o que ele mesmo criou: ' + doc);
      } catch (err) {
        out.pendencias.push('Briefing no Google Drive (' + docId + ') não foi para a lixeira; apague à mão');
        console.error('briefing de ' + intakeId + ': ' + maskEmails_(err.message));
      }
    } else if (link) {
      out.pendencias.push('Briefing com um link que não é de Google Docs; apague o documento à mão');
    }
    try { sh.deleteRow(at); out.linhas++; } catch (err) {
      sh.getRange(at, 1, 1, sh.getLastColumn()).clearContent();   // última linha não congelada: limpa em vez de apagar
      out.linhas++;
    }
  });
  return out;
}

function convidadoOutrasLinhasComDoc_(sh, cc, docId, intakeId) {
  var last = sh.getLastRow();
  if (last < 2) return false;
  var ids = sh.getRange(2, cc.id, last - 1, 1).getValues();
  for (var i = 0; i < ids.length; i++) {
    if (ids[i][0] !== intakeId && docIdFromLink(briefingLink_(sh.getRange(i + 2, cc.briefing))) === docId) return true;
  }
  return false;
}

/** Refaz a aba Convidados a partir da aba intake. Monta tudo antes de apagar: uma linha ruim não esvazia a aba. */
function reconstruirAbaConvidados() {
  var intake = intakeSheet_(), ss = intake.getParent(), meta = loadMeta_();
  var i18n = selectLocale(BUNDLE, meta.locale, allowUnreviewed_()), sh = convidadosSheet_(i18n), store = store_();
  var cc = convidadosCols_(sh, i18n), briefing = {};
  var last = sh.getLastRow();
  for (var r = 2; r <= last; r++) {   // guarda o briefing de cada código: fórmula, ou o texto rico com o link
    var id = sh.getRange(r, cc.id).getValue(), cell = sh.getRange(r, cc.briefing);
    if (!id) continue;
    var f = cell.getFormula();
    if (f) briefing[id] = { formula: f };
    else if (cell.getValue()) briefing[id] = { rich: cell.getRichTextValue() };
  }
  var src = intake.getLastRow() > 1 ? intake.getRange(2, 1, intake.getLastRow() - 1, 5).getValues() : [], built = [];
  src.forEach(function (v) {
    try {
      var it = JSON.parse(v[2]);
      built.push({ id: it.intake_id, row: convidadoRow(it, JSON.parse(v[3] || '[]'), JSON.parse(v[4] || '[]'), i18n, !admittedRow_(v, store)) });
    } catch (err) {
      console.error('reconstruir: linha ' + JSON.stringify(v[0]) + ' ilegível (' + maskEmails_(err.message) + '); pulada');
    }
  });
  if (last > 1) sh.getRange(2, 1, last - 1, Math.max(sh.getLastColumn(), cc.n)).clearContent();
  built.forEach(function (b, i) {
    writeConvidadoRow_(sh, cc, i + 2, b.row);
    var keep = briefing[b.id], cell = sh.getRange(i + 2, cc.briefing);
    if (keep && keep.formula) cell.setFormula(keep.formula);
    else if (keep && keep.rich) cell.setRichTextValue(keep.rich);
  });
  intake.hideSheet();
  ss.setActiveSheet(sh);
  ss.moveActiveSheet(1);
  console.log('aba Convidados: ' + built.length + ' convidado(s)');
  return built.length;
}

/** Reenvia o aviso ao dono de um intake (ou do último, sem argumento). Útil para testar o e-mail. */
function reenviarAviso(intakeId) {
  var rows = intakeSheet_().getDataRange().getValues().slice(1);
  var v = intakeId ? rows.filter(function (r) { return r[0] === intakeId; })[0] : rows[rows.length - 1];
  if (!v) throw new Error('reenviarAviso(' + JSON.stringify(intakeId) + '): intake não está na aba "intake"; esperado o código do registro');
  var show = loadShow_(), i18n = selectLocale(BUNDLE, loadMeta_().locale, allowUnreviewed_()), it = JSON.parse(v[2]);
  var at = 0;
  try { var sh = convidadosSheetExistente_(i18n); if (sh) at = convidadoRows_(sh, convidadosCols_(sh, i18n), it.intake_id)[0] || 0; } catch (err) { at = 0; }
  notifyOwner_(show, it, i18n, JSON.parse(v[3] || '[]'), JSON.parse(v[4] || '[]'), at);
  return v[0];
}

if (typeof module !== 'undefined') {
  module.exports = { cellText: cellText, ownerSendLines: ownerSendLines, ownerAttention: ownerAttention,
    ownerSummary: ownerSummary, buildOwnerEmail: buildOwnerEmail, convidadoRow: convidadoRow, isoLocal: isoLocal,
    guestConfirmItems: guestConfirmItems, buildGuestConfirmation: buildGuestConfirmation, checkVars: checkVars,
    docIdFromLink: docIdFromLink };
}
