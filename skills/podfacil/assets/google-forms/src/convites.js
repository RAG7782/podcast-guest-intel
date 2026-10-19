/**
 * convites.js — fila de convites na aba "Convites" (PodFácil 2.2, item 6).
 *
 * Uma linha por convidado (nome, e-mail, data, modalidade, link da sala, WhatsApp). Só o clique do dono em
 * "PodFácil > Convidar" (depois do SIM) põe uma linha na fila: o envio é pelo enviarConvite (automations.js),
 * idempotente por convidado+data, e a Situação da linha diz o que houve. Erro numa linha não trava as outras.
 * Cota do MailApp (100 destinatários/dia no gmail.com, 1.500 no Workspace): a fila nunca gasta a reserva do dia (kit,
 * lembrete e avisos ao dono). Limite de 6 min por execução: a fila para antes, contado do início da execução. O que
 * sobrar fica "⏳ na fila" e sai no gatilho diário (que só manda "⏳", nunca linha que o dono não confirmou), com
 * resumo ao dono. Duas rodadas ao mesmo tempo: a 2ª não começa (convites_rodando).
 *
 * WhatsApp da linha (LGPD, minimização): depois de lido, a célula passa a "***3820"; nas Propriedades fica só um
 * hash com sal do projeto + os 4 últimos dígitos (invite_wa:<email>), com validade, para o aviso ao dono acusar
 * quando o convidado digita outro número no formulário. Esquecer o convidado apaga a linha dele nesta aba.
 */

if (typeof module !== 'undefined') {   // Node (testes); no Apps Script o escopo é global
  var renderTemplate = require('./core.js').renderTemplate, intake7_ = require('./intake.js');
  var EMAIL_RE = intake7_.EMAIL_RE, toE164 = intake7_.toE164;
}

var CONVITE_RESERVA_COTA = 20;          // mínimo de e-mails do dia que a fila nunca gasta (ou 30% da cota, o maior)
var CONVITE_TEMPO_MS = 240000;          // 4 min desde o início da execução: o Apps Script corta em 6 min
var CONVITE_WA_PROP = 'invite_wa:';
var CONVITE_WA_DIAS = 60;               // o número anotado no convite vale para comparar por até 60 dias
var CONVITE_RODANDO_PROP = 'convites_rodando';
var CONVITE_PENDENTE_MS = 3600000;      // reserva de envio "pending" com mais de 1 h: execução cortada no meio

// ── parte pura (testável em Node) ────────────────────────────────────────

function pad2_(n) { return (n < 10 ? '0' : '') + n; }

function offsetIso_(minutes) {
  var a = Math.abs(minutes);
  return (minutes < 0 ? '-' : '+') + pad2_(Math.floor(a / 60)) + ':' + pad2_(a % 60);
}

/** Data e hora válidas? (31/02 não passa) -> ISO com o fuso daquela data (ctx.offsetAt), ou undefined. */
function isoDe_(y, mo, d, h, mi, ctx) {
  var dt = new Date(Date.UTC(y, mo - 1, d, h, mi));
  if (dt.getUTCFullYear() !== y || dt.getUTCMonth() !== mo - 1 || dt.getUTCDate() !== d || h > 23 || mi > 59) return undefined;
  return y + '-' + pad2_(mo) + '-' + pad2_(d) + 'T' + pad2_(h) + ':' + pad2_(mi) + ':00' + offsetIso_(ctx.offsetAt(y, mo, d, h, mi));
}

/**
 * Data da célula -> ISO 8601. ctx: {locale, partes(Date) -> {y, mo, d, h, mi} no fuso da planilha,
 * offsetAt(y, mo, d, h, mi) -> minutos do fuso NAQUELA data (horário de verão incluído)}.
 * Data da planilha: precisa ter hora (display com ":"), senão o convite sairia para a meia-noite. Texto:
 * "2026-10-20 14:30" em qualquer idioma; "20/10/2026 14:30" ou "14h30" em pt-BR e es. Vazio -> null; ilegível -> undefined.
 */
