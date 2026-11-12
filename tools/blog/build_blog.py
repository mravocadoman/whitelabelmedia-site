"""Generate /blog/ pages for whitelabelmedia.eu. Run from this folder: python3 build_blog.py ../.."""
import json, sys, os
from html import escape
from charts import hbar_pairs, per_account_line, margin_bars, flow_diagram, report_mockup, eur

REPO = sys.argv[1]
SITE = "https://whitelabelmedia.eu"
DATE = "2026-11-12"
DATE_H = "12 November 2026"
AUTHOR = "Rihards Zeila"

# --- shared numbers, same sources as the site's calculator (ECB rate 3 Nov 2026) ---
ONCOST = 0.20
MARKETS = [  # name, monthly gross EUR, source
    ("United States", 65712 / 12 / 1.1179, "Indeed, Social Media Manager average $65,712 a year (29 Oct 2026)"),
    ("United Kingdom", 46267 / 12 / 0.83358, "Digital Waffle, UK social media roles average £46,267 a year (2026)"),
    ("Germany", 4409, "gehalt.de, Performance-Marketing-Manager median €4,409 a month (checked 3 Nov 2026)"),
    ("Netherlands", 39000 / 12, "Searchlab, Social Media Manager median €39,000 a year excl. holiday pay (2026)"),
]
FEE = 450
ACCTS = 5
UK_COST = MARKETS[1][1] * (1 + ONCOST)

LOGO = '<svg width="34" height="34" viewBox="0 0 32 32" aria-hidden="true"><path d="M4 9a5 5 0 0 1 5-5h12.6a5 5 0 0 1 3.6 1.5l3.3 3.4a5 5 0 0 1 0 7l-11 11a5 5 0 0 1-7 0L5.5 21A5 5 0 0 1 4 17.4z" fill="#f4f2ec"/><circle cx="10.5" cy="10.5" r="2.3" fill="#0f1012"/><path d="M13 18.5l5.5-5.5M16 21.5l5.5-5.5" stroke="#0f1012" stroke-width="2.2" stroke-linecap="round"/></svg>'


def page(path, title, desc, body, schema=None, robots=None):
    canon = f"{SITE}{path}"
    ld = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>' if schema else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <script>if (location.protocol === "http:") location.replace("https://" + location.host + location.pathname + location.search + location.hash);</script>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#0f1012">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(desc)}">
  <link rel="canonical" href="{canon}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:url" content="{canon}">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/styles.css">
  {ld}
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header">
    <nav class="nav wrap" aria-label="Main">
      <a class="logo" href="/" aria-label="White Label Media, home">
        {LOGO}
        <span>White Label <b>Media</b></span>
      </a>
      <span class="nav-mini"><a href="/blog/">Blog</a><a class="btn btn-accent btn-sm" href="/#start">Partner with us</a></span>
    </nav>
  </header>

  <main class="page" id="main">
{body}
  </main>

  <footer class="site-footer">
    <div class="wrap foot">
      <p class="logo"><span>White Label <b>Media</b></span></p>
      <p>Riga, Latvia · <a href="mailto:rihards@whitelabelmedia.eu">rihards@whitelabelmedia.eu</a></p>
      <p><a href="/">Home</a> · <a href="/blog/">Blog</a> · <a href="/privacy/">Privacy</a> · <button type="button" class="linklike" data-cookie-settings>Cookie settings</button> · © <span data-year>2026</span> White Label Media</p>
    </div>
  </footer>
  <script src="/main.js" defer></script>
</body>
</html>
"""


def figure(svg, caption, table_head, table_rows, source=None):
    rows = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in table_rows)
    head = "".join(f"<th scope=\"col\">{h}</th>" for h in table_head)
    src = f'<p class="fig-src">Source: {source}</p>' if source else ""
    return f"""<figure class="fig">
  {svg}
  <figcaption>{caption}</figcaption>
  {src}
  <details class="fig-data"><summary>Show the numbers</summary>
    <table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>
  </details>
