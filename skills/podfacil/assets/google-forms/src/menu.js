/**
 * menu.js — menu "PodFácil" na planilha (PodFácil 2.2, itens 2 a 4).
 *
 * Só aparece quando o código mora DENTRO da planilha (planilha-modelo, etapa 5 do plano 2.2): num projeto avulso
 * o onOpen nunca roda e nada aqui muda o que já funciona. Cada item chama o que já existe (licenca.js,
 * convidados.js, automations.js); nenhuma regra de envio, licença ou LGPD é decidida aqui.
 *
 * Chave de licença: entra por uma janela com campo oculto, vai direto às Propriedades do script e nunca volta
 * para a tela, para o log ou para a mensagem de erro (licencaSalvar devolve só {ok, texto}).
 */

if (typeof module !== 'undefined') {   // Node (testes): dependências puras dos outros arquivos; no Apps Script o escopo é global
  var renderTemplate = require('./core.js').renderTemplate, actions5_ = require('./actions.js');
  var escapeHtml = actions5_.escapeHtml, addressLine = actions5_.addressLine, cellText = require('./convidados.js').cellText;
  var LOGO_MAX_BYTES = require('./drive.js').LOGO_MAX_BYTES;
}

// ── parte pura (testável em Node) ────────────────────────────────────────

/** Itens do menu na ordem: [rótulo, função] ou null (separador). */
function menuItens(i18n) {
  var m = i18n.menu;
  return [[m.activate_license, 'menuAtivarLicenca'], [m.config.item, 'menuConfigurarPrograma'],
    [m.config.logo_item, 'menuEnviarLogo'], [m.invite, 'menuConvidar'],
    [m.check_install, 'menuVerificarInstalacao'], null,
    [m.resend_notice, 'menuReenviarAviso'], [m.confirm_guest, 'menuEnviarConfirmacao'], [m.rebuild_guests, 'menuRefazerAbaConvidados'],
    [m.forget_guest, 'menuEsquecerConvidado'], null, [m.release_devices, 'menuLiberarDispositivos']];
}

/** Valor da coluna `nome` (cabeçalho exato) na linha; '' se a coluna não existe. Nunca pela posição. */
function valorDaColuna(header, row, nome) {
  var col = header.indexOf(nome);
  return col < 0 ? '' : String(row[col] == null ? '' : row[col]).trim();
}

/** {id, nome} do convidado de uma linha da aba Convidados, ou null se a linha não tem código do registro. */
function convidadoDaLinha(header, row, i18n) {
  var cols = i18n.sheet.columns, id = valorDaColuna(header, row, cols[cols.length - 1]);
  return id ? { id: id, nome: valorDaColuna(header, row, cols[1]) || id } : null;
}

/** Tem o formato das chaves emitidas pelo servidor (pgi_ + base64url, license_store.py)? A conferência é do servidor. */
function chaveComFormato(key) {
  return typeof key === 'string' && /^pgi_[A-Za-z0-9_-]{40,200}$/.test(key.trim());
}

/** Linhas da aba Configuração: [rótulo, valor] em linguagem simples, sem JSON; texto nunca vira fórmula. */
function linhasConfiguracao(show, i18n) {
  var c = i18n.menu.config, l = c.labels, lg = show.logistics || {}, brand = show.brand || {};
  var colors = brand.colors || {}, logo = brand.logo || {}, ctl = show.controller || {};
  var rows = [[l.name, show.name], [l.tagline, show.tagline], [l.locale, show.locale], [l.editorial, show.editorial_line],
    [l.modes, (lg.recording_modes || []).join(', ')], [l.studio, lg.studio_name],
    [l.address, lg.address ? addressLine(lg.address) : ''],
    [l.colors, [colors.primary, colors.secondary].filter(Boolean).join(' / ')], [l.logo, logo.url || logo.drive_file_id],
    [l.controller, [ctl.name, ctl.contact_email].filter(Boolean).join(' · ')],
    [l.retention, show.retention_days_after_publish ? renderTemplate(c.retention_days, { dias: show.retention_days_after_publish }) : '']];
  return rows.map(function (r) { return [r[0], r[1] == null || r[1] === '' ? i18n.sheet.none : cellText(r[1])]; });
}

/** Texto do "Verificar instalação": resumo + uma linha por item ({status: ok|fixed|warn|fail, text}). */
function relatorioInstalacao(checks, i18n) {
  var icon = { ok: '✅', fixed: '🔧', warn: '⚠️', fail: '❌' }, c = i18n.menu.check;
  var bad = checks.filter(function (x) { return x.status === 'fail'; }).length;
  return (bad ? renderTemplate(c.summary_fail, { n: bad }) : c.summary_ok) + '\n\n' +
    checks.map(function (x) { return icon[x.status] + ' ' + x.text; }).join('\n');
}