function dataDoConvite(v, display, ctx) {
  if (v === '' || v === null || v === undefined) return null;
  if (typeof v === 'object' && typeof v.getTime === 'function') {
    if (isNaN(v.getTime()) || !/\d[:h]\d/.test(String(display || ''))) return undefined;
    var p = ctx.partes(v);
    return p.y < 1900 ? undefined : isoDe_(p.y, p.mo, p.d, p.h, p.mi, ctx);   // 1899 = célula só com hora
  }
  var s = String(v).trim(), m = /^(\d{4})-(\d{1,2})-(\d{1,2})[ T,]+(\d{1,2})[:h](\d{2})?$/i.exec(s);
  if (m) return isoDe_(+m[1], +m[2], +m[3], +m[4], +(m[5] || 0), ctx);
  m = /^(\d{1,2})\/(\d{1,2})\/(\d{4})[ ,]+(?:às\s+|a las\s+)?(\d{1,2})[:h](\d{2})?$/i.exec(s);
  if (m && (ctx.locale === 'pt-BR' || ctx.locale === 'es')) return isoDe_(+m[3], +m[2], +m[1], +m[4], +(m[5] || 0), ctx);
  return undefined;
}

/** Modalidade digitada ou escolhida na lista -> {modo: 'presencial' | 'remoto' | null (vazio)} ou {erro}. */
function modoDoConvite(v, i18n, show) {
  var s = String(v == null ? '' : v).trim().toLowerCase();
  if (!s) return { modo: null };
  var modes = show.logistics.recording_modes, choices = (i18n.form.choices || {}).recording_mode || {}, own = i18n.owner.mode || {};
  for (var i = 0; i < modes.length; i++) {
    var k = modes[i], nomes = [k, choices[k], own[k]].filter(Boolean).map(function (x) { return String(x).toLowerCase(); });
    var primeira = String(own[k] || k).toLowerCase().split(/[\s,]+/)[0];
    if (nomes.indexOf(s) >= 0 || s === primeira || s.indexOf(k.slice(0, 5)) === 0) return { modo: k };
  }
  return { erro: true };
}

/** Nomes das modalidades do programa, para a mensagem de erro e a lista da coluna. */
function modosDoPrograma(i18n, show) {
  var own = i18n.owner.mode || {};
  return show.logistics.recording_modes.map(function (k) { return own[k] || k; });
}

/** "***3820": o que fica na célula do WhatsApp depois de lido. */
function whatsappMascarado(e164) {
  return '***' + String(e164).slice(-4);
}

/**
 * Linha da aba Convites -> {convidado: {nome, email, data, modo, link_remoto?}, whatsapp} | {erro: texto} | null (vazia).
 * As colunas são achadas pelo cabeçalho (i18n.menu.invites.columns), nunca pela posição. display = os mesmos valores
 * como a planilha mostra (para saber se a data tem hora). ctx: o de dataDoConvite + {agora (ms), country}.
 */
function conviteDaLinha(header, row, display, i18n, show, ctx) {
  var t = i18n.menu.invites, e = t.errors, cols = t.columns;
  var at = function (i) { return header.indexOf(cols[i]); };
  var get = function (i) { return at(i) < 0 ? '' : row[at(i)]; };
  var txt = function (i) { var v = get(i); return String(v === null || v === undefined ? '' : v).trim(); };
  if ([0, 1, 2, 3, 4, 5].every(function (i) { return txt(i) === ''; })) return null;
  var nome = txt(0), email = txt(1);
  if (!nome) return { erro: e.name };
  if (!EMAIL_RE.test(email)) return { erro: e.email };
  var data = dataDoConvite(get(2), at(2) < 0 ? '' : (display || [])[at(2)], Object.assign({ locale: i18n.locale }, ctx));
  if (data === undefined) return { erro: e.date };
  if (data && Date.parse(data) < ctx.agora) return { erro: e.past };
  var modo = modoDoConvite(get(3), i18n, show), modes = show.logistics.recording_modes;
  if (modo.erro || (!modo.modo && modes.length !== 1)) {
    return { erro: renderTemplate(e.mode, { modos: modosDoPrograma(i18n, show).join(' / ') }) };
  }
  var link = txt(4);
  if (link && !/^https:\/\/\S+$/i.test(link)) return { erro: e.link };
  var wa = null;
  if (txt(5) && !/^\*{3}\d{4}$/.test(txt(5))) {   // "***3820" = já lido numa rodada anterior
    wa = toE164(txt(5), ctx.country);
    if (!wa) return { erro: e.whatsapp };
  }
  var c = { nome: nome, email: email, data: data, modo: modo.modo || modes[0] };
  if (link) c.link_remoto = link;
  return { convidado: c, whatsapp: wa };
}

