/**
 * licenca.js — chave do plano pago no Apps Script: formulário completo e automações pós-envio
 * (e-mail com kit, WhatsApp, agenda, lembrete D-1). Convite, formulário essencial, aviso ao dono,
 * esquecerTitular e a retenção LGPD NUNCA dependem da licença.
 *
 * A chave fica em Propriedades do script (PODFACIL_LICENSE_KEY), nunca no código. O endereço do
 * servidor vem de BUNDLE.produto (references/contracts/produto.json, fonte única). Resultado positivo fica em
 * cache (Script Property licenca_cache): revalida depois de licenca_revalidar_horas e vale até
 * licenca_offline_horas se o servidor não responder. Recusa explícita do servidor nunca usa o cache.
 *
 * HTTP: o Apps Script fixa o User-Agent ("Google-Apps-Script", doc do URL Fetch Service) e não
 * aceita timeout no UrlFetchApp; o cliente se identifica pelo header X-PodFacil-Cliente.
 *
 * ponytail: este gate é contornável por quem editar o código aberto colado no próprio projeto; o
 * gate real é o do servidor. Se a fraude passar a importar, mover as automações para o MCP.
 */

var LICENCA_PROP = 'PODFACIL_LICENSE_KEY';
var DISPOSITIVO_PROP = 'PODFACIL_DEVICE_ID';
var LICENCA_CACHE_PROP = 'licenca_cache';

function licencaNegadaMsg_(recurso, motivo) {
  return 'O recurso "' + recurso + '" é do plano pago do PodFácil: ' + motivo + '. Planos e assinatura: ' +
    BUNDLE.produto.precos + '. Já tem a chave? Em Configurações do projeto > Propriedades do script, crie ' +
    LICENCA_PROP + ' com a chave (nunca no código) e ' + DISPOSITIVO_PROP +
    ' com o mesmo X-Device-Id do seu conector MCP (assim o plano conta 1 dispositivo).';
}

function dispositivo_() {
  var p = props_(), id = p.getProperty(DISPOSITIVO_PROP);
  if (!id) {
    id = 'dev_' + Utilities.getUuid().replace(/-/g, '').slice(0, 16);
    p.setProperty(DISPOSITIVO_PROP, id);
  }
  return id;
}

function chaveHash_(key) {
  return Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, key, Utilities.Charset.UTF_8)
    .slice(0, 8).map(function (b) { return ('0' + (b & 255).toString(16)).slice(-2); }).join('');
}

/** Cache positivo desta chave com idade em horas, ou null. */
function licencaCache_(key) {
  var raw = props_().getProperty(LICENCA_CACHE_PROP);
  if (!raw) return null;
  var doc;
  try { doc = JSON.parse(raw); } catch (err) {
    console.error('licenca_cache ilegível (' + err.message + '); ignorado');
    return null;
  }
  if (doc.chave !== chaveHash_(key)) return null;
  doc.idadeH = (Date.now() - Date.parse(doc.confirmado_em)) / 3600000;
  return doc;
}

/** {answer} da tool licenca_status, ou {indisponivel: motivo} (rede, 5xx, 429, formato). */
function perguntarServidor_(key) {
  var rpc = { jsonrpc: '2.0', id: 1, method: 'tools/call', params: { name: 'licenca_status', arguments: {} } };
  var resp;
  try {
    resp = UrlFetchApp.fetch(BUNDLE.produto.servidor_mcp, { method: 'post', contentType: 'application/json',
      payload: JSON.stringify(rpc), muteHttpExceptions: true,
      headers: { Authorization: 'Bearer ' + key, 'X-Device-Id': dispositivo_(), 'X-PodFacil-Cliente': 'apps-script' } });
  } catch (err) {
    return { indisponivel: 'rede: ' + err.message };
  }
  var code = resp.getResponseCode(), body = resp.getContentText();
  if (code === 401) return { answer: { error: 'license_unknown', message: 'chave de licença não reconhecida pelo servidor' } };
  if (code !== 200) return { indisponivel: 'HTTP ' + code + ': ' + body.slice(0, 200) };
  try {
    return { answer: JSON.parse(body).result.structuredContent || {} };
  } catch (err) {
    return { indisponivel: 'resposta fora do JSON-RPC (' + err.message + '): ' + body.slice(0, 200) };
  }
}

/** {ok: true, plano} ou {ok: false, motivo}. Chave errada nunca vira "ok" pelo cache. */
function licencaPaga_() {
  var key = (props_().getProperty(LICENCA_PROP) || '').trim(), cfg = BUNDLE.produto;
  if (!key) return { ok: false, motivo: 'nenhuma chave em ' + LICENCA_PROP };
  var cache = licencaCache_(key);
  if (cache && cache.idadeH < cfg.licenca_revalidar_horas) return { ok: true, plano: cache.plano };
  var r = perguntarServidor_(key);
  if (r.indisponivel) {
    if (cache && cache.idadeH < cfg.licenca_offline_horas) return { ok: true, plano: cache.plano, offline: r.indisponivel };
    return { ok: false, motivo: 'não consegui confirmar a licença agora (' + r.indisponivel + ')' };
  }
  var info = r.answer.result || {};
  if (r.answer.error) return { ok: false, motivo: r.answer.message || r.answer.error };
  if (info.tier !== 'paid') return { ok: false, motivo: 'a chave está no plano ' + (info.plan || 'free') };
  props_().setProperty(LICENCA_CACHE_PROP, JSON.stringify({ chave: chaveHash_(key), plano: info.plan,
    confirmado_em: new Date().toISOString() }));
  return { ok: true, plano: info.plan };
}

/** Para com a mensagem de como assinar/configurar (usado antes de criar o formulário completo). */
function exigirLicenca_(recurso) {
  var r = licencaPaga_();
  if (!r.ok) throw new Error(licencaNegadaMsg_(recurso, r.motivo));
  return r.plano;
}

/** Automações pós-envio liberadas? Sem licença, loga o motivo e devolve false (o resto segue). */
function automacoesLiberadas_() {
  var r = licencaPaga_();
  if (!r.ok) console.error(licencaNegadaMsg_('formulario-completo-e-automacoes', r.motivo));
  return r.ok;
}

/** Envio pulado por falta de licença: entra no relatório do dono, não some. */
function semLicencaResultado_(intakeId) {
  return { key: intakeId + ':automacoes', status: 'skipped',
    reason: 'automações pós-envio são do plano pago; sem licença válida (veja o log). Assine: ' + BUNDLE.produto.precos };
}

