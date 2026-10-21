# COORDINATION.md — Shared Task Board

Shared coordination board for all agent sessions working on this repo (Korea trip itinerary site).
Read this file before starting work. Claim a task (session ID + file scope), commit and push the claim
immediately, and never start a task another session has claimed.

## Session / branch note

- Executed by session **`arena-f4788cee`** on branch **`arena/f4788cee-koreatrip4`** (platform-assigned
  branch name; serves as session + integration branch — no other sessions exist; verified 2026-10-21:
  only `main` and this branch, repo started as a stub README).
- If another session joins later: claim a row below first, work only in your claimed file scope,
  `git pull --rebase` before every push, and log requests for files outside your scope here instead
  of editing them. Claims stale >60 min with no commits may be taken over with a handoff note below.

## Verification rules (binding for all sessions)

1. Every data value must come from an **official source** (venue/operator official site, or official
   tourism/government publishers: visitkorea.or.kr, visitseoul.net, visitbusan.net, seoul.go.kr,
   royalpalacekr.org, korail.com, airportlimousine.co.kr, official hotel/brand sites). No blogs, OTAs,
   aggregators, or inference as evidence.
2. Every published table row links to its official source.
3. If a value cannot be read on an official page, it stays **blank** and the item is flagged on the
   site's "Flagged for Review" page. Never infer or fill in values (no USD conversions without an FX source).
4. Conflicts between the itinerary and official sources are flagged with both values shown — never
   silently corrected.

## Task board

| # | Task | Status | Owner session | File scope | Notes |
|---|------|--------|---------------|------------|-------|
| T1 | Repo review + preserve original itinerary | done | arena-f4788cee | `itinerary-original.md` | Repo was empty except stub README |
| T2 | Calendar/date verification | done | arena-f4788cee | `data/itinerary.json` | Weekdays match **2026**; "2006" = typo (F-01) |
| T3 | Verify transport (AREX, bus 6015, Namsan buses, KTX) | done | arena-f4788cee | `data/itinerary.json` | KTX fare/time + 6015 fare unverified → blank (F-11/F-12) |
| T4 | Verify hotels (Stanford Myeongdong, L7 Haeundae) | done | arena-f4788cee | `data/itinerary.json` | Check-in/out unverified for both (F-13) |
| T5 | Verify attractions (tower, palace, Bukchon, DDP, COEX, markets) | done | arena-f4788cee | `data/itinerary.json` | Palace closed Tue (F-02); Bukchon curfew (F-14) |
| T6 | Verify dining/cafes/shopping; flag unverifiable | done | arena-f4788cee | `data/itinerary.json` | 28 of 46 venues unverified (no official pages) → blank |
| T7 | Build GitHub Pages site (dashboard + subpages) | done | arena-f4788cee | `docs/`, `tools/build_site.py` | Generated from `data/itinerary.json`; 9 pages |
| T8 | Integration: re-verify combined data, link/build checks | done | arena-f4788cee | `tools/check_links.py` | All checks pass (internal links + source integrity) |
| T9 | PR → merge → enable Pages → confirm live | in progress | arena-f4788cee | — | Record below |

## Verification record (2026-10-21, session arena-f4788cee)

All values below were read directly on the linked official pages on 2026-10-21. Full source list:
site `sources.html` / `data/itinerary.json` → `official_sources` (27 links).

**Verified (9 venues):** Namsan Outdoor Escalator (hours + Mon suspension), Bukchon Red Zone restriction
(10:00–17:00, ₩100,000 fine), Starfield COEX Mall (10:30–22:00), Starfield Library (10:30–22:00, free),
Mangwon Market (10:00–21:00 varies), Haeundae Market (09:00–22:00), Myeongdong Kyoja (10:30–21:00,
relocated 129 Toegye-ro, Michelin-listed), Cafe Onion Anguk (wkday 07:00–22:00), Cafe Onion Seongsu (wkday 08:00–22:00).
**Verified with conflicts vs itinerary (5):** N Seoul Tower observatory (₩29,000; Mon closes 22:30),
Namsan Cable Car (10:00–23:00; ₩15,000 RT), Gyeongbokgung Palace (09:00–17:00 Nov; CLOSED Tuesdays; ₩3,000),
Gwangjang Market (food alley 09:00–23:00), DDP (Dongdaemun, not Seongsu; 10:00–20:00).
**Partially verified (4):** Stanford Hotel (address/station yes; check times no), Lotte Dept. Main
(hours yes; Nov 2 calendar day-type no), Shinsegae Main (hours yes; monthly closures vary),
Gangnam Style statue (location yes; hours n/a unpublished).
**Unverified (28 venues + KTX + 6015 fare + Busan taxi):** left blank and flagged — mostly small
independent restaurants/cafes/shops in Seongsu, Ikseon-dong, Myeongdong without official pages
readable/confirmable this pass, plus unnamed items (tea house, palace lunch, caricature studio).
**Transport verified:** AREX Express (₩13,000; 43/51 min) & All-Stop (₩4,150–4,750; 59/66 min) via Seoul
Metropolitan Government; Namsan shuttle 01A/01B (₩1,500; routes incl. Lotte stop 02140 → tower/palace/
Insadong) via tower official + Lotte official; subway anchors (lines/exits) only from official venue pages.