/**
 * A linha entra na rodada? manual (o dono clicou em Convidar e disse SIM): vazia, "⏳" e "⚠️" (falha, tenta de novo).
 * Gatilho diário: SÓ "⏳", que o dono já mandou enviar. Linha digitada e nunca confirmada não sai sozinha.
 */
function linhaPendente(status, manual) {
  var s = String(status == null ? '' : status).trim();
  if (s.indexOf('⏳') === 0) return true;
  return !!manual && (!s || s.indexOf('⚠️') === 0);
}

/** Situação que o dono "conserta" editando a linha (onEdit apaga; a linha volta a esperar o clique em Convidar). */
function situacaoCorrigivel(status) {
  var s = String(status == null ? '' : status).trim();
  return s.indexOf('❌') === 0 || s.indexOf('⚠️') === 0;
}

/** Quantos e-mails a fila ainda pode gastar hoje: a cota menos a reserva (o maior entre o mínimo e 30% da cota). */
function cotaDaFila(restante, inicial) {
  return restante - Math.max(CONVITE_RESERVA_COTA, Math.ceil(0.3 * inicial));
}

/** Resumo da rodada no idioma do programa. */
function resumoConvites(cont, i18n) {
  var t = i18n.menu.invites;
  return renderTemplate(t.done, cont) + (cont.depois ? '\n\n' + t.later : '');
}

// ── lado Google ──────────────────────────────────────────────────────────

/** Textos no idioma do formulário (o mesmo da aba Convidados e dos convites). */
function convitesI18n_() {
  try { return selectLocale(BUNDLE, loadMeta_().locale, allowUnreviewed_()); } catch (err) { return menuI18n_(); }
}

/** {sheet, i18n} da aba Convites em qualquer idioma já usado (os textos e colunas saem do idioma da ABA), ou null. */
function abaConvites_(ss) {
  var locs = Object.keys(BUNDLE.i18n);
  for (var i = 0; i < locs.length; i++) {
    var sh = ss.getSheetByName(BUNDLE.i18n[locs[i]].menu.invites.tab);
    if (sh) return { sheet: sh, i18n: BUNDLE.i18n[locs[i]] };
  }
  return null;
}

/** Cria a aba com cabeçalho, nota e lista de modalidades. -> {sheet, i18n, criada}. */
function convitesSheet_(i18n, show) {
  var ss = planilhaDoPodFacil_();
  if (!ss) throw new Error('planilha do PodFácil não encontrada (sem planilha ativa e sem SHEET_ID)');
  var achada = abaConvites_(ss), t = i18n.menu.invites;
  if (achada) return { sheet: achada.sheet, i18n: achada.i18n, criada: false };
  var sh = ss.insertSheet(t.tab);
  sh.getRange(1, 1, 1, t.columns.length).setValues([t.columns]).setFontWeight('bold');
  sh.setFrozenRows(1);
  sh.getRange(1, 1).setNote(t.note);
  var regra = SpreadsheetApp.newDataValidation().requireValueInList(modosDoPrograma(i18n, show), true)
    .setAllowInvalid(true).build();   // aceita digitar, mas mostra a lista
  sh.getRange(2, 4, 500, 1).setDataValidation(regra);
  return { sheet: sh, i18n: i18n, criada: true };
}

/** Datas no fuso da PLANILHA (onde o dono digita), com o deslocamento certo de cada data (horário de verão). */
function ctxDatas_(ss) {
  var tz = (ss && ss.getSpreadsheetTimeZone && ss.getSpreadsheetTimeZone()) || Session.getScriptTimeZone();
  var minutosEm = function (ms) {
    var m = /^([+-])(\d{2})(\d{2})$/.exec(Utilities.formatDate(new Date(ms), tz, 'Z'));
    return m ? (m[1] === '-' ? -1 : 1) * (Number(m[2]) * 60 + Number(m[3])) : 0;
  };
  return {
    partes: function (d) {
      var m = /^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})$/.exec(Utilities.formatDate(d, tz, 'yyyy-MM-dd HH:mm'));
      return { y: +m[1], mo: +m[2], d: +m[3], h: +m[4], mi: +m[5] };
    },
    offsetAt: function (y, mo, d, h, mi) {   // 2 passos: o fuso da hora "local" tomada como UTC, depois corrigido
      var local = Date.UTC(y, mo - 1, d, h, mi), off = minutosEm(local);
      return minutosEm(local - off * 60000);
    }
  };
}

function agoraLocal_(i18n, ctx) {
  var p = ctx.partes(new Date());
  return formatScheduled(isoDe_(p.y, p.mo, p.d, p.h, p.mi, ctx), i18n.locale);
}

