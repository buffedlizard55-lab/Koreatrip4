#!/usr/bin/env python3
"""Pre-publish checks for the generated site in docs/.

1. Every internal href/src in every HTML file resolves to a real file/anchor.
2. Data integrity: any venue/transport row publishing a value must carry an
   official source URL; all day -> venue / flag references must exist.
External URLs are NOT fetched here (sandbox has no general internet); they were
each opened and read during the research pass on 2026-10-21 and are listed on
sources.html for manual review.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
errors = []

# ---- data integrity ----
with open(os.path.join(ROOT, "data", "itinerary.json"), encoding="utf-8") as f:
    D = json.load(f)

vids = {v["id"] for v in D["venues"]}
fids = {f["id"] for f in D["irregularities"]}
for v in D["venues"]:
    has_value = any(v.get(k) for k in ("hours", "closed", "price", "address", "station", "checkin", "checkout"))
    if has_value and not v.get("source_url"):
        errors.append(f"venue {v['id']}: publishes values without an official source_url")
    if v["status"] == "verified" and not v.get("source_url"):
        errors.append(f"venue {v['id']}: marked verified without source_url")
for t in D["transport"]:
    if t["status"] == "verified" and not t.get("source_url"):
        errors.append(f"transport {t['id']}: marked verified without source_url")
for d in D["days"]:
    for s in d["steps"]:
        if s.get("venue") and s["venue"] not in vids:
            errors.append(f"day {d['n']}: unknown venue {s['venue']}")
    for a in d["alert_ids"]:
        if a not in fids:
            errors.append(f"day {d['n']}: unknown flag {a}")

# ---- internal link check ----
html_files = [f for f in os.listdir(DOCS) if f.endswith(".html")]
if not html_files:
    errors.append("no HTML files in docs/ — run tools/build_site.py first")
ids_by_file = {}
contents = {}
for fn in html_files:
    with open(os.path.join(DOCS, fn), encoding="utf-8") as fh:
        contents[fn] = fh.read()
    ids_by_file[fn] = set(re.findall(r'id="([^"]+)"', contents[fn]))

for fn, content in contents.items():
    for href in re.findall(r'(?:href|src)="([^"]+)"', content):
        if href.startswith(("http://", "https://", "mailto:", "data:")):
            continue
        target, _, anchor = href.partition("#")
        target_file = target if target else fn
        path = os.path.join(DOCS, target_file)
        if not os.path.exists(path):
            errors.append(f"{fn}: broken internal link -> {href}")
        elif anchor and target_file.endswith(".html") and anchor not in ids_by_file.get(target_file, set()):
            errors.append(f"{fn}: missing anchor #{anchor} in {target_file}")

if errors:
    print("CHECKS FAILED:")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print(f"ALL CHECKS PASSED ({len(html_files)} pages, {len(D['venues'])} venues, {len(D['transport'])} transport rows)")
