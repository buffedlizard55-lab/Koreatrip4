# COORDINATION.md — Shared Task Board

Shared coordination board for all agent sessions working on this repo (Korea trip itinerary site).
Read this file before starting work. Claim a task (session ID + file scope), commit and push the claim
immediately, and never start a task another session has claimed.

## Session / branch note

- This project is executed by session **`arena-f4788cee`** on branch **`arena/f4788cee-koreatrip4`**
  (platform-assigned branch name; this serves as both the session branch and the final integration
  branch because no other sessions exist — verified 2026-10-21: only `main` and this branch exist,
  repo contains only a stub README).
- If another session joins later: claim a row below first, work only in your claimed file scope,
  `git pull --rebase` before every push, and log requests for files outside your scope here instead
  of editing them.

## Verification rules (binding for all sessions)

1. Every data value must come from an **official source** (venue's official website, official
   tourism/government sites: visitkorea.or.kr, visitseoul.net, visitbusan.net, royalpalace.go.kr,
   korail.com, arex.or.kr, official hotel/brand sites). No blogs, no aggregators, no inference.
2. Every table row on the site links to its official source.
3. If a value cannot be confirmed from an official source, it stays **blank** and the item is flagged
   **Unverified** on the "Flagged for Review" page. Never infer or fill in values.
4. Conflicts between the user-provided itinerary and official sources are flagged as irregularities,
   never silently "fixed" in the data — both values are shown.

## Task board

| # | Task | Status | Owner session | File scope | Notes |
|---|------|--------|---------------|------------|-------|
| T1 | Repo review + preserve original itinerary | done | arena-f4788cee | `itinerary-original.md`, `COORDINATION.md` | Repo was empty except stub README |
| T2 | Calendar/date verification (year, weekdays) | done | arena-f4788cee | `data/itinerary.json` | Weekdays match **2026**; "2006" is a typo → flagged |
| T3 | Verify transport (AREX, airport bus, KTX) from official sources | in progress | arena-f4788cee | `data/itinerary.json` | arex.or.kr, airportlimousine.co.kr, letskorail.com |
| T4 | Verify hotels (Stanford Myeongdong, L7 Haeundae) | in progress | arena-f4788cee | `data/itinerary.json` | Official hotel sites |
| T5 | Verify attractions (N Seoul Tower, Gyeongbokgung, Bukchon, DDP, COEX, markets) | in progress | arena-f4788cee | `data/itinerary.json` | Official + visitkorea/visitseoul pages |
| T6 | Verify dining/cafes/shopping venues; flag unverifiable ones | in progress | arena-f4788cee | `data/itinerary.json` | Unverified → blank + flagged |
| T7 | Build GitHub Pages site (dashboard + category subpages + Flagged page) | unclaimed → claimed | arena-f4788cee | `docs/`, `tools/build_site.py` | Static HTML generated from `data/itinerary.json` |
| T8 | Final integration: re-verify combined data, link check, build check | unclaimed → claimed | arena-f4788cee | whole repo (integration only) | Internal link checker + source audit |
| T9 | PR to `main`, merge, enable GitHub Pages, confirm live deploy | unclaimed → claimed | arena-f4788cee | — | Record PR link + result below |

## Irregularities log (running)

| # | Irregularity | Evidence | Disposition |
|---|--------------|----------|-------------|
| I-01 | Itinerary says "Nov 2, 2006" but all weekday labels match **2026** (Nov 1 2026 = Sunday). | Calendar computation; 2006-11-02 was a Thursday | Flagged for review; site uses 2026 dates, labeled as assumed |
| I-02 | Day 3 (Tue Nov 3) schedules Gyeongbokgung Palace, but itinerary itself notes palace is "Closed: Tuesdays". Guard ceremony also not held Tuesdays. | Itinerary text; to confirm at royalpalace.go.kr | Flagged for review (needs review) |
| I-03+ | Additional findings appended as verification proceeds | | |

## Sources & verification record

(Appended per task as verification completes. Each entry links the official source used.)

## PR / merge record

- PR: _(pending)_
- Merge result: _(pending)_
- GitHub Pages URL: _(pending)_

## Handoff / conflict log

- 2026-10-21 — Session arena-f4788cee created this board; no other sessions or claims found.