/** Hash com sal do projeto: o número não sai de um dicionário de DDD + 4 dígitos. */
function hashWhatsapp_(e164) {
  var sal = props_().getProperty('invite_wa_salt');
  if (!sal) { sal = Utilities.getUuid(); props_().setProperty('invite_wa_salt', sal); }
  return tokenHash_(sal + ':' + e164);
}

function guardarWhatsappDoConvite_(email, e164) {
  props_().setProperty(CONVITE_WA_PROP + normEmail_(email), JSON.stringify({ h: hashWhatsapp_(e164), end: e164.slice(-4),
    exp: Date.now() + CONVITE_WA_DIAS * 86400000 }));
}

/** Uma rodada por vez (menu e gatilho diário podem coincidir): true se pegou a vez. */
function pegarVezDaFila_() {
  return withScriptLock_(function () {
    var desde = Number(props_().getProperty(CONVITE_RODANDO_PROP) || 0);
    if (desde && Date.now() - desde < 7 * 60000) return false;   // a outra rodada ainda pode estar viva (corte em 6 min)
    props_().setProperty(CONVITE_RODANDO_PROP, String(Date.now()));
    return true;
  });
}

/**
 * Uma rodada da fila. manual = o dono clicou e disse SIM. inicio = início da EXECUÇÃO (o limite de 6 min conta dali).
 * -> contagem {enviados, pulados, corrigir, falhas, depois, ocupada?}. Pré-requisito faltando (programa, formulário):
 * lança, sem mexer em linha.
 */
function convidarPendentes_(manual, inicio) {
  var show = loadShow_(), meta = loadMeta_();
  if (!props_().getProperty('FORM_URL')) throw new Error('FORM_URL ausente; esperado o formulário criado');
  var cont = { enviados: 0, pulados: 0, corrigir: 0, falhas: 0, depois: 0 };
  if (!pegarVezDaFila_()) { cont.ocupada = true; return cont; }
  try {
    rodarFila_(manual, inicio || Date.now(), show, meta, cont);
  } finally {
    props_().deleteProperty(CONVITE_RODANDO_PROP);
  }
  console.log('fila de convites: ' + JSON.stringify(cont));
  return cont;
}

