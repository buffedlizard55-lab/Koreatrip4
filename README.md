# Korea Trip Desk — Seoul → Busan Itinerary (Nov 1–9, 2026)

Static, mobile-friendly GitHub Pages site(s) for a two-adult Korea itinerary:
**Seoul / Myeongdong** (Stanford Hotel Myeongdong) → **Busan / Haeundae** (L7 Haeundae by LOTTE).

**Live site:** <https://buffedlizard55-lab.github.io/Koreatrip4/>

> ℹ️ Two independent, fully verified builds of this project were produced in parallel
> (see `COORDINATION.md`). The **root site** is the live homepage. A second,
> deep-verification build lives under **`docs/`** (same domain, `/docs/`) with a
> machine-readable dataset (`data/itinerary.json`). Both are conservative:
> unconfirmed facts are left blank and flagged, never inferred.

## Root site (live homepage)

- Day-by-day itinerary review preserving the supplied plan; transport guidance anchored to
  official operator/authority material; places, food/shopping, sources, and
  **Flagged for review** pages; source chips on supported rows; custom 404.
- Files: `index.html`, `itinerary.html`, `transport.html`, `places.html`,
  `food-shopping.html`, `sources.html`, `flagged.html`, `404.html`,
  `assets/data.js` (source/itinerary dataset), `assets/site.css`, `assets/site.js`.
- Dependency-free static HTML/CSS/JS. Research snapshot checked 21 Oct 2026 UTC;
  see the in-site [source register](https://buffedlizard55-lab.github.io/Koreatrip4/sources.html).

## `docs/` deep-verification build

- 9 generated pages: Dashboard, Day by Day, Attractions & Markets, Food/Cafes/Bars,
  Shopping, Transport, Hotels, **Flagged for Review** (22 flags), Sources (27 official links).
- Every value read on an official page on 2026-10-21; blanks where unconfirmable.
- Data & tooling: `data/itinerary.json` (source of truth), `tools/build_site.py`
  (regenerates `docs/`), `tools/check_links.py` (link + source-integrity checks).
- `itinerary-original.md` preserves the owner's itinerary verbatim.

## Verification approach (both builds)

1. Claims presented as verified link to official/primary operator or authority sources.
2. No inference from similarly named venues, map estimates, old hours, or generic brand pages.
3. Transit times/fares/closures are live information — reconfirm on official pages before travel.

## Local preview

```bash
python3 -m http.server 8000 --bind 0.0.0.0   # repo root → http://localhost:8000/  (docs/ at /docs/)
python3 tools/build_site.py && python3 tools/check_links.py   # rebuild + verify the docs/ site
```

## GitHub Pages

Published from the root of `main` (legacy build). No build step or external dependency required;
`docs/` is served as a subpath of the same site.
