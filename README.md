# Koreatrip4 — South Korea Itinerary Site

A verified, mobile-friendly travel itinerary site for two adults visiting Seoul (Myeongdong) and Busan (Haeundae), October 31 – November 9, 2026.

## What this is

A static, dashboard-style site with day-by-day itinerary, verification table, public transit routes, dining/shopping directory, and a flagged-for-review page. Every entry is checked against official sources with links provided.

## Site structure

| Page | Description |
|------|-------------|
| `index.html` | Landing dashboard with trip overview and quick links |
| `itinerary.html` | Day-by-day schedule (Days 1–9) |
| `verification-table.html` | Line-by-line verification with source links |
| `transit.html` | Public transportation (AREX, Limousine Bus, KTX, subway) |
| `dining-shopping.html` | Restaurants, cafes, markets, stores |
| `flagged.html` | Items flagged for review (unverified / irregularities) |

## Data

`data/itinerary-data.js` — single source of truth for all itinerary entries, transit routes, and flagged items. Each entry includes:
- `verified` boolean
- `source` and `sourceUrl` (official/trusted source)
- `notes` with verification details

## Verification standard

- Every table row must have a source link to an official site.
- If a value can't be confirmed from an official source, it is left blank and flagged as unverified.
- Never infer or fill in values.

## Local development

Open any HTML file directly in a browser, or serve with a local static server:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Deployment

GitHub Pages is configured via `.github/workflows/pages.yml`. Pushing to `arena/5d411753-koreatrip4` triggers deployment.

## Sources

Primary official/trusted sources used:
- [VisitKorea (Korea Tourism Organization)](https://english.visitkorea.or.kr/)
- [Seoul Metropolitan Government](https://english.seoul.go.kr/)
- [Visit Seoul](https://english.visitseoul.net/)
- [Stanford Hotel Myeongdong](https://stanford.webhelper.co.kr/myeongdong/en/)
- [L7 Haeundae by LOTTE Hotels](https://www.lottehotel.com/)
- [Michelin Guide Seoul](https://guide.michelin.com/)
- [KORAIL / Welcome Busan (KTX)](https://welcome-busan.com/)
- Operator official pages (N Seoul Tower, DDP, Olive Young, etc.)

## License

MIT