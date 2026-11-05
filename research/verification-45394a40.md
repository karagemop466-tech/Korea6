# Verification log — session arena/45394a40-korea6 (2026-11-05)

Scope of this pass: add labeled **2028–2029 estimated season schedules**, compute
**per-year vacation window analysis for 2027/2028/2029**, refresh the executive
summary, re-verify load-bearing anchors against official sources, and run final
integration (tests → PR → merge → GitHub Pages).

## Anchors verified today (links for manual review)

| Claim | Evidence | Status |
| --- | --- | --- |
| Super Bowl LXIII awarded to Las Vegas / Allegiant Stadium (announced Mar 30, 2026 at the NFL Annual Meeting) | [LVCVA/NFL release via PR Newswire](https://www.prnewswire.com/news-releases/super-bowl-returns-to-las-vegas-in-2029-302729218.html) (fetched 2026-11-05) | **Verified (venue)**; game date NOT announced — model uses estimated Feb 11, 2029 (F32) |
| Super Bowl LXII at Mercedes-Benz Stadium, Atlanta (NFL announcement Oct 15, 2024) | [media.nfl.com release](https://media.nfl.com/news-and-releases/corporate-communications/atlanta-to-host-super-bowl-lxii-in-2028) (fetched 2026-11-05) | Verified (host). Release states no date. |
| Super Bowl LXII date Feb 13, 2028 | [nfl.com news page](https://www.nfl.com/news/mercedes-benz-stadium-in-atlanta-to-host-super-bowl-lxii-in-2028) (fetched 2026-11-05) still lists the date as **TBA**; the date was announced Jul 24, 2026 by the host stadium (Mercedes-Benz Stadium official account) and ESPN's Adam Schefter | **Reported/venue-announced**, not on nfl.com — evidence chain recorded in F24 (reconciled) and F31 |
| 2028 MLB All-Star Game awarded to the San Francisco Giants at Oracle Park (official MLB release, Aug 14, 2026) | [mlb.com press release](https://www.mlb.com/news/release-mlb-awards-the-2028-all-star-game-presented-by-mastercard-to-the-san-francisco-giants) | **Verified (award + venue)**. Date not fixed in the release; press reports give Jul 11 or Jul 12, 2028 — both blocked in the model (F28) |
| LA28 Olympic baseball at Dodger Stadium, ~Jul 13–20, 2028 | [NBCOlympics event guide](https://www.nbcolympics.com/news/baseball-2028-los-angeles-olympics); published LA28/WBSC schedules differ slightly on first/last day | **Verified (published schedule)**. MLB player participation and SF radio carriage unverified (F29) |
| MLB CBA expires Dec 1, 2026; lockout risk to the 2027 season; MLB proposed Nov 3, 2026 to phase any salary cap in by 2028 | [Yahoo Sports](https://sports.yahoo.com/articles/latest-mlb-proposal-players-pushes-231147442.html), [Sportico](https://www.sportico.com/leagues/baseball/2026/mlb-labor-fight-lockout-future-salary-cap-cba-1234956712/) | Press-sourced (no official league publication); flagged F27 |
| MLB 2028+ schedule not released | [MLB schedule feed (2028 window empty)](https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate=2028-01-01&endDate=2028-12-31) | Verified absence → all 2028–2029 rows are labeled estimates (F30) |
| Pro Bowl game discontinued starting with the 2026 season | [nfl.com](https://www.nfl.com/news/nfl-elevates-pro-bowl-selection-game-s-will-cease-being-contested) (verified in a prior session; relied on here) | Verified |

## Analysis computed from the merged dataset (official feeds + labeled estimates)

Vacation runs use the brief's core definition (all MLB incl. spring training, all
NFL incl. preseason/postseason, Stanford/Cal football, Westwood One NFL windows).
Conditional rows (possible Stanford/Cal bowls) annotate runs but do not block
them ("scheduled to be played" per the brief).

- **2027:** longest clear run **Feb 1–13 (13 days)**, bounded entirely by official
  rows (AFC/NFC Championship Games Jan 31 → Super Bowl LXI Feb 14). Second:
  Feb 15–18 (4 days, post-Super-Bowl, official bounds: SB Feb 14 → spring
  training Feb 19). Also Jan 25–30 (6 days) and Jan 11–15 (5 days).
- **2028:** **Jan 31–Feb 12 (13 days, estimated bounds)**; **Jul 13–20 (8 days,
  SCENARIO F29)** — the only ≥7-day lead in 2027–2029, conditional on an MLB
  Olympic pause and unverified Olympic radio carriage; Feb 14–17 (4 days).
- **2029:** **Jan 29–Feb 10 (13 days, estimated bounds)**; Feb 12–15 (4 days).
- **No 14- or 21-day clear run exists** in any of the three years under the core
  definition. On the full AM/FM dial (Warriors, Cal MBB, USF, etc.) the February
  2027 window shrinks to isolated single days (see core-scope proof page).

## Irregularities flagged (published on Flagged for Review)

- **F24 reconciled**: the Oct 15, 2024 NFL release did not state the Super Bowl
  LXII date; the date comes from the host stadium/ESPN (Jul 24, 2026) and
  nfl.com still shows TBA (F31).
- **F27** MLB labor risk (CBA expiry Dec 1, 2026) affects every 2027+ anchor.
- **F28** 2028 All-Star Game date tentative (Jul 11 vs Jul 12 reports).
- **F29** LA28 Olympic-break scenario not confirmed; Olympic radio carriage
  unverified; date variants across published schedules (Jul 13–20 vs 15–20).
- **F30** 2028–2029 fixtures are estimates, never released schedules.
- **F32** Super Bowl LXIII date estimated (Feb 11, 2029).

## Tests run this session

- `python3 scripts/season_estimates.py` (deterministic, 959 rows, IDs asserted unique)
- `python3 tests/validate.py` — 8/8 (incl. new estimate-labeling and ID-collision tests)
- `node --test tests/*.test.js tests/*.test.mjs` — pass (engine tests extended for
  `windowEnd` spans and `clearRuns`)
- `node tests/check-site.js` — pass
- `npm run test:browser` — 13/13 Playwright tests pass (desktop + 390 px mobile,
  day navigation, vacation controls, TBD guard, exports)