/** HTML da janela "Ativar licença". O campo é de senha; a chave é apagada do campo antes de seguir ao servidor. */
function licencaHtml(t) {
  var e = escapeHtml, js = function (s) { return JSON.stringify(String(s)).replace(/</g, '\\u003c'); };
  return '<!DOCTYPE html><html><head><base target="_top"><style>' +
    'body{font-family:Arial,sans-serif;font-size:14px;line-height:1.4;margin:16px;color:#202124}' +
    'input{width:100%;box-sizing:border-box;padding:8px;font-size:14px;margin:6px 0 12px}' +
    'button{padding:8px 18px;font-size:14px;cursor:pointer}#msg{margin-top:12px;white-space:pre-wrap;' +
    'word-break:break-all;user-select:text}</style></head><body>' +
    '<p>' + e(t.lead) + '</p><label for="k">' + e(t.label) + '</label>' +
    '<input id="k" type="password" autocomplete="off" spellcheck="false" autofocus>' +
    '<button id="b" type="button">' + e(t.button) + '</button><div id="msg" role="status" aria-live="polite"></div>' +
    '<script>var W=' + js(t.working) + ',b=document.getElementById("b"),k=document.getElementById("k"),' +
    'm=document.getElementById("msg");' +
    'function done(r){m.textContent=r.texto;b.disabled=false;if(r.ok&&!r.fica){setTimeout(function(){google.script.host.close();},2500);}}' +
    'function go(){var v=k.value;k.value="";if(!v)return;b.disabled=true;m.textContent=W;' +
    'google.script.run.withSuccessHandler(done).withFailureHandler(function(){done({ok:false,texto:' + js(t.failed) + '});})' +
    '.licencaSalvar(v);}' +
    'b.addEventListener("click",go);k.addEventListener("keydown",function(ev){if(ev.key==="Enter")go();});</script>' +
    '</body></html>';
}

/** HTML da janela "Enviar logo": confere tipo e tamanho antes de mandar; o servidor confere de novo. */
function logoHtml(t) {
  var e = escapeHtml, js = function (s) { return JSON.stringify(String(s)).replace(/</g, '\\u003c'); };
  return '<!DOCTYPE html><html><head><base target="_top"><style>' +
    'body{font-family:Arial,sans-serif;font-size:14px;line-height:1.4;margin:16px;color:#202124}' +
    'input{margin:8px 0 12px}button{padding:8px 18px;font-size:14px;cursor:pointer}#msg{margin-top:12px}</style>' +
    '</head><body><p>' + e(t.lead) + '</p><input id="f" type="file" accept="image/png,image/jpeg"><br>' +
    '<button id="b" type="button">' + e(t.button) + '</button><div id="msg" role="status" aria-live="polite"></div>' +
    '<script>var T={working:' + js(t.working) + ',big:' + js(t.too_big) + ',type:' + js(t.bad_type) + ',fail:' + js(t.failed) +
    '},b=document.getElementById("b"),f=document.getElementById("f"),m=document.getElementById("msg");' +
    'function done(r){m.textContent=r.texto;b.disabled=false;if(r.ok){setTimeout(function(){google.script.host.close();},2500);}}' +
    'b.addEventListener("click",function(){var x=f.files&&f.files[0];if(!x)return;' +
    'if(x.type!=="image/png"&&x.type!=="image/jpeg"){m.textContent=T.type;return;}' +
    'if(x.size>' + LOGO_MAX_BYTES + '){m.textContent=T.big;return;}' +
    'b.disabled=true;m.textContent=T.working;var rd=new FileReader();' +
    'rd.onload=function(){google.script.run.withSuccessHandler(done).withFailureHandler(function(){done({ok:false,texto:T.fail});})' +
    '.logoSalvar({nome:x.name,tipo:x.type,dados:String(rd.result).split(",")[1]||""});};rd.readAsDataURL(x);});</script>' +
    '</body></html>';
}

// ── lado Google ──────────────────────────────────────────────────────────

// ── cópia da planilha (planilha-modelo, 2.2 etapa 5) ─────────────────────

var INSTANCIA_PROP = 'PODFACIL_PLANILHA_ID';

/**
 * "Fazer uma cópia" pode levar as Propriedades do script junto (chave de licença, convidados, códigos de convite).
 * As propriedades ficam marcadas com o id da planilha a que pertencem; numa cópia (id diferente), tudo é apagado
 * antes de qualquer coisa, e a cópia começa do zero. Projeto avulso (sem planilha ativa): nada a fazer.
 * -> true se acabou de limpar uma cópia.
 */
function garantirInstancia_() {
  var ss = null;
  try { ss = SpreadsheetApp.getActiveSpreadsheet(); } catch (err) { return false; }
  if (!ss) return false;
  var p = props_(), id = String(ss.getId()), dono = p.getProperty(INSTANCIA_PROP);
  if (dono === id) return false;
  if (dono) p.deleteAllProperties();
  p.setProperty(INSTANCIA_PROP, id);
  return !!dono;
}

