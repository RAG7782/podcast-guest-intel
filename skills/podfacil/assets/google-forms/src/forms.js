/**
 * forms.js — lado Google, parte 1: configuração, criação do Formulário e instalação dos gatilhos.
 * Funções que o usuário roda pelo botão "Executar" do editor: criarFormularioEssencial,
 * criarFormularioCompleto. Toda a lógica de conteúdo vem de core.js (buildFormSpec).
 */

var PROP_SHOW = 'SHOW_PROFILE_JSON';

function props_() {
  return PropertiesService.getScriptProperties();
}

/** show-profile: propriedade SHOW_PROFILE_JSON, ou variável SHOW_PROFILE num arquivo config.gs. */
function loadShow_() {
  var raw = props_().getProperty(PROP_SHOW);
  if (raw) {
    try {
      return JSON.parse(raw);
    } catch (e) {
      throw new Error(PROP_SHOW + ' não é JSON válido (' + e.message + '); início: ' + JSON.stringify(raw.slice(0, 40)));
    }
  }
  if (typeof SHOW_PROFILE !== 'undefined') return SHOW_PROFILE;
  throw new Error('config ausente: defina a propriedade ' + PROP_SHOW + ' ou a variável SHOW_PROFILE em config.gs');
}

function loadMeta_() {
  var raw = props_().getProperty('FORM_META');
  if (!raw) throw new Error('FORM_META ausente: rode criarFormularioEssencial ou criarFormularioCompleto primeiro');
  return JSON.parse(raw);
}

function allowUnreviewed_() {
  return props_().getProperty('ALLOW_UNREVIEWED_LOCALE') === 'true';
}

function criarFormularioEssencial() {
  return buildForm('essencial', null);
}

/** Variante completa (sem marca) é do plano pago: confere a chave antes de criar (licenca.js). */
function criarFormularioCompleto() {
  exigirLicenca_('formulario-completo-e-automacoes');
  return buildForm('completo', null);
}

/** Cria Form + planilha + aba "intake", grava o mapa de itens e instala os gatilhos. */
function buildForm(variant, locale) {
  var show = loadShow_();
  var loc = locale || props_().getProperty('LOCALE') || show.locale;
  var jurisdiction = props_().getProperty('JURISDICTION') || show.jurisdiction || 'BR-LGPD';
  var i18n = selectLocale(BUNDLE, loc, allowUnreviewed_());
  var spec = buildFormSpec({ i18n: i18n, show: show, variant: variant, jurisdiction: jurisdiction, variants: BUNDLE.variants });
  var form = FormApp.create(spec.title).setDescription(spec.description).setConfirmationMessage(spec.confirmation);
  var itemMap = {};
  spec.items.forEach(function (it) { addItem_(form, it, itemMap); });
  var ss = linkSpreadsheet_(form, spec.title);
  publish_(form);
  props_().setProperties({
    FORM_ID: form.getId(), FORM_URL: form.getPublishedUrl(), SHEET_ID: ss.getId(), FORM_ITEM_MAP: JSON.stringify(itemMap),
    FORM_META: JSON.stringify({ variant: variant, locale: loc, jurisdiction: jurisdiction,
      clause_id: spec.clause_id, text_version: spec.text_version })
  });
  installTriggers_(form);
  props_().deleteProperty('CONVIDADOS_SHEET_ID');   // planilha nova: a aba Convidados nasce nela, antes de tudo
  try {
    convidadosSheet_(i18n);
    ss.getSheetByName('intake').hideSheet();   // o registro técnico fica oculto; o dono vê só a aba legível
  } catch (err) { console.error('aba Convidados: ' + err.message + '; rode reconstruirAbaConvidados depois'); }
  console.log('Formulário pronto. Link para o convidado: ' + form.getPublishedUrl() +
    '\nEditar: ' + form.getEditUrl() + '\nRespostas: ' + ss.getUrl());
  return form.getPublishedUrl();
}

function addItem_(form, it, itemMap) {
  if (it.type === 'section') {
    var big = ['section.consent', 'section.sensitive', 'section.localization'].indexOf(it.key) >= 0;
    (big ? form.addPageBreakItem() : form.addSectionHeaderItem()).setTitle(it.title).setHelpText(it.help || '');
    return;
  }
  var item = createItem_(form, it);
  item.setTitle(it.title).setHelpText(it.help || '').setRequired(!!it.required);
  var choices = {};
  (it.choices || []).forEach(function (c) { choices[c.label] = c.value; });
  itemMap[String(item.getId())] = { key: it.key, choices: choices };
}

function createItem_(form, it) {
  var labels = (it.choices || []).map(function (c) { return c.label; });
  switch (it.type) {
    case 'text': return form.addTextItem();
    case 'email': return form.addTextItem().setValidation(FormApp.createTextValidation().requireTextIsEmail().build());
    case 'url': return form.addTextItem().setValidation(FormApp.createTextValidation().requireTextIsUrl().build());
    case 'paragraph': return form.addParagraphTextItem();
    case 'choice': return form.addMultipleChoiceItem().setChoiceValues(labels);
    case 'checkbox': return form.addCheckboxItem().setChoiceValues(labels);
    case 'datetime': return form.addDateTimeItem();
    default: throw new Error('tipo de item "' + it.type + '" (' + it.key + '); esperado text|email|url|paragraph|choice|checkbox|datetime');
  }
}

function linkSpreadsheet_(form, title) {
  var ss = SpreadsheetApp.create(title + ' (respostas)');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());
  var sheet = ss.insertSheet('intake');
  sheet.appendRow(['intake_id', 'submitted_at', 'intake_json', 'resultado_envios', 'descartados']);
  return ss;
}

/** setPublished existe só em forms que suportam publicação; o padrão é publicado. */
function publish_(form) {
  if (form.supportsAdvancedResponderPermissions() && !form.isPublished()) form.setPublished(true);
}

/** Um gatilho onFormSubmit + um diário (D-1). Remove os antigos destes handlers (sem duplicar). */
function installTriggers_(form) {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    var h = t.getHandlerFunction();
    if (h === 'onFormSubmit' || h === 'lembreteDiario') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('onFormSubmit').forForm(form).onFormSubmit().create();
  var hour = Number(props_().getProperty('REMINDER_HOUR') || 9);
  ScriptApp.newTrigger('lembreteDiario').timeBased().everyDays(1).atHour(hour).create();
}
