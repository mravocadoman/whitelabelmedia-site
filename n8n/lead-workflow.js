// Source of the n8n workflow "White Label Media — leads" (n8n Workflow SDK).
// Kept in the repo so the form and the workflow change together; the live copy is in n8n.
import { workflow, node, trigger, expr } from '@n8n/workflow-sdk';

const hook = trigger({
  type: 'n8n-nodes-base.webhook',
  version: 2.1,
  config: {
    name: 'Lead from whitelabelmedia.eu',
    parameters: { httpMethod: 'POST', path: 'wlm-lead', responseMode: 'responseNode', options: { rawBody: true } },
  },
});

const gate = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Parse and gate',
    parameters: {
      mode: 'runOnceForAllItems',
      jsCode: `// The site posts text/plain (no CORS preflight), so the body arrives as a string.
// The key ships in client JS, so it only stops drive-by noise. Never read $env here.
const KEY = 'wlm-eu-2026';
const NL = String.fromCharCode(10);
const ORIGINS = ['https://whitelabelmedia.eu', 'https://www.whitelabelmedia.eu', 'http://localhost:4174', 'http://127.0.0.1:4174'];
const inp = $input.first().json;
if ((inp.query || {}).k !== KEY) throw new Error('bad key');
let body = inp.body;
if (typeof body === 'string') { try { body = JSON.parse(body); } catch (e) { throw new Error('bad body'); } }
body = body || {};
if (body.website) throw new Error('honeypot');
if (Number(body.t) > 0 && Number(body.t) < 3000) throw new Error('too fast');
if (body.consent !== true) throw new Error('no consent');

// Public webhook: every value is cut to size before it goes anywhere.
const clip = (v, n) => String(v == null ? '' : v).trim().slice(0, n);
const list = (v, n) => (Array.isArray(v) ? v : []).slice(0, 15).map((x) => clip(x, n)).filter(Boolean).join(', ');
const name = clip(body.name, 100);
const email = clip(body.email, 254);
const at = email.indexOf('@');
if (at < 1 || email.lastIndexOf('.') < at + 2 || email.includes(' ')) throw new Error('bad email');
if (!name) throw new Error('no name');
const agency = clip(body.agency, 120);
if (!agency) throw new Error('no agency');

const MODELS = { 'white-label': 'White label', referral: 'Referral', 'not-sure': 'Not sure yet' };
const row = {
  agency, name, email,
  role: clip(body.role, 80),
  phone: clip(body.phone, 40),
  channel: clip(body.channel, 20),
  site: clip(body.site, 200),
  country: clip(body.country, 40),
  team: clip(body.team, 20),
  offers: list(body.offers, 40),
  model: MODELS[body.model] || '',
  channels: list(body.channels, 40),
  accounts: clip(body.accounts, 20),
  spend: clip(body.spend, 40),
  start: clip(body.start, 40),
  price: Math.max(0, Math.min(100000, Math.round(Number(body.price) || 0))),
  calc: clip(body.calc, 300),
  nda: body.nda === true,
  message: clip(body.message, 3000),
  source: clip(body.source, 200),
  page: clip(body.page, 300),
  consent_at: new Date().toISOString(),
  status: 'new',
  raw: JSON.stringify(body).slice(0, 8000),
};

const line = (k, v) => (v ? k + ': ' + v + NL : '');
const subject = 'White Label Media request: ' + agency + (row.country ? ' (' + row.country + ')' : '') + ' | ' + (row.model || 'model?') + (row.accounts ? ', ' + row.accounts + ' accounts' : '');
const detail =
  line('Agency', agency) + line('Website', row.site) + line('Country', row.country) + line('Team size', row.team) + line('Offers today', row.offers) +
  NL + line('Model', row.model) + line('Channels', row.channels) + line('Accounts to start', row.accounts) + line('Ad spend per client', row.spend) +
  line('Start', row.start) + line('Bills clients (per month)', row.price ? 'EUR ' + row.price : '') + line('Calculator', row.calc) + line('NDA first', row.nda ? 'yes' : '') +
  NL + line('Contact', name + (row.role ? ', ' + row.role : '')) + line('E-mail', email) + line('Phone / WhatsApp', row.phone) + line('Prefers', row.channel) +
  (row.message ? NL + row.message + NL : '') + NL + line('Source', row.source) + line('Page', row.page);
const alert = '🏷️ New partner request' + NL + agency + (row.country ? ' (' + row.country + ')' : '') + ' | ' + (row.model || '-') +
  (row.accounts ? ' | ' + row.accounts + ' accounts' : '') + (row.spend ? ' | ' + row.spend : '') + (row.nda ? NL + '🔒 NDA first' : '') +
  NL + name + ' | ' + [row.phone, email].filter(Boolean).join(' | ') + (row.source ? NL + '🔗 ' + row.source : '');

const origin = (inp.headers || {}).origin || '';
return [{ json: { row, email, subject, detail, alert, cors: ORIGINS.includes(origin) ? origin : ORIGINS[0] } }];`,
    },
  },
});