/** Abas vazias que o Google cria sozinho numa planilha nova ("Página1"): confundem o leigo, que digita nelas. */
var ABAS_PADRAO = ['Página1', 'Sheet1', 'Hoja 1', '工作表1'];

/**
 * Aba "Comece aqui" numa planilha ainda sem programa nem formulário (o modelo e cada cópia nova). O texto é
 * reescrito a cada abertura enquanto a planilha não tem programa (o modelo pega a versão nova do guia a cada
 * `ops/modelo.py atualizar`; cópias já feitas ficam com o código da época). Só as linhas do guia são tocadas: o que
 * o dono digitar abaixo dele fica.
 */
var COMECE_LINHAS_PROP = 'COMECE_LINHAS';

function comeceAqui_(i18n) {
  var ss = SpreadsheetApp.getActiveSpreadsheet(), t = i18n.menu.start;
  if (!ss || props_().getProperty(PROP_SHOW) || props_().getProperty('FORM_ID')) return;
  var sh = ss.getSheetByName(t.tab);
  Object.keys(BUNDLE.i18n).forEach(function (l) {   // guia de outro idioma: só se a aba for mesmo o guia (título em A1)
    var s = BUNDLE.i18n[l].menu.start, cand = sh ? null : ss.getSheetByName(s.tab);
    if (cand && String(cand.getRange(1, 1).getValue()) === s.title) sh = cand;
  });
  if (!sh && ss.getSheetByName(t.tab) === null) sh = ss.insertSheet(t.tab, 0);
  if (!sh) return;
  if (sh.getName() !== t.tab) sh.setName(t.tab);
  var guia = BUNDLE.produto[i18n.locale === 'pt-BR' ? 'guia_planilha' : 'guia_planilha_en'];
  var rows = [[t.title]].concat(t.steps.map(function (s, i) { return [(i + 1) + '. ' + s]; }))
    .concat([[t.guide + ' ' + guia], [t.footer]]);
  var antes = Number(props_().getProperty(COMECE_LINHAS_PROP)) || rows.length;
  sh.getRange(1, 1, Math.max(antes, rows.length), 1).clearContent();
  props_().setProperty(COMECE_LINHAS_PROP, String(rows.length));
  sh.getRange(1, 1, rows.length, 1).setValues(rows).setWrap(true).setVerticalAlignment('top');
  sh.getRange(1, 1).setFontWeight('bold').setFontSize(14);
  sh.setColumnWidth(1, 760);
  ABAS_PADRAO.forEach(function (nome) {
    var vazia = ss.getSheetByName(nome);
    if (vazia && vazia.getLastRow() === 0 && vazia.getLastColumn() === 0 && !vazia.getCharts().length &&
        !vazia.getImages().length && ss.getSheets().length > 1) ss.deleteSheet(vazia);
  });
}

/** Textos no idioma do programa; sem configuração (ou idioma não revisado), em português. */
function menuI18n_() {
  try { garantirInstancia_(); } catch (err) { console.error('cópia da planilha: ' + err.message); }
  var loc = 'pt-BR';
  try { loc = props_().getProperty('LOCALE') || loadShow_().locale || loc; } catch (err) { loc = idiomaDaPlanilha_(); }
  try { return selectLocale(BUNDLE, loc, allowUnreviewed_()); } catch (err) { return selectLocale(BUNDLE, 'pt-BR', false); }
}

/** Sem programa ainda: o idioma da própria planilha (Arquivo > Configurações), que o gatilho simples pode ler. */
function idiomaDaPlanilha_() {
  try {
    var l = String(SpreadsheetApp.getActiveSpreadsheet().getSpreadsheetLocale() || '').toLowerCase().slice(0, 2);
    return { en: 'en', es: 'es', zh: 'zh' }[l] || 'pt-BR';
  } catch (err) { return 'pt-BR'; }
}

/**
 * Gatilho simples da planilha: monta o menu. Sem rede e sem nada que peça autorização; mexe só na própria planilha
 * (limpa propriedades copiadas de outra planilha e escreve a aba Comece aqui).
 */
function onOpen() {
  var i18n = menuI18n_(), menu = SpreadsheetApp.getUi().createMenu(i18n.menu.title);
  menuItens(i18n).forEach(function (it) { if (it) menu.addItem(it[0], it[1]); else menu.addSeparator(); });
  menu.addToUi();
  try { comeceAqui_(i18n); } catch (err) { console.error('aba Comece aqui: ' + err.message); }   // nunca derruba o menu
}

