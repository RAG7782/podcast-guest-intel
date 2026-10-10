/**
 * invitation.js — LÓGICA PURA do Convite Oficial (primeiro envio ao convidado, com o link do
 * formulário). Marca do programa vem de show-profile.brand; textos de i18n.invitation; a versão
 * texto puro vem de assets/templates/guest-invitation-official.md (BUNDLE.invitationTemplate).
 * Todo valor vindo de usuário (convidado, show-profile) é escapado antes de entrar no HTML.
 */
if (typeof module !== 'undefined') {
  var core3_ = require('./core.js'), actions3_ = require('./actions.js'), intake3_ = require('./intake.js');
  var renderTemplate = core3_.renderTemplate, stripDocComment = core3_.stripDocComment;
  var resolveController = core3_.resolveController, escapeHtml = actions3_.escapeHtml;
  var formatScheduled = actions3_.formatScheduled, addressLine = actions3_.addressLine;
  var EMAIL_RE = intake3_.EMAIL_RE;
}

var HEX_RE = /^#[0-9A-Fa-f]{6}$/;
var HTTPS_RE = /^https:\/\/\S+$/;
var DEFAULT_COLORS = { primary: '#1F2937', background: '#FFFFFF', text: '#1F2937' };
var LOGO_CID = 'showlogo';

// ---------- contraste (WCAG 2.2, SC 1.4.3) ----------

function relativeLuminance(hex) {
  var lin = function (i) {
    var c = parseInt(hex.slice(i, i + 2), 16) / 255;
    return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  };
  return 0.2126 * lin(1) + 0.7152 * lin(3) + 0.0722 * lin(5);
}

function contrastRatio(a, b) {
  var la = relativeLuminance(a), lb = relativeLuminance(b);
  return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05);
}

// ---------- marca ----------

function requireHttps(value, field) {
  if (!HTTPS_RE.test(String(value))) throw new Error(field + '=' + JSON.stringify(value) + '; esperado URL https://…');
  return value;
}

function brandColors(b) {
  var c = Object.assign({}, DEFAULT_COLORS, b.colors || {});
  Object.keys(c).forEach(function (k) {
    if (!HEX_RE.test(c[k])) throw new Error('brand.colors.' + k + '=' + JSON.stringify(c[k]) + '; esperado #RRGGBB');
  });
  var ratio = contrastRatio(c.text, c.background);
  if (ratio < 4.5) {
    throw new Error('R-BRAND-CONTRAST: brand.colors.text=' + c.text + ' sobre background=' + c.background +
      ' = ' + ratio.toFixed(2) + ':1; esperado >= 4.5:1 (WCAG 2.2 AA)');
  }
  // destaque só se legível; botão em preto ou branco, o que contrastar mais com a primária
  c.accent = c.secondary && contrastRatio(c.secondary, c.background) >= 4.5 ? c.secondary : c.text;
  c.on_primary = contrastRatio(c.primary, '#FFFFFF') >= contrastRatio(c.primary, '#000000') ? '#FFFFFF' : '#000000';
  return c;
}

function brandLogo(b) {
  var logo = b.logo;
  if (!logo || (!logo.url && !logo.drive_file_id)) return null;
  if (!logo.alt) throw new Error('brand.logo sem alt (url=' + JSON.stringify(logo.url) + '); esperado texto alternativo');
  if (logo.url) requireHttps(logo.url, 'brand.logo.url');
  return { url: logo.url || null, drive_file_id: logo.drive_file_id || null, alt: logo.alt, width: logo.width || 120 };
}

/** Marca normalizada. Sem brand: cores neutras, nome do show em texto, assinatura do controlador. */
function resolveBrand(show) {
  var b = show.brand || {}, sig = b.host_signature;
  if (sig && sig.photo_url) requireHttps(sig.photo_url, 'brand.host_signature.photo_url');
  var font = b.font ? b.font.family + ', ' + b.font.fallback : 'Arial, sans-serif';
  return {
    display_name: b.display_name || show.name, colors: brandColors(b), logo: brandLogo(b), font: font,
    signature: sig || { name: (show.controller && show.controller.name) || show.name, role: null },
    links: (b.links || []).map(function (l) { return { label: l.label, url: requireHttps(l.url, 'brand.links[].url') }; }),
    tone: b.invitation_tone || 'cordial'
  };
}

// ---------- convidado ----------

function pickMode(c, show) {
  var modes = show.logistics.recording_modes;
  var mode = c.modo || (modes.length === 1 ? modes[0] : null);
  if (modes.indexOf(mode) < 0) {
    throw new Error('convidado.modo=' + JSON.stringify(c.modo) + '; esperado um de ' + JSON.stringify(modes));
  }
  return mode;
}

