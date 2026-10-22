/**
 * Diálogo único do PodFácil (2.2.1, achados do teste de ponta a ponta): pergunta, campo de texto, espera com
 * progresso e resultado na MESMA janela e no mesmo visual (janela.js). Substitui ui.alert(SIM/NÃO) e ui.prompt,
 * que o Google desenha do jeito dele, e mostra que o PodFácil está trabalhando nas opções lentas (criar o
 * formulário leva 1-2 min).
 *
 * Tela = {tipo: 'resultado'|'pergunta'|'entrada'|'espera', texto, ...}:
 *   pergunta: sim {rotulo, passo, args?, espera?}, nao {rotulo, passo?, args?}   (sem passo: fecha)
 *   entrada:  rotulo (do campo), erro?, sim {...}, nao {...}                   (o valor vai em args.valor)
 *   espera:   passo, args                                                       (chama o passo e mostra a próxima tela)
 * O navegador só chama podfacilPasso(nome, args); os passos ficam em PASSOS_ (lista fechada) e sempre devolvem tela.
 */

// arquivos do Apps Script rodam numa ordem que não controlamos: quem chegar primeiro cria, ninguém zera
var PASSOS_ = PASSOS_ || {};

/** Abre o diálogo já na 1ª tela (normalmente uma espera que chama o 1º passo). */
function abrirDialogo_(titulo, tela) {
  var w = menuI18n_().menu.window;
  try {
    SpreadsheetApp.getUi().showModalDialog(
      HtmlService.createHtmlOutput(dialogoHtml(prepararTela_(tela, w), w)).setWidth(560).setHeight(470), titulo);
  } catch (err) {   // sem tela de HTML (raro): o texto da tela na caixa padrão
    SpreadsheetApp.getUi().alert(titulo, String(tela.texto || ''), SpreadsheetApp.getUi().ButtonSet.OK);
  }
}

/** Ponto único que o navegador chama. Passo desconhecido ou erro: tela de resultado com o motivo, nunca uma exceção crua. */
function podfacilPasso(nome, args) {
  var w = menuI18n_().menu.window;
  try {
    if (!Object.prototype.hasOwnProperty.call(PASSOS_, nome)) throw new Error('passo desconhecido: ' + nome);
    try { SpreadsheetApp.flush(); } catch (err) { /* sem planilha ativa */ }
    var tela = PASSOS_[nome](args || {});
    try { SpreadsheetApp.flush(); } catch (err) { /* o que foi gravado aparece antes da próxima tela */ }
    return prepararTela_(tela, w);
  } catch (err) {
    console.error('passo ' + nome + ': ' + maskEmails_(err.message));
    return prepararTela_(telaResultado(renderTemplate(menuI18n_().menu.error, { motivo: maskEmails_(err.message) })), w);
  }
}

function telaResultado(texto) { return { tipo: 'resultado', texto: String(texto || '') }; }
function telaEspera(texto, passo, args) { return { tipo: 'espera', texto: texto, passo: passo, args: args || {} }; }
function telaPergunta(texto, sim, nao) { return { tipo: 'pergunta', texto: texto, sim: sim, nao: nao }; }
function telaEntrada(texto, rotulo, sim, nao, erro) { return { tipo: 'entrada', texto: texto, rotulo: rotulo, sim: sim, nao: nao, erro: erro || '' }; }

/** Texto -> HTML escapado no servidor (corpoJanela); o navegador só encaixa o que já veio pronto. */
function prepararTela_(tela, w) {
  var t = JSON.parse(JSON.stringify(tela || telaResultado('')));
  t.html = corpoJanela(t.texto, w);
  if (t.erro) t.erroHtml = corpoJanela(t.erro, w);
  if (t.sim && t.sim.espera) t.sim.esperaHtml = corpoJanela(t.sim.espera, w);
  delete t.texto;
  delete t.erro;
  return t;
}