/**
 * Formulário criado pelo menu (ninguém roda função no editor): o completo se a licença paga estiver ativa, senão o
 * essencial. -> texto para o dono (link do convidado ou o motivo da falha).
 */
function criarFormularioPeloMenu_(trocar) {
  var c = menuI18n_().menu.config, lock = LockService.getScriptLock();
  if (!lock.tryLock(1000)) return c.form_busy;   // outro clique já está criando (leva 10-30 s): não sai um 2º formulário
  try {
    if (!trocar && props_().getProperty('FORM_ID')) {
      return renderTemplate(c.form_exists, { url: String(props_().getProperty('FORM_URL') || '') });
    }
    var pago = licencaPaga_().ok, url = buildForm(pago ? 'completo' : 'essencial', null);
    return renderTemplate(c.form_created, { variante: c.variants[pago ? 'completo' : 'essencial'], url: url });
  } catch (err) {
    console.error('formulário pelo menu: ' + maskEmails_(err.message));
    return renderTemplate(c.form_fail, { motivo: maskEmails_(err.message) });
  } finally {
    lock.releaseLock();
  }
}

/** Formulário essencial com licença paga ativa: o completo está liberado (troca pelo Verificar instalação). */
function formularioParaTrocar_() {
  var meta = {};
  try { meta = JSON.parse(props_().getProperty('FORM_META') || '{}'); } catch (err) { meta = {}; }
  return meta.variant === 'essencial' && !!props_().getProperty('FORM_ID') && licencaPaga_().ok;
}

function menuAtivarLicenca() {
  var t = menuI18n_().menu.license;
  SpreadsheetApp.getUi().showModalDialog(HtmlService.createHtmlOutput(licencaHtml(t)).setWidth(440).setHeight(280), t.title);
}

/**
 * Chamada pela janela "Ativar licença". Devolve só {ok, texto}: nunca a chave.
 * - recusa explícita do servidor (chave desconhecida, revogada, grátis): não grava nada;
 * - limite de dispositivos: a chave existe e é paga; grava sem cache e aponta "Liberar outros dispositivos";
 * - servidor fora do ar: grava sem cache só se não houver outra chave (não troca uma chave boa às cegas).
 */
function licencaSalvar(key) {
  var t = menuI18n_().menu.license, old = (props_().getProperty(LICENCA_PROP) || '').trim();
  key = String(key == null ? '' : key).trim();
  if (!chaveComFormato(key)) return { ok: false, texto: t.invalid };
  var r = perguntarServidor_(key);
  var importado = function () {   // pago: numa planilha ainda SEM programa, o perfil salvo no chat entra junto
    try { loadShow_(); return formularioParaTrocar_() ? t.upgrade_hint + ' ' : ''; } catch (err) { /* sem programa: segue */ }
    var got = buscarPerfil_(key, null);
    if (!got.show) return '';
    try {
      aplicarPerfil_(got.show);
      var form = props_().getProperty('FORM_ID') ? '' : criarFormularioPeloMenu_() + ' ';   // 1ª vez: já sai com formulário
      return renderTemplate(menuI18n_().menu.config.imported, { nome: String(got.show.name || '') }) + ' ' + form;
    } catch (err) {   // o perfil já saiu do servidor (uso único): o dono precisa saber, não pode sumir calado
      console.error('perfil do programa não gravado: ' + err.message);
      return renderTemplate(menuI18n_().menu.config.import_failed, { motivo: err.message }) + ' ';
    }
  };
  if (r.indisponivel) {
    if (old && old !== key) return { ok: false, texto: t.offline_keep };
    if (old !== key) { props_().setProperty(LICENCA_PROP, key); props_().deleteProperty(LICENCA_CACHE_PROP); }
    return { ok: true, texto: t.saved_offline };
  }
  var info = r.answer.result || {}, code = r.answer.error;
  if (code === 'device_limit') {
    props_().setProperty(LICENCA_PROP, key);
    props_().deleteProperty(LICENCA_CACHE_PROP);
    return { ok: true, texto: t.saved_limit };
  }
  if (code === 'license_unknown') return { ok: false, texto: t.unknown };
  if (code) return { ok: false, texto: renderTemplate(t.refused, { motivo: String(r.answer.message || code) }) };
  if (info.tier !== 'paid') return { ok: false, texto: t.free_key };
  props_().setProperty(LICENCA_PROP, key);
  props_().setProperty(LICENCA_CACHE_PROP, JSON.stringify({ chave: chaveHash_(key), plano: info.plan,
    confirmado_em: new Date().toISOString() }));
  var extra = importado();   // com texto (link do formulário, falha, dica): a janela fica aberta para o dono ler
  return { ok: true, fica: !!extra, texto: extra + renderTemplate(extra ? t.ok_stay : t.ok, { plano: String(info.plan || '') }) };
}

