# Koreatrip4 — Korea Trip Itinerary (Seoul → Busan)

A verified, mobile-friendly travel itinerary site for two adults, Nov 1–9, 2026:
8 nights based in Myeongdong, Seoul (Stanford Hotel Myeongdong), then Busan (L7 Haeundae by LOTTE).

**Live site (GitHub Pages):** published from `docs/` on `main` — see `COORDINATION.md` for the URL.

## How to read the site

- **Dashboard** — trip overview, critical warnings, day cards.
- **Day by Day** — the plan for each day with verified opening hours and step-by-step transit.
- **Attractions & Markets / Food, Cafes & Bars / Shopping / Hotels** — every place in tables:
  verified hours, closed days, prices, nearest station, status, and an **official source link**.
- **Transport** — AREX, airport bus 6015, Namsan buses 01A/01B, subway anchors, KTX booking.
- **Flagged for Review** — all 22 irregularities, every unverified (blank) item, suggested fixes.
- **Sources** — the 27 official links used and the verification method.

## Verification rule

Every published value was read on an **official source** (venue/operator site or official
tourism/government publisher). Anything not confirmable is **left blank and flagged** — never
inferred, never converted from USD. See `COORDINATION.md` for the full verification record.

## Repo layout

| Path | What it is |
|---|---|
| `itinerary-original.md` | The trip owner's itinerary, preserved verbatim |
| `data/itinerary.json` | Single source of truth: days, venues, transport, flags, sources |
| `tools/build_site.py` | Generates the static site into `docs/` from the JSON |
| `tools/check_links.py` | Internal-link + data-integrity checks (must pass before publishing) |
| `docs/` | Generated GitHub Pages site (do not hand-edit) |
| `COORDINATION.md` | Multi-session task board, verification log, irregularities, PR record |

## Rebuild

```bash
python3 tools/build_site.py   # regenerate docs/
python3 tools/check_links.py  # verify links + source integrity
```
