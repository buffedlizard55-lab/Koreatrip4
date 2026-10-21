# Project Coordination & Shared Task Board (`COORDINATION.md`)

> **Branch Policy Note**: This session (`5d411753`) is bound to the fixed branch `arena/5d411753-koreatrip4`. Per platform policy, the current branch name is fixed and all commits, pushes, and pull requests from this session are performed on `arena/5d411753-koreatrip4`.

## Active Session Registry

| Session ID | Branch | Role | Started (UTC) | Status |
| :--- | :--- | :--- | :--- | :--- |
| `5d411753` | `arena/5d411753-koreatrip4` | Full Verification, Site Creation, Transit Analysis & Final Integration | 2026-10-21 | In Progress |

---

## Shared Task Board

| Task ID | Task Description | Status | Owning Session | File Scope |
| :--- | :--- | :--- | :--- | :--- |
| `TASK-01` | Line-by-line verification of Days 1–3 (ICN Airport, AREX, Limousine Bus, Stanford Hotel Myeongdong, N Seoul Tower, Myeongdong Shopping/Dining/Night Markets, Gyeongbokgung Palace, Bukchon Hanok Village) | `done` | `5d411753` | `data/itinerary-data.js`, `verification-table.html` |
| `TASK-02` | Line-by-line verification of Days 4–6 (Seongsu-dong, DDP, Starfield COEX Mall, Gangnam, Ikseon-dong, Insadong, Cafes, Retail & Restaurants) | `done` | `5d411753` | `data/itinerary-data.js`, `dining-shopping.html` |
| `TASK-03` | Line-by-line verification of Days 7–9 (Itaewon, Open Sunday Day 8, Seoul Station KTX to Busan, L7 Haeundae by LOTTE, Haeundae Beach & Traditional Market) | `done` | `5d411753` | `data/itinerary-data.js`, `itinerary.html` |
| `TASK-04` | Public Transportation & Hotel Route Engineering (ICN to Myeongdong, Daily Seoul Metro/Bus Routes, KTX & Busan Metro/Bus Routes) | `done` | `5d411753` | `transit.html`, `data/itinerary-data.js` |
| `TASK-05` | Irregularities Audit & "Flagged for Review" Page Construction | `done` | `5d411753` | `flagged.html`, `data/itinerary-data.js` |
| `TASK-06` | Final Integration, Responsive Static Site Build, Link Verification, PR & GitHub Pages Deployment | `done` | `5d411753` | `index.html`, `assets/styles.css`, `assets/app.js`, `.github/workflows/pages.yml`, `README.md` |

---

## Verification Summary (Sources Checked)

All entries verified against official/trusted sources:

