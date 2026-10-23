/**
 * importar.js — trazer os convidados de outra planilha do PodFácil (2.2.2): migração de uma instalação antiga e o
 * jeito de "atualizar" uma cópia (cópias não recebem código novo: faz-se uma cópia nova do modelo e importa-se a
 * antiga). O que vem: o registro de cada resposta (aba intake), o que já foi enviado a cada convidado (para nada
 * sair em dobro) e o link do briefing. Na planilha antiga: o formulário para de
 * aceitar respostas e os registros vão para a aba "intake (migrado)", fora da lista de lembretes do código antigo.
 * Nada é apagado.
 *
 * Puro (testado em node): idDaPlanilha, chavesJaEnviadas.
 */

var PASSOS_ = PASSOS_ || {};   // passos do diálogo (dialogo.js); a ordem dos arquivos não importa
var ABA_MIGRADO = 'intake (migrado)';
var STATUS_JA_TRATADO = ['sent', 'skipped', 'off'];   // o que não deve sair de novo na planilha nova

/** Link da planilha (…/d/<id>/…) ou o próprio id -> id; senão ''. */
function idDaPlanilha(texto) {
  var s = String(texto || '').trim(), m = /\/d\/([A-Za-z0-9_-]{25,})/.exec(s);
  if (m) return m[1];
  return /^[A-Za-z0-9_-]{25,}$/.test(s) ? s : '';
}

/** Coluna resultado_envios (JSON) -> chaves do store que já foram tratadas (sent:<chave> na planilha nova). */
function chavesJaEnviadas(resultadosJson) {
  var lista = [];
  try { lista = JSON.parse(resultadosJson || '[]'); } catch (err) { lista = []; }
  return (Array.isArray(lista) ? lista : []).filter(function (r) {
    return r && r.key && STATUS_JA_TRATADO.indexOf(r.status) >= 0;
  }).map(function (r) { return String(r.key); });
}

function menuImportar() {
  var m = menuI18n_().menu, t = m.import;
  abrirDialogo_(t.title, telaEntrada(t.ask, t.label, { rotulo: m.window.continue, passo: 'importar_ver', espera: t.wait },
    { rotulo: m.window.cancel }));
}

/** Abre a planilha antiga e confere se é do PodFácil. -> {ss, intake, linhas} ou {erro}. */
function planilhaAntiga_(valor) {
  var t = menuI18n_().menu.import, id = idDaPlanilha(valor);
  if (!id) return { erro: t.bad_link };
  var aqui = planilhaDoPodFacil_();
  if (aqui && aqui.getId() === id) return { erro: t.same };
  var ss;
  try { ss = SpreadsheetApp.openById(id); } catch (err) { return { erro: t.no_access }; }
  var intake = ss.getSheetByName('intake');
  if (!intake || String(intake.getRange(1, 1, 1, INTAKE_HEADER.length).getValues()[0]) !== String(INTAKE_HEADER)) {
    return { erro: renderTemplate(t.not_podfacil, { nome: ss.getName() }) };
  }
  var linhas = intake.getLastRow() > 1 ? intake.getRange(2, 1, intake.getLastRow() - 1, INTAKE_HEADER.length).getValues() : [];
  return { ss: ss, intake: intake, linhas: linhas.filter(function (r) { return r[0]; }) };
}

function idsJaAqui_() {
  var sh = intakeSheet_(), n = sh.getLastRow();
  return n > 1 ? sh.getRange(2, 1, n - 1, 1).getValues().map(function (r) { return String(r[0]); }) : [];
}

PASSOS_.importar_ver = function (args) {
  var m = menuI18n_().menu, t = m.import;
  if (!props_().getProperty('FORM_ID')) return telaResultado(t.need_setup);
  var antiga = planilhaAntiga_(args.valor);
  if (antiga.erro) {
    return telaEntrada(t.ask, t.label, { rotulo: m.window.continue, passo: 'importar_ver', espera: t.wait }, { rotulo: m.window.cancel }, antiga.erro);
  }
  var ja = idsJaAqui_(), novos = antiga.linhas.filter(function (r) { return ja.indexOf(String(r[0])) < 0; }).length;
  if (!novos) return telaResultado(renderTemplate(t.nothing, { nome: antiga.ss.getName(), n: antiga.linhas.length }));
  return telaPergunta(renderTemplate(t.confirm, { nome: antiga.ss.getName(), n: novos, ja: antiga.linhas.length - novos }),
    { rotulo: renderTemplate(t.yes, { n: novos }), passo: 'importar_ja', args: { valor: antiga.ss.getId() }, espera: t.wait_import },
    { rotulo: m.window.cancel });
};

