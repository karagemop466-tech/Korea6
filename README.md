# Free Time Vacation

A static GitHub Pages planner for Pacific Time. The daily scoreboard requests available MLB schedules from MLB's Stats API; manually researched football listings are a partial snapshot, not a complete feed. Empty results are **not** proof of free time. The site documents sources, assumptions, and known gaps on its Flagged for Review page.

Open `index.html` through a local HTTP server, for example `python3 -m http.server 8000`, or use the GitHub Pages site. Internet access and a browser that permits the MLB API request are required for live MLB listings. Run the local checks with `node --test tests/*.test.js` and `node tests/check-site.js`.

## Main planner

**Start here: [Evidence dashboard](https://karagemop466-tech.github.io/Korea6/site/).** The dashboard provides daily/monthly navigation, league/team/priority filters, CSV export, a source register, and a clearly labeled Flagged for Review page. `calendar.html`, `windows.html`, and `summary.html` are supporting legacy pages; the window page deliberately does not certify a vacation date.

## Coverage and limitations (reviewed 2026-11-03)

- Official MLB snapshots are populated for 2026 and 2027. Empty 2028–2029 API responses mean unknown coverage, not no games. The daily dashboard is dependent on an upstream MLB API request.
- The stored NFL fixture set is for 2026 only. Curated Westwood One slots, 49ers listings, Stanford/Cal football, and local station research are partial; they do not establish complete radio carriage or reception in Outer Sunset 94122.
- The interval engine uses Pacific civil time with daylight-saving transitions and separately labeled duration assumptions. Estimated open intervals are not proof of broadcast-free time.
- No 2027–2029 vacation window is currently certified conflict-free. In particular, July 13, 2027 has a scheduled MLB All-Star Game; the prior July 12–14 “all-clear” claim is withdrawn. February 15–18, 2027 is only an unverified candidate between league milestones, not a confirmed free period. We cannot establish whether a 7-, 14-, or 21-day all-clear window exists without complete schedule and radio coverage.
- See [Flagged for Review](https://karagemop466-tech.github.io/Korea6/site/review.html) and [Sources & method](https://karagemop466-tech.github.io/Korea6/site/sources.html) before relying on any result. Official links are provided in the pages and source data; no missing value should be read as a confirmed absence.

### Development and verification
- `npm ci`; `npm test`; `npm run test:browser`.
- `python3 -m http.server 8000 --bind 0.0.0.0` then visit `/site/`.
- Browser tests use an npm-packaged Chromium. On minimal Linux environments, extract its `al2023.tar.br` with the package's `inflate` function and set `LD_LIBRARY_PATH=/tmp/al2023/lib`; standard GitHub Ubuntu runners include the required libraries.
- `scripts/refresh.py`: official MLB importer; `scripts/nfl.py`: official NFL rendered-state importer. `scripts/seed.py`: reproducible November 3 curated snapshot, not a live scraper.
- GitHub Pages workflow runs tests before deployment and refreshes official automated feeds daily without committing to main. Reviewed radio entries keep their original review dates. A failed upstream fetch is recorded as a coverage issue, not interpreted as free time.

## Final verification pass — session arena/69f77e26-korea6 (2026-11-03)

- Re-verified the load-bearing anchors line by line against official sources (full log: `research/verification-69f77e26.md`): MLB 2027 schedule released Jul 16, 2026 (Opening Night Mar 24, Opening Day Mar 25, All-Star Game Jul 13 at Wrigley, season ends Sep 26); 2027 Spring Training opens Feb 19, 2027 for all 30 clubs; NFL 2026 key dates incl. Super Bowl LXI on Feb 14, 2027 at SoFi; **Super Bowl LXII announced for Feb 13, 2028 (Atlanta)**; Westwood One 2026 NFL package incl. TNF/SNF/MNF and the full postseason; KNBR 680/104.5 flagship for both Giants and 49ers (extension through 2030); Cal 2027 nonconference + ACC opponents (calbears.com); Stanford 2027 ACC opponents per the ACC's Sep 16, 2026 announcement (gostanford.com); MLB 2025 average game 2:38 (mlb.com).
- New review flags F17–F21 are published on the site's Flagged for Review page: corrected Stanford 2027 opponent list, the Jul 14–15, 2027 feed-vs-press All-Star-break nuance, the verified 2028 Super Bowl date, the KNBR 1050 HD3 carriage nuance, and 2027 TBD start times / CBA risk.
- Conclusion stands: under the strict all-leagues definition, **no 7/14/21-day all-clear vacation window exists in 2027–2029**; the best verified 2027 gap is Feb 15–18 (between Super Bowl LXI and the first spring-training games), and 2028/2029 equivalents are anchored to the announced Feb 13, 2028 Super Bowl and remain estimated on the MLB side until those schedules release. The dashboard never labels an unverified day "free."
- Tests: `node --test` 14/14, `python3 tests/validate.py` 6/6, `node tests/check-site.js` pass.
