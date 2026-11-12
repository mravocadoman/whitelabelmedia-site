"""Inline SVG charts for the blog. Palette validated with dataviz validate_palette.js (light, white surface)."""
from html import escape

WL = "#4d6b00"      # White Label Media (olive)
HIRE = "#8a5a9e"    # in-house hire (purple)
INK, MUTED, GRID = "#16171a", "#5b5e66", "#e6e3da"


def eur(v):
    return "€" + f"{round(v):,}"


def nice(maxv, n=4):
    """Round axis: returns (top, step) with step in 1/2/2.5/5 x 10^k and about n ticks."""
    import math
    raw = maxv / n
    mag = 10 ** math.floor(math.log10(raw))
    step = next(m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= raw)
    return math.ceil(maxv / step) * step, step


def hbar_pairs(rows, title, desc, unit=eur, labels=("In-house hire", "White Label Media")):
    """rows: [(category, hire_value, wl_value)] -> grouped horizontal bars, one axis from 0."""
    w, left, right, top = 680, 120, 90, 46
    band, bh, gap = 64, 20, 4
    h = top + band * len(rows) + 34
    vmax, step = nice(max(max(r[1], r[2]) for r in rows))
    x = lambda v: left + (w - left - right) * v / vmax
    out = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d" class="chart">',
           f'<title id="t">{escape(title)}</title><desc id="d">{escape(desc)}</desc>']
    # legend
    out.append(f'<g font-size="13" fill="{INK}"><rect x="{left}" y="12" width="12" height="12" rx="3" fill="{HIRE}"/>'
               f'<text x="{left+18}" y="22">{labels[0]}</text>'
               f'<rect x="{left+150}" y="12" width="12" height="12" rx="3" fill="{WL}"/>'
               f'<text x="{left+168}" y="22">{labels[1]}</text></g>')
    for i in range(0, int(round(vmax / step)) + 1):
        v = step * i
        gx = x(v)
        out.append(f'<line x1="{gx:.1f}" x2="{gx:.1f}" y1="{top-6}" y2="{h-30}" stroke="{GRID}"/>'
                   f'<text x="{gx:.1f}" y="{h-12}" font-size="12" fill="{MUTED}" text-anchor="middle">{unit(v)}</text>')
    for i, (cat, a, b) in enumerate(rows):
        y0 = top + i * band
        out.append(f'<text x="{left-12}" y="{y0+bh+4}" font-size="14" fill="{INK}" text-anchor="end" font-weight="600">{escape(cat)}</text>')
        for j, (val, col, lab) in enumerate(((a, HIRE, labels[0]), (b, WL, labels[1]))):
            yy = y0 + j * (bh + gap)
            out.append(f'<g class="mark"><title>{escape(cat)}, {lab}: {unit(val)} a month</title>'
                       f'<rect x="{left}" y="{yy}" width="{x(val)-left:.1f}" height="{bh}" rx="4" fill="{col}"/>'
                       f'<text x="{x(val)+6:.1f}" y="{yy+15}" font-size="13" fill="{INK}">{unit(val)}</text></g>')
    out.append('</svg>')
    return "".join(out)


def per_account_line(salary_cost, fee, ks, title, desc):
    """In-house cost per account (salary_cost / k) vs flat fee, k accounts per person."""
    w, h, l, r, t, b = 680, 340, 70, 30, 30, 56
    vmax, step = nice(salary_cost / ks[0])
    X = lambda k: l + (w - l - r) * (k - ks[0]) / (ks[-1] - ks[0])
    Y = lambda v: t + (h - t - b) * (1 - v / vmax)
    o = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-labelledby="t2 d2" class="chart">',
         f'<title id="t2">{escape(title)}</title><desc id="d2">{escape(desc)}</desc>']
    for i in range(int(round(vmax / step)) + 1):
        v = step * i
        o.append(f'<line x1="{l}" x2="{w-r}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{GRID}"/>'
                 f'<text x="{l-8}" y="{Y(v)+4:.1f}" font-size="12" fill="{MUTED}" text-anchor="end">{eur(v)}</text>')
    for k in ks:
        if k % 2 == 0:
            o.append(f'<text x="{X(k):.1f}" y="{h-b+20}" font-size="12" fill="{MUTED}" text-anchor="middle">{k}</text>')
    o.append(f'<text x="{(l+w-r)/2}" y="{h-10}" font-size="12" fill="{MUTED}" text-anchor="middle">Client accounts one person runs</text>')
    pts = " ".join(f"{X(k):.1f},{Y(salary_cost/k):.1f}" for k in ks)
    o.append(f'<polyline points="{pts}" fill="none" stroke="{HIRE}" stroke-width="2"/>')
    o.append(f'<line x1="{X(ks[0])}" x2="{X(ks[-1])}" y1="{Y(fee):.1f}" y2="{Y(fee):.1f}" stroke="{WL}" stroke-width="2"/>')
    for k in ks:
        v = salary_cost / k
        o.append(f'<g class="mark"><title>{k} accounts per person: in-house {eur(v)} per account a month, White Label Media {eur(fee)}</title>'
                 f'<circle cx="{X(k):.1f}" cy="{Y(v):.1f}" r="4" fill="{HIRE}" stroke="#fff" stroke-width="2"/>'
                 f'<rect x="{X(k)-14:.1f}" y="{t}" width="28" height="{h-t-b}" fill="transparent"/></g>')
    be = salary_cost / fee
    o.append(f'<line x1="{X(be):.1f}" x2="{X(be):.1f}" y1="{t}" y2="{h-b}" stroke="{MUTED}" stroke-dasharray="4 4"/>'
             f'<text x="{X(be)+6:.1f}" y="{t+14}" font-size="12" fill="{INK}">break-even: {be:.1f} accounts</text>')
    o.append(f'<text x="{X(ks[0])+8:.1f}" y="{Y(salary_cost/ks[0])-8:.1f}" font-size="13" fill="{INK}" font-weight="600">In-house hire</text>')
    o.append(f'<text x="{X(ks[-1])-4:.1f}" y="{Y(fee)-8:.1f}" font-size="13" fill="{INK}" font-weight="600" text-anchor="end">White Label Media, {eur(fee)}</text>')
    o.append('</svg>')
    return "".join(o)