</figure>"""


CTA = """<aside class="cta-box">
  <p class="eyebrow">Run the numbers for your agency</p>
  <h2>Your accounts, your prices, your market.</h2>
  <p>The calculator puts an in-house hire and a white-label partner side by side with your own figures. If it adds up, the request form takes two minutes and Rihards replies personally within two working days.</p>
  <p><a class="btn btn-dark" href="/#calculator">Open the calculator</a> <a class="btn btn-ghost-dark" href="/#start">Partner with us</a></p>
</aside>"""


def article(slug, title, h1, desc, lead, toc, content, faq=None):
    path = f"/blog/{slug}/"
    schema = [{
        "@context": "https://schema.org", "@type": "BlogPosting", "headline": h1, "description": desc,
        "datePublished": DATE, "dateModified": DATE, "inLanguage": "en",
        "author": {"@type": "Person", "name": AUTHOR, "url": SITE + "/"},
        "publisher": {"@type": "Organization", "name": "White Label Media", "url": SITE + "/"},
        "mainEntityOfPage": SITE + path,
    }, {
        "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog/"},
            {"@type": "ListItem", "position": 3, "name": h1, "item": SITE + path}]}]
    faq_html = ""
    if faq:
        schema.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
        faq_html = '<h2 id="faq">Questions agencies ask</h2>' + "".join(
            f'<details class="faq-item"><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for q, a in faq)
    toc_html = "".join(f'<li><a href="#{a}">{escape(t)}</a></li>' for a, t in toc)
    body = f"""    <article class="wrap prose post">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/blog/">Blog</a></nav>
      <h1>{escape(h1)}</h1>
      <p class="post-meta">By {AUTHOR} · {DATE_H}</p>
      <p class="lead">{lead}</p>
      <nav class="toc" aria-label="In this article"><p class="eyebrow">In this article</p><ol>{toc_html}</ol></nav>
{content}
{faq_html}
{CTA}
    </article>"""
    out = os.path.join(REPO, "blog", slug)
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "index.html"), "w") as f:
        f.write(page(path, title, desc, body, schema))
    return {"slug": slug, "h1": h1, "desc": desc}


posts = []

# ---------------------------------------------------------------- 1. pillar
posts.append(article(
    "white-label-facebook-ads",
    "White Label Facebook Ads: How It Works for Agencies | White Label Media",
    "White label Facebook ads: how it works for agencies",
    "What white label Facebook and Meta ads management is, how the handover works, who owns the ad account, what it costs and how to pick a partner.",
    "White label Facebook ads means another team runs your clients' Meta campaigns while your agency keeps the client, the brand and the margin. Here is how it works in practice, what to check before you sign, and where it doesn't fit.",
    [("what", "What white label Facebook ads means"), ("how", "How the handover works"), ("account", "Who owns the ad account"),
     ("options", "In-house, freelancer or white label"), ("cost", "What it costs"), ("checklist", "How to choose a partner"), ("faq", "Questions agencies ask")],
    f"""
      <h2 id="what">What white label Facebook ads means</h2>
      <p>A white label (or "white-label") partner does work that your agency sells under its own name. In paid social, that means a specialist team plans, builds, runs and optimises Facebook and Instagram ads for your clients, and your agency presents the results as its own.</p>
      <p>Your client never deals with the partner. They brief you, they pay you, and they receive a report with your logo on it. The partner charges your agency a fixed fee, and the difference between that fee and what you bill is your margin.</p>
      <p>Agencies usually look for this when one of three things happens:</p>
      <ul>
        <li><b>A client asks for ads and you don't run them.</b> Branding, web, design, video and PR agencies hear this all the time. Saying no sends the client to another agency, which then pitches for the rest of the work.</li>
        <li><b>Your paid social person is full or away.</b> One specialist can only run so many accounts well, and holidays and sick days still happen.</li>
        <li><b>You priced a hire and it didn't add up.</b> A full-time media buyer needs enough accounts to stay busy from month one.</li>
      </ul>

      <h2 id="how">How the handover works</h2>
      <p>The work moves in a loop, and your agency sits at the front of it.</p>
{figure(flow_diagram(), "Your agency keeps the client relationship and the brand. The partner works inside the client's own ad account.",
        ["Step", "Who", "What happens"],
        [["1", "Your client", "Briefs your agency and pays your invoice"], ["2", "Your agency", "Agrees the scope and the price"],
         ["3", "White Label Media", "Sets up, runs and optimises the campaigns"], ["4", "Client's ad account", "Campaigns run here, through partner access"],
         ["5", "Your agency", "Sends the client the monthly report under your brand"]])}
      <p>In practice, the first two weeks look like this:</p>
      <ol>
        <li><b>Brief and access.</b> You share the client's goals, budget and assets. The client (or you) gives the partner access to the Meta Business portfolio as a partner, so nothing changes hands.</li>
        <li><b>Tracking check.</b> Before any money is spent, the pixel, Conversions API and the events that count as a result are checked. Bad tracking is the most common reason paid social "doesn't work".</li>
        <li><b>Build and launch.</b> Campaigns, audiences and creative tests go live. You approve the plan before launch if you want to.</li>
        <li><b>Optimise and report.</b> The team adjusts budgets and creative each week, and you get a branded monthly report to forward or present.</li>
      </ol>

      <h2 id="account">Who owns the ad account</h2>
      <p>The client should. Meta's business tools let an outside team work in an ad account through <b>partner access</b>, without owning it. That matters for three reasons:</p>
      <ul>
        <li>If you ever change partner, the account, its history and its pixel data stay with the client.</li>
        <li>The client's payment method stays on their own account, so your agency isn't financing ad spend.</li>
        <li>Access can be removed in one click, which makes the arrangement easy to trust.</li>
      </ul>
      <p>Be wary of any partner that wants to run your clients' ads from its own ad account. It makes leaving expensive, and it hides the numbers from you.</p>

      <h2 id="options">In-house, freelancer or white label</h2>
      <div class="table-wrap"><table>
        <thead><tr><th scope="col"></th><th scope="col">In-house hire</th><th scope="col">Freelancer</th><th scope="col">White label partner</th></tr></thead>
        <tbody>
          <tr><th scope="row">Monthly cost</th><td>Full salary plus employer costs</td><td>Day rate, billed by the hour</td><td>Fixed fee per client account</td></tr>
          <tr><th scope="row">Holiday and sick cover</th><td>None, unless you hire two</td><td>None</td><td>A team covers it</td></tr>
          <tr><th scope="row">Fewer clients next quarter</th><td>You still pay the salary</td><td>You pay less</td><td>You pay less</td></tr>
          <tr><th scope="row">Client sees</th><td>Your team</td><td>Often the freelancer</td><td>Only your agency</td></tr>
          <tr><th scope="row">Time to start</th><td>Months of recruiting</td><td>Days to weeks</td><td>Days</td></tr>
        </tbody>
      </table></div>
      <p>An in-house team wins once you have enough steady accounts to keep people fully busy. Below that, a partner usually costs less and carries less risk. <a href="/blog/hire-or-outsource-paid-social/">We worked through the maths in a separate article.</a></p>

      <h2 id="cost">What it costs</h2>
      <p>Most white label partners charge either a fixed monthly fee per client account or a percentage of ad spend. White Label Media charges from {eur(FEE)} per client account a month, and the exact quote depends on spend and channels. Agencies that would rather not manage the work at all can refer a client instead and receive a {eur(FEE)} referral fee per signed client.</p>
      <p>Whatever the model, work out your margin per account before you sign. <a href="/blog/meta-ads-management-pricing/">Our pricing guide shows how agencies price Meta ads management</a> and what margin each price point leaves.</p>
      <p>Results depend on the product, the offer and the budget, so treat any partner's case studies as proof of skill, not a promise. Ours are on the homepage with the Ads Manager screenshots, for example a fashion outlet where Advantage+ campaigns returned €35,877 in sales from €987 of ad spend.</p>

      <h2 id="checklist">How to choose a partner</h2>
      <ul class="checklist">
        <li><b>Ad accounts stay with the client</b>, through partner access.</li>
        <li><b>An NDA and a GDPR data processing agreement</b> are offered before you share client data.</li>
        <li><b>Real proof</b>: Ads Manager screenshots, not just logos and percentages.</li>
        <li><b>Reporting you can rebrand</b>, ready to forward without editing.</li>
        <li><b>One named contact</b> and a stated reply time.</li>
        <li><b>No lock-in</b>: monthly terms, and you can take an account back in-house whenever you like.</li>
        <li><b>Honest scope</b>: a partner that says "this budget is too small to test properly" is worth more than one that says yes to everything.</li>
      </ul>