function rodarFila_(manual, inicio, show, meta, cont) {
  var aba = convitesSheet_(convitesI18n_(), show), sh = aba.sheet, i18n = aba.i18n, t = i18n.menu.invites, st = t.status;
  var ctx = Object.assign(ctxDatas_(sh.getParent()), { agora: Date.now(), country: phoneCountry({ jurisdiction: meta.jurisdiction }) });
  var n = sh.getLastRow(), w = t.columns.length;
  if (n < 2) return;
  var largura = Math.max(w, sh.getLastColumn());
  var header = sh.getRange(1, 1, 1, largura).getValues()[0].map(function (h) { return String(h).trim(); });
  var colSit = header.indexOf(t.columns[w - 1]) + 1, colMail = header.indexOf(t.columns[1]) + 1, colWa = header.indexOf(t.columns[5]) + 1;
  if (!colSit || !colMail) throw new Error('aba ' + sh.getName() + ' sem as colunas "' + t.columns[1] + '" e "' + t.columns[w - 1] + '"');
  var faixa = sh.getRange(2, 1, n - 1, largura), rows = faixa.getValues(), shown = faixa.getDisplayValues();
  var cotaInicial = MailApp.getRemainingDailyQuota();
  // grava na linha CERTA: se o dono ordenou ou apagou linhas durante a rodada, acha a linha pelo e-mail
  var linhaDe = function (i, email) {
    var at = i + 2, e = normEmail_(email);
    if (normEmail_(sh.getRange(at, colMail).getValue()) === e) return at;
    var lin = sh.getLastRow();
    if (lin < 2) return 0;
    var mails = sh.getRange(2, colMail, lin - 1, 1).getValues();
    for (var k = 0; k < mails.length; k++) if (normEmail_(mails[k][0]) === e) return k + 2;
    return 0;
  };
  var escrever = function (i, email, texto, mascarar) {
    var at = linhaDe(i, email);
    if (!at) { console.error('fila de convites: linha de ' + (i + 2) + ' sumiu durante a rodada; nada gravado'); return; }
    sh.getRange(at, colSit).setValue(texto);
    if (mascarar && colWa) sh.getRange(at, colWa).setValue(mascarar);
  };
  rows.forEach(function (row, i) {
    if (!linhaPendente(row[colSit - 1], manual)) return;
    var lido = conviteDaLinha(header, row, shown[i], i18n, show, ctx), email = row[colMail - 1];
    if (!lido) return;
    if (!lido.erro) {
      try { normalizeInvitee(lido.convidado, show); } catch (err) { lido = { erro: maskEmails_(err.message).slice(0, 200) }; }
    }
    if (lido.erro) { escrever(i, email, renderTemplate(st.fix, { motivo: lido.erro })); cont.corrigir++; return; }
    var mascara = lido.whatsapp ? whatsappMascarado(lido.whatsapp) : null;
    if (Date.now() - inicio > CONVITE_TEMPO_MS) { escrever(i, email, st.time); cont.depois++; return; }
    if (cotaDaFila(MailApp.getRemainingDailyQuota(), cotaInicial) < 1) { escrever(i, email, st.quota); cont.depois++; return; }
    var res;
    try { res = enviarConvite(lido.convidado); } catch (err) {
      res = { status: 'error', error: err.message };
    }
    if (res.status === 'skipped' && res.reason === 'já enviado') {   // reserva "pending" antiga: a execução foi cortada
      var reserva = String(props_().getProperty('sent:' + res.key) || ''), quando = Date.parse(reserva.slice(8));
      if (reserva.indexOf('pending:') === 0) {
        if (Date.now() - quando < CONVITE_PENDENTE_MS) { escrever(i, email, st.time); cont.depois++; return; }
        props_().deleteProperty('sent:' + res.key);   // o próximo Convidar tenta de novo
        escrever(i, email, st.unsure); cont.falhas++; return;
      }
    }
    try {
      if (lido.whatsapp && res.status !== 'error' && res.reason !== 'opt-out') guardarWhatsappDoConvite_(lido.convidado.email, lido.whatsapp);
    } catch (err) { console.error('fila de convites: WhatsApp não anotado (' + err.message + ')'); }
    if (res.status === 'sent') {
      escrever(i, email, renderTemplate(res.aviso ? st.sent_logo : st.sent, { quando: agoraLocal_(i18n, ctx) }), mascara);
      cont.enviados++;
    } else if (res.status === 'skipped') {
      escrever(i, email, res.reason === 'opt-out' ? st.optout : st.already, mascara);
      cont.pulados++;
    } else {
      escrever(i, email, renderTemplate(st.failed, { motivo: maskEmails_(String(res.error || res.status)).slice(0, 200) }));
      cont.falhas++;
    }
  });
}

/** PodFácil > Convidar. O tempo da execução conta desde já (o dono pensando no SIM também gasta os 6 min). */
function menuConvidar() {
  var inicio = Date.now(), ui = SpreadsheetApp.getUi(), m = menuI18n_().menu, show;
  try { show = loadShow_(); loadMeta_(); } catch (err) { ui.alert(convitesI18n_().menu.invites.need_form); return; }
  if (!props_().getProperty('FORM_URL')) { ui.alert(convitesI18n_().menu.invites.need_form); return; }
  try {
    var r = convitesSheet_(convitesI18n_(), show), t = r.i18n.menu.invites;
    if (r.criada) { ui.alert(renderTemplate(t.created, { aba: t.tab })); return; }
    var pend = pendentesNaAba_(r.sheet, t);
    if (!pend) { ui.alert(renderTemplate(t.nothing, { aba: r.sheet.getName() })); return; }
    if (ui.alert(t.tab, renderTemplate(t.confirm, { n: pend }), ui.ButtonSet.YES_NO) !== ui.Button.YES) return;
    var cont = convidarPendentes_(true, inicio);
    ui.alert(cont.ocupada ? t.busy : resumoConvites(cont, r.i18n));
  } catch (err) { ui.alert(renderTemplate(m.error, { motivo: maskEmails_(err.message) })); }
}

/** Quantas linhas com nome ou e-mail entram numa rodada manual. */
function pendentesNaAba_(sh, t) {
  var n = sh.getLastRow(), w = t.columns.length;
  if (n < 2) return 0;
  var header = sh.getRange(1, 1, 1, Math.max(w, sh.getLastColumn())).getValues()[0].map(function (h) { return String(h).trim(); });
  var iNome = header.indexOf(t.columns[0]), iMail = header.indexOf(t.columns[1]), iSit = header.indexOf(t.columns[w - 1]);
  if (iNome < 0 || iMail < 0) return 0;
  return sh.getRange(2, 1, n - 1, header.length).getValues().filter(function (row) {
    var cheia = String(row[iNome] || '').trim() || String(row[iMail] || '').trim();
    return cheia && linhaPendente(iSit < 0 ? '' : row[iSit], true);
  }).length;
}