const save = node({
  type: 'n8n-nodes-base.dataTable',
  version: 1.1,
  config: {
    name: 'Save to table',
    parameters: {
      resource: 'row',
      operation: 'insert',
      dataTableId: { __rl: true, mode: 'id', value: 'UT1N4Ax18x9oryqJ', cachedResultName: 'White Label Media leads' },
      columns: {
        mappingMode: 'defineBelow',
        value: {
          agency: '={{ $json.row.agency }}',
          name: '={{ $json.row.name }}',
          role: '={{ $json.row.role }}',
          email: '={{ $json.row.email }}',
          phone: '={{ $json.row.phone }}',
          channel: '={{ $json.row.channel }}',
          site: '={{ $json.row.site }}',
          country: '={{ $json.row.country }}',
          team: '={{ $json.row.team }}',
          offers: '={{ $json.row.offers }}',
          model: '={{ $json.row.model }}',
          channels: '={{ $json.row.channels }}',
          accounts: '={{ $json.row.accounts }}',
          spend: '={{ $json.row.spend }}',
          start: '={{ $json.row.start }}',
          price: '={{ $json.row.price }}',
          calc: '={{ $json.row.calc }}',
          nda: '={{ $json.row.nda }}',
          message: '={{ $json.row.message }}',
          source: '={{ $json.row.source }}',
          page: '={{ $json.row.page }}',
          consent_at: '={{ $json.row.consent_at }}',
          status: '={{ $json.row.status }}',
          raw: '={{ $json.row.raw }}'
        },
        schema: [
          { id: 'agency', displayName: 'agency', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'name', displayName: 'name', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'role', displayName: 'role', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'email', displayName: 'email', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'phone', displayName: 'phone', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'channel', displayName: 'channel', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'site', displayName: 'site', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'country', displayName: 'country', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'team', displayName: 'team', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'offers', displayName: 'offers', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'model', displayName: 'model', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'channels', displayName: 'channels', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'accounts', displayName: 'accounts', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'spend', displayName: 'spend', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'start', displayName: 'start', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'price', displayName: 'price', required: false, defaultMatch: false, display: true, type: 'number', canBeUsedToMatch: true },
          { id: 'calc', displayName: 'calc', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'nda', displayName: 'nda', required: false, defaultMatch: false, display: true, type: 'boolean', canBeUsedToMatch: true },
          { id: 'message', displayName: 'message', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'source', displayName: 'source', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'page', displayName: 'page', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'consent_at', displayName: 'consent_at', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'status', displayName: 'status', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'raw', displayName: 'raw', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true }
        ],
      },
      options: {},
    },
  },
});

const reply = node({
  type: 'n8n-nodes-base.respondToWebhook',
  version: 1.5,
  config: {
    name: 'Answer the site',
    parameters: {
      respondWith: 'json',
      responseBody: '{"ok":true}',
      options: {
        responseHeaders: {
          entries: [
            { name: 'Access-Control-Allow-Origin', value: expr("{{ $('Parse and gate').item.json.cors }}") },
            { name: 'Vary', value: 'Origin' },
          ],
        },
      },
    },
  },
});

const mail = node({
  type: 'n8n-nodes-base.gmail',
  version: 2.1,
  config: {
    name: 'E-mail Rihards',
    parameters: {
      resource: 'message',
      operation: 'send',
      sendTo: 'rihards@marketingaskola.lv',
      subject: expr("{{ $('Parse and gate').item.json.subject }}"),
      emailType: 'text',
      message: expr("{{ $('Parse and gate').item.json.detail }}"),
      options: { appendAttribution: false, senderName: 'White Label Media website', replyTo: expr("{{ $('Parse and gate').item.json.email }}") },
    },
    credentials: { gmailOAuth2: { id: 'OxLeeAoOPOzsUtpV', name: 'Rihards personal | Gmail account' } },
  },
});

const ping = node({
  type: 'n8n-nodes-base.telegram',
  version: 1.2,
  config: {
    name: 'Telegram alert',
    onError: 'continueRegularOutput',
    parameters: {
      resource: 'message',
      operation: 'sendMessage',
      chatId: '6091120403',
      text: expr("{{ $('Parse and gate').item.json.alert }}"),
      additionalFields: { appendAttribution: false, disable_web_page_preview: true },
    },
    credentials: { telegramApi: { id: 'Q8gMn5hYpVdgOH6K', name: 'Telegram account' } },
  },
});

export default workflow('wlm-lead', 'White Label Media — leads', { settings: { executionOrder: 'v1', errorWorkflow: 'R9OmXjBXdhYetZkM' } })
  .add(hook)
  .to(gate)
  .to(save)
  .to(reply)
  .to(mail)
  .to(ping);