def margin_bars(fee, prices, title, desc):
    """Vertical bars: agency margin per account at each client price, single series."""
    w, h, l, r, t, b = 680, 320, 60, 20, 34, 56
    vmax, step = nice((max(prices) - fee) * 1.12)
    n = len(prices)
    slot = (w - l - r) / n
    bw = slot * 0.56
    Y = lambda v: t + (h - t - b) * (1 - v / vmax)
    o = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-labelledby="t3 d3" class="chart">',
         f'<title id="t3">{escape(title)}</title><desc id="d3">{escape(desc)}</desc>']
    for i in range(int(round(vmax / step)) + 1):
        v = step * i
        o.append(f'<line x1="{l}" x2="{w-r}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{GRID}"/>'
                 f'<text x="{l-8}" y="{Y(v)+4:.1f}" font-size="12" fill="{MUTED}" text-anchor="end">{eur(v)}</text>')
    for i, p in enumerate(prices):
        m = p - fee
        cx = l + slot * i + slot / 2
        o.append(f'<g class="mark"><title>Client pays {eur(p)}: you keep {eur(m)} ({m/p:.0%})</title>'
                 f'<path d="M{cx-bw/2:.1f},{Y(0):.1f} V{Y(m)+4:.1f} q0,-4 4,-4 H{cx+bw/2-4:.1f} q4,0 4,4 V{Y(0):.1f} Z" fill="{WL}"/>'
                 f'<text x="{cx:.1f}" y="{Y(m)-8:.1f}" font-size="13" fill="{INK}" text-anchor="middle" font-weight="600">{eur(m)} · {m/p:.0%}</text>'
                 f'<text x="{cx:.1f}" y="{h-b+20}" font-size="12" fill="{MUTED}" text-anchor="middle">{eur(p)}</text></g>')
    o.append(f'<text x="{(l+w-r)/2}" y="{h-10}" font-size="12" fill="{MUTED}" text-anchor="middle">What you bill the client per account, per month</text>')
    o.append('</svg>')
    return "".join(o)


def flow_diagram():
    """How white label works: client -> your agency -> White Label Media -> client's ad account."""
    boxes = [("Your client", "Briefs you, pays you,\nsees only your brand"),
             ("Your agency", "Owns the relationship,\nsets the price"),
             ("White Label Media", "Sets up, runs and\noptimises the ads"),
             ("Client's ad account", "Stays in the client's name,\npartner access only")]
    w, h, bw, bh = 680, 210, 150, 104
    gap = (w - 4 * bw) / 3
    o = ['<svg viewBox="0 0 680 210" role="img" aria-labelledby="t4 d4" class="chart">',
         '<title id="t4">How a white-label paid social partnership works</title>'
         '<desc id="d4">Four steps left to right: your client briefs and pays your agency; your agency passes the work to White Label Media; '
         'White Label Media runs the ads inside the client\'s own ad account through partner access; results come back as a report under your agency\'s brand.</desc>',
         '<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#5b5e66"/></marker></defs>']
    for i, (head, sub) in enumerate(boxes):
        x = i * (bw + gap)
        fill = "#4d6b00" if head == "White Label Media" else "#ffffff"
        ink = "#ffffff" if head == "White Label Media" else INK
        sub_ink = "#e9f1d6" if head == "White Label Media" else MUTED
        o.append(f'<rect x="{x+1}" y="30" width="{bw-2}" height="{bh}" rx="14" fill="{fill}" stroke="#dedad0"/>'
                 f'<text x="{x+bw/2}" y="62" font-size="14" font-weight="700" fill="{ink}" text-anchor="middle">{escape(head)}</text>')
        for j, line in enumerate(sub.split("\n")):
            o.append(f'<text x="{x+bw/2}" y="{86+j*17}" font-size="12" fill="{sub_ink}" text-anchor="middle">{escape(line)}</text>')
        if i < 3:
            o.append(f'<line x1="{x+bw+4}" x2="{x+bw+gap-6}" y1="82" y2="82" stroke="#5b5e66" stroke-width="2" marker-end="url(#ar)"/>')
    o.append(f'<path d="M{3*(bw+gap)+bw/2},{30+bh+6} V178 H{bw/2} V{30+bh+10}" fill="none" stroke="{WL}" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#ar)"/>'
             f'<text x="340" y="198" font-size="12.5" fill="{INK}" text-anchor="middle">Monthly report, branded as your agency, goes back to the client</text>')
    o.append('</svg>')
    return "".join(o)