/**
 * Gatilho diário, por ÚLTIMO no lembreteDiario (inicio = início da execução): o que o dono mandou e ficou "⏳"
 * sai hoje; resumo ao dono se algo andou. Nunca lança.
 */
function filaDeConvitesDiaria_(inicio) {
  var ss, aba;
  try { ss = planilhaDoPodFacil_(); aba = ss && abaConvites_(ss); } catch (err) { return null; }
  if (!aba) return null;
  try {
    var t = aba.i18n.menu.invites, cont = convidarPendentes_(false, inicio);
    if (cont.enviados || cont.corrigir || cont.falhas) {
      var v = Object.assign({ aba: aba.sheet.getName(), url: ss.getUrl() }, cont);
      MailApp.sendEmail(Session.getEffectiveUser().getEmail(), renderTemplate(t.digest_subject, v), renderTemplate(t.digest_body, v),
        { name: 'PodFácil' });
    }
    return cont;
  } catch (err) {
    console.error(maskEmails_('fila de convites: ' + err.message + '; tenta de novo amanhã'));
    return null;
  }
}

/** Esquecer o titular: as linhas dele na aba Convites saem também (pelo e-mail). -> nº de linhas apagadas. */
function removerConvites_(email) {
  var e = normEmail_(email), ss = planilhaDoPodFacil_(), aba = e && ss && abaConvites_(ss);
  if (!aba) return 0;
  var sh = aba.sheet, cols = aba.i18n.menu.invites.columns, n = sh.getLastRow();
  if (n < 2) return 0;
  var header = sh.getRange(1, 1, 1, Math.max(cols.length, sh.getLastColumn())).getValues()[0].map(function (h) { return String(h).trim(); });
  var col = header.indexOf(cols[1]) + 1;
  if (!col) return 0;
  var mails = sh.getRange(2, col, n - 1, 1).getValues(), apagadas = 0;
  for (var k = mails.length - 1; k >= 0; k--) {
    if (normEmail_(mails[k][0]) === e) { sh.deleteRow(k + 2); apagadas++; }
  }
  return apagadas;
}

/**
 * Gatilho simples da planilha: quem corrige uma linha com "❌" ou "⚠️" na aba Convites apaga a Situação dela, e a
 * linha volta a esperar o próximo clique em Convidar. Editar a Situação à mão não dispara nada.
 */
function onEdit(e) {
  var rg = e && e.range, sh = rg && rg.getSheet();
  if (!sh) return;
  var i18n = null;
  Object.keys(BUNDLE.i18n).forEach(function (l) { if (BUNDLE.i18n[l].menu.invites.tab === sh.getName()) i18n = BUNDLE.i18n[l]; });
  if (!i18n) return;
  var cols = i18n.menu.invites.columns, header = sh.getRange(1, 1, 1, Math.max(cols.length, sh.getLastColumn())).getValues()[0]
    .map(function (h) { return String(h).trim(); });
  var colSit = header.indexOf(cols[cols.length - 1]) + 1;
  if (!colSit) return;
  var c0 = rg.getColumn(), c1 = c0 + rg.getNumColumns() - 1;
  if (c0 === colSit && c1 === colSit) return;
  var r0 = Math.max(2, rg.getRow()), r1 = rg.getRow() + rg.getNumRows() - 1;
  if (r1 < r0) return;
  var sit = sh.getRange(r0, colSit, r1 - r0 + 1, 1), vals = sit.getValues(), mudou = false;   // uma leitura e uma escrita
  vals.forEach(function (v) { if (situacaoCorrigivel(v[0])) { v[0] = ''; mudou = true; } });
  if (mudou) sit.setValues(vals);
}

if (typeof module !== 'undefined') {
  module.exports = { dataDoConvite: dataDoConvite, modoDoConvite: modoDoConvite, conviteDaLinha: conviteDaLinha,
    linhaPendente: linhaPendente, situacaoCorrigivel: situacaoCorrigivel, resumoConvites: resumoConvites,
    modosDoPrograma: modosDoPrograma, whatsappMascarado: whatsappMascarado, cotaDaFila: cotaDaFila };
}
