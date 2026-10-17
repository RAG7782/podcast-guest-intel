/**
 * admission.js — lado Google, parte 3: o que serializa e o que admite (varredura do Codex Security, 2026-10-10).
 * withScriptLock_: check-and-set atômico das chaves de idempotência (sent:*) entre execuções do gatilho.
 * Código de convite (Codex #5): o enviarConvite gera 1 código por convidado, embute no link pré-preenchido do
 * Form e guarda só o sha256 (invite:<hash>), ligado ao e-mail, com validade; o onFormSubmit o consome 1 vez.
 * Sem código válido, o envio fica retido para o host (confirmarIntake). O invited:<email> não admite mais nada.
 */

var INVITE_TTL_DAYS = 30;   // ponytail: validade fixa do código; virar Script Property se um host convidar com mais antecedência

/** Roda fn com o ScriptLock do projeto (espera até 10 s; sem o lock, lança em vez de seguir sem proteção). */
function withScriptLock_(fn) {
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    return fn();
  } finally {
    lock.releaseLock();
  }
}

function normEmail_(email) {
  return String(email || '').trim().toLowerCase();
}

function tokenHash_(token) {
  return Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, String(token), Utilities.Charset.UTF_8)
    .map(function (b) { return ('0' + ((b + 256) % 256).toString(16)).slice(-2); }).join('');
}

/** Gera o código do convidado (122+122 bits do getUuid), guarda só o hash e devolve o link do Form pré-preenchido. */
function issueInviteLink_(email) {
  var token = (Utilities.getUuid() + Utilities.getUuid()).replace(/-/g, '');
  props_().setProperty('invite:' + tokenHash_(token), JSON.stringify({ email: normEmail_(email),
    exp: Date.now() + INVITE_TTL_DAYS * 86400000 }));
  return prefilledUrl_(token);
}

function prefilledUrl_(token) {
  var map = JSON.parse(props_().getProperty('FORM_ITEM_MAP') || '{}');
  var id = Object.keys(map).filter(function (k) { return map[k].key === 'invite.token'; })[0];
  if (!id) throw new Error('formulário sem o campo invite.token no FORM_ITEM_MAP; esperado rodar criarFormulario* de novo');
  var form = FormApp.openById(props_().getProperty('FORM_ID'));
  var answer = form.getItemById(Number(id)).asTextItem().createResponse(token);
  return form.createResponse().withItemResponse(answer).toPrefilledUrl();
}

/** Consome o código: vale 1 vez (a reexecução da MESMA resposta passa), até expirar, só para o e-mail convidado. */
function admitByToken_(token, email, responseId) {
  if (!token) return false;
  var key = 'invite:' + tokenHash_(String(token).trim());
  return withScriptLock_(function () {
    var rec = JSON.parse(props_().getProperty(key) || 'null');
    if (!rec || rec.email !== normEmail_(email) || Date.now() > rec.exp) return false;
    if (rec.used && rec.used !== responseId) return false;
    rec.used = responseId;
    props_().setProperty(key, JSON.stringify(rec));
    return true;
  });
}

/** Códigos vencidos saem das Script Properties (o espaço total é limitado); roda no gatilho diário. */
function expireInvites_(nowMs) {
  var p = props_();
  p.getKeys().filter(function (k) { return k.indexOf('invite:') === 0; }).forEach(function (k) {
    var rec = {};
    try { rec = JSON.parse(p.getProperty(k)); } catch (err) { console.error('código de convite ilegível (' + err.message + '); removido'); }
    if (!(rec.exp > nowMs)) p.deleteProperty(k);
  });
}

/** Linha da aba intake admitida: não retida, ou retida e aprovada pelo host (confirmarIntake). */
function admittedRow_(row, store) {
  return String(row[3] || '').indexOf('"status":"held"') < 0 || store.has(row[0] + ':admitted');
}

/**
 * Envio sem código de convite válido: nada sai ao convidado nem ao dono na hora (só o resumo diário agregado).
 * Até HELD_MAX_ROWS retidos abertos, a linha fica para o host confirmar; acima, a resposta some do Forms e da
 * planilha ligada sem criar linha nem chave (um envio em massa pelo link não esgota cota nem armazenamento).
 */
function holdSubmission_(response, intake, res, policy, store, rawGone) {
  var result = heldResult_(intake, policy);
  var keep = withScriptLock_(function () { return noteHeld_(intake.intake_id); });
  if (!keep) {
    if (!rawGone) discardRaw_(response, intake);   // a sensível sem aceite já apagou a resposta crua
    return [{ key: result.key, status: 'skipped', reason: 'descartado: teto de ' + HELD_MAX_ROWS + ' retidos abertos' }];
  }
  if (store.claim(intake.intake_id + ':record')) {
    intakeSheet_().appendRow([intake.intake_id, intake.submitted_at, JSON.stringify(intake), JSON.stringify([result]), JSON.stringify(res.dropped)]);
    store.set(intake.intake_id + ':record', new Date().toISOString());
  }
  return [result];
}

/** Conta o retido no resumo diário (sob lock). true se ainda cabe uma linha retida (abaixo do teto). */
function noteHeld_(intakeId) {
  var p = props_(), d = JSON.parse(p.getProperty('held_digest') || '{"count":0,"ids":[],"discarded":0}');
  var open = intakeSheet_().getDataRange().getValues().slice(1).filter(function (r) { return !admittedRow_(r, store_()); }).length;
  var keep = open < HELD_MAX_ROWS;
  d.count++;
  if (!keep) d.discarded = (d.discarded || 0) + 1;
  else if (d.ids.length < HELD_MAX_ROWS) d.ids.push(intakeId);
  p.setProperty('held_digest', JSON.stringify(d));
  return keep;
}

/** Campos sensíveis cujo descarte (sem aceite específico, LGPD art. 11, I) apaga também a resposta crua (Codex #1). */
var SENSITIVE_DROPS = ['sensitive', 'accessibility'];

/** Apaga a resposta crua (Forms + linha da planilha ligada) deste envio; o valor nunca vai para log. */
function discardRaw_(response, intake) {
  var formId = props_().getProperty('FORM_ID');
  if (formId) FormApp.openById(formId).deleteResponse(response.getId());
  return deleteLinkedRows_(intake.contacts && intake.contacts.email, intake.submitted_at, true);
}