Checks run: `python3 tools/build_site.py` (9 pages generated) + `python3 tools/check_links.py`
→ ALL CHECKS PASSED (internal links/anchors resolve; every row publishing a value has an official
source URL; no dangling day→venue/flag references). Local preview served on :8000, all pages HTTP 200.
External links are not machine-fetchable from the sandbox; each was opened/read during research today.

## Irregularities log (22 flags — full text on site `flagged.html`, data `irregularities`)

| ID | Sev | Summary |
|----|-----|---------|
| F-01 | Info | "Nov 2, 2006" typo — weekdays match 2026 |
| F-02 | **Critical** | Gyeongbokgung Palace planned Tue Nov 3 — palace CLOSED Tuesdays, guard ceremony not held |
| F-03 | High | N Seoul Tower hours in itinerary wrong (official 10:00–22:30 Mon) |
| F-04 | High | Cable car hours wrong (official 10:00–23:00) |
| F-05 | High | Gwangjang hours wrong (food alley 09:00–23:00; no 2am stalls officially) |
| F-06 | Medium | DDP filed under Seongsu; it's in Dongdaemun — description swapped |
| F-07 | Medium | Rain Report Cafe in both Seongsu (D4) and Insadong (D6) |
| F-08 | Medium | Merged/duplicate restaurant notes (Uri Wang Galbitang / Chwihyang / "Favorite of Ikseon") |
| F-09 | Low | Misspellings: Namsun, Myeongdog, Starfiel, Musina, Limosine |
| F-10 | Medium | AREX "$7" matches neither official fare |
| F-11 | Medium | Bus 6015 fare unconfirmed on operator site (route/stops verified) |
| F-12 | High | KTX time/fare unverified (train-dependent); "board 45 min early" has no official basis |
| F-13 | Medium | Stanford check-in/out not on official site text (itinerary's 12:00 checkout unverified) |
| F-14 | High | Bukchon tourist curfew (17:00–10:00, ₩100k fine) missing from itinerary |
| F-15 | Medium | Namsan escalator suspended Mon 09:00–14:00 — Day 2 is Monday |
| F-16 | Medium | Dept-store monthly closed day: Lotte Main closed Mon Nov 9; Nov 2 status unconfirmed |
| F-17 | High | Gaps: Day 7 no venues, Day 8 blank, no Busan days, no flights/return plan |
| F-18 | Medium | Myeongdong Kyoja main branch relocated 2026 → 129 Toegye-ro (KTO EN address outdated) |
| F-19 | Info | Palace free-admission wording differs (KTO vs palace office); adult ₩3,000 same |
| F-20 | Low | "Soul Market" at COEX unidentified from official info |
| F-21 | Info | All itinerary USD prices unverified (site uses official KRW only) |
| F-22 | Info | Day 9 list numbering repeats "1." (cosmetic) |

Status key: these are all **needs review** (published on Flagged for Review) and do not block the merge,
per project instructions. Suggested fixes S-1…S-4 are listed on the Flagged page, not applied.

## PR / merge record

- PR: [#3](https://github.com/buffedlizard55-lab/Koreatrip4/pull/3) — arena/f4788cee-koreatrip4 → main (created 2026-10-21, session arena-f4788cee)
- Merge result: merging immediately after this commit, per instructions (final result in follow-up PR)
- GitHub Pages URL: _(pending)_

## Handoff / conflict log

- 2026-10-21 — Session arena-f4788cee created this board; no other sessions or claims found.
- 2026-10-21 — T1–T8 completed by arena-f4788cee; proceeding to T9 (PR/merge/Pages) without waiting
  for review, per instructions. No merge conflicts encountered (single session).
