(() => {
  'use strict';

  const LEAD_URL = 'https://marketingaskola.app.n8n.cloud/webhook/wlm-lead?k=wlm-eu-2026';
  const loadedAt = Date.now();
  const $ = (s, root = document) => root.querySelector(s);
  const $$ = (s, root = document) => [...root.querySelectorAll(s)];
  const eur = (n) => (n < 0 ? '−' : '') + '€' + Math.round(Math.abs(n)).toLocaleString('en-GB');
  const store = {
    get(k) { try { return JSON.parse(localStorage.getItem(k)); } catch { return null; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} },
    del(k) { try { localStorage.removeItem(k); } catch {} },
  };

  /* ---------- Header, menu, year, reveal ---------- */
  const header = $('.site-header');
  const onScroll = () => header.classList.toggle('scrolled', scrollY > 8);
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  const toggle = $('.menu-toggle');
  const links = $('#nav-links');
  if (toggle) {
    toggle.addEventListener('click', () => {
      const open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open);
    });
    links.addEventListener('click', (e) => {
      if (e.target.closest('a')) { links.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); }
    });
  }
  $$('[data-year]').forEach((el) => { el.textContent = new Date().getFullYear(); });
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
    }), { rootMargin: '0px 0px -8% 0px' });
    $$('.reveal').forEach((el) => io.observe(el));
  } else {
    $$('.reveal').forEach((el) => el.classList.add('in'));
  }

  const wizard = $('#wizard');
  if (!wizard) return; // the rest is the homepage only

  /* ---------- Where the visitor came from (first touch, kept for the visit) ---------- */
  const leadSource = (() => {
    const q = new URLSearchParams(location.search);
    const utm = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term'].map((k) => q.get(k)).filter(Boolean).join('/');
    let s = utm ? 'utm:' + utm : '';
    if (q.get('gclid')) s += (s ? ' ' : '') + 'gclid';
    if (q.get('fbclid')) s += (s ? ' ' : '') + 'fbclid';
    if (q.get('li_fat_id')) s += (s ? ' ' : '') + 'linkedin';
    if (!s && document.referrer) { try { const h = new URL(document.referrer).host; if (h !== location.host) s = 'ref:' + h; } catch {} }
    try {
      if (s && !sessionStorage.getItem('wlm-src')) sessionStorage.setItem('wlm-src', (s + ' | landed ' + location.pathname).slice(0, 200));
      return sessionStorage.getItem('wlm-src') || 'direct';
    } catch { return s || 'direct'; }
  })();

  /* ---------- White-label report demo ---------- */
  const demo = $('#demo');
  const report = $('#report');
  const agencyOut = [$('#report-agency'), $('#report-by')];
  const initials = $('#report-initials');
  const logoBox = $('#report-logo');
  let logoUrl = null;
  let lastDemoName = '';
  const prev = new Date();
  prev.setDate(1);
  prev.setMonth(prev.getMonth() - 1);
  $('#report-month').textContent = prev.toLocaleString('en-GB', { month: 'long', year: 'numeric' });

  function setBrand(color) {
    report.style.setProperty('--brand', color);
    $('.swatch-custom').classList.toggle('on', !demo.querySelector('input[name=color]:checked'));
  }
  function setAgency(raw) {
    const name = raw.trim() || 'Your Agency';
    agencyOut.forEach((el) => { el.textContent = name; });
    initials.textContent = name.split(/\s+/).filter(Boolean).slice(0, 2).map((w) => w[0]).join('').toUpperCase() || 'YA';
    // Carry the name into the request form, unless the visitor already typed something else there.
    const f = wizard.elements.agency;
    if (!f.value || f.value === lastDemoName) { f.value = raw.trim(); saveDraft(); }
    lastDemoName = raw.trim();
  }
  demo.elements.agency.addEventListener('input', (e) => setAgency(e.target.value));
  demo.addEventListener('change', (e) => {
    if (e.target.name === 'color') setBrand(e.target.value);
    if (e.target.name === 'logo') {
      const file = e.target.files[0];
      if (!file) return;
      if (!/^image\//.test(file.type) || file.size > 5e6) { alert('Please choose a PNG, JPG, SVG or WebP image under 5 MB.'); e.target.value = ''; return; }
      if (logoUrl) URL.revokeObjectURL(logoUrl);
      logoUrl = URL.createObjectURL(file); // stays in this tab, never uploaded
      logoBox.replaceChildren(Object.assign(document.createElement('img'), { src: logoUrl, alt: '' }));
    }
  });
  demo.elements.custom.addEventListener('input', (e) => {
    demo.querySelectorAll('input[name=color]').forEach((r) => { r.checked = false; });
    setBrand(e.target.value);
  });

  /* ---------- Margin calculator ----------
     Gross salary presets, see the Sources list on the page. GBP and USD at the ECB reference rate of 3 Nov 2026. */
  const MARKETS = {
    de: { month: 4409, note: 'Germany: median for a Performance-Marketing-Manager (gehalt.de, checked 3 Nov 2026).' },
    nl: { month: 39000 / 12, note: 'Netherlands: median for a Social Media Manager, €39,000 a year excl. holiday pay (Searchlab 2026).' },
    uk: { month: 46267 / 12 / 0.83358, note: 'United Kingdom: average for social media roles, £46,267 a year (Digital Waffle 2026).' },
    us: { month: 65712 / 12 / 1.1179, note: 'United States: average for a Social Media Manager, $65,712 a year (Indeed, 29 Oct 2026).' },
    custom: { note: 'Type the monthly gross salary you’d pay.' },
  };
  const calc = $('#calc');
  const c = calc.elements;
  const num = (el) => Math.max(0, Number(el.value) || 0);
  let calcTouched = false;

  function setMarket(key) {
    const m = MARKETS[key];
    if (m.month) c.salary.value = Math.round(m.month);
    $('#salary-source').textContent = m.note;
  }
  function runCalc() {
    const n = Math.max(1, Math.round(num(c.accounts)));
    const price = num(c.price);
    const fee = Math.max(450, num(c.fee));
    const salary = num(c.salary);
    const oncost = Math.min(100, num(c.oncost));
    const cap = Math.max(1, Math.round(num(c.cap)) || 1);
    c.accountsOut.value = n;

    const usMargin = n * (price - fee);
    const hires = Math.ceil(n / cap);
    const hireCost = hires * salary * (1 + oncost / 100);
    const hireMargin = n * price - hireCost;
    const diff = usMargin - hireMargin;

    $('#out-us').textContent = eur(usMargin);
    $('#out-us-sub').textContent = price > 0
      ? `margin a month, ${String(Math.round(((price - fee) / price) * 100)).replace('-', '−')}% of what you bill (${eur(usMargin * 12)} a year)`
      : 'margin a month';
    const warn = $('#out-warn');
    warn.hidden = price >= fee;
    warn.textContent = price < fee ? `At ${eur(price)} you’d bill less than our fee of ${eur(fee)}, so each account loses money.` : '';
    const v = $('#out-verdict');
    if (!salary) {
      $('#out-hire').textContent = '–';
      $('#out-hire-sub').textContent = 'enter a salary to compare';
      v.textContent = '';
      return;
    }
    $('#out-hire').textContent = eur(hireMargin);
    $('#out-hire-sub').textContent = `margin a month, after ${hires} hire${hires > 1 ? 's' : ''} costing ${eur(hireCost)} a month`;
    if (price < fee) v.textContent = '';
    else if (diff > 0) v.innerHTML = `Partnering keeps <b>${eur(diff)} more a month</b>, ${eur(diff * 12)} a year, before you count recruiting.`;
    else if (diff < 0) v.innerHTML = `At this volume an in-house team costs ${eur(-diff)} a month less on paper. Ask us about volume pricing, or use us for overflow and holiday cover.`;
    else v.textContent = 'Both come out the same on paper. Partnering saves you the recruiting.';
  }
  const lang = (navigator.language || '').toLowerCase();
  c.market.value = lang.startsWith('nl') ? 'nl' : lang === 'en-gb' ? 'uk' : lang === 'en-us' ? 'us' : 'de';
  setMarket(c.market.value);
  calc.addEventListener('input', (e) => {
    calcTouched = true;
    if (e.target.name === 'salary' && c.market.value !== 'custom') { c.market.value = 'custom'; $('#salary-source').textContent = MARKETS.custom.note; }
    runCalc();
  });
  c.market.addEventListener('change', () => { setMarket(c.market.value); runCalc(); });
  c.fee.addEventListener('change', () => { if (num(c.fee) < 450) { c.fee.value = 450; runCalc(); } });
  runCalc();

  $('#calc-cta').addEventListener('click', () => {
    const n = Math.round(num(c.accounts));
    wizard.elements.accounts.value = n <= 1 ? '1' : n <= 3 ? '2–3' : n <= 10 ? '4–10' : '10+';
    if (num(c.price)) wizard.elements.price.value = Math.round(num(c.price));
    calcTouched = true;
    saveDraft();
  });

  /* ---------- Case dialogs ---------- */
  $$('[data-case]').forEach((btn) => btn.addEventListener('click', () => $('#' + btn.dataset.case).showModal()));
  $$('.case-dialog').forEach((d) => {
    $('.dialog-close', d).addEventListener('click', () => d.close());
    d.addEventListener('click', (e) => { if (e.target === d) d.close(); }); // click on the backdrop
  });

  /* ---------- Pricing buttons pick the model ---------- */
  $$('[data-model]').forEach((a) => a.addEventListener('click', () => {
    const r = wizard.querySelector(`input[name=model][value="${a.dataset.model}"]`);
    if (r) { r.checked = true; saveDraft(); }
  }));

  /* ---------- Riga clock ---------- */
  const rigaEl = $('#riga-time');
  function rigaTime() {
    const now = new Date();
    const at = (tz) => new Date(now.toLocaleString('en-US', tz ? { timeZone: tz } : {}));
    const diff = Math.round((at('Europe/Riga') - at()) / 18e5) / 2; // hours, to the half hour
    const t = now.toLocaleTimeString('en-GB', { timeZone: 'Europe/Riga', hour: '2-digit', minute: '2-digit' });
    const h = Math.abs(diff);
    const rel = diff === 0 ? 'the same time as where you are' : `${h} hour${h === 1 ? '' : 's'} ${diff > 0 ? 'ahead of' : 'behind'} you`;
    rigaEl.textContent = `It’s ${t} in Riga right now, ${rel}.`;
  }
  rigaTime();
  setInterval(rigaTime, 30000);

  /* ---------- Wizard ---------- */
  const steps = $$('.step', wizard);
  const labels = ['Your agency', 'What you need', 'Your details'];
  const back = $('#back');
  const next = $('#next');
  const submit = $('#submit');
  const status = $('#status');
  let step = 1;
  const say = (text, tone = '') => { status.textContent = text; status.dataset.tone = tone; };

  function showStep(n, focus = true) {
    step = n;
    steps.forEach((s) => { s.hidden = Number(s.dataset.step) !== n; });
    $$('.progress span', wizard).forEach((s, i) => s.classList.toggle('done', i < n));
    $('#step-label').textContent = `Step ${n} of 3: ${labels[n - 1]}`;
    back.hidden = n === 1;
    next.hidden = n === 3;
    submit.hidden = n !== 3;
    say('');
    if (focus) steps[n - 1].querySelector('input:not([type=hidden]), select, textarea')?.focus({ preventScroll: true });
  }

  function validStep(n) {
    const fields = $$('input, select, textarea', steps[n - 1]).filter((f) => f.name !== 'website');
    for (const f of fields) {
      f.removeAttribute('aria-invalid');
      if (!f.checkValidity()) {
        f.setAttribute('aria-invalid', 'true');
        f.reportValidity();
        return false;
      }
    }
    return true;
  }

  next.addEventListener('click', () => { if (validStep(step)) { showStep(step + 1); wizard.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); } });
  back.addEventListener('click', () => showStep(step - 1));
  // Enter in a text field moves forward instead of submitting a half-filled form.
  wizard.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && step < 3 && e.target.tagName === 'INPUT') { e.preventDefault(); next.click(); }
  });

  /* ---------- Draft: a reload or a closed tab loses nothing ---------- */
  const DRAFT = 'wlm-draft';
  const SKIP = ['consent', 'website'];
  function saveDraft() {
    const d = {};
    for (const el of wizard.elements) {
      if (!el.name || SKIP.includes(el.name)) continue;
      if (el.type === 'checkbox') { if (el.checked) (d[el.name] = d[el.name] || []).push(el.value); } else if (el.type === 'radio') { if (el.checked) d[el.name] = el.value; } else d[el.name] = el.value;
    }
    store.set(DRAFT, d);
  }
  function loadDraft() {
    const d = store.get(DRAFT);
    if (!d) return;
    for (const el of wizard.elements) {
      if (!el.name || SKIP.includes(el.name)) continue;
      if (el.type === 'checkbox') el.checked = [].concat(d[el.name] || []).includes(el.value);
      else if (el.type === 'radio') { if (el.name in d) el.checked = d[el.name] === el.value; } else if (el.name in d) el.value = d[el.name];
    }
  }
  wizard.addEventListener('input', saveDraft);
  wizard.addEventListener('change', saveDraft);
  loadDraft();

  /* ---------- Submit ---------- */
  async function sendLead(payload) {
    // text/plain keeps this a "simple" request: no CORS preflight.
    const res = await fetch(LEAD_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain' },
      body: JSON.stringify({ ...payload, source: leadSource, page: location.href.split('#')[0], t: Date.now() - loadedAt }),
    });
    if (!res.ok) throw new Error('HTTP ' + res.status);
    (window.dataLayer = window.dataLayer || []).push({ event: 'generate_lead', lead_model: payload.model });
  }

  wizard.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (step !== 3) { next.click(); return; }
    for (let n = 1; n <= 3; n++) if (!validStep(n)) { showStep(n, false); validStep(n); return; }
    const d = new FormData(wizard);
    submit.disabled = true;
    say('Sending your request…');
    try {
      await sendLead({
        agency: d.get('agency'), site: d.get('site'), country: d.get('country'), team: d.get('team'), offers: d.getAll('offers'),
        model: d.get('model'), channels: d.getAll('channels'), accounts: d.get('accounts'), spend: d.get('spend'), start: d.get('start'),
        price: d.get('price'),
        calc: calcTouched ? `${c.accounts.value} accounts, bills ${eur(num(c.price))}, our fee ${eur(num(c.fee))}, salary ${eur(num(c.salary))} (${c.market.value}) +${c.oncost.value}%, ${c.cap.value} per person` : '',
        name: d.get('name'), role: d.get('role'), email: d.get('email'), phone: d.get('phone'), channel: d.get('channel'),
        message: d.get('message'), nda: d.get('nda') === 'yes',
        website: d.get('website'), consent: d.get('consent') === 'on',
      });
      store.del(DRAFT);
      steps.forEach((s) => { s.hidden = true; });
      $('#wizard-nav').hidden = true;
      $('.progress', wizard).hidden = true;
      $('#step-label').hidden = true;
      say('');
      const done = $('#done');
      done.hidden = false;
      done.focus();
    } catch {
      say('Sorry, that didn’t go through. Your answers are saved, so please try again in a moment, or e-mail rihards@marketingaskola.lv.', 'error');
    } finally {
      submit.disabled = false;
    }
  });

  /* ---------- FAQ structured data, built from the visible answers ---------- */
  $('#faq-schema').textContent = JSON.stringify({
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: $$('.faq details').map((q) => ({
      '@type': 'Question',
      name: $('summary', q).textContent.trim(),
      acceptedAnswer: { '@type': 'Answer', text: $('div', q).textContent.replace(/It’s \d\d:\d\d in Riga.*$/, '').trim() },
    })),
  });
})();
