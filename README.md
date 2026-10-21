# Korea Trip Desk

A static, mobile-friendly GitHub Pages dashboard for a two-adult Korea itinerary covering **Seoul / Myeongdong** and **Busan / Haeundae**.

**Live site:** <https://buffedlizard55-lab.github.io/Koreatrip4/>

## What is included

- A day-by-day itinerary review that preserves the supplied plan.
- Public-transport guidance anchored to official operator or authority material where available.
- Separate places, food/shopping, sources, and **Flagged for review** pages.
- Source chips on factual table rows that are supported by an official, authority, tourism-authority, or operator page.
- Deliberately blank/`Unverified` facts when an exact branch, schedule, terminal, station, date, or route cannot be confirmed.

## Verification approach

This site is intentionally conservative:

1. It links official or primary operator sources for claims presented as verified.
2. It does not infer missing details from similarly named venues, map estimates, old opening hours, or generic brand pages.
3. Transit travel times, routes, fares, closures and booking rules are treated as live information and should be reconfirmed before travel.
4. The research snapshot in the site was checked on **21 Oct 2026 UTC**. See the in-site [source register](https://buffedlizard55-lab.github.io/Koreatrip4/sources.html) for the scope of each source.

## Local preview

The site is dependency-free. From the repository root:

```bash
python3 -m http.server 8000 --bind 0.0.0.0
```

Then open `http://localhost:8000/` locally. (In the Arena preview environment, use the preview URL shown by the running process rather than `localhost`.)

## Files

- `index.html` — dashboard
- `itinerary.html` — day-by-day plan
- `transport.html` — airport, Seoul, KTX and Busan transport review
- `places.html` — stays and core attractions
- `food-shopping.html` — food, cafés, markets, retail and activities
- `sources.html` — reviewable source register
- `flagged.html` — decisions and irregularities to resolve
- `assets/data.js` — conservative source/itinerary dataset
- `assets/site.css`, `assets/site.js` — responsive UI

## GitHub Pages

The repository is configured to publish from the root of `main` using GitHub Pages. No build output or external dependency is required.