""",
    faq=[
        ("Is white label Facebook ads management legal?", "Yes. Subcontracting is normal agency practice. Put the partner under an NDA and a GDPR data processing agreement, and make sure your own client contract allows subcontractors."),
        ("Will my client find out?", "Not from the partner. The client deals only with your agency and receives reports under your brand. In Meta's tools the partner's business name can be visible to people who check account access, so if that matters, tell the client you work with a specialist team."),
        ("What is the difference between white label and outsourcing?", "Outsourcing is the broader term for handing work to an outside team. White label is outsourcing where the work is delivered under your agency's brand and the outside team stays invisible to the client."),
        ("Does a white label partner also do creative?", "Many do. White Label Media can write ad copy and direct creative, and also works with the creative your own team makes, which suits design and video agencies."),
    ]))

# ---------------------------------------------------------------- 2. hire vs outsource
rows = [(m, c * (1 + ONCOST), FEE * ACCTS) for m, c, _ in MARKETS]
ks = list(range(4, 17))
posts.append(article(
    "hire-or-outsource-paid-social",
    "Hire a Media Buyer or Outsource Paid Social? The Real Cost | White Label Media",
    "Hire a media buyer or outsource paid social? The real cost",
    "Salary, employer costs and how many accounts one person must run before an in-house paid social hire beats a white-label partner. UK, US, Germany and Netherlands.",
    "The salary is only the start. What decides whether an in-house paid social hire pays off is how many client accounts one person can run, every month, from the day they start. Here are the numbers for four markets.",
    [("salary", "What a paid social hire costs"), ("compare", "Hire vs partner at five accounts"), ("breakeven", "The break-even point"),
     ("hidden", "Costs the salary doesn't show"), ("when", "When hiring is the right call"), ("faq", "Questions agencies ask")],
    f"""
      <h2 id="salary">What a paid social hire costs</h2>
      <p>Public salary data for "media buyer" and "paid social manager" is thin and inconsistent. Sources disagree by up to two times, and some UK pages rest on a handful of profiles from years ago. So we use the same published figures as our calculator, for comparable social media and performance marketing roles:</p>
      <div class="table-wrap"><table>
        <thead><tr><th scope="col">Market</th><th scope="col">Gross salary per month</th><th scope="col">With 20% employer costs</th><th scope="col">Source</th></tr></thead>
        <tbody>{"".join(f"<tr><th scope='row'>{m}</th><td>{eur(c)}</td><td>{eur(c*(1+ONCOST))}</td><td>{s}</td></tr>" for m, c, s in MARKETS)}</tbody>
      </table></div>
      <p class="fine">GBP and USD converted at the ECB reference rate of 3 November 2026. "Employer costs" is an assumption you should replace with your own: in the UK, for example, employer National Insurance is 15% above the threshold and the minimum auto-enrolment pension contribution is 3%, before equipment, software and training.</p>

      <h2 id="compare">Hire vs partner at five accounts</h2>
      <p>Take an agency with five clients running Meta ads. One specialist could handle all five. A white-label partner at {eur(FEE)} per account costs {eur(FEE*ACCTS)} a month.</p>
{figure(hbar_pairs(rows, "Monthly cost: one in-house hire vs a white-label partner for five client accounts",
                   "Grouped bars for four markets. One hire including 20% employer costs: United States about €5,878, United Kingdom about €5,551, Germany about €5,291, Netherlands €3,900 a month. White Label Media for five accounts: €2,250 a month in every market."),
        f"At five accounts a partner costs less than half of one hire in the UK, US and Germany. Hire cost includes 20% employer costs.",
        ["Market", "One hire, per month", f"Partner, {ACCTS} accounts"], [[m, eur(a), eur(b)] for m, a, b in rows],
        "salary figures as in the table above; White Label Media from €450 per account a month.")}
      <p>The gap is widest where salaries are highest. It narrows in the Netherlands, where the published median is lower, but the partner still costs less at this volume.</p>

      <h2 id="breakeven">The break-even point</h2>
      <p>The useful question isn't "is a hire expensive?" but "how many accounts must one person run before a hire costs less per account?" Divide the monthly cost of the hire by the number of accounts they run and compare it with the partner's fee.</p>
{figure(per_account_line(UK_COST, FEE, ks, "In-house cost per client account by workload, United Kingdom",
                         f"Line chart. A UK hire costing about {eur(UK_COST)} a month costs {eur(UK_COST/4)} per account at 4 accounts, {eur(UK_COST/8)} at 8 and {eur(UK_COST/16)} at 16. The White Label Media fee is a flat €450. The lines cross at about {UK_COST/FEE:.1f} accounts per person."),
        f"In the UK a hire only beats a €450 partner fee once one person runs more than about {UK_COST/FEE:.0f} accounts, every month.",
        ["Accounts per person", "In-house cost per account", "Partner fee per account"], [[k, eur(UK_COST/k), eur(FEE)] for k in ks],
        "Digital Waffle 2026 UK average, 20% employer costs assumed.")}
      <p>Twelve or more active accounts per person is a heavy load if each one gets weekly optimisation, new creative tests and a monthly report. We plan around eight accounts per person, which is why our calculator uses eight by default. Change it to match your own team.</p>

      <h2 id="hidden">Costs the salary doesn't show</h2>
      <ul>
        <li><b>Recruiting.</b> Agency fees or weeks of the founders' time, and a hiring process that can run for months.</li>
        <li><b>Ramp-up.</b> A new hire is paid in full before they are productive.</li>
        <li><b>Empty capacity.</b> If you lose a client next quarter, the salary stays the same.</li>
        <li><b>Cover.</b> One specialist means no paid social during holidays or sick leave, unless you pay for a second person or a freelancer.</li>
        <li><b>Tools.</b> Reporting, creative and analytics software per seat.</li>
      </ul>
      <p>None of these are in the charts above, so the real gap is usually larger than shown.</p>

      <h2 id="when">When hiring is the right call</h2>
      <p>A white-label partner isn't always the answer. Hire when:</p>
      <ul>
        <li>you have more than about a dozen steady paid social accounts per person you'd hire,</li>
        <li>paid social is the core of what your agency sells, not an add-on,</li>
        <li>you need someone in your office every day for client workshops and pitches.</li>
      </ul>
      <p>Many agencies do both: an in-house lead for the biggest accounts, and a partner for overflow, holidays and the smaller clients. <a href="/blog/white-label-facebook-ads/">Here is how a white-label setup works day to day.</a></p>
