/**
 * drive.js — Google Drive SÓ com o escopo drive.file (PodFácil 2.2, item 9; decisão 4.1 do dono).
 *
 * O DriveApp exige o acesso TOTAL ao Drive, que o Google classifica como restrito e que trava a verificação do app.
 * Aqui o Drive é falado pela API REST v3 com o token do próprio script (ScriptApp.getOAuthToken): com drive.file, o
 * PodFácil só enxerga os arquivos que ele mesmo criou (o logo enviado pelo menu, por exemplo). Arquivo criado por
 * outro caminho (o briefing que o Claude gera no Docs) fica invisível: vira pendência com o link, nunca erro mudo.
 */

var DRIVE_API_ = 'https://www.googleapis.com/drive/v3/files/';
var DRIVE_UPLOAD_ = 'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id';
var LOGO_TIPOS = { 'image/png': [0x89, 0x50, 0x4E, 0x47], 'image/jpeg': [0xFF, 0xD8, 0xFF] };
var LOGO_MAX_BYTES = 1024 * 1024;   // vai embutido em cada convite: 1 MB sobra para um logo

function driveFetch_(url, opts) {
  opts = opts || {};
  opts.muteHttpExceptions = true;
  opts.headers = Object.assign({ Authorization: 'Bearer ' + ScriptApp.getOAuthToken() }, opts.headers || {});
  return UrlFetchApp.fetch(url, opts);
}

/** Conteúdo de um arquivo que o PodFácil criou (o logo). Arquivo de fora: erro claro, com o caminho para resolver. */
function driveBlob_(fileId) {
  var resp = driveFetch_(DRIVE_API_ + encodeURIComponent(fileId) + '?alt=media');
  if (resp.getResponseCode() === 200) {
    var blob = resp.getBlob(), tipo = String(blob.getContentType() || '');
    if (tipo.indexOf('image/') !== 0) throw new Error('o arquivo ' + fileId + ' do Drive não é imagem (' + tipo + ')');
    return blob.setName('logo.' + (tipo === 'image/jpeg' ? 'jpg' : 'png'));   // inlineImages pede o blob com nome
  }
  throw new Error('o logo do Drive (' + fileId + ') não abriu (HTTP ' + resp.getResponseCode() + '). O PodFácil só ' +
    'abre o logo enviado por ele: use PodFácil > Enviar logo, ou ponha um link https em brand.logo.url');
}

/**
 * Manda para a lixeira um arquivo do Drive, se o PodFácil puder vê-lo e ele for da conta que roda o script.
 * -> 'trashed' | 'not_mine' (de outra conta) | 'not_visible' (não foi criado pelo PodFácil, ou sumiu).
 */
function driveTrash_(fileId) {
  var meta = driveFetch_(DRIVE_API_ + encodeURIComponent(fileId) + '?fields=ownedByMe');
  if (meta.getResponseCode() !== 200) return 'not_visible';
  if (!JSON.parse(meta.getContentText()).ownedByMe) return 'not_mine';
  var r = driveFetch_(DRIVE_API_ + encodeURIComponent(fileId), { method: 'patch', contentType: 'application/json',
    payload: JSON.stringify({ trashed: true }) });
  if (r.getResponseCode() !== 200) throw new Error('lixeira do Drive respondeu HTTP ' + r.getResponseCode());
  return 'trashed';
}

/** Os primeiros bytes batem com o tipo declarado? (um .exe renomeado para .png não passa) */
function assinaturaConfere(bytes, mime) {
  var sig = LOGO_TIPOS[mime];
  if (!sig || !bytes || bytes.length < sig.length) return false;
  for (var i = 0; i < sig.length; i++) if ((bytes[i] & 255) !== sig[i]) return false;
  return true;
}

/** Cria o arquivo no Drive da conta (multipart: metadados + bytes). -> id. */
function driveCriarImagem_(nome, mime, bytes) {
  var boundary = 'podfacil' + Utilities.getUuid().replace(/-/g, '');
  var head = '--' + boundary + '\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n' +
    JSON.stringify({ name: nome, mimeType: mime }) + '\r\n--' + boundary + '\r\nContent-Type: ' + mime + '\r\n\r\n';
  var payload = Utilities.newBlob(head).getBytes().concat(bytes, Utilities.newBlob('\r\n--' + boundary + '--').getBytes());
  var r = driveFetch_(DRIVE_UPLOAD_, { method: 'post', contentType: 'multipart/related; boundary=' + boundary, payload: payload });
  if (r.getResponseCode() !== 200) throw new Error('o Drive não aceitou o logo (HTTP ' + r.getResponseCode() + ')');
  return JSON.parse(r.getContentText()).id;
}

if (typeof module !== 'undefined') {
  module.exports = { assinaturaConfere: assinaturaConfere, LOGO_MAX_BYTES: LOGO_MAX_BYTES };
}
