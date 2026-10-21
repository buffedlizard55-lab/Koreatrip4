#!/usr/bin/env python3
"""Check the current root site's static HTML links and page anchors.

The deep-verification build under docs/ is checked separately by
`tools/check_links.py`; this script intentionally does not modify or generate
files in either published site. JavaScript template links containing `${...}`
are runtime values and are not treated as filesystem paths here.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_PAGES = (
    "index.html",
    "itinerary.html",
    "verification-table.html",
    "transit.html",
    "dining-shopping.html",
    "flagged.html",
    "404.html",
)
HTML_PAGES = tuple(sorted(path.name for path in ROOT.glob("*.html")))
errors: list[str] = []
contents: dict[str, str] = {}
ids_by_page: dict[str, set[str]] = {}

for page in REQUIRED_PAGES:
    if not (ROOT / page).is_file():
        errors.append(f"missing current root-site page: {page}")
if not HTML_PAGES:
    errors.append("no root HTML pages found")

for page in HTML_PAGES:
    path = ROOT / page
    text = path.read_text(encoding="utf-8")
    contents[page] = text
    ids_by_page[page] = set(re.findall(r'\bid="([^"]+)"', text))
    if 'name="viewport"' not in text:
        errors.append(f"{page}: missing responsive viewport metadata")

for page, text in contents.items():
    for ref in re.findall(r'(?:href|src)="([^"]+)"', text):
        if ref.startswith("//") or "${" in ref:
            continue
        parsed = urlsplit(ref)
        if parsed.scheme or parsed.netloc:
            continue
        raw_path = unquote(parsed.path)
        if raw_path.startswith("/"):
            target = (ROOT / raw_path.lstrip("/")).resolve()
        elif raw_path:
            target = (ROOT / raw_path).resolve()
        else:
            target = ROOT / page
        if not target.is_relative_to(ROOT):
            errors.append(f"{page}: reference escapes the repository: {ref}")
            continue
        if not target.is_file():
            errors.append(f"{page}: broken local reference -> {ref}")
            continue
        if parsed.fragment and target.suffix.lower() == ".html":
            target_page = target.relative_to(ROOT).as_posix()
            if target_page in ids_by_page and unquote(parsed.fragment) not in ids_by_page[target_page]:
                errors.append(f"{page}: missing anchor #{parsed.fragment} in {target_page}")

for asset in (
    "assets/styles.css",
    "assets/app.js",
    "assets/data.js",
    "data/itinerary-data.js",
    # Retained legacy pages are also included in the root HTML scan.
    "assets/site.css",
    "assets/site.js",
):
    if not (ROOT / asset).is_file():
        errors.append(f"missing root-site asset: {asset}")

if errors:
    print("ROOT SITE CHECKS FAILED:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)

print(f"ROOT SITE CHECKS PASSED ({len(contents)} pages, local links and anchors resolved)")