/** Página do diálogo: mesmo estilo das janelas (cssJanela), botão principal cheio, o outro só com contorno. */
function dialogoHtml(tela, w) {
  var js = function (v) { return JSON.stringify(v).replace(/</g, '\\u003c').replace(/[\u2028\u2029]/g, ''); };
  return '<!DOCTYPE html><html><head><base target="_top"><meta charset="utf-8"><style>' + cssJanela() +
    'label{display:block;font-weight:600;margin:4px 0 6px}' +
    'input#v{width:100%;box-sizing:border-box;padding:10px 12px;font:15px Menlo,monospace;border:1px solid var(--borda);' +
    'border-radius:10px;background:#fff}input#v:focus{outline:3px solid #F2B33D;border-color:var(--veludo)}' +
    '.erro{color:var(--fail);margin-top:10px}.erro p{margin:0}' +
    '.fim button.sec{background:transparent;color:var(--veludo);border:1px solid var(--veludo);margin-right:8px}' +
    '.fim button:disabled{opacity:.55;cursor:default}' +
    '.esp{display:flex;align-items:center;gap:12px;margin-top:6px;color:var(--nevoa)}' +
    '.roda{width:22px;height:22px;border:3px solid var(--borda);border-top-color:var(--veludo);border-radius:50%;animation:g 1s linear infinite}' +
    '@keyframes g{to{transform:rotate(360deg)}}' +
    '</style></head><body><div id="corpo" role="status" aria-live="polite"></div>' +
    '<div class="fim" id="fim"></div>' +
    '<script>var W=' + js(w) + ',T0=' + js(tela) + ';' +
    'var C=document.getElementById("corpo"),F=document.getElementById("fim"),relogio=null;' +
    'function bt(r,cls,fn){var b=document.createElement("button");b.type="button";b.textContent=r;if(cls)b.className=cls;' +
    'b.addEventListener("click",fn);F.appendChild(b);return b;}' +
    'function fechar(){google.script.host.close();}' +
    'function ir(op,valor){if(!op||!op.passo){fechar();return;}var a=JSON.parse(JSON.stringify(op.args||{}));' +
    'if(valor!==undefined)a.valor=valor;mostra({tipo:"espera",html:op.esperaHtml||"",passo:op.passo,args:a});}' +
    'function mostra(t){if(relogio){clearInterval(relogio);relogio=null;}F.textContent="";C.innerHTML=t.html||"";' +
    'if(t.tipo==="resultado"){bt(W.ok,"",fechar).focus();return;}' +
    'if(t.tipo==="pergunta"){bt(t.nao.rotulo,"sec",function(){ir(t.nao);});bt(t.sim.rotulo,"",function(){ir(t.sim);}).focus();return;}' +
    'if(t.tipo==="entrada"){var l=document.createElement("label");l.htmlFor="v";l.textContent=t.rotulo;var i=document.createElement("input");' +
    'i.id="v";i.autocomplete="off";i.spellcheck=false;C.appendChild(l);C.appendChild(i);' +
    'if(t.erroHtml){var e=document.createElement("div");e.className="erro";e.innerHTML=t.erroHtml;C.appendChild(e);}' +
    'var ok=function(){var v=i.value.trim();if(v)ir(t.sim,v);};' +
    'bt(t.nao.rotulo,"sec",function(){ir(t.nao);});bt(t.sim.rotulo,"",ok);' +
    'i.addEventListener("keydown",function(ev){if(ev.key==="Enter")ok();});i.focus();return;}' +
    // espera: roda + segundos; chama o passo e mostra o que voltar
    'var d=document.createElement("div");d.className="esp";var r=document.createElement("div");r.className="roda";' +
    'var s=document.createElement("span");s.textContent=W.working;d.appendChild(r);d.appendChild(s);C.appendChild(d);' +
    'var ini=Date.now();relogio=setInterval(function(){s.textContent=W.working+" "+Math.round((Date.now()-ini)/1000)+" s";},1000);' +
    'google.script.run.withSuccessHandler(mostra).withFailureHandler(function(err){' +
    'mostra({tipo:"resultado",html:"<p class=\\"lead\\"></p>"});C.firstChild.textContent=W.failed;}).podfacilPasso(t.passo,t.args);}' +
    'mostra(T0);' + scriptCopiar(w) + '</script></body></html>';
}

if (typeof module !== 'undefined') module.exports = { dialogoHtml: dialogoHtml, telaResultado: telaResultado };