/** A planilha do PodFácil: a que tem o código dentro (modelo) ou, no projeto avulso, a das respostas. */
function planilhaDoPodFacil_() {
  try { var ativa = SpreadsheetApp.getActiveSpreadsheet(); if (ativa) return ativa; } catch (err) { /* projeto avulso */ }
  var id = props_().getProperty('SHEET_ID');
  return id ? SpreadsheetApp.openById(id) : null;
}

/** Perfil salvo pelo Claude no servidor: pela licença (pago, sem código) ou pelo código. -> {show} | {erro, code}. */
function buscarPerfil_(key, codigo) {
  var r = chamarServidor_('programa_buscar', codigo ? { codigo: codigo } : {}, key || null);
  if (r.indisponivel) return { erro: r.indisponivel };
  if (r.answer.error) return { erro: String(r.answer.message || r.answer.error), code: r.answer.error };
  var show = (r.answer.result || {}).show_profile;
  return show && typeof show === 'object' ? { show: show } : { erro: 'resposta do servidor sem show_profile' };
}

/** Guarda a cópia do perfil (SHOW_PROFILE_JSON) e redesenha a aba Configuração, só para leitura. O logo enviado
 *  pela planilha fica: o perfil que vem do chat não sabe dele (o arquivo é do Drive desta conta). */
function aplicarPerfil_(show) {
  var antes = null;
  try { antes = loadShow_(); } catch (err) { antes = null; }
  var logo = antes && antes.brand && antes.brand.logo;
  if (logo && logo.drive_file_id && !(show.brand && show.brand.logo)) {
    show.brand = Object.assign({ colors: Object.assign({}, DEFAULT_COLORS) }, show.brand || {}, { logo: logo });
  }
  props_().setProperty(PROP_SHOW, JSON.stringify(show));
  var i18n = menuI18n_(), c = i18n.menu.config, ss = planilhaDoPodFacil_();
  if (!ss) return;
  var sh = ss.getSheetByName(c.tab) || abaConfigEmOutroIdioma_(ss) || ss.insertSheet(c.tab);
  if (sh.getName() !== c.tab) sh.setName(c.tab);   // idioma do programa mudou: a mesma aba, com o nome novo
  var rows = [[c.note, '']].concat(linhasConfiguracao(show, i18n)), last = sh.getLastRow();
  if (last) sh.getRange(1, 1, last, 2).clearContent();
  sh.getRange(1, 1, rows.length, 2).setValues(rows);
}

function menuEnviarLogo() {
  var t = menuI18n_().menu.config.logo;
  SpreadsheetApp.getUi().showModalDialog(HtmlService.createHtmlOutput(logoHtml(t)).setWidth(440).setHeight(260), t.title);
}

/**
 * Chamada pela janela "Enviar logo": confere tipo (pelos bytes, não só pelo nome), tamanho e perfil; grava no Drive
 * da conta pelo drive.file (drive.js) e aponta brand.logo para o arquivo. Devolve só {ok, texto}.
 */
function logoSalvar(arq) {
  var t = menuI18n_().menu.config.logo, show;
  try { show = loadShow_(); } catch (err) { return { ok: false, texto: t.need_show }; }
  arq = arq || {};
  var tipo = String(arq.tipo || ''), bytes;
  if (!LOGO_TIPOS[tipo]) return { ok: false, texto: t.bad_type };
  try { bytes = Utilities.base64Decode(String(arq.dados || '')); } catch (err) { return { ok: false, texto: t.bad_type }; }
  if (bytes.length > LOGO_MAX_BYTES) return { ok: false, texto: t.too_big };
  if (!assinaturaConfere(bytes, tipo)) return { ok: false, texto: t.bad_type };
  try {
    var id = driveCriarImagem_('PodFácil · logo · ' + String(show.name || ''), tipo, bytes);
    var antigo = (show.brand && show.brand.logo) || {}, logo = { drive_file_id: id, alt: antigo.alt || String(show.name || 'Logo') };
    if (antigo.width) logo.width = antigo.width;
    show.brand = Object.assign({ colors: Object.assign({}, DEFAULT_COLORS) }, show.brand || {}, { logo: logo });
    aplicarPerfil_(show);
    if (antigo.drive_file_id && antigo.drive_file_id !== id) {   // o logo anterior que o PodFácil guardou vai para a lixeira
      try { driveTrash_(antigo.drive_file_id); } catch (err) { console.error('logo anterior ficou no Drive: ' + err.message); }
    }
    return { ok: true, texto: t.ok };
  } catch (err) {
    console.error('logo não enviado: ' + err.message);
    return { ok: false, texto: t.failed };
  }
}

function abaConfigEmOutroIdioma_(ss) {
  var nomes = Object.keys(BUNDLE.i18n).map(function (l) { return BUNDLE.i18n[l].menu.config.tab; });
  for (var i = 0; i < nomes.length; i++) { var sh = ss.getSheetByName(nomes[i]); if (sh) return sh; }
  return null;
}

