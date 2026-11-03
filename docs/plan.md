# whitelabelmedia.eu rebuild — plan (2026-11-03)

## Why
The current site is a single WordPress/Divi page on SiteGround. It has no form (every "Book a call" button jumps to an e-mail address), mixes $ and €, and some case numbers don't match the Ads Manager screenshots shown next to them (Četras Zoles says "over €36,000", the screenshot says €35,877; Brew's €75k is total spend, not per month; Excel Know How's €0.38 per sign-up doesn't add up).

The new site sells one idea to agencies in expensive markets (DE, AT, CH, NL, Nordics, UK, US): **a senior paid-social team in Riga, at Baltic rates, working invisibly under your brand.** The agency keeps the client and the margin.

## Goals
- Turn agency visits into qualified partnership requests (agency, market, accounts, spend, channels, model).
- Make the price gap concrete: a margin calculator (outsource vs. hire, with sourced salary presets).
- Make "white label" tangible: a live preview of a monthly client report in the visitor's own brand.
- Keep proof honest: every result comes from the Ads Manager screenshots, shown in the case dialogs.
- Every lead lands in an n8n table, an e-mail and a Telegram ping within seconds.

## Non-goals (for now)
- No client portal or logins. A Slack/WhatsApp channel per agency covers it.
- No German version until ads show demand from DACH.
- No Calendly. The request form is the booking step; Rihards replies with times.

## Anti-goals
- Invented numbers. Salary presets name the role, source and date, and every field is editable.
- Calling it "cheap labour" on the page. The pitch is Baltic rates for senior people; "cheap" reads as low quality to the buyer.

## Stack (same as Rent in Riga and Impromotion)
- Static HTML/CSS/JS, no build step, no npm, no third-party requests (fonts are system fonts; German agencies care about Google Fonts and GDPR).
- Form → `POST text/plain` → n8n webhook `wlm-lead` → validate + honeypot + key → data table → reply → Gmail → Telegram.
- Deploy: push to `main` → GitHub Actions → rsync over SSH to SiteGround → cache flush.

## Page (`/`)
1. Hero: promise, two CTAs (start a partnership / calculate your margin), proof numbers.
2. Logos of brands we've run ads for.
3. The problem: saying no to paid social, or hiring a media buyer you can't keep busy.
4. What we run: Meta Ads (core), plus Google & YouTube, TikTok, creative, tracking.
5. How it plugs in: four steps.
6. Margin calculator: accounts × your price − our fee vs. in-house salary.
7. White-label report preview: type your agency name, pick a colour, add your logo (stays in the browser).
8. Results: four cases, each opens a dialog with the screenshot.
9. Partnership models: white label (from €450/month per account) and referral (€450 per signed client).
10. Team, testimonials, FAQ (+ FAQPage schema), 3-step partnership request, footer.

`/privacy/`: GDPR notice for the form.

## Open (owner)
- Pricing currency: the old site said "$450+"; the new one says "€450". Confirm.
- Confirm the three testimonials are real and approved for use. Matīss Seipulāns and Katrīna Malacanova are on the Marketinga Skola team page, so two "agency partner" quotes come from people who now work with us. ("Kristaps Apeināns" spelling confirmed from the Marketinga Skola team page.)
- Services beyond Meta (Google & YouTube, TikTok, creative, tracking): cut any you won't deliver.
- Legal entity for the privacy notice (currently Rihards Zeila as controller).
- Go-live: SiteGround SSH host/user for whitelabelmedia.eu, a GitHub repo and the `SG_*` secrets.
