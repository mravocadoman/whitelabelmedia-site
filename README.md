# White Label Media

whitelabelmedia.eu rebuilt from WordPress (Divi) as a lead-generation site for agencies in expensive markets: a senior paid-social team in Riga runs their clients' ads under the agency's name, at Baltic rates. Static HTML/CSS/JS, English only, no build step, no third-party requests (system fonts on purpose: German agencies notice Google Fonts).

## Files

- `index.html`: the whole pitch. Hero with a live white-label report demo (name, colour, logo), options + comparison table, services, process, margin calculator, results with Ads Manager screenshots in dialogs, pricing, team, testimonials, FAQ (+ FAQPage schema), 3-step partnership request, sources.
- `privacy/`: GDPR notice. Keep it in step with what the form collects and where the data goes.
- `styles.css`, `main.js`: shared by both pages. `main.js` returns early on pages without the wizard.
- `assets/img/`: logos, team photos and case images from the old site (WebP), plus `og.jpg`.
- `n8n/lead-workflow.js`: source of the live n8n workflow, kept here so the form and the workflow change together.
- `docs/plan.md`: the rebuild plan and open owner decisions.

## Run locally

```bash
python3 -m http.server 4174
```

Port 4174 matters: the n8n workflow only echoes CORS for `localhost:4174`, `127.0.0.1:4174` and the live domain.

## Numbers on the page

- Case results come from the Ads Manager screenshots shown in each dialog. Don't round them up (the old site said "over €36,000" for €35,877).
- Calculator salary presets (`MARKETS` in `main.js`) and the "€4,409" on the page: gehalt.de (DE), Searchlab (NL), Digital Waffle (UK), Indeed (US), GBP/USD at the ECB rate of 3 Nov 2026. Update the Sources list in `index.html` at the same time.
- Report demo data is fictional and labelled "Sample data". Its numbers add up (spend × ROAS = purchase value, weekly bars sum to the total); keep it that way if you change them.

## Leads

The request form POSTs `text/plain` JSON to the n8n workflow **White Label Media — leads** (`fMjOqDJ0wQo4htUj`, webhook `/webhook/wlm-lead?k=wlm-eu-2026`). The workflow:

1. Rejects posts with a bad key, a filled honeypot, a fill time under 3 s, no consent, no agency, or an invalid e-mail.
2. Saves the request to the n8n data table **White Label Media leads** (`UT1N4Ax18x9oryqJ`, status `new`).
3. Answers the site.
4. E-mails rihards@marketingaskola.lv with reply-to set to the agency contact.
5. Sends a Telegram message to Rihards' private chat.

Failures go to the shared alert workflow. The privacy notice promises deletion 12 months after a request that doesn't turn into a partnership.

## Deploy

Push to `main`, and GitHub Actions (`.github/workflows/deploy.yml`) does the rest, the same way as Rent in Riga and Impromotion:

1. Stamps `?v=<commit>` on our own CSS, JS and image links.
2. Rsyncs the site files over SSH (port 18765) into `www/whitelabelmedia.eu/public_html/`, without `--delete`, so the old WordPress install stays in place.
3. Flushes the SiteGround cache.

`index.html` takes precedence over WordPress's `index.php`. The workflow needs the repo secrets `SG_SSH_KEY`, `SG_HOST` and `SG_USER` for the SiteGround site that hosts whitelabelmedia.eu. New top-level files or folders have to be added to the rsync list.
