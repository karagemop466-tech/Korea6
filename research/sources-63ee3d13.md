# Verification log — session `arena/63ee3d13-korea6` (2026-11-05)

Scope of this session: the **2027 / 2028 / 2029 vacation-window question**, plus a
line-by-line re-check of the anchors that drive it and of the Bay Area AM/FM flagship
facts. Everything below was opened and read on **2026-11-05** unless stated otherwise.

Companion artifacts:

* `scripts/projections.py` → generates `site/data/projections.json` (27 anchors, 15
  rule-set windows, a 37-row day-by-day table for Feb 15 – Mar 23, 2027).
* `site/year-windows.html` + `site/year-windows.js` → the published page.
* `scripts/research_append.py` → idempotent additive merge of this session's source and
  flag rows into `site/data/research.json` (flags **F27–F38**).
* `tests/projections.test.mjs` → 7 assertions over the generated data.

---

## 1. Anchors read from official sources today

| # | Fact | Value | Status | Official source |
|---|---|---|---|---|
| 1 | 2027 MLB spring training first games | Fri **Feb 19, 2027** — 17 games; zero games Feb 15–18 | VERIFIED | [MLB Stats API 2027-02-15→02-22](https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate=2027-02-15&endDate=2027-02-22) · [MLB press release](https://www.mlb.com/press-release/press-release-mlb-announces-2027-spring-training-schedule) |
| 2 | 2027 MLB Opening Night | Wed **Mar 24, 2027** (Netflix, matchup TBD) | VERIFIED | [mlb.com — 2027 schedule released](https://www.mlb.com/news/mlb-2027-schedule-released) |
| 3 | 2027 MLB traditional Opening Day | Thu **Mar 25, 2027** — 14 games, earliest ever | VERIFIED | same |
| 4 | 2027 first full slate | Sat **Mar 27, 2027** | VERIFIED | same |
| 5 | 97th MLB All-Star Game | Tue **Jul 13, 2027**, Wrigley Field (FOX) | VERIFIED | same |
| 6 | 2027 Home Run Derby | Mon **Jul 12, 2027** (Netflix) | VERIFIED | same |
| 7 | 2027 second half begins | Thu **Jul 15, 2027** | VERIFIED | same |
| 8 | 2027 regular season final day | Sun **Sep 26, 2027** | VERIFIED | same |
| 9 | NFL 2026 Week 18 | Sat–Sun **Jan 9–10, 2027** | VERIFIED | [NFL Football Operations — important dates](https://operations.nfl.com/calendar-events/nfl-important-dates) |
| 10 | NFL Wild Card / Divisional / Championships | Jan 16–18 / Jan 23–24 / **Jan 31, 2027** | VERIFIED | same |
| 11 | Super Bowl LXI | Sun **Feb 14, 2027**, SoFi Stadium, Inglewood | VERIFIED | same |
| 12 | Pro Bowl | No AFC–NFC game staged from the 2026 season onward | VERIFIED | [nfl.com](https://www.nfl.com/news/nfl-elevates-pro-bowl-selection-game-s-will-cease-being-contested) |
| 13 | 49ers Week 18 | at Arizona Cardinals, **TBD** date and TV | VERIFIED | [49ers.com schedule](https://www.49ers.com/schedule/) |
| 14 | 49ers per-game radio | **KSAN 107.7 FM / KNBR 104.5 FM / 680 AM** on every listed game | VERIFIED | same |
| 15 | 49ers Week 11 | Sun Nov 22, 2026, 5:20 PM PST, vs Vikings at **Estadio Banorte, Mexico City** | VERIFIED | same · [NFL Operations](https://operations.nfl.com/calendar-events/nfl-important-dates) |
| 16 | Westwood One 2026 NFL package | TNF / SNF / MNF, Thanksgiving, Christmas, Week 15–16 Saturday doubleheaders, postseason | VERIFIED | [westwoodonesports.com/nfl-schedule](https://www.westwoodonesports.com/nfl-schedule/) |
| 17 | Super Bowl LXII host | **Mercedes-Benz Stadium, Atlanta** — NFL.com's own table lists the date as **TBA** | REPORTED for the date | [nfl.com](https://www.nfl.com/news/mercedes-benz-stadium-in-atlanta-to-host-super-bowl-lxii-in-2028) |
| 18 | Super Bowl LXIII host | **Allegiant Stadium, Las Vegas**, “February 2029”, no firm date | ESTIMATED for the date | [nfl.com](https://www.nfl.com/news/las-vegas-to-host-super-bowl-lxiii-in-2029) |
| 19 | MLB 2028 schedule | MLB Stats API returns **totalItems 0** | UNRELEASED | [MLB Stats API 2028](https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate=2028-01-01&endDate=2028-12-31) |
| 20 | MLB 2029 schedule | MLB Stats API returns **totalItems 0** | UNRELEASED | [MLB Stats API 2029](https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate=2029-01-01&endDate=2029-12-31) |
| 21 | Giants English / Spanish flagships | **KNBR 680 AM / 104.5 FM**; **KSFN 1510 AM / 99.3 FM** | VERIFIED | [mlb.com/giants/schedule/broadcast-partners](https://www.mlb.com/giants/schedule/broadcast-partners) |
| 22 | Athletics terrestrial radio | **960 AM KNEW** (Bay Area); **650 AM KSTE** (Sacramento) | VERIFIED | [mlb.com/athletics/schedule/affiliates](https://www.mlb.com/athletics/schedule/affiliates) |
| 23 | Cal football radio | **KSFO 810 AM** (not KGO — see F36) | VERIFIED | [UC Berkeley events](https://events.berkeley.edu/sports/event/315720-california-football-vs-pittsburgh) |

## 2. Non-official sources used, and how they are labelled

* Super Bowl LXII = **Feb 13, 2028** — reported by ESPN (Adam Schefter) and Pro Football
  Talk ([link](https://sports.yahoo.com/articles/nfl-sends-message-2028-super-153037714.html)).
  NFL.com's own Super Bowl table still shows **TBA**, so the site labels this row
  **REPORTED**, never VERIFIED. It is registered as a source row whose claim says
  explicitly that it is not official.
* Super Bowl LXIII = **Feb 11, 2029** — the second Sunday of February 2029. The NFL
  announcement gives no date, so this is labelled **ESTIMATED**.

## 3. What the numbers say

Under the rule **exactly as written** (every MLB game including spring training, every
NFL game, Stanford and Cal football, every Westwood One national NFL slot):

| Year | Longest clean run | Days | Status |
|---|---|---|---|
| 2027 | Feb 15 – Feb 18 | **4** | VERIFIED (Super Bowl LXI Feb 14 and MLB spring training Feb 19 are both official) |
| 2028 | ≈ Feb 14 – Feb 17 | **4** | ESTIMATED |
| 2029 | ≈ Feb 12 – Feb 15 | **4** | ESTIMATED |

**No 7-, 14- or 21-day window exists in any of the three years.** This is not a coverage
artefact — MLB spring training starts four to five days after the Super Bowl every year,
and the NFL season runs continuously from August to the Super Bowl, so the calendar has
no unoccupied week between late February and the following mid-February.

The single rule change that produces a real trip is dropping MLB spring training:

| Year | Feb 15 → day before Opening Night | Days | Status |
|---|---|---|---|
| 2027 | **Feb 15 – Mar 23** | **37** | VERIFIED at both ends: Super Bowl LXI (Feb 14, 2027, NFL Operations) and MLB Opening Night (Mar 24, 2027, MLB.com) |
| 2028 | ≈ Feb 14 – Mar 21 | 37 | ESTIMATED |
| 2029 | ≈ Feb 12 – Mar 20 | 37 | ESTIMATED |

What that 2027 run costs you, computed from the official MLB 2027 snapshot:
**32 of the 37 days** contain a Giants or Athletics game (spring training), and only
**4** days (Feb 15–18) are completely free of MLB. Golden State Warriors games
(KGMZ 95.7 FM) and Cal men's basketball (KSFO 810 AM) are on Bay Area AM/FM during this
period regardless — they are outside the brief's four categories but inside the
terrestrial dial, which is why the page points at
[Scope & AM/FM proof](site/core-scope.html).

## 4. Irregularities found and flagged

Published on the site's Flagged for Review page via `site/data/research.json`:

* **F27** — the stored NFL 2026 snapshot stops at Jan 3–4, 2027. NFL Operations lists
  Week 18 as Jan 9–10, 2027 and 49ers.com lists SF's Week 18 game at Arizona as TBD.
  24 imported rows (including the 49ers game) carry null date/start because of flex
  scheduling. Jan 9–10, 2027 is BUSY even though the dashboard shows no rows.
* **F28** — the 2027 MLB postseason is absent from the official snapshot, which ends at
  Sep 26, 2027. The 2026 snapshot did contain postseason rows, so this is a gap. October
  2027 is scored BUSY UNKNOWN.
* **F29** — 2027 Opening Night (Mar 24, Netflix, matchup TBD) is announced by MLB.com but
  absent from the feed, so a naive gap scan reports Mar 24 as empty.
* **F30** — Super Bowl LXII's date is reported, not tabled. Corrects an earlier source
  register row that claimed the Oct 15, 2024 NFL release announced Feb 13, 2028; the
  official [media.nfl.com release](https://media.nfl.com/news-and-releases/corporate-communications/atlanta-to-host-super-bowl-lxii-in-2028)
  states no date.
* **F31** — Super Bowl LXIII's date is not announced.
* **F32** — MLB 2028 and 2029 return zero rows; all 2028/2029 dates are projections.
* **F33** — Official sources disagree about Jul 15, 2027: MLB.com says the second half
  begins that day, the MLB Stats API has no game. Conservative reading used, which caps
  the All-Star break at one isolated clear day (Jul 12 or Jul 14).
* **F34** — **Withdrawn claim.** A stale, unmerged PR and older page wording described
  “Mon Jul 12 – Wed Jul 14, 2027” as a verified 3-day window. Tue **Jul 13, 2027 is the
  All-Star Game**. That PR (#13) also asserted VERIFIED status against non-official
  sources (topendsports, sportsbrackets.net, academicjobs.com, upintherafters,
  Wikipedia) and was closed unmerged rather than republished.
* **F35** — Restates the verdict with its boundaries.
* **F36** — Cal's 810 AM call sign is **KSFO**, not KGO (call moved from 560 AM in
  Jan 2025). The legacy `data-ncaaf.html` row was corrected; `research.json` was already
  correct.
* **F37** — Athletics flagship is KNEW 960 AM (Bay Area), KSTE 650 AM (Sacramento).
  “Bloomberg 960” branding is stale.
* **F38** — Giants flagships confirmed (KNBR 680/104.5, KSFN 1510/99.3).

## 5. Files changed by this session

New: `scripts/projections.py`, `scripts/research_append.py`,
`site/data/projections.json`, `site/year-windows.html`, `site/year-windows.js`,
`tests/projections.test.mjs`, this log.

Additive edits: `scripts/pages.py` (new nav entry + per-page script map; regenerated
`site/*.html`), `site/app.js` (two cross-links to the new page, `node --check` clean),
`tests/browser.spec.cjs` (added `year-windows` to the page list and one content test),
`site/data/research.json` (6 new source rows, 3 merged, 12 new flags), `README.md`,
`COORDINATION.md`, and two stale value corrections on the legacy pages
`data-ncaaf.html` (Cal radio call sign) and `data-nfl.html` (49ers radio stations and
source link), both recorded in the flags above.

## 6. Tests run

* `npm test` → 26 Node tests + 6 Python `validate.py` tests + `check-site.js`, all pass.
* `npm run test:browser` (with `LD_LIBRARY_PATH=/tmp/al2023/lib`) → **15/15 pass**,
  including the 9-page load / no-JS-error / no-390px-overflow sweep and the new
  year-windows content test.
* `git diff --check` clean.

## 7. Not done / deliberately left blank

* No 2028 or 2029 MLB game rows were invented. Both feeds are empty; the site stores
  projections with an explicit ESTIMATED label instead of fabricating fixtures.
* No 2027 NFL game rows were invented. The schedule releases in May 2027.
* Reception of any specific station at a specific address in 94122 is still
  **unverified**; no coverage contour was consulted. A fixture proves a game is played,
  not that it reaches an AM/FM radio.
* The MLB snapshot could not be re-pulled from this sandbox (outbound network is limited
  to github/npm/pypi), so `scripts/refresh.py` was not run here; the daily GitHub Actions
  workflow refreshes it on `main`.