/** {nome, email, data?, modo?, link_remoto?} → convidado normalizado (erro com o valor ofensor). */
function normalizeInvitee(c, show) {
  c = c || {};
  var name = String(c.nome || '').trim();
  if (!name) throw new Error('convidado.nome=' + JSON.stringify(c.nome) + '; esperado nome do convidado');
  var email = String(c.email || '').trim();
  if (!EMAIL_RE.test(email)) throw new Error('convidado.email=' + JSON.stringify(c.email) + '; esperado e-mail');
  if (c.data) formatScheduled(c.data, 'pt-BR'); // valida o ISO (lança com o valor)
  var mode = pickMode(c, show);
  var link = c.link_remoto ? requireHttps(c.link_remoto, 'convidado.link_remoto') : null;
  return { name: name, email: email, scheduled_at: c.data || null, mode: mode, remote_link: mode === 'remoto' ? link : null };
}

/** Um convite por convidado e data: reexecutar não reenvia. */
function invitationKey(invitee) {
  return 'convite:' + invitee.email.toLowerCase() + ':' + (invitee.scheduled_at || 'sem-data');
}

// ---------- view ----------

function placeView(show, invitee) {
  var lg = show.logistics, pres = invitee.mode === 'presencial';
  return {
    presencial: pres, remoto: !pres, remote_link: invitee.remote_link,
    studio_name: pres ? lg.studio_name || null : null, address_line: pres ? addressLine(lg.address) : null,
    gps_hint: pres ? lg.gps_hint || null : null, arrival_instructions: pres ? lg.arrival_instructions || null : null,
    arrive: pres && lg.arrive_minutes_before ? lg.arrive_minutes_before : null
  };
}

/** Textos do convite já escolhidos (tom e variante), ainda como template. */
function invitationTemplates(inv, brand, variant) {
  var src = Object.assign({}, inv, { intro: inv.intro[brand.tone], cta_intro: inv.cta_intro[variant] });
  if (src.intro === undefined) throw new Error('invitation_tone=' + JSON.stringify(brand.tone) + '; esperado um de ' + JSON.stringify(Object.keys(inv.intro)));
  if (src.cta_intro === undefined) throw new Error('variante=' + JSON.stringify(variant) + '; esperado um de ' + JSON.stringify(Object.keys(inv.cta_intro)));
  return src;
}

function renderMap(src, view) {
  var out = {};
  Object.keys(src).forEach(function (k) { out[k] = renderTemplate(src[k], view); });
  return out;
}

/** opts: {formUrl, variant}. → {view (texto puro, sem escape), html (view escapada), brand}. */
function invitationView(show, invitee, i18n, opts) {
  var brand = resolveBrand(show), formUrl = requireHttps(opts && opts.formUrl, 'formUrl');
  if (!i18n.invitation) throw new Error('i18n ' + i18n.locale + ' sem bloco "invitation"; rode build.js');
  var view = Object.assign(placeView(show, invitee), {
    show: { name: show.name, tagline: show.tagline || null, editorial_line: show.editorial_line },
    guest: { name: invitee.name }, brand: { display_name: brand.display_name },
    controller: resolveController(show, i18n), signature: brand.signature,
    scheduled_text: formatScheduled(invitee.scheduled_at, i18n.locale), form_url: formUrl,
    links_text: brand.links.map(function (l) { return l.label + ': ' + l.url; })
  });
  var src = invitationTemplates(i18n.invitation, brand, opts.variant);
  var html = escapeDeep(view);
  view.t = renderMap(src, view);
  html.t = renderMap(escapeDeep(src), html);
  return { view: view, html: html, brand: brand };
}

/** Escapa recursivamente toda string (dado de usuário) antes de virar HTML. */
function escapeDeep(v) {
  if (typeof v === 'string') return escapeHtml(v);
  if (Array.isArray(v)) return v.map(escapeDeep);
  if (v && typeof v === 'object') {
    var o = {};
    Object.keys(v).forEach(function (k) { o[k] = escapeDeep(v[k]); });
    return o;
  }
  return v;
}

// ---------- HTML (tabelas + CSS inline: Outlook/Gmail descartam <style> e não fazem flex/grid) ----------

function headerCell(v, brand, logoSrc) {
  var c = brand.colors, logo = brand.logo;
  var inner = logo && logoSrc
    ? '<img src="' + escapeHtml(logoSrc) + '" width="' + Number(logo.width) + '" alt="' + escapeHtml(logo.alt) +
      '" style="display:block;margin:0 auto;border:0;height:auto;max-width:100%;font-family:' + escapeHtml(brand.font) +
      ';font-size:20px;font-weight:bold;color:' + c.on_primary + ';">'
    : '<span style="font-family:' + escapeHtml(brand.font) + ';font-size:24px;font-weight:bold;color:' + c.on_primary + ';">' +
      v.brand.display_name + '</span>';
  return '<tr><td align="center" bgcolor="' + c.primary + '" style="background-color:' + c.primary + ';padding:24px;">' + inner + '</td></tr>';
}

