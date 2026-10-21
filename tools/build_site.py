#!/usr/bin/env python3
"""Build the static GitHub Pages site from data/itinerary.json into docs/.

Rules enforced here:
- Blank verified fields render as an em dash (never filled in).
- Every venue/transport row shows its status badge and official source link
  (or an explicit "no official source" marker for unverified rows).
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "itinerary.json")
OUT = os.path.join(ROOT, "docs")

with open(DATA, encoding="utf-8") as f:
    D = json.load(f)

META = D["meta"]
VENUES = {v["id"]: v for v in D["venues"]}
FLAGS = {f["id"]: f for f in D["irregularities"]}

NAV = [
    ("index.html", "🏠 Dashboard"),
    ("days.html", "🗓️ Day by Day"),
    ("attractions.html", "🏯 Attractions & Markets"),
    ("food.html", "🍜 Food, Cafes & Bars"),
    ("shopping.html", "🛍️ Shopping"),
    ("transport.html", "🚇 Transport"),
    ("hotels.html", "🛏️ Hotels"),
    ("flagged.html", "🚩 Flagged for Review"),
    ("sources.html", "📚 Sources"),
]

CSS = """
:root{--ink:#17202a;--muted:#5d6d7e;--line:#dfe6ec;--bg:#f6f8fa;--card:#fff;--accent:#0b5cad;--accent2:#083c73;
--ok:#137333;--okbg:#e6f4ea;--part:#9a6700;--partbg:#fef7e0;--bad:#b3261e;--badbg:#fce8e6;--unv:#5f6368;--unvbg:#f1f3f4}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;color:var(--ink);background:var(--bg);line-height:1.5}
a{color:var(--accent)}a:hover{color:var(--accent2)}
header.top{background:linear-gradient(160deg,#0b3b6e,#0b5cad 55%,#2a7fd2);color:#fff;padding:26px 18px 20px}
header.top h1{margin:0 0 6px;font-size:1.65rem;line-height:1.2}
header.top p{margin:2px 0;opacity:.92}
.wrap{max-width:1080px;margin:0 auto;padding:0 14px}
nav.mainnav{position:sticky;top:0;z-index:50;background:#fff;border-bottom:1px solid var(--line);box-shadow:0 1px 4px rgba(0,0,0,.05)}
nav.mainnav .wrap{display:flex;gap:4px;overflow-x:auto;padding-top:8px;padding-bottom:8px;-webkit-overflow-scrolling:touch;scrollbar-width:none}
nav.mainnav .wrap::-webkit-scrollbar{display:none}
nav.mainnav a{white-space:nowrap;text-decoration:none;color:var(--ink);font-weight:600;font-size:.9rem;padding:8px 12px;border-radius:999px;background:#eef3f8}
nav.mainnav a.active{background:var(--accent);color:#fff}
main{padding:18px 0 40px}
h2{font-size:1.3rem;margin:26px 0 10px}h3{font-size:1.05rem;margin:20px 0 8px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;margin:12px 0;box-shadow:0 1px 3px rgba(16,42,67,.05)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:14px}
.daycard{display:block;text-decoration:none;color:inherit;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px;box-shadow:0 1px 3px rgba(16,42,67,.05)}
.daycard:hover{border-color:var(--accent)}
.daycard .d{font-weight:800;color:var(--accent);font-size:.85rem;text-transform:uppercase;letter-spacing:.04em}
.daycard h3{margin:4px 0 6px;font-size:1.02rem}
.daycard p{margin:4px 0;color:var(--muted);font-size:.92rem}
.daycard.today{outline:3px solid #f2b705;outline-offset:-3px}
.alert{background:var(--badbg);border:1px solid #f2b8b5;color:#5f1410;border-radius:12px;padding:12px 14px;margin:12px 0}
.alert b{color:var(--bad)}
.note{background:#eef4fb;border:1px solid #d3e3f5;border-radius:12px;padding:12px 14px;margin:12px 0}
.badge{display:inline-block;font-size:.72rem;font-weight:700;padding:2px 9px;border-radius:999px;white-space:nowrap}
.b-verified{background:var(--okbg);color:var(--ok)} .b-partial{background:var(--partbg);color:var(--part)}
.b-conflict{background:var(--badbg);color:var(--bad)} .b-unverified{background:var(--unvbg);color:var(--unv)}
.b-crit{background:var(--bad);color:#fff}.b-high{background:#f2b8b5;color:#5f1410}.b-med{background:#fde293;color:#5b4500}.b-low{background:#e8f0fe;color:#174ea6}.b-info{background:#e8eaed;color:#3c4043}
.flagchip{display:inline-block;background:var(--badbg);color:var(--bad);font-weight:700;font-size:.78rem;border-radius:6px;padding:1px 7px;margin:2px 3px 2px 0;text-decoration:none}
.tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:12px;background:#fff;-webkit-overflow-scrolling:touch}
table{border-collapse:collapse;width:100%;min-width:760px;font-size:.92rem}
th,td{border-bottom:1px solid var(--line);padding:9px 10px;text-align:left;vertical-align:top}
th{background:#eef3f8;font-size:.8rem;text-transform:uppercase;letter-spacing:.03em;color:#33475b;position:sticky;top:0}
tr:last-child td{border-bottom:none}
td .sub{display:block;color:var(--muted);font-size:.82rem;margin-top:2px}
td .notes{display:block;font-size:.82rem;margin-top:4px}
.blank{color:#b0b7bd}
.src a{font-weight:600;font-size:.86rem}
.small{font-size:.86rem;color:var(--muted)}
.step{border-left:4px solid var(--accent);background:#fbfdff;border-radius:0 10px 10px 0;padding:8px 12px;margin:8px 0}
.step .lab{font-weight:800;color:var(--accent2)}
.step .tr{display:block;margin-top:4px;font-size:.9rem;background:#eef4fb;border-radius:8px;padding:6px 9px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:12px 0}
.kpi{background:#fff;border:1px solid var(--line);border-radius:12px;padding:12px;text-align:center}
.kpi .num{font-size:1.5rem;font-weight:800}.kpi .cap{font-size:.8rem;color:var(--muted)}
input.filter{width:100%;padding:11px 13px;border:1px solid var(--line);border-radius:10px;font-size:1rem;margin:8px 0 12px}
footer{border-top:1px solid var(--line);background:#fff;padding:20px 0 34px;color:var(--muted);font-size:.88rem}
ol.sources li{margin:7px 0}
.anchors a{display:inline-block;margin:3px 5px 3px 0;background:#eef3f8;border-radius:999px;padding:5px 11px;text-decoration:none;font-weight:600;font-size:.85rem;color:var(--ink)}
@media (max-width:640px){header.top h1{font-size:1.35rem}table{min-width:680px}body{font-size:15px}}
@media print{nav.mainnav,input.filter{display:none}body{background:#fff}.card,.daycard{box-shadow:none}}
"""

def esc(s):
    return html.escape(str(s or ""), quote=True)

def dash(s):
    return esc(s) if s else '<span class="blank">—</span>'

def badge(status):
    return f'<span class="badge b-{esc(status)}">{esc(status.capitalize())}</span>'

def sev_badge(sev):
    cls = {"Critical": "b-crit", "High": "b-high", "Medium": "b-med", "Low": "b-low", "Info": "b-info"}.get(sev, "b-info")
    return f'<span class="badge {cls}">{esc(sev)}</span>'

def src_links(v):
    parts = []
    if v.get("source_url"):
        parts.append(f'<a href="{esc(v["source_url"])}" target="_blank" rel="noopener">{esc(v.get("source_label") or "Official source")} ↗</a>')
    if v.get("source2_url"):
        parts.append(f'<a href="{esc(v["source2_url"])}" target="_blank" rel="noopener">{esc(v.get("source2_label") or "Official source 2")} ↗</a>')
    if not parts:
        return '<span class="blank">No official source found — flagged</span>'
    return "<br>".join(parts)

def page(title, active, body):
    nav = "".join(
        f'<a href="{href}" class="{"active" if href==active else ""}">{label}</a>' for href, label in NAV
    )
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · Korea Trip Itinerary</title>
<link rel="stylesheet" href="assets/style.css"></head>
<body>
<header class="top"><div class="wrap">
<h1>🇰🇷 {esc(META["title"])}</h1>
<p><b>{esc(META["dates_label"])}</b> · {esc(META["travelers"])} · Seoul (Myeongdong) → Busan (Haeundae)</p>
<p class="small" style="color:#dcebfb">Verified against official sources on {esc(META["verified_on"])}. {esc(META["rule"])}</p>
</div></header>
<nav class="mainnav"><div class="wrap">{nav}</div></nav>
<main><div class="wrap">
{body}
</div></main>
<footer><div class="wrap">
<p>Built from <code>data/itinerary.json</code> in the <a href="https://github.com/buffedlizard55-lab/Koreatrip4" target="_blank" rel="noopener">Koreatrip4 repo</a> · Verification pass {esc(META["verified_on"])} · Hours, fares and closures change — always re-check the linked official page before you go. Items marked Unverified are deliberately blank and listed on the <a href="flagged.html">Flagged for Review</a> page.</p>
</div></footer>
<script>
document.querySelectorAll('input.filter').forEach(function(inp){{
  inp.addEventListener('input',function(){{
    var q=inp.value.toLowerCase();
    document.querySelectorAll('table[data-filterable] tbody tr').forEach(function(tr){{
      tr.style.display = tr.textContent.toLowerCase().indexOf(q)>-1 ? '' : 'none';
    }});
  }});
}});
(function(){{
  var today = new Date().toISOString().slice(0,10);
  document.querySelectorAll('[data-date]').forEach(function(el){{
    if(el.getAttribute('data-date')===today){{ el.classList.add('today'); el.insertAdjacentHTML('afterbegin','<span class="badge b-high">TODAY</span> '); }}
  }});
}})();
</script>
</body></html>"""

def venue_row(v):
    notes = "".join(f'<span class="notes">• {esc(n)}</span>' for n in v.get("notes", []))
    says = f'<span class="sub">Your itinerary: “{esc(v["itinerary_says"])}”</span>' if v.get("itinerary_says") else ""
    days = ", ".join(f"Day {d}" for d in v.get("days", [])) or "—"
    extra = v.get("checkin") or v.get("checkout")
    pricecell = v.get("price", "")
    if v["category"] == "Hotel":
        pricecell = f'Check-in {v.get("checkin") or "—"} · Check-out {v.get("checkout") or "—"}' if extra else ""
    return f"""<tr>
<td><b>{esc(v["name"])}</b><span class="sub">As written: {esc(v["as_written"])}</span>{says}{notes}</td>
<td>{esc(v["city"])}<span class="sub">{esc(v["area"])}</span><span class="sub">{dash(v.get("address"))}</span></td>
<td>{esc(days)}</td>
<td>{dash(v.get("hours"))}</td>
<td>{dash(v.get("closed"))}</td>
<td>{dash(pricecell)}</td>
<td>{dash(v.get("station"))}</td>
<td>{badge(v["status"])}</td>
<td class="src">{src_links(v)}</td></tr>"""

def venue_table(venues):
    rows = "".join(venue_row(v) for v in venues)
    return f"""<div class="tablewrap"><table data-filterable>
<thead><tr><th>Place</th><th>City / Area / Address</th><th>Trip day</th><th>Hours (verified)</th><th>Closed days</th><th>Price / Check-in–out</th><th>Nearest station</th><th>Status</th><th>Official source</th></tr></thead>
<tbody>{rows}</tbody></table></div>"""

def cat_page(fn, title, intro, cats):
    body = f"<h2>{esc(title)}</h2><p>{intro}</p><input class=\"filter\" type=\"search\" placeholder=\"Filter places… (try: verified, Seongsu, 10:30)\">"
    for cat in cats:
        vs = [v for v in D["venues"] if v["category"] == cat]
        if vs:
            body += f"<h3>{esc(cat)} ({len(vs)})</h3>" + venue_table(vs)
    return page(title, fn, body)

# ---------------- Dashboard ----------------
def build_index():
    crit = [f for f in D["irregularities"] if f["severity"] in ("Critical", "High")]
    counts = {"verified": 0, "partial": 0, "conflict": 0, "unverified": 0}
    for v in D["venues"]:
        counts[v["status"]] += 1
    cards = ""
    for d in D["days"]:
        chips = "".join(
            f'<a class="flagchip" href="flagged.html#{esc(a)}">{esc(a)}</a>' for a in d["alert_ids"]
        )
        cards += f"""<a class="daycard" data-date="{esc(d["date"])}" href="days.html#day{d["n"]}">
<span class="d">Day {d["n"]} · {esc(d["weekday"])} {esc(d["date"])}</span>
<h3>{esc(d["title"])}</h3><p>🛏️ {esc(d["base"])}</p><p>{esc(d["summary"])}</p>{chips}</a>"""
    crit_items = "".join(
        f'<li><b>{esc(f["id"])}</b> {sev_badge(f["severity"])} <a href="flagged.html#{esc(f["id"])}">{esc(f["title"])}</a></li>' for f in crit
    )
    body = f"""
<div class="alert"><b>⚠️ Read first — {len(crit)} critical/high findings</b> (full list: <a href="flagged.html">Flagged for Review</a>)<ul>{crit_items}</ul></div>
<div class="kpis">
<div class="kpi"><div class="num">{len(D["venues"])}</div><div class="cap">Places checked line-by-line</div></div>
<div class="kpi"><div class="num">{counts["verified"]}</div><div class="cap">Fully verified (official source)</div></div>
<div class="kpi"><div class="num">{counts["partial"]}</div><div class="cap">Partially verified</div></div>
<div class="kpi"><div class="num">{counts["conflict"]}</div><div class="cap">Conflicts with itinerary</div></div>
<div class="kpi"><div class="num">{counts["unverified"]}</div><div class="cap">Unverified — blank &amp; flagged</div></div>
<div class="kpi"><div class="num">{len(D["irregularities"])}</div><div class="cap">Flags for your review</div></div>
</div>
<div class="card"><h3 style="margin-top:0">Bases</h3>
<p>🛏️ <b>Nov 1–9:</b> <a href="hotels.html">Stanford Hotel Myeongdong</a> (Euljiro 1-ga, Line 2) → <b>from Nov 9:</b> <a href="hotels.html">L7 Haeundae by LOTTE, Busan</a></p>
<p class="small">Status key: <span class="badge b-verified">Verified</span> read on the official source · <span class="badge b-partial">Partial</span> some fields official, rest blank · <span class="badge b-conflict">Conflict</span> official source contradicts the itinerary · <span class="badge b-unverified">Unverified</span> not confirmable officially — left blank, never guessed.</p></div>
<h2>Day by day</h2><div class="grid">{cards}</div>
<h2>Getting around (verified anchors)</h2>
<div class="card">
<p>✈️ <b>ICN → hotel:</b> AREX Express ₩13,000 (43–51 min) · AREX All-Stop ₩4,150–4,750 via Hongik Univ. → Line 2 · Bus 6015 to the hotel block (fare unconfirmed). → <a href="transport.html">Transport</a></p>
<p>🚌 <b>Bus 01A (₩1,500)</b> from outside Lotte links the hotel to N Seoul Tower, Gyeongbokgung Palace and Insadong (Days 2, 3, 6).</p>
<p>🚇 <b>Line 2 direct from the hotel</b> (Euljiro 1-ga) to Seongsu (Day 4) and Samseong/COEX (Day 5). 🚄 <b>KTX Seoul→Busan:</b> book at korail.com — time/fare unverified here by design.</p></div>
"""
    return page("Dashboard", "index.html", body)

# ---------------- Days ----------------
def build_days():
    toc = "".join(f'<a href="#day{d["n"]}">Day {d["n"]} · {esc(d["weekday"][:3])} {esc(d["date"][5:])}</a>' for d in D["days"])
    body = f"<h2>Day by Day</h2><p>Times shown are <b>verified opening hours from official sources</b>; anything from the original itinerary that couldn't be verified is labeled. Steps keep your order — flagged problems are called out, not silently fixed.</p><p class=\"anchors\">{toc}</p>"
    for d in D["days"]:
        steps = ""
        for s in d["steps"]:
            vb = ""
            if s.get("venue") and s["venue"] in VENUES:
                v = VENUES[s["venue"]]
                vb = f' {badge(v["status"])}'
            tr = f'<span class="tr">🚇 {esc(s["transit"])}</span>' if s.get("transit") else ""
            steps += f'<div class="step"><span class="lab">{esc(s["label"])}</span>{vb}<br>{esc(s["text"])}{tr}</div>'
        day_venues = [v for v in D["venues"] if d["n"] in v.get("days", [])]
        chips = "".join(f'<a class="flagchip" href="flagged.html#{esc(a)}">{esc(a)} {esc(FLAGS[a]["title"])}</a>' for a in d["alert_ids"])
        body += f"""<section class="card" id="day{d["n"]}" data-date="{esc(d["date"])}">
<h3 style="margin-top:0">Day {d["n"]} · {esc(d["weekday"])}, {esc(d["date"])} — {esc(d["title"])}</h3>
<p class="small">🛏️ Base: {esc(d["base"])}</p><p>{esc(d["summary"])}</p>{steps}
<p>{chips}</p>
<h4>Places today ({len(day_venues)})</h4>{venue_table(day_venues) if day_venues else '<p class="small">No named places for this day yet.</p>'}
</section>"""
    return page("Day by Day", "days.html", body)

# ---------------- Transport ----------------
def build_transport():
    rows = ""
    for t in D["transport"]:
        notes = "".join(f'<span class="notes">• {esc(n)}</span>' for n in t.get("notes", []))
        says = f'<span class="sub">Your itinerary: “{esc(t["itinerary_says"])}”</span>' if t.get("itinerary_says") else ""
        src = (f'<a href="{esc(t["source_url"])}" target="_blank" rel="noopener">{esc(t["source_label"])} ↗</a>'
               if t.get("source_url") else '<span class="blank">No official source — flagged</span>')
        days = ", ".join(f"Day {x}" for x in t.get("days", []))
        rows += f"""<tr><td><b>{esc(t["name"])}</b><span class="sub">{esc(t["route"])}</span>{says}{notes}</td>
<td>{esc(days)}</td><td>{dash(t.get("duration"))}</td><td>{dash(t.get("fare"))}</td><td>{dash(t.get("frequency"))}</td>
<td>{badge(t["status"])}</td><td class="src">{src}</td></tr>"""
    anchors = ""
    seen = []
    for v in D["venues"]:
        if v.get("station"):
            anchors += f'<tr><td>{esc(v["name"].split(" — ")[0])}</td><td>{esc(v["station"])}</td><td>{badge(v["status"])}</td></tr>'
            seen.append(v["id"])
    body = f"""<h2>Transport</h2>
<p>Every fare/time below was read on an official page (linked). Durations for subway rides inside Seoul are <b>not</b> published here unless an official source states them — use live routing on the day (Naver Map; Google Maps transit does not work properly in Korea).</p>
<h3>Airport, intercity &amp; key city legs</h3>
<div class="tablewrap"><table>
<thead><tr><th>Leg</th><th>Trip day</th><th>Duration (verified)</th><th>Fare (verified)</th><th>Frequency / hours</th><th>Status</th><th>Official source</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<div class="note"><b>Verified cost snapshot (per adult, official KRW):</b> AREX Express ₩13,000 · AREX All-Stop ₩4,150–4,750 · Namsan bus 01A/01B ₩1,500 · N Seoul Tower observatory ₩29,000 · Namsan Cable Car round-trip ₩15,000 · Gyeongbokgung Palace ₩3,000. No USD conversions are published (no FX source) — see flag F-21.</div>
<h3>Nearest-station anchors (from official venue pages)</h3>
<div class="tablewrap"><table><thead><tr><th>Place</th><th>Nearest station (as published officially)</th><th>Place status</th></tr></thead><tbody>{anchors}</tbody></table></div>
"""
    return page("Transport", "transport.html", body)

# ---------------- Hotels ----------------
def build_hotels():
    hotels = [v for v in D["venues"] if v["category"] == "Hotel"]
    body = "<h2>Hotels</h2><p>Check-in/out times are published only if read on the hotel's official website — confirm against your booking confirmations.</p>" + venue_table(hotels)
    body += """<div class="card"><h3>Hotel → KTX (Day 9)</h3>
<p>Stanford Hotel Myeongdong → Seoul Station: taxi per itinerary, or Line 4 (Myeong-dong/Hoehyeon → Seoul Station; Lines 1 &amp; 4 + KTX per Seoul City). Busan Station → L7 Haeundae: taxi per itinerary. Details on the <a href="transport.html">Transport</a> page.</p></div>"""
    return page("Hotels", "hotels.html", body)

# ---------------- Flagged ----------------
def build_flagged():
    frows = ""
    for f in D["irregularities"]:
        frows += f"""<tr id="{esc(f["id"])}"><td><b>{esc(f["id"])}</b></td><td>{sev_badge(f["severity"])}</td>
<td><b>{esc(f["title"])}</b><span class="notes">{esc(f["detail"])}</span></td><td>{esc(f["action"])}</td></tr>"""
    unv = [v for v in D["venues"] if v["status"] in ("unverified", "partial", "conflict")]
    urows = ""
    for v in unv:
        missing = [k for k, label in (("hours", "hours"), ("closed", "closed days"), ("price", "price"), ("address", "address"), ("station", "station")) if not v.get(k)]
        urows += f"""<tr><td><b>{esc(v["name"])}</b><span class="sub">{esc(v["category"])} · {esc(v["area"])}</span></td>
<td>{badge(v["status"])}</td><td>{esc(", ".join(missing) or "—")}</td><td class="src">{src_links(v)}</td></tr>"""
    unv_t = [t for t in D["transport"] if t["status"] != "verified"]
    for t in unv_t:
        missing = [k for k in ("duration", "fare", "frequency") if not t.get(k)]
        src = (f'<a href="{esc(t["source_url"])}" target="_blank" rel="noopener">{esc(t["source_label"])} ↗</a>'
               if t.get("source_url") else '<span class="blank">None</span>')
        urows += f"""<tr><td><b>{esc(t["name"])}</b><span class="sub">Transport · {esc(t["route"])}</span></td>
<td>{badge(t["status"])}</td><td>{esc(", ".join(missing) or "—")}</td><td class="src">{src}</td></tr>"""
    sugg = "".join(f'<div class="card"><b>{esc(s["id"])} — {esc(s["title"])}</b><p>{esc(s["detail"])}</p></div>' for s in D["suggestions"])
    body = f"""<h2>🚩 Flagged for Review</h2>
<p>Everything on this page needs a human decision or a manual check. Nothing here blocked publication — but items marked Critical/High will affect the trip (the Tuesday palace closure most of all). Unverified values are <b>blank on purpose</b>.</p>
<h3>Irregularities ({len(D["irregularities"])})</h3>
<div class="tablewrap"><table><thead><tr><th>ID</th><th>Severity</th><th>Finding &amp; evidence</th><th>What to do</th></tr></thead><tbody>{frows}</tbody></table></div>
<h3>Items with blank (unverified) fields ({len(unv) + len(unv_t)})</h3>
<p class="small">To verify a blank: open the official link (if any) or find the venue's official site / Naver Map listing operated by the venue, then update <code>data/itinerary.json</code> and rebuild.</p>
<div class="tablewrap"><table><thead><tr><th>Item</th><th>Status</th><th>Fields left blank</th><th>Official source (if any)</th></tr></thead><tbody>{urows}</tbody></table></div>
<h3>Suggested fixes — need your approval (not applied)</h3>{sugg}"""
    return page("Flagged for Review", "flagged.html", body)

# ---------------- Sources ----------------
def build_sources():
    items = "".join(f'<li><a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["label"])} ↗</a><br><span class="small">{esc(s["url"])}</span></li>' for s in D["official_sources"])
    body = f"""<h2>📚 Official Sources &amp; Method</h2>
<div class="card"><h3 style="margin-top:0">How verification worked</h3>
<p>Each itinerary line was checked against an <b>official source only</b>: the venue's/operator's own website, or an official tourism/government publisher (Korea Tourism Organization / Visit Korea, Visit Seoul, Visit Busan, Visit Gangnam, Seoul Metropolitan Government, palace &amp; foundation sites, Korail, Airport Limousine Co.). Blog posts, OTAs, map listings and review sites were used only to <i>find</i> official pages — never as evidence. All links below were opened and read on {esc(META["verified_on"])}.</p>
<p>If a value could not be read on an official page, it is blank on this site and listed under <a href="flagged.html">Flagged for Review</a>. Weekday/date checks were computed against the 2026 calendar. The original itinerary text is preserved verbatim in <code>itinerary-original.md</code> in the repo.</p></div>
<ol class="sources">{items}</ol>"""
    return page("Sources", "sources.html", body)

def main():
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    with open(os.path.join(OUT, "assets", "style.css"), "w", encoding="utf-8") as f:
        f.write(CSS)
    with open(os.path.join(OUT, ".nojekyll"), "w", encoding="utf-8") as f:
        f.write("")
    pages = {
        "index.html": build_index(),
        "days.html": build_days(),
        "attractions.html": cat_page("attractions.html", "Attractions & Markets",
            "Palaces, towers, markets and activities. “Hours” are shown exactly as published by official sources; blanks mean unverified.",
            ["Attraction", "Market", "Activity"]),
        "food.html": cat_page("food.html", "Food, Cafes & Bars",
            "Restaurants, cafes/bakeries and bars from the itinerary. Most small independents have no official English pages we could verify — those rows stay blank and flagged.",
            ["Restaurant", "Cafe & Bakery", "Bar"]),
        "shopping.html": cat_page("shopping.html", "Shopping",
            "Department stores and Seongsu/Myeongdong shops. Department-store hours change monthly — always confirm the specific date on the official calendar.",
            ["Shopping"]),
        "transport.html": build_transport(),
        "hotels.html": build_hotels(),
        "flagged.html": build_flagged(),
        "sources.html": build_sources(),
    }
    for fn, content in pages.items():
        with open(os.path.join(OUT, fn), "w", encoding="utf-8") as f:
            f.write(content)
        print("built", fn, f"({len(content)} bytes)")

if __name__ == "__main__":
    main()