- **Stanford Hotel Myeongdong**: 84 Namdaemun-ro, Jung-gu, Seoul 04534; check-in 15:00, check-out 12:00. Source: stanford.webhelper.co.kr FAQ
- **AREX Express**: T1→Seoul Station 43 min, ₩13,000; T2→Seoul Station 51 min, ₩13,000. Source: english.seoul.go.kr
- **Limousine Bus 6015**: ~80 min, ₩17,000. Source: Stanford Hotel FAQ
- **N Seoul Tower**: Observatory 10:00–22:30 (weekday) / 10:00–23:00 (weekend), ₩29,000 adult. Cable car 10:00–23:00, ₩15,000 RT. Source: english.visitkorea.or.kr
- **Lotte Dept Store Main**: Weekdays 10:30–20:00 / Weekends 10:30–20:30. Source: english.visitkorea.or.kr
- **Shinsegae Dept Store Main**: Mon–Thu 10:30–20:00 / Fri–Sun 10:30–20:30. Source: english.visitkorea.or.kr
- **Olive Young Myeongdong Town**: Daily 10:00–22:30. Source: myeongdongtown.oliveyoung.com
- **Gwangjang Market**: General 09:00–18:00 / Food street 09:00–23:00, closed Sundays (general). Source: english.visitkorea.or.kr
- **Mangwon Market**: 27 Poeun-ro 6-gil, Mapo-gu. Source: english.visitkorea.or.kr
- **Myeongdong Kyoja**: Daily 10:30–21:00, Michelin Bib Gourmand, closed Seollal/Chuseok. Source: guide.michelin.com
- **Crystal Jade Sogong**: Daily 11:00–15:00 / 17:00–21:30, B1F 16 Namdaemun-ro 7-gil. Source: catchtable.net
- **Hongojib Myeongdong**: Daily 11:00–01:00, 40 Myeongdong 3-gil. Source: eatingseoul.com
- **Pig Restaurant 2**: Daily 16:30–00:00, 14-1 Bogwang-ro 59-gil 1F. Source: tripadvisor.com
- **Myeongdong Sookhee**: Daily 18:00–01:00. Source: autoreserve.com
- **Gyeongbokgung Palace**: Nov–Feb 09:00–17:00, closed Tuesdays, ₩3,000. Source: english.visitkorea.or.kr
- **Guard Ceremony**: 10:00 & 14:00, not Tuesdays. Source: seoultourism.org
- **Bukchon Hanok Village**: Visiting window 10:00–17:00 (curfew since Nov 2024). Source: ktriptips.com
- **Cafe Onion Anguk**: Weekdays 07:00–22:00 / Weekends 09:00–22:00. Source: m.onionkr.com
- **Solsot Seongsu**: Daily 11:30–15:00 / 17:00–21:00. Source: autoreserve.com
- **DDP**: 10:00–20:00 daily. Source: english.visitkorea.or.kr
- **Starfield COEX Mall**: Daily 10:30–22:00. Source: english.visitkorea.or.kr
- **Gangnam Style Statue**: COEX East Plaza, free, 24hr. Source: delibinu.com
- **Ikseon Chwihyang**: Daily 12:00–21:00, 17-32 Supyo-ro 28-gil. Source: koreatodo.com
- **Jayeondo Salt Bread**: Daily 09:00–22:00, ₩12,000 for 4. Source: english.visitseoul.net
- **L7 Haeundae by LOTTE**: 55 Haeun-daero 570beon-gil, Busan 48094; check-in 15:00, check-out 11:00. Source: trip.com property info
- **KTX Seoul→Busan**: ~2h15m–2h45m, ₩54,400 standard (reduced Sep 1, 2026). Source: welcome-busan.com
- **Haeundae Market**: 09:00–22:00, 22-1 Gunam-ro 41beon-gil. Source: english.visitkorea.or.kr

---

## Flagged Irregularities (11 items)

See `flagged.html` for full details. Key flags:
- **F-01**: Gyeongbokgung closed Tuesdays — Day 3 (Nov 3) is a Tuesday. Needs day swap or alternative palace.
- **F-02**: Myeongdong Night Market hours (itinerary says 21:00–23:00; sources show ~17:00–23:00).
- **F-03**: N Seoul Tower hours typo in itinerary (10:00–10:30 → should be 10:00–22:30/23:00).
- **F-05**: Olive Young hours (itinerary says 8:00–12:00am; official is 10:00–22:30).
- **F-06**: Uri Wang Galbitang — no official source found.
- **F-07**: Rain Report Cafe — multiple branches, unspecified location.
- **F-08**: Day 8 — no activities planned.
- **F-09**: Pig Restaurant 2 on Day 2 — cross-town Itaewon dinner on a Myeongdong day.
- **F-10**: Flight SFO→ICN not yet booked.
- **F-11**: Crystal Jade exact Shinsegae basement location needs confirmation.

---

## Coordination Log

- **2026-10-21 (Session `5d411753`)**: Created `COORDINATION.md`, claimed all tasks `TASK-01`–`TASK-06`.
- **2026-10-21 (Session `5d411753`)**: Completed official source verification for all Days 1–9 entries, transit routes, dining/shopping, and flagged irregularities.
- **2026-10-21 (Session `5d411753`)**: Built static site — `index.html`, `itinerary.html`, `verification-table.html`, `transit.html`, `dining-shopping.html`, `flagged.html`, `assets/styles.css`, `assets/app.js`, `data/itinerary-data.js`, `.github/workflows/pages.yml`, `README.md`.
- **2026-10-21 (Session `5d411753`)**: Committed and pushed site files to `arena/5d411753-koreatrip4`. Created PR #5, merged into main via `gh pr merge 5 --merge`.
- **2026-10-21 (Session `5d411753`)**: GitHub Pages deployment succeeded — site live at `https://buffedlizard55-lab.github.io/Koreatrip4/`. Pages status: built, source: main branch at path `/`.
- **2026-10-21 (Session `5d411753`)**: Verified live subpages — `itinerary.html`, `verification-table.html`, `transit.html`, `dining-shopping.html`, `flagged.html` all render correctly with verified source links.
- **PR link**: https://github.com/buffedlizard55-lab/Koreatrip4/pull/5
- **Merge result**: Merged successfully (merge commit `d6d761a` on main).
- **Site URL**: https://buffedlizard55-lab.github.io/Koreatrip4/
- **Pages status**: Built and deployed successfully.