function row(label, value, c) {
  return '<tr><td valign="top" width="34%" style="padding:6px 12px 6px 0;font-weight:bold;color:' + c.accent + ';">' +
    label + '</td><td valign="top" style="padding:6px 0;color:' + c.text + ';">' + value + '</td></tr>';
}

function detailRows(v, c) {
  var t = v.t, rows = [row(t.when_label, v.scheduled_text || t.when_tbd, c)];
  if (v.presencial) {
    rows.push(row(t.where_label, (v.studio_name ? v.studio_name + ' · ' : '') + v.address_line, c));
    if (v.gps_hint) rows.push(row(t.gps_label, '<b>' + v.gps_hint + '</b>', c));
    if (v.arrival_instructions) rows.push(row(t.arrival_label, v.arrival_instructions, c));
    if (v.arrive) rows.push(row('', t.arrive, c));
  } else {
    rows.push(row(t.remote_label, v.remote_link ? '<a href="' + v.remote_link + '" style="color:' + c.accent + ';">' + v.remote_link + '</a>' : t.remote_link_tbd, c));
  }
  return '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="font-size:15px;line-height:1.5;">' + rows.join('') + '</table>';
}

/** Botão "à prova de bala": célula com bgcolor + link em bloco (funciona sem imagem e no Outlook). */
function ctaButton(v, brand) {
  var c = brand.colors;
  return '<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:16px 0;"><tr>' +
    '<td align="center" bgcolor="' + c.primary + '" style="background-color:' + c.primary + ';border-radius:6px;">' +
    '<a href="' + v.form_url + '" target="_blank" style="display:inline-block;padding:14px 28px;font-family:' + escapeHtml(brand.font) +
    ';font-size:17px;font-weight:bold;color:' + c.on_primary + ';text-decoration:none;border-radius:6px;">' + v.t.cta_button + '</a>' +
    '</td></tr></table><p style="margin:0;font-size:13px;color:' + c.text + ';">' + v.t.cta_fallback + '<br>' +
    '<a href="' + v.form_url + '" style="color:' + c.accent + ';word-break:break-all;">' + v.form_url + '</a></p>';
}

function signatureBlock(v, brand) {
  var s = v.signature, c = brand.colors, links = brand.links.map(function (l) {
    return '<a href="' + escapeHtml(l.url) + '" style="color:' + c.accent + ';">' + escapeHtml(l.label) + '</a>';
  });
  var photo = s.photo_url ? '<td valign="top" style="padding-right:12px;"><img src="' + s.photo_url + '" width="56" height="56" alt="' +
    escapeHtml(brand.signature.photo_alt || brand.signature.name) + '" style="display:block;border:0;border-radius:28px;"></td>' : '';
  return '<p style="margin:24px 0 8px;">' + v.t.signoff + '</p><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>' +
    photo + '<td valign="top" style="color:' + c.text + ';"><b>' + s.name + '</b><br>' +
    (s.role ? s.role + ' · ' : '') + v.brand.display_name + (links.length ? '<br>' + links.join(' · ') : '') + '</td></tr></table>';
}

function bodySection(v, brand) {
  var c = brand.colors;
  return '<p style="margin:0 0 4px;font-size:13px;letter-spacing:2px;text-transform:uppercase;color:' + c.accent + ';">' + v.t.title + '</p>' +
    '<h1 style="margin:0 0 16px;font-size:26px;line-height:1.25;color:' + c.text + ';">' + v.t.greeting + '</h1>' +
    '<p style="margin:0 0 16px;">' + v.t.intro + '</p>' + detailRows(v, c) +
    '<h2 style="margin:24px 0 8px;font-size:18px;color:' + c.accent + ';">' + v.t.about_heading + '</h2>' +
    (v.show.tagline ? '<p style="margin:0 0 8px;font-style:italic;">' + v.show.tagline + '</p>' : '') +
    '<p style="margin:0 0 16px;">' + v.show.editorial_line + '</p><p style="margin:0;">' + v.t.cta_intro + '</p>' +
    ctaButton(v, brand) + signatureBlock(v, brand);
}

function footerSection(v, c) {
  // rodapé com a MESMA cor de texto (cinza claro reprovaria o contraste AA)
  return '<tr><td style="padding:16px 24px 24px;font-size:12px;line-height:1.5;color:' + c.text + ';border-top:1px solid ' + c.primary + ';">' +
    '<p style="margin:0 0 6px;">' + v.t.footer_controller + '</p><p style="margin:0 0 6px;">' + v.t.footer_purpose + '</p>' +
    '<p style="margin:0;">' + v.t.footer_optout + '</p></td></tr>';
}

