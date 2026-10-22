/**
 * Janelas de resultado do PodFácil (2.2, achado do teste de ponta a ponta): a caixa padrão do Google (ui.alert) só
 * mostra texto corrido, corta o link do formulário e não deixa copiar. Aqui o mesmo texto vira uma janela com o
 * visual do site: blocos espaçados, lista de situação com cor (✅ 🔧 ⚠️ ❌ ➖ ⏳), e cada link numa caixa com
 * "Copiar" e "Abrir". Perguntas, campo de texto e espera ficam no diálogo (dialogo.js), com este mesmo estilo.
 *
 * Puro (testado em node): corpoJanela, janelaHtml, alturaJanela. Lado Google: mostrar_.
 */

var JANELA_ICONES = { '✅': 'ok', '🔧': 'fixed', '⚠️': 'warn', '❌': 'fail', '➖': 'skip', '⏳': 'wait', '•': 'dot' };
var JANELA_URL = /(https:\/\/[^\s<>"']+)/g;

function escJanela_(s) {
  return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

/** Ícone de situação no começo da linha -> [ícone, classe, resto] ou null. */
function iconeDaLinha_(linha) {
  var s = String(linha).trim();
  var icones = Object.keys(JANELA_ICONES);
  for (var i = 0; i < icones.length; i++) {
    if (s.indexOf(icones[i]) === 0) return [icones[i], JANELA_ICONES[icones[i]], s.slice(icones[i].length).trim()];
  }
  return null;
}

/** Texto com links: o texto escapado; cada link numa caixa própria (endereço inteiro, Copiar, Abrir). */
function linhaComLinks_(texto, r) {
  var partes = String(texto).split(JANELA_URL), html = '';
  for (var i = 0; i < partes.length; i++) {
    var p = partes[i];
    if (!p) continue;
    if (i % 2 === 0) { html += escJanela_(p); continue; }
    var fim = (/[.,;:)\]]+$/.exec(p) || [''])[0], url = fim ? p.slice(0, -fim.length) : p;
    html += '<span class="link"><code>' + escJanela_(url) + '</code>' +
      '<button type="button" class="copiar" data-url="' + escJanela_(url) + '">' + escJanela_(r.copy) + '</button>' +
      '<a href="' + escJanela_(url) + '" target="_blank" rel="noopener">' + escJanela_(r.open) + '</a></span>' + escJanela_(fim);
  }
  return html;
}

/**
 * Texto das mensagens (o mesmo do i18n) -> HTML do corpo. Blocos separados por linha em branco; bloco em que toda
 * linha começa com ícone vira lista de situação; o 1º bloco é o destaque. Nada do texto vira HTML sem escapar.
 */
function corpoJanela(texto, r) {
  var blocos = String(texto == null ? '' : texto).replace(/\r/g, '').split(/\n\s*\n/)
    .map(function (b) { return b.trim(); }).filter(Boolean);
  return blocos.map(function (bloco, n) {
    var linhas = bloco.split('\n').map(function (l) { return l.trim(); }).filter(Boolean);
    if (iconeDaLinha_(linhas[0])) {   // lista de situação; linha sem ícone continua o item de cima (ex.: um link)
      var itens = [];
      linhas.forEach(function (l) {
        var ic = iconeDaLinha_(l);
        if (ic) itens.push(ic); else itens[itens.length - 1][2] += ' ' + l;
      });
      return '<ul class="st">' + itens.map(function (it) {
        return '<li class="' + it[1] + '"><span class="ic" aria-hidden="true">' + it[0] + '</span><span>' +
          linhaComLinks_(it[2], r) + '</span></li>';
      }).join('') + '</ul>';
    }
    return '<p class="' + (n === 0 ? 'lead' : '') + '">' + linhas.map(function (l) { return linhaComLinks_(l, r); }).join('<br>') + '</p>';
  }).join('');
}

/** Estilo das janelas (o mesmo da janela da licença). */
function cssJanela() {
  return ':root{--tinta:#17151F;--nevoa:#5E5A6B;--papel:#FAF6EE;--folha:#FFFDF8;--borda:#E4DDD0;--veludo:#7A1F3D;' +
    '--ok:#1E7B4A;--fixed:#1F5FA8;--warn:#9A6200;--fail:#C9302A}' +
    'body{margin:0;padding:18px 22px 76px;font:15px/1.55 "Bricolage Grotesque",Arial,sans-serif;color:var(--tinta);background:var(--folha)}' +
    'p{margin:0 0 14px}p.lead{font-size:16px;font-weight:600}' +
    'ul.st{list-style:none;margin:0 0 14px;padding:0;border:1px solid var(--borda);border-radius:12px;background:var(--papel);overflow:hidden}' +
    'ul.st li{display:flex;gap:10px;padding:10px 14px;border-top:1px solid var(--borda)}ul.st li:first-child{border-top:0}' +
    'ul.st li>span:last-child{flex:1;min-width:0}.ic{flex:0 0 auto}' +
    'li.ok{border-left:4px solid var(--ok)}li.fixed{border-left:4px solid var(--fixed)}' +
    'li.warn{border-left:4px solid var(--warn)}li.fail{border-left:4px solid var(--fail)}' +
    'li.skip,li.wait,li.dot{border-left:4px solid var(--borda)}' +
    '.link{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:8px 0 2px;padding:8px 10px;border:1px solid var(--borda);' +
    'border-radius:10px;background:#fff}' +
    '.link code{flex:1 1 220px;min-width:0;overflow-wrap:anywhere;font:12.5px/1.4 Menlo,monospace;color:var(--nevoa)}' +
    '.link button,.link a{flex:0 0 auto;font:600 13px Arial,sans-serif;padding:6px 12px;border-radius:999px;cursor:pointer;text-decoration:none}' +
    // Copiar/Abrir são opcionais: discretos (contorno e link); o único botão cheio é o principal, embaixo
    '.link button{border:1px solid var(--veludo);background:#fff;color:var(--veludo)}' +
    '.link a{border:0;padding:6px 4px;color:var(--veludo);text-decoration:underline}' +
    '.fim{position:fixed;left:0;right:0;bottom:0;padding:12px 22px;background:var(--folha);border-top:1px solid var(--borda);text-align:right}' +
    '.fim button{font:600 14px Arial,sans-serif;padding:9px 26px;border:0;border-radius:999px;background:var(--veludo);color:#fff;cursor:pointer}' +
    'button:focus-visible,a:focus-visible{outline:3px solid #F2B33D;outline-offset:2px}';
}

/** Script do botão "Copiar" (vale para links que aparecem depois, como na janela da licença). */
function scriptCopiar(r) {
  return 'document.addEventListener("click",function(ev){var b=ev.target;if(!b||!b.classList||!b.classList.contains("copiar"))return;' +
    'var u=b.getAttribute("data-url"),t=document.createElement("textarea");t.value=u;document.body.appendChild(t);t.select();' +
    'var ok=false;try{ok=document.execCommand("copy");}catch(e){}document.body.removeChild(t);' +
    'if(!ok&&navigator.clipboard){navigator.clipboard.writeText(u);}b.textContent=' + JSON.stringify(String(r.copied)) + ';' +
    'setTimeout(function(){b.textContent=' + JSON.stringify(String(r.copy)) + ';},2000);});';
}

/** Página inteira da janela (visual do site: papel, veludo, Bricolage/Arial). */
function janelaHtml(texto, r) {
  return '<!DOCTYPE html><html><head><base target="_top"><meta charset="utf-8"><style>' + cssJanela() +
    '</style></head><body>' + corpoJanela(texto, r) +
    '<div class="fim"><button type="button" id="ok" autofocus>' + escJanela_(r.ok) + '</button></div>' +
    '<script>document.getElementById("ok").addEventListener("click",function(){google.script.host.close();});' +
    scriptCopiar(r) + '</script></body></html>';
}

/** Altura que cabe o texto sem barra de rolagem na maioria dos casos (a janela rola se precisar). */
function alturaJanela(texto) {
  var s = String(texto || ''), linhas = s.split('\n').length, longas = Math.floor(s.length / 70), links = (s.match(JANELA_URL) || []).length;
  return Math.max(200, Math.min(600, 120 + (linhas + longas) * 24 + links * 46));
}

/** Mostra o resultado de uma opção do menu. Sem tela de HTML (raro), cai na caixa padrão do Google. */
function mostrar_(titulo, texto) {
  var ui = SpreadsheetApp.getUi();
  try { SpreadsheetApp.flush(); } catch (err) { /* a gravação aparece na planilha antes da janela */ }
  try {
    var r = menuI18n_().menu.window;
    ui.showModalDialog(HtmlService.createHtmlOutput(janelaHtml(texto, r)).setWidth(560).setHeight(alturaJanela(texto)), titulo);
  } catch (err) {
    ui.alert(titulo, texto, ui.ButtonSet.OK);
  }
}

if (typeof module !== 'undefined') module.exports = { corpoJanela: corpoJanela, janelaHtml: janelaHtml, alturaJanela: alturaJanela, cssJanela: cssJanela };