/** Pago: busca pela licença; sem licença (ou sem perfil guardado nela), pede o código de 15 letras e números. O código vai
 *  SEM a chave: uma chave suspensa não pode barrar um código válido. Servidor fora do ar: avisa na hora. */
function menuConfigurarPrograma() {
  var ui = SpreadsheetApp.getUi(), m = menuI18n_().menu, c = m.config;
  var key = (props_().getProperty(LICENCA_PROP) || '').trim(), got = key ? buscarPerfil_(key, null) : null;
  if (got && !got.show && !got.code) { ui.alert(renderTemplate(m.error, { motivo: got.erro })); return; }
  if (!got || !got.show) {
    var r = ui.prompt(c.ask_code_title, c.ask_code, ui.ButtonSet.OK_CANCEL);
    if (r.getSelectedButton() !== ui.Button.OK) return;
    got = buscarPerfil_(null, String(r.getResponseText() || '').trim());
  }
  if (!got.show) { ui.alert(renderTemplate(m.error, { motivo: got.erro })); return; }
  aplicarPerfil_(got.show);
  c = menuI18n_().menu.config;   // o idioma pode ter mudado com o perfil novo
  var form = props_().getProperty('FORM_ID') ? '' : '\n\n' + criarFormularioPeloMenu_();   // 1ª configuração: já sai com formulário
  ui.alert(renderTemplate(c.done, { nome: String(got.show.name || ''), aba: c.tab }) + form);
}

/** Confere configuração, formulário, gatilhos, aba Convidados e licença; religa gatilhos e recria a aba. */
function menuVerificarInstalacao() {
  var ui = SpreadsheetApp.getUi();   // antes de mexer em algo: sem tela (projeto avulso), não conserta às cegas
  var i18n = menuI18n_(), c = i18n.menu.check, checks = [], form = null;
  try { checks.push({ status: 'ok', text: renderTemplate(c.show_ok, { nome: String(loadShow_().name || '') }) }); }
  catch (err) { checks.push({ status: 'fail', text: c.show_missing }); }
  var formId = props_().getProperty('FORM_ID'), criado = null;
  if (!formId && checks[0].status === 'ok' && ui.alert(c.title, c.form_ask, ui.ButtonSet.YES_NO) === ui.Button.YES) {
    criado = criarFormularioPeloMenu_();   // com programa e sem formulário: cria aqui mesmo, sem ir ao editor
    formId = props_().getProperty('FORM_ID');
  }
  if (formId && !criado) {
    try { FormApp.openById(formId); } catch (err) {   // apagado: sem o editor, o dono só sai daqui pelo menu
      if (ui.alert(c.title, c.form_gone_ask, ui.ButtonSet.YES_NO) === ui.Button.YES) criado = criarFormularioPeloMenu_(true);
    }
    if (!criado && formularioParaTrocar_() && ui.alert(c.title, c.upgrade_ask, ui.ButtonSet.YES_NO) === ui.Button.YES) {
      criado = criarFormularioPeloMenu_(true);
    }
    formId = props_().getProperty('FORM_ID');
  }
  if (!formId) checks.push({ status: 'fail', text: criado || c.form_missing });
  else {
    try { form = FormApp.openById(formId); checks.push({ status: criado ? 'fixed' : 'ok', text: criado || c.form_ok }); }
    catch (err) { checks.push({ status: 'fail', text: criado || c.form_gone }); }
  }
  if (form) {
    checks.push(gatilhosNoLugar_(form, c));
    checks.push(abaConvidadosNoLugar_(c));
    var tel = validacaoNoLugar_(form, c);
    if (tel) checks.push(tel);
  }
  var logoCheck = logoNoLugar_(c);
  if (logoCheck) checks.push(logoCheck);
  checks.push(licencaNoLugar_(c));
  ui.alert(c.title, relatorioInstalacao(checks, i18n), ui.ButtonSet.OK);
}

/** Gatilhos são por conta: um coeditor não vê os do dono e não deve criar um 2º jogo em nome dele (revisão 2.2). */
function gatilhosNoLugar_(form, c) {
  var have = ScriptApp.getProjectTriggers().map(function (t) { return t.getHandlerFunction(); });
  if (have.indexOf('onFormSubmit') >= 0 && have.indexOf('lembreteDiario') >= 0) return { status: 'ok', text: c.triggers_ok };
  var dono = String(props_().getProperty(TRIGGERS_OWNER_PROP) || ''), eu = String(Session.getEffectiveUser().getEmail() || '').toLowerCase();
  if (dono && eu && dono !== eu) return { status: 'warn', text: renderTemplate(c.triggers_other, { dono: dono }) };
  installTriggers_(form);
  return { status: 'fixed', text: c.triggers_fixed };
}