PASSOS_.importar_ja = function (args) {
  var t = menuI18n_().menu.import, antiga = planilhaAntiga_(args.valor);
  if (antiga.erro) return telaResultado(antiga.erro);
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(5000)) return telaResultado(t.busy);
  try {
    var ja = idsJaAqui_(), intake = intakeSheet_(), p = props_(), agora = new Date().toISOString(), trazidos = [];
    antiga.linhas.forEach(function (r) {
      var id = String(r[0]);
      if (ja.indexOf(id) >= 0) return;
      intake.appendRow(r.slice(0, INTAKE_HEADER.length));
      // o que a planilha antiga já mandou não sai de novo (kit, agenda, aviso ao dono); a resposta já foi registrada
      chavesJaEnviadas(r[3]).concat([id + ':record', id + ':convidados', id + ':owner:notify']).forEach(function (k) {
        if (p.getProperty('sent:' + k) !== null) return;
        // o convite da agenda guarda o id do evento (Esquecer convidado apaga por ele); o resto, a data da importação
        var evento = k === id + ':calendar:invite' ? eventoDoConvidado_(r[2]) : '';
        p.setProperty('sent:' + k, evento || 'importado:' + agora);
      });
      // resposta retida (convite não confirmado) continua retida: o dono confirma aqui, como faria lá
      trazidos.push(r);
    });
    reconstruirAbaConvidados(briefingsDe_(antiga.ss));
    var fechado = fecharFormulariosDe_(antiga.ss), movidos = tirarDaListaAntiga_(antiga, trazidos);
    var linhas = [renderTemplate(t.done_rows, { n: trazidos.length }), t.done_sent,
      movidos ? t.done_moved : t.done_not_moved, fechado ? t.done_form : t.done_form_manual];
    return telaResultado(renderTemplate(t.done, { nome: antiga.ss.getName() }) + '\n\n' + linhas.join('\n'));
  } finally {
    lock.releaseLock();
  }
};

/** Evento que a planilha antiga criou (mesma conta, mesmo horário, convidado na lista) -> id, ou ''. */
function eventoDoConvidado_(intakeJson) {
  try {
    var it = JSON.parse(intakeJson), email = String((it.contacts && it.contacts.email) || '').toLowerCase();
    var ini = new Date(it.scheduled_at);
    if (!email || isNaN(ini.getTime())) return '';
    var evs = CalendarApp.getDefaultCalendar().getEvents(new Date(ini.getTime() - 60000), new Date(ini.getTime() + 60000));
    for (var i = 0; i < evs.length; i++) {
      if (evs[i].getStartTime().getTime() !== ini.getTime()) continue;
      var lista = evs[i].getGuestList().map(function (g) { return String(g.getEmail()).toLowerCase(); });
      if (lista.indexOf(email) >= 0) return evs[i].getId();
    }
  } catch (err) { console.error('evento da agenda não achado: ' + maskEmails_(err.message)); }
  return '';
}

/** {intake_id: {formula}|{rich}} da aba Convidados da planilha antiga (o briefing já preparado não se perde). */
function briefingsDe_(ss) {
  var out = {};
  try {
    var i18n = selectLocale(BUNDLE, loadMeta_().locale, allowUnreviewed_());
    var sh = ss.getSheetByName(i18n.sheet.tab);
    if (!sh || sh.getLastRow() < 2) return out;
    var cc = convidadosCols_(sh, i18n);
    for (var r = 2; r <= sh.getLastRow(); r++) {
      var id = sh.getRange(r, cc.id).getValue(), cell = sh.getRange(r, cc.briefing);
      if (!id) continue;
      var f = cell.getFormula();
      if (f) out[id] = { formula: f };
      else if (cell.getValue()) out[id] = { rich: cell.getRichTextValue() };
    }
  } catch (err) { console.error('briefings da planilha antiga: ' + maskEmails_(err.message)); }
  return out;
}

/** O formulário antigo para de aceitar respostas (uma resposta lá não chegaria aqui). -> true se fechou algum. */
function fecharFormulariosDe_(ss) {
  var fechou = false;
  ss.getSheets().forEach(function (sh) {
    var url = '';
    try { url = String(sh.getFormUrl() || ''); } catch (err) { url = ''; }
    if (!url) return;
    try { FormApp.openByUrl(url).setAcceptingResponses(false); fechou = true; }
    catch (err) { console.error('formulário antigo não fechado: ' + err.message); }
  });
  return fechou;
}

/**
 * Os registros trazidos saem da aba "intake" da planilha antiga para "intake (migrado)" (oculta): o código antigo,
 * que ainda roda lá, não manda o lembrete da véspera em dobro. Movidos, não apagados. -> true se moveu.
 */
function tirarDaListaAntiga_(antiga, trazidos) {
  if (!trazidos.length) return true;
  try {
    var ss = antiga.ss, destino = ss.getSheetByName(ABA_MIGRADO);
    if (!destino) { destino = ss.insertSheet(ABA_MIGRADO); destino.appendRow(INTAKE_HEADER); destino.hideSheet(); }
    var ids = trazidos.map(function (r) { return String(r[0]); }), sh = antiga.intake;
    var valores = sh.getDataRange().getValues();   // [0] = cabeçalho; linha i da lista = linha i+1 da aba
    for (var i = valores.length - 1; i >= 1; i--) {
      if (ids.indexOf(String(valores[i][0])) < 0) continue;
      destino.appendRow(valores[i].slice(0, INTAKE_HEADER.length));
      sh.deleteRow(i + 1);
    }
    return true;
  } catch (err) {
    console.error('registros antigos não movidos: ' + maskEmails_(err.message));
    return false;
  }
}

if (typeof module !== 'undefined') module.exports = { idDaPlanilha: idDaPlanilha, chavesJaEnviadas: chavesJaEnviadas };