""",
    faq=[
        ("How much does a media buyer cost in the UK?", "Published averages vary widely. For comparable UK social media roles Digital Waffle reports an average of £46,267 a year (2026). Add employer National Insurance, pension and tools on top of the salary."),
        ("How many ad accounts can one media buyer manage?", "It depends on budgets and how much creative testing each account needs. We plan around eight active accounts per person. Past a dozen, weekly optimisation and reporting get hard to keep up."),
        ("Is outsourcing paid social cheaper than hiring?", f"Below roughly {UK_COST/FEE:.0f} accounts per person in the UK, a partner at €450 per account costs less than one hire, before counting recruiting, cover and empty capacity."),
    ]))

# ---------------------------------------------------------------- 3. pricing
prices = [750, 1000, 1200, 1500, 2000]
posts.append(article(
    "meta-ads-management-pricing",
    "How to Price Meta Ads Management for Clients | White Label Media",
    "How to price Facebook and Meta ads management for your clients",
    "Flat fee, percentage of ad spend or hybrid: how agencies price Meta ads management, what each model rewards, and the margin each price leaves with a white-label partner.",
    "Paid social pricing goes wrong in two ways: too cheap to do properly, or tied to a number the client can't see the reason for. Here are the common models, what each one rewards, and how to set a price that leaves a healthy margin.",
    [("models", "The four pricing models"), ("which", "Which model to use"), ("margin", "Your margin at each price"),
     ("scope", "What the fee should cover"), ("mistakes", "Pricing mistakes to avoid"), ("faq", "Questions agencies ask")],
    f"""
      <h2 id="models">The four pricing models</h2>
      <div class="table-wrap"><table>
        <thead><tr><th scope="col">Model</th><th scope="col">How it works</th><th scope="col">Good for</th><th scope="col">Watch out for</th></tr></thead>
        <tbody>
          <tr><th scope="row">Flat monthly fee</th><td>One fixed fee per account per month</td><td>Predictable work and budgets</td><td>Scope creep as spend grows</td></tr>
          <tr><th scope="row">Percentage of ad spend</th><td>A share of what the client spends on ads</td><td>Large, growing budgets</td><td>Rewards spending more, not results</td></tr>
          <tr><th scope="row">Hybrid</th><td>A minimum fee, or a fee plus a percentage above a spend level</td><td>Most agencies</td><td>Needs a clear spend threshold in the contract</td></tr>
          <tr><th scope="row">Performance-based</th><td>Paid per lead, sale or target hit</td><td>Mature accounts with reliable tracking</td><td>You carry the risk of the product, offer and website</td></tr>
        </tbody>
      </table></div>

      <h2 id="which">Which model to use</h2>
      <p>For most agencies adding paid social, a <b>flat fee with a spend ceiling</b> is the easiest to sell and to deliver: the client knows the cost, and you agree in writing that the fee is reviewed once monthly spend passes a set level. A pure percentage of spend is easy to explain but leaves small accounts unprofitable and invites the question "are you recommending more budget because it's good for us, or for you?"</p>
      <p>Performance pricing sounds attractive, but results depend on things you don't control, such as the product, the price, the website and stock. Use it only on accounts with proven tracking and a track record.</p>

      <h2 id="margin">Your margin at each price</h2>
      <p>If a white-label partner runs the account for {eur(FEE)} a month, your margin is simply what you bill minus that fee. Here is what you keep per account at common price points.</p>
{figure(margin_bars(FEE, prices, "Agency margin per client account at different monthly prices, with a €450 partner fee",
                    "Bar chart of monthly margin per account: billing €750 leaves €300 (40%), €1,000 leaves €550 (55%), €1,200 leaves €750 (62%), €1,500 leaves €1,050 (70%), €2,000 leaves €1,550 (78%)."),
        "Every extra euro you bill above the partner fee is margin. Percentages are your share of what the client pays.",
        ["You bill per month", "Partner fee", "You keep", "Margin"], [[eur(p), eur(FEE), eur(p - FEE), f"{(p-FEE)/p:.0%}"] for p in prices],
        "White Label Media fee from €450 per client account a month; your own prices will differ.")}
      <p>Multiply by the number of accounts to see the monthly total. At five accounts billed at {eur(1200)}, that is {eur(5*(1200-FEE))} a month, or {eur(12*5*(1200-FEE))} a year, without a hire. <a href="/#calculator">Try your own numbers in the calculator.</a></p>

      <h2 id="scope">What the fee should cover</h2>
      <p>Write the scope down, so a price is a price and not the start of a negotiation. A typical monthly paid social retainer covers:</p>
      <ul class="checklist">
        <li>Campaign structure, audiences and budgets on Facebook and Instagram</li>
        <li>Pixel, Conversions API and event checks</li>
        <li>A set number of new ad variations or creative tests per month</li>
        <li>Weekly optimisation</li>
        <li>A monthly report and a short call</li>
      </ul>
      <p>Things to price separately: new creative production (video shoots, design), landing pages, extra platforms such as TikTok or Google, and set-up for brand-new ad accounts.</p>

      <h2 id="mistakes">Pricing mistakes to avoid</h2>
      <ul>
        <li><b>Pricing below the work.</b> If the fee can't pay for weekly optimisation and testing, the account will be neglected, and the client will leave.</li>
        <li><b>Including ad spend in your invoice.</b> Keep the client's card on the client's ad account. It keeps your cash flow and VAT simple and the numbers transparent.</li>
        <li><b>No spend threshold.</b> A €2,000 account and a €40,000 account are different jobs. Say in the contract when the fee changes.</li>
        <li><b>Hiding the partner's role from your contract.</b> Your client agreement should allow specialist subcontractors under NDA.</li>
      </ul>
      <p>Before you set prices, check the reporting side too: <a href="/blog/white-label-paid-social-reporting/">what a monthly white-label report should contain</a>.</p>
