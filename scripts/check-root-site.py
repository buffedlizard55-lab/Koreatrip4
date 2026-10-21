#!/usr/bin/env python3
"""Check the live root site's static HTML links and page anchors.

The deep-verification build under docs/ is checked separately by
`tools/check_links.py`; this script intentionally does not modify or generate
files in either published site.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
HTML_PAGES = (
    "index.html",
    "itinerary.html",
    "transport.html",
    "places.html",
    "food-shopping.html",
    "sources.html",
    "flagged.html",
    "404.html",
)
errors: list[str] = []
contents: dict[str, str] = {}
ids_by_page: dict[str, set[str]] = {}

for page in HTML_PAGES:
    path = ROOT / page
    if not path.is_file():
        errors.append(f"missing root page: {page}")
        continue
    text = path.read_text(encoding="utf-8")
    contents[page] = text
    ids_by_page[page] = set(re.findall(r'\bid="([^"]+)"', text))
    if 'name="viewport"' not in text:
        errors.append(f"{page}: missing responsive viewport metadata")

for page, text in contents.items():
    for ref in re.findall(r'(?:href|src)="([^"]+)"', text):
        if ref.startswith("//"):
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

for asset in ("assets/data.js", "assets/site.css", "assets/site.js"):
    if not (ROOT / asset).is_file():
        errors.append(f"missing root-site asset: {asset}")

if errors:
    print("ROOT SITE CHECKS FAILED:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)

print(f"ROOT SITE CHECKS PASSED ({len(contents)} pages, local links and anchors resolved)")