/** Formulário de antes da 2.2: põe a validação do WhatsApp (o campo não informa se já tem; pôr de novo é inofensivo). */
function validacaoNoLugar_(form, c) {
  try {
    var i18n = selectLocale(BUNDLE, loadMeta_().locale, allowUnreviewed_());
    return validarTelefoneNoFormulario_(form, i18n) ? { status: 'ok', text: c.phone_ok } : null;
  } catch (err) {
    console.error('validação do WhatsApp: ' + err.message);
    return null;
  }
}

function abaConvidadosNoLugar_(c) {
  try {
    var i18n = selectLocale(BUNDLE, loadMeta_().locale, allowUnreviewed_());
    if (convidadosSheetExistente_(i18n)) return { status: 'ok', text: c.guests_ok };
    reconstruirAbaConvidados();
    return { status: 'fixed', text: c.guests_fixed };
  } catch (err) {
    return { status: 'fail', text: renderTemplate(c.guests_fail, { motivo: err.message }) };
  }
}

/** Logo no Drive: abre para o PodFácil? (com drive.file, só o enviado pelo menu abre) Sem logo do Drive: nada. */
function logoNoLugar_(c) {
  var show;
  try { show = loadShow_(); } catch (err) { return null; }
  var logo = show.brand && show.brand.logo;
  if (!logo || !logo.drive_file_id || logo.url) return null;
  try { driveBlob_(logo.drive_file_id); return { status: 'ok', text: c.logo_ok }; }
  catch (err) { return { status: 'warn', text: c.logo_fail }; }
}

function licencaNoLugar_(c) {
  if (!(props_().getProperty(LICENCA_PROP) || '').trim()) return { status: 'warn', text: c.license_none };
  var r = licencaPaga_();
  if (!r.ok) return { status: 'fail', text: renderTemplate(c.license_fail, { motivo: r.motivo }) };
  if (r.offline) return { status: 'warn', text: c.license_offline };
  return { status: 'ok', text: renderTemplate(c.license_paid, { plano: String(r.plano || '') }) };
}

/** Convidado da linha selecionada na aba Convidados; sem seleção válida, pede o código do registro. */
function convidadoSelecionado_(i18n, ui) {
  var m = i18n.menu, sh = SpreadsheetApp.getActiveSheet(), sel = sh && sh.getActiveRange();
  var tabId = props_().getProperty('CONVIDADOS_SHEET_ID'), tab = i18n;   // a aba usa o idioma do formulário
  try { tab = selectLocale(BUNDLE, loadMeta_().locale, allowUnreviewed_()); } catch (err) { tab = i18n; }
  var abaCerta = sh && (!tabId || String(sh.getSheetId()) === tabId);
  if (abaCerta && sel && sel.getRow() > 1 && sh.getLastColumn() > 0) {
    var n = sh.getLastColumn(), header = sh.getRange(1, 1, 1, n).getValues()[0];
    var hit = convidadoDaLinha(header, sh.getRange(sel.getRow(), 1, 1, n).getValues()[0], tab);
    if (hit) return hit;
  }
  var r = ui.prompt(m.ask_code_title, m.ask_code, ui.ButtonSet.OK_CANCEL);
  if (r.getSelectedButton() !== ui.Button.OK) return null;
  var id = String(r.getResponseText() || '').trim();
  return id ? { id: id, nome: id } : null;
}

function menuReenviarAviso() {
  var i18n = menuI18n_(), m = i18n.menu, ui = SpreadsheetApp.getUi(), who = convidadoSelecionado_(i18n, ui);
  if (!who) return;
  try { reenviarAviso(who.id); ui.alert(m.resend_done); }
  catch (err) { ui.alert(renderTemplate(m.error, { motivo: err.message })); }
}

/**
 * Decisão 3.1: e-mail pronto ao convidado da linha selecionada, pedindo para confirmar o que veio com problema.
 * Só depois do SIM do dono; nunca a quem pediu para sair nem a resposta retida (e-mail não confirmado: Codex #5).
 * A resposta do convidado volta para o e-mail do dono (replyTo).
 */