/** HTML do e-mail. logoSrc: URL https ou "cid:showlogo" (logo do Drive como imagem embutida); null = nome em texto. */
function renderInvitationHtml(built, locale, logoSrc) {
  var v = built.html, brand = built.brand, c = brand.colors;
  return '<!DOCTYPE html><html lang="' + escapeHtml(locale) + '"><head><meta charset="utf-8">' +
    '<meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light">' +
    '<meta name="supported-color-schemes" content="light"><title>' + v.t.subject + '</title></head>' +
    '<body style="margin:0;padding:0;background-color:' + c.background + ';">' +
    '<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;">' + v.t.preheader + '</div>' +
    '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="' + c.background + '" style="background-color:' + c.background + ';">' +
    '<tr><td align="center" style="padding:24px 12px;"><table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" ' +
    'style="width:100%;max-width:600px;border-collapse:collapse;background-color:' + c.background + ';">' +
    headerCell(v, brand, logoSrc) + '<tr><td style="padding:28px 24px 8px;font-family:' + escapeHtml(brand.font) +
    ';font-size:16px;line-height:1.6;color:' + c.text + ';">' + bodySection(v, brand) + '</td></tr>' + footerSection(v, c) +
    '</table></td></tr></table></body></html>\n';
}

// ---------- texto puro e .ics ----------

function renderInvitationText(template, built) {
  return renderTemplate(stripDocComment(template), built.view).replace(/\n{3,}/g, '\n\n').trim() + '\n';
}

function icsText(s) {
  return String(s).replace(/\\/g, '\\\\').replace(/;/g, '\\;').replace(/,/g, '\\,').replace(/\r\n|\r|\n/g, '\\n');
}

/** RFC 5545 §3.1: dobra linhas em 75 octetos (UTF-8), continuação começa com espaço. */
function foldIcsLine(line) {
  var out = '', n = 0;
  Array.from(line).forEach(function (ch) {
    var cp = ch.codePointAt(0), len = cp < 0x80 ? 1 : cp < 0x800 ? 2 : cp < 0x10000 ? 3 : 4;
    if (n + len > 75) { out += '\r\n '; n = 1; }
    out += ch; n += len;
  });
  return out;
}

function icsStamp(ms) {
  return new Date(ms).toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '');
}

/** Anexo .ics (METHOD:PUBLISH: o convidado adiciona à agenda dele). null sem data. */
function buildInvitationIcs(show, invitee, built, nowMs) {
  if (!invitee.scheduled_at) return null;
  var start = Date.parse(invitee.scheduled_at), v = built.view;
  var minutes = show.logistics.recording_duration_minutes || 90;
  var where = v.presencial ? [v.address_line, v.gps_hint].filter(Boolean).join(' — ') : (v.remote_link || 'online');
  return ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//podcast-production//convite-oficial//PT', 'METHOD:PUBLISH',
    'BEGIN:VEVENT', 'UID:' + invitationKey(invitee).replace(/[^\w.@-]/g, '-') + '@podcast-production',
    'DTSTAMP:' + icsStamp(nowMs), 'DTSTART:' + icsStamp(start), 'DTEND:' + icsStamp(start + minutes * 60000),
    'SUMMARY:' + icsText(v.t.subject), 'LOCATION:' + icsText(where), 'DESCRIPTION:' + icsText(v.t.ics_description),
    'END:VEVENT', 'END:VCALENDAR'].map(foldIcsLine).join('\r\n') + '\r\n';
}

/**
 * Tudo que o e-mail precisa. opts: {formUrl, variant, nowMs}.
 * → {to, subject, text, html, ics, logo: {cid, drive_file_id}|null, sender}
 */
function buildInvitationEmail(template, show, invitee, i18n, opts) {
  var built = invitationView(show, invitee, i18n, opts), logo = built.brand.logo;
  var logoSrc = logo ? (logo.url || 'cid:' + LOGO_CID) : null;
  return {
    to: invitee.email, subject: built.view.t.subject, sender: built.brand.display_name,
    text: renderInvitationText(template, built), html: renderInvitationHtml(built, i18n.locale, logoSrc),
    ics: buildInvitationIcs(show, invitee, built, opts.nowMs || Date.now()),
    logo: logo && !logo.url ? { cid: LOGO_CID, drive_file_id: logo.drive_file_id } : null
  };
}

if (typeof module !== 'undefined') {
  module.exports = { contrastRatio: contrastRatio, resolveBrand: resolveBrand, normalizeInvitee: normalizeInvitee,
    invitationKey: invitationKey, invitationView: invitationView, escapeDeep: escapeDeep, LOGO_CID: LOGO_CID,
    buildInvitationEmail: buildInvitationEmail, foldIcsLine: foldIcsLine, icsText: icsText };
}
