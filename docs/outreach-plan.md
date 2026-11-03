# Outreach plan: agencies in expensive markets (2026-11-03)

## Goal
First **5 partner agencies in 90 days**, each starting with 1–3 client accounts. At the €450 floor that is roughly €2,250–6,750 a month in management fees. These are targets to steer by, not forecasts. Replace them with real rates after the first 200 contacts.

## Who we're after (ICP)
- **Agency type:** branding, design, web, video, organic social or PR agencies that clients already trust, and that say "no" or "we partner" to paid social today.
- **Size:** 3–50 people. Smaller can't afford a hire; bigger usually has a performance team.
- **Person:** founder, managing director, or head of client services / accounts.
- **Markets, in order:** UK and Ireland, then Nordics and Netherlands, then US, then DACH (see the legal table for why DACH is last).
- **Buying signals, strongest first:**
  1. A job ad for a Performance Marketing Manager, Paid Social Manager or Media Buyer. They've just priced the hire, so the calculator lands.
  2. "Social media advertising" listed as a service, but nobody on the team page does it.
  3. Case studies that show creative work but no ad results.
  4. A recent client win or rebrand launch (a reason to talk now).

## Where outreach is allowed

| Market | Cold e-mail | LinkedIn (manual) | Notes |
|---|---|---|---|
| UK | Yes, to corporate addresses, with opt-out | Yes | PECR covers individual subscribers; sole traders and partnerships need consent. |
| Ireland | Yes, to company addresses, with opt-out | Yes | Same caveat for sole traders. |
| US | Yes (CAN-SPAM: real address, opt-out) | Yes | Time zones: send 14:00–16:00 Riga for East Coast mornings. |
| Netherlands, Sweden, Denmark, Finland, Switzerland | **Verify first** | Yes | Sources conflict. Treat as LinkedIn-only until checked. |
| Germany, Austria | **No**: B2B cold e-mail needs prior consent (UWG §7, TKG 2021 §174) | Yes, connect first, pitch only after they reply | Get a lawyer's view before any DACH e-mail. |

Every e-mail carries Rihards' name, White Label Media, a postal address and a one-line opt-out. Honour opt-outs the same day and keep a suppression list.

## The offer we lead with
**A 20-minute call, nothing else** (owner decision, 2026-11-03). No free audit and no discount: the proof (Ads Manager screenshots) and the calculator carry the pitch. If replies stay low after the first 200 contacts, a free white-label audit of one client account is the next lever to test.

## List building (week 1, then 50 new prospects a week)
1. **Directories:** Clutch, Sortlist, DesignRush and Google Maps ("branding agency Manchester", "creative agency Dublin" and so on), filtered by country and services.
2. **Hiring signals:** LinkedIn Jobs, Indeed, StepStone and Totaljobs for "paid social" / "performance marketing" at agencies. Tag these "hiring": they get the calculator e-mail first.
3. **Contacts:** founder or MD name from the site or LinkedIn; e-mail via Hunter or Apollo (both connectors need authorising with `/mcp` before I can use them).
4. **LinkedIn by hand only.** No automation tools, scrapers or browser agents on Rihards' account: LinkedIn paused search on it after an automated run in October.