function menuEnviarConfirmacao() {
  var i18n = menuI18n_(), m = i18n.menu, t = m.confirm, ui = SpreadsheetApp.getUi(), who = convidadoSelecionado_(i18n, ui);
  if (!who) return;
  try {
    var row = intakeSheet_().getDataRange().getValues().slice(1).filter(function (r) { return r[0] === who.id; })[0];
    if (!row) { ui.alert(renderTemplate(t.not_found, { id: who.id })); return; }
    var intake = JSON.parse(row[2]), nome = who.nome, email = intake.contacts && intake.contacts.email;
    if (!admittedRow_(row, store_())) { ui.alert(t.held); return; }
    if (guestPolicy_(email).optedOut) { ui.alert(renderTemplate(t.optout, { nome: nome })); return; }
    var lang = selectLocale(BUNDLE, intake.locale || loadMeta_().locale, allowUnreviewed_());   // no idioma do formulário
    var mail = buildGuestConfirmation(loadShow_(), intake, JSON.parse(row[4] || '[]'), lang);
    var key = 'sent:' + who.id + ':email:confirmacao', antes = props_().getProperty(key);
    var pergunta = mail.itens.length
      ? renderTemplate(t.ask, { nome: nome, n: mail.itens.length, itens: mail.itens.map(function (x) { return '• ' + x; }).join('\n') })
      : renderTemplate(t.ask_none, { nome: nome });
    if (antes) pergunta += '\n\n' + renderTemplate(t.again, { quando: formatScheduled(isoLocal(antes.replace(/^pending:/, ''), intake), i18n.locale) });
    if (ui.alert(t.title, pergunta, ui.ButtonSet.YES_NO) !== ui.Button.YES) return;
    if (MailApp.getRemainingDailyQuota() < 1) { ui.alert(t.quota); return; }
    var livre = withScriptLock_(function () {   // 2 cliques seguidos: só o 1º manda
      if (props_().getProperty(key) !== antes) return false;
      props_().setProperty(key, 'pending:' + new Date().toISOString());
      return true;
    });
    if (!livre) { ui.alert(t.busy); return; }
    var show = loadShow_(), dono = String(props_().getProperty(TRIGGERS_OWNER_PROP) || '') || Session.getEffectiveUser().getEmail();
    try {   // a resposta volta para o dono do programa, mesmo se quem clicou for um coeditor
      MailApp.sendEmail(email, mail.subject, mail.text, { htmlBody: mail.html, name: show.name, replyTo: dono });
    } catch (err) {
      if (antes) props_().setProperty(key, antes); else props_().deleteProperty(key);
      throw err;
    }
    props_().setProperty(key, new Date().toISOString());
    ui.alert(renderTemplate(t.done, { nome: nome }));
  } catch (err) { ui.alert(renderTemplate(m.error, { motivo: maskEmails_(err.message) })); }
}

function menuRefazerAbaConvidados() {
  var m = menuI18n_().menu, ui = SpreadsheetApp.getUi();
  try { reconstruirAbaConvidados(); ui.alert(m.rebuild_done); }
  catch (err) { ui.alert(renderTemplate(m.error, { motivo: err.message })); }
}

/** LGPD: pede confirmação com o nome; só então chama esquecerTitular. Pendências manuais aparecem na tela. */
function menuEsquecerConvidado() {
  var i18n = menuI18n_(), m = i18n.menu, ui = SpreadsheetApp.getUi(), who = convidadoSelecionado_(i18n, ui);
  if (!who) return;
  if (ui.alert(m.forget_guest, renderTemplate(m.forget_confirm, { nome: who.nome }), ui.ButtonSet.YES_NO) !== ui.Button.YES) return;
  try {
    var rep = esquecerTitular(who.id), notas = [rep.calendar && rep.calendar.note, rep.form_responses && rep.form_responses.note];
    var pend = (rep.pendencias_manuais || []).concat(notas.filter(Boolean));   // nada sobra escondido atrás do "Pronto"
    ui.alert(renderTemplate(m.forget_done, { nome: who.nome }) +
      (pend.length ? '\n\n' + m.forget_pending + '\n- ' + pend.join('\n- ') : ''));
  } catch (err) { ui.alert(renderTemplate(m.error, { motivo: err.message })); }
}

/** Troca de computador sem suporte: chama licenca_liberar_dispositivos no servidor (2 vezes por mês). */
function menuLiberarDispositivos() {
  var m = menuI18n_().menu, t = m.devices, ui = SpreadsheetApp.getUi();
  var key = (props_().getProperty(LICENCA_PROP) || '').trim();
  if (!key) { ui.alert(t.no_key); return; }
  if (ui.alert(t.title, t.confirm, ui.ButtonSet.YES_NO) !== ui.Button.YES) return;
  var r = perguntarServidor_(key, 'licenca_liberar_dispositivos');
  if (r.indisponivel) { ui.alert(renderTemplate(m.error, { motivo: r.indisponivel })); return; }
  if (r.answer.error) { ui.alert(renderTemplate(m.error, { motivo: String(r.answer.message || r.answer.error) })); return; }
  ui.alert(t.done);
}

if (typeof module !== 'undefined') {
  module.exports = { menuItens: menuItens, convidadoDaLinha: convidadoDaLinha, chaveComFormato: chaveComFormato,
    relatorioInstalacao: relatorioInstalacao, licencaHtml: licencaHtml, linhasConfiguracao: linhasConfiguracao,
    logoHtml: logoHtml };
}