""",
    faq=[
        ("Should I charge a percentage of ad spend for Facebook ads?", "It works for large, growing budgets, but on small accounts a percentage rarely pays for the work. A flat fee with a spend threshold, or a minimum fee plus a percentage, is safer."),
        ("Should ad spend go through my agency's invoice?", "Usually not. Let the client pay Meta directly from their own ad account, and invoice only your management fee."),
        ("What margin can I make reselling Meta ads management?", f"With a €450 partner fee, billing €1,000 leaves €550 per account (55%) and billing €1,500 leaves €1,050 (70%). Your own price decides the margin."),
    ]))

# ---------------------------------------------------------------- 4. reporting
posts.append(article(
    "white-label-paid-social-reporting",
    "White Label Paid Social Reporting: What to Send Clients | White Label Media",
    "White label reporting for paid social: what to send clients every month",
    "What a white-label Facebook and Meta ads report should contain, which numbers clients actually read, and a one-page layout you can brand as your own.",
    "Clients don't read dashboards. They read one page that says what was spent, what came back, what worked and what happens next. Here is a white-label report layout that does that, under your agency's logo.",
    [("what", "What white label reporting means"), ("page", "A one-page report clients read"), ("metrics", "Which numbers to include"),
     ("story", "Turn numbers into next steps"), ("tools", "Tools and delivery"), ("faq", "Questions agencies ask")],
    f"""
      <h2 id="what">What white label reporting means</h2>
      <p>A white-label report is prepared by a partner and delivered under your agency's brand: your logo, your colours, your contact details. The client sees one consistent agency, whoever ran the campaigns.</p>
      <p>Good white-label reporting is also the part of the partnership your client actually sees. The ads can be excellent, but if the report is a raw export from Ads Manager, the client will judge the work by it.</p>

      <h2 id="page">A one-page report clients read</h2>
{figure(report_mockup(), "One page, branded as your agency: four headline numbers, the month's trend, the best ad and three next steps. Figures are illustrative.",
        ["Section", "What it shows"],
        [["Header", "Your agency's logo and name, client, month"], ["Headline numbers", "Spend, results, cost per result, return on ad spend"],
         ["Trend", "Spend by week, labelled with results"], ["Best ad", "Which ad drove most results, and at what cost"], ["Next month", "Three concrete actions"]])}
      <p>You can try this on our homepage: <a href="/#demo">add your logo to the sample report</a> and see it with your agency's name on it.</p>

      <h2 id="metrics">Which numbers to include</h2>
      <p>Pick the numbers that match the client's goal, and stop there. Four is enough for the headline.</p>
      <div class="table-wrap"><table>
        <thead><tr><th scope="col">Client goal</th><th scope="col">Headline numbers</th><th scope="col">Leave out of the headline</th></tr></thead>
        <tbody>
          <tr><th scope="row">Online sales</th><td>Spend, purchases, cost per purchase, ROAS</td><td>Reach, CPM, link clicks</td></tr>
          <tr><th scope="row">Leads</th><td>Spend, leads, cost per lead, qualified leads (from the client's CRM)</td><td>Clicks, CTR</td></tr>
          <tr><th scope="row">Bookings or visits</th><td>Spend, bookings, cost per booking, new vs returning customers</td><td>Impressions</td></tr>
          <tr><th scope="row">Awareness</th><td>Spend, reach, frequency, cost per 1,000 people reached</td><td>Conversions it wasn't optimised for</td></tr>
        </tbody>
      </table></div>
      <p>Vanity metrics aren't useless. They help explain why results moved, so keep them in an appendix or in the call, not on the first page.</p>

      <h2 id="story">Turn numbers into next steps</h2>
      <p>The last box is the one clients remember. Every report should end with three plain actions, for example:</p>
      <ul class="checklist">
        <li>Scale what worked, with the budget change in euros</li>
        <li>Test one new idea, and say why</li>
        <li>Stop what didn't work</li>
      </ul>
      <p>When results dip, say so first and explain the cause in one sentence: seasonality, stock, a tracking change, a new competitor. Clients forgive a bad month far more easily than a report that hides it.</p>

      <h2 id="tools">Tools and delivery</h2>
      <p>Most agencies use a reporting tool that pulls data from Meta and lets you add your own branding, or a well-designed slide or PDF template. Whatever you use:</p>
      <ul>
        <li>send it on the same day every month,</li>
        <li>use the client's own time zone and currency,</li>
        <li>keep the partner's name off the report, but keep their data honest and unedited.</li>
      </ul>
      <p>At White Label Media, the monthly report is part of the fee, branded as your agency and ready to forward. <a href="/blog/white-label-facebook-ads/">Read how the whole partnership works.</a></p>
""",
    faq=[
        ("What should a Facebook ads report include?", "Spend, the result the campaign was optimised for, cost per result, and return on ad spend where there are sales, plus the trend, the best ad and next steps."),
        ("How often should I send clients a paid social report?", "Monthly, with a short call, is standard. Large accounts may also get a short weekly update."),
        ("Can a white label partner make reports with my logo?", "Yes. That is the point of white-label reporting: the partner prepares it, and it goes to the client under your agency's brand."),
    ]))

# ---------------------------------------------------------------- index
cards = "".join(f'<li class="post-card"><a href="/blog/{p["slug"]}/"><h2>{escape(p["h1"])}</h2><p>{escape(p["desc"])}</p><span class="more">Read the article →</span></a></li>' for p in posts)
idx = f"""    <section class="wrap prose post">
      <p class="eyebrow">Blog</p>
      <h1>Paid social for agencies</h1>
      <p class="lead">Practical guides for agencies that want to offer Meta ads without hiring a team: the maths, the pricing, the reporting and how a white-label partnership works.</p>
      <ul class="post-list">{cards}</ul>
{CTA}
    </section>"""
with open(os.path.join(REPO, "blog", "index.html"), "w") as f:
    f.write(page("/blog/", "Blog: Paid Social for Agencies | White Label Media",
                 "Guides for agencies on white label Facebook ads, hiring vs outsourcing paid social, pricing Meta ads management and client reporting.", idx))
print("built", [p["slug"] for p in posts])
