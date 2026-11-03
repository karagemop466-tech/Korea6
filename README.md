# Free Time Vacation

A static GitHub Pages planner for Pacific Time. The daily scoreboard requests available MLB schedules from MLB's Stats API; manually researched football listings are a partial snapshot, not a complete feed. Empty results are **not** proof of free time. The site documents sources, assumptions, and known gaps on its Flagged for Review page.

Open `index.html` through a local HTTP server, for example `python3 -m http.server 8000`, or use the GitHub Pages site. Internet access and a browser that permits the MLB API request are required for live MLB listings. Run the local checks with `node --test tests/*.test.js` and `node tests/check-site.js`.

## Additional verified analysis (session arena/fbb7cd8f-korea6)

- `calendar.html` — day-by-day free/busy model (Pacific time, Nov 2026 – Dec 2029) from `data/calendar.json` (generator: `tools/generate_calendar.py`).
- `windows.html` — vacation windows 2027–2029: **Feb 15–18, 2027 (verified)** and **Jul 12–14, 2027 (verified)** all-clear; 2028/2029 estimated and flagged.
- `summary.html`, `data-mlb.html`, `data-nfl.html`, `data-ncaaf.html` — executive summary and per-league tables, each row linked to an official source.
- `research/sources.md` — full verification log. Unverified items are never filled in; see the Flagged for Review page.

## Evidence dashboard — integration update (2026-11-03)

**Start here: [Evidence dashboard](https://karagemop466-tech.github.io/Korea6/site/).**

The separate `site/` application preserves previous sessions' pages and adds:
- Full official MLB feed snapshots for 2026–2029, including all 30 clubs; 2027 currently has 2,901 records. Empty 2028–2029 responses mean unknown coverage, not no games.
- 321 official 2026 NFL fixtures (49 preseason, 272 regular season); 46 Westwood One NFL slots, 49ers local station listings, Cal/Stanford football, and partial Warriors listings.
- Daily/monthly navigation through December 2029, league/team/priority filters, CSV exports, source register and explicit review flags.
- DST-aware interval union/complement with separately labeled duration estimates. No fixture dates or unknown kickoffs are invented.

**Correction to earlier analysis above:** July 12–14, 2027 is NOT verified all-clear: the official MLB feed lists the All-Star Game on July 13. February 15–18 is only four intervening dates between verified league anchors, not verified sports-free time across all radio sports. No 7/14/21-day trip is currently certified. Earlier root pages and datasets are preserved with integration notices for comparison, not endorsed.

### Development and verification
- `npm ci`; `npm test`; `npm run test:browser`.
- `python3 -m http.server 8000 --bind 0.0.0.0` then visit `/site/`.
- Browser tests use an npm-packaged Chromium. On minimal Linux environments, extract its `al2023.tar.br` with the package's `inflate` function and set `LD_LIBRARY_PATH=/tmp/al2023/lib`; standard GitHub Ubuntu runners include the required libraries.
- `scripts/refresh.py`: official MLB importer; `scripts/nfl.py`: official NFL rendered-state importer. `scripts/seed.py`: reproducible November 3 curated snapshot, not a live scraper.
- GitHub Pages workflow runs tests before deployment and refreshes official automated feeds daily without committing to main. Reviewed radio entries keep their original review dates. A failed upstream fetch is recorded as a coverage issue, not interpreted as free time.