Track every prospect in the Google Sheet **White Label Media: prospects** (https://docs.google.com/spreadsheets/d/1lGWqxCYWlV_3AZCdUd97rk9hrHTx9G4nUDm5E8ghzcs/edit, in Rihards' Drive). The **Prospects** tab has one row per agency with dropdowns for status, channel and step. A next-touch date that's due turns lime, and ticking Opt-out strikes the row through. **Funnel** counts each stage; **Opt-outs** is the suppression list. Check it before every send.

## Sending setup (before the first cold e-mail)
- whitelabelmedia.eu already has SPF, DKIM and DMARC (checked 2026-11-03). **Don't send cold e-mail from it.** Use a second domain (for example `getwhitelabelmedia.eu`) with 2–3 mailboxes, so a spam complaint can't hurt the main domain.
- Warm the new mailboxes for 2–3 weeks, then stay at 30–40 cold e-mails per mailbox per day.
- Plain text, one link at most, no open-tracking pixel, no attachments in the first e-mail.
- Every link to the site carries UTMs. The site saves them with each request, so every lead shows its campaign and step:
  `?utm_source=coldemail&utm_medium=outreach&utm_campaign=uk-agencies-q4&utm_content=e1`
  (`utm_source=linkedin` for LinkedIn; `utm_content` = e1–e4 or li1–li3).

## E-mail sequence (UK, Ireland, US)
Personalise the first line every time. A generic opener is the main reason cold e-mail fails.

**E1, day 1.** Subject: `{{agency}} + paid social`
> Hi {{first_name}},
>
> {{personal line, e.g. "The rebrand you did for X is sharp work."}}
>
> When a client like that asks for Meta ads, do you run them in-house or pass them on?
>
> We're a small paid-social team in Riga that agencies hire under their own name. We set up and run the campaigns, you send the client a report with your logo on it, and you keep the margin.
>
> Worth a 20-minute call to see if it fits how you work?
>
> Rihards Zeila
> White Label Media · whitelabelmedia.eu
> {{postal address}} · Not relevant? Reply "no" and I won't write again.

**E2, day 4.** Subject: reply in thread
> One example of the work: for a fashion outlet we ran Advantage+ campaigns that returned €35,877 in sales from €987 of ad spend. The Ads Manager screenshot is on our site: {{link}}
>
> That's the kind of result that would go out under {{agency}}'s name. Open to a short call this week or next?

**E3, day 8.** Subject: `hiring vs. partnering`
> If you've thought about hiring a media buyer instead: {{salary_line}}, before employer costs, and they need enough accounts to stay busy.
>
> We start at €450 per client account a month. This calculator puts your own numbers side by side: {{calculator link}}

`{{salary_line}}` per market, only from the sourced figures on the site:
- UK: "UK social media roles average £46,267 a year (Digital Waffle 2026)"
- US: "a US social media manager averages $65,712 a year (Indeed)"
- Ireland: no sourced figure yet. Leave E3 out or find one first.

**E4, day 14.** Subject: reply in thread
> Last one from me. If paid social comes up with a client, the request form takes two minutes: {{link}}. Or reply "later" and I'll check in next quarter.

## LinkedIn sequence (all markets, by hand)
Up to 20 connection requests a working day, and stay under LinkedIn's weekly invite limit.
- **LI1, connect note (no pitch):** "Hi {{first_name}}, I run a small paid-social team in Riga that works behind agencies. I like what {{agency}} does with {{specific}}. Good to connect."
- **LI2, two days after they accept:** "Thanks for connecting. Quick question: when clients ask {{agency}} for Meta ads, do you keep that in-house or pass it on?"
- **LI3, only if they reply with interest:** suggest a 20-minute call and share the site link (with UTMs). In DACH, never pitch before they've replied.

## Replies
- **Interested:** offer two call times within 3 working days, and link the request form so their details arrive in the lead table.
- **"We do it in-house":** offer overflow and holiday cover: "Most teams use us when the in-house person is full or away."
- **"How much?":** "From €450 per client account a month. The exact quote depends on spend and channels, so it's easiest to scope on a call."
- **"Not now":** ask when, set a follow-up date in the tracker.
- **"No" / unsubscribe:** thank them, add to the suppression list the same day.

## Alongside outreach
- **LinkedIn posts by Rihards, twice a week:** case breakdowns, the hire-vs-partner maths, what a white-label report looks like. Prospects check the profile after a DM.
- **Paid retargeting** once the Meta and LinkedIn IDs are in: site visitors who used the calculator or opened a case (custom events `CalculatorUsed`, `CaseOpened`).
- **Partnerships:** ask the three agencies quoted on the site (Addtwo, Artisuno, Creo Dizains) for one introduction each. Referral fee from €450 per signed client applies.
- **German landing page:** only if DACH replies show demand. The site is English only.

## Weekly rhythm
- **Monday:** add 50 prospects with signals and personal lines.
- **Tuesday–Thursday:** e-mails go out 09:00–11:00 local time; 20 LinkedIn connects a day; answer replies within 4 working hours.
- **Friday:** review the numbers and update the copy that's underperforming. Record calls held.

## Numbers to watch
For each market and step: sent, replies, positive replies, calls booked, calls held, partners signed. Starting targets to beat: 5% positive replies on e-mail, 25% LinkedIn accept rate, 1 call per 50 prospects. These are rules of thumb, not measured benchmarks, so replace them with your own after the first 200 contacts.

## 30 / 60 / 90 days
- **Days 1–30:** register and warm the sending domain, build the first 200 prospects (UK + IE), start LinkedIn by hand in every market right away.
- **Days 31–60:** e-mail sequence live in UK, IE and US. First calls held. Rewrite the copy once with what the replies say.
- **Days 61–90:** add the markets that pass the legal check, start retargeting, sign 5 partners.

## Open owner decisions
1. Sending domain name, and who is allowed to sign the e-mails.
2. Postal address for the e-mail footer.
3. Pricing currency (€ or $), still open from the site rebuild.