def report_mockup():
    """A white-label monthly report page, as the client sees it."""
    o = ['<svg viewBox="0 0 680 400" role="img" aria-labelledby="t5 d5" class="chart">',
         '<title id="t5">Example of a white-label monthly paid social report</title>'
         '<desc id="d5">A one-page report with the agency\'s own logo and name at the top, four headline numbers (spend, purchases, cost per purchase, return on ad spend), '
         'a spend-and-results trend for the month, the best ad, and three plain-language next steps. Figures are illustrative.</desc>',
         '<rect x="1" y="1" width="678" height="398" rx="18" fill="#fff" stroke="#dedad0"/>',
         '<rect x="28" y="26" width="34" height="34" rx="9" fill="#16171a"/><text x="45" y="49" font-size="14" font-weight="800" fill="#fff" text-anchor="middle">YA</text>',
         '<text x="74" y="40" font-size="15" font-weight="800" fill="#16171a">Your Agency</text>',
         '<text x="74" y="57" font-size="12" fill="#5b5e66">Paid social report · October · Client: Example Store</text>',
         '<text x="652" y="45" font-size="11" fill="#5b5e66" text-anchor="end">ILLUSTRATIVE FIGURES</text>']
    tiles = [("Spend", "€4,200"), ("Purchases", "312"), ("Cost per purchase", "€13.46"), ("ROAS", "4.1×")]
    for i, (k, v) in enumerate(tiles):
        x = 28 + i * 158
        o.append(f'<rect x="{x}" y="80" width="146" height="74" rx="12" fill="#f4f2ec"/>'
                 f'<text x="{x+14}" y="104" font-size="12" fill="#5b5e66">{k}</text>'
                 f'<text x="{x+14}" y="136" font-size="24" font-weight="800" fill="#16171a">{v}</text>')
    # trend: 4 weekly bars of spend (single series) with results labels
    weeks = [(900, 61), (1050, 74), (1100, 82), (1150, 95)]
    o.append('<text x="28" y="186" font-size="13" font-weight="700" fill="#16171a">Spend by week, with purchases</text>')
    for i, (s, p) in enumerate(weeks):
        x = 40 + i * 92
        hgt = s / 1150 * 100
        o.append(f'<path d="M{x},{320} V{320-hgt+4:.1f} q0,-4 4,-4 H{x+56} q4,0 4,4 V320 Z" fill="{WL}"/>'
                 f'<text x="{x+30}" y="{320-hgt-8:.1f}" font-size="12" fill="#16171a" text-anchor="middle">{p} sales</text>'
                 f'<text x="{x+30}" y="338" font-size="11" fill="#5b5e66" text-anchor="middle">Week {i+1}</text>')
    o.append('<line x1="28" x2="400" y1="320" y2="320" stroke="#dedad0"/>')
    o.append('<rect x="420" y="172" width="232" height="96" rx="12" fill="#f4f2ec"/>'
             '<text x="434" y="196" font-size="13" font-weight="700" fill="#16171a">Best ad</text>'
             '<text x="434" y="218" font-size="12" fill="#16171a">UGC video, 15 s, "unboxing"</text>'
             '<text x="434" y="238" font-size="12" fill="#5b5e66">41% of purchases</text>'
             '<text x="434" y="256" font-size="12" fill="#5b5e66">€9.80 per purchase</text>')
    o.append('<text x="420" y="292" font-size="13" font-weight="700" fill="#16171a">Next month</text>')
    for j, t in enumerate(["Scale the UGC video by 20%", "Test two new hooks", "Pause the static carousel"]):
        o.append(f'<circle cx="428" cy="{311+j*22}" r="3" fill="{WL}"/><text x="438" y="{315+j*22}" font-size="12" fill="#16171a">{t}</text>')
    o.append('<text x="28" y="378" font-size="11" fill="#5b5e66">Prepared by Your Agency · questions: hello@youragency.com</text>')
    o.append('</svg>')
    return "".join(o)
