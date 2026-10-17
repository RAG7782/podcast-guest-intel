/**
 * drive-logo.js — OPCIONAL. Cole só se o logo estiver no seu Google Drive (brand.logo.drive_file_id).
 * Este arquivo faz o Apps Script pedir o escopo do Drive na autorização; com brand.logo.url ele não é preciso.
 * O logo vai embutido no e-mail (inlineImages, <img src="cid:showlogo">), sem depender de link público.
 */
function logoBlobFromDrive_(fileId) {
  return DriveApp.getFileById(fileId).getBlob();
}
