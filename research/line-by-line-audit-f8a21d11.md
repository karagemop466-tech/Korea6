# Line-by-Line Official Source Verification & Bay Area AM/FM Audit (`arena-f8a21d11`)

- **Audit Date:** 2026-11-03 (UTC)
- **Listener Profile:** Outer Sunset, San Francisco, CA (`94122`) · Standard AM/FM Terrestrial Radio · Pacific Time (`America/Los_Angeles`, PST `-08:00` / PDT `-07:00`)
- **Total Official Primary-Source Event Records Verified:** **6,475** (`2,990` MLB 2026 + `2,901` MLB 2027 + `321` NFL 2026 + `87` baseline curated + `176` newly verified official expansion records in `site/data/expanded-official.json`)

---

## 1. Executive Summary of New Primary-Source Discoveries & Corrections

1. **2027 NFL Pro Bowl Game Officially Discontinued (`nfl.com`, Aug 26, 2026):**
   - Earlier session artifacts (`research/sources.md` line 48; `site/data/research.json` flag `F03`) treated a 2027 Pro Bowl game as either part of Westwood One's live game package or an "unverified" missing fixture between the Jan 31, 2027 Conference Championships and Feb 14, 2027 Super Bowl LXI.
   - **Primary-source verification:** On August 26, 2026, the NFL officially announced (*"NFL elevates Pro Bowl selection; AFC-NFC Pro Bowl game will no longer be staged"*, <https://www.nfl.com/news/nfl-elevates-pro-bowl-selection-game-s-will-cease-being-contested> and <https://media.nfl.com/news-and-releases/pbg/nfl-elevates-pro-bowl-selection--honoring-the-league-s-best-of-t0>) that starting with the 2026 season (2027 Pro Bowl class), 88 players earn Pro Bowl honors with an in-person celebration in Los Angeles and **no AFC-NFC Pro Bowl game is staged**.

2. **Definitive Two-Scope Proof on the February 15–18, 2027 Post–Super Bowl Window:**
   - **Core 4-Category Prompt Scope** (*All 30 MLB + All NFL + Stanford/Cal NCAAF + Westwood One NFL*): Super Bowl LXI airs **Sun Feb 14, 2027** (<https://operations.nfl.com/calendar-events/nfl-important-dates>) and 2027 MLB Spring Training opens **Fri Feb 19, 2027** (<https://statsapi.mlb.com/api/v1/schedule?sportId=1&season=2027&startDate=2027-02-19&endDate=2027-02-19>). That leaves **4 consecutive zero-game days (`Feb 15–18, 2027`)**, which is still `< 7` days (**0** 1-week, 2-week, or 3-week conflict-free vacations).
   - **Full SF 94122 Terrestrial AM/FM Scope:** Even that 4-day post–Super Bowl gap is **broken on two of its four days** by verified local terrestrial radio broadcasts:
     - **Mon Feb 15, 2027 (4:30 PM PST):** Indiana Pacers at Golden State Warriors on **`KGMZ 95.7 FM`** (<https://www.nba.com/game/ind-vs-gsw-0022600084>).
     - **Wed Feb 17, 2027 (Triple Conflict):**
       1. **4:00 PM PST:** California Men's Basketball at Pittsburgh on **`KSFO 810 AM`** (<https://calbears.com/sports/mens-basketball/schedule/2026-27>).
       2. **7:00 PM PST:** New Orleans Pelicans at Golden State Warriors on **`KGMZ 95.7 FM`** (<https://www.nba.com/game/nop-vs-gsw-0022600842>).
       3. **Time TBA:** USF Dons Men's Basketball at LMU (<https://usfdons.com/sports/mens-basketball/schedule/2026-27>; season partner `KNBR 1050 AM`).
     - NBA All-Star Break (`Feb 19–24, 2027`, with the 2027 NBA All-Star Game in Phoenix on `Sun Feb 21, 2027`) immediately overlaps MLB Spring Training opening on **Fri Feb 19, 2027**.

3. **Superseded Stanford 2027 ACC Opponents Corrected + Notre Dame Extension Added:**
   - `research/sources.md` line 55 cited an October 30, 2023 ACC 8-game model listing Stanford *Away at Virginia Tech* in 2027.
   - **Primary-source correction:** Stanford's September 16, 2026 9-game ACC announcement (<https://gostanford.com/news/2026/09/16/acc-announces-2027-conference-opponents>) supersedes the 2023 model and confirms **Home: California, Duke, North Carolina, Syracuse, Virginia; Away: Boston College, Clemson, Florida State, SMU** (Virginia Tech is not on Stanford's 2027 schedule).
   - In addition, Stanford's May 20, 2026 release (<https://gostanford.com/news/2026/05/20/two-dates-added-to-notre-dame-rivalry>) confirms **Notre Dame at Stanford on Sat Nov 27, 2027** and **Stanford at Notre Dame on Sat Oct 14, 2028**.

4. **Six Missing Westwood One National Radio Broadcasts Added:**
   - Prior `curated.json` included 46 NFL Westwood One broadcasts and only 1 NCAAF broadcast (`ww-557143` Nov 7 Oregon at Ohio State), omitting **5 official upcoming Westwood One NCAAF broadcasts** (<https://www.westwoodonesports.com/ncaa-football/>: `Nov 14` Texas Tech at Oklahoma State, `Nov 21` LSU at Tennessee, `Nov 28` Michigan at Ohio State 8:30 AM PST, `Dec 5` SEC Championship 12:30 PM PST, `Dec 12` Army vs. Navy 11:00 AM PST) and **1 Westwood One U.S. Soccer broadcast** (<https://www.westwoodonesports.com/us-soccer/>: `Nov 17` USMNT vs. Haiti 3:45 PM PST).

5. **Complete SF 94122 Terrestrial AM/FM Station Matrix & Verified Digital-Only Exclusions:**
   - **Verified terrestrial AM/FM conflict properties in 94122:**
     - `KNBR 680 AM / KNBR-FM 104.5`: SF Giants (`mlb.com/giants/schedule/watch`), SF 49ers (`49ers.com/fans/tv-radio`), Nov 21 Big Game (`calbears.com`), Westwood One affiliate (`westwoodonesports.com/station-finder/`).
     - `KSAN 107.7 FM`: SF 49ers FM flagship (`49ers.com/fans/tv-radio`).
     - `KTCT 1050 AM (KNBR 1050)`: Stanford Football (`gostanford.com`), **USF Dons Men's Basketball** (`usfdons.com`), Westwood One affiliate (`westwoodonesports.com/station-finder/`).
     - `KSFO 810 AM`: California Football (`calbears.com`), **California Men's Basketball — all 32 regular-season games** (`calbears.com/sports/mens-basketball/schedule/2026-27`), **San Jose Earthquakes English flagship** (`sjearthquakes.com`).
     - `KGMZ 95.7 FM`: Golden State Warriors (`nba.com/warriors/schedule`) and **Golden State Valkyries WNBA** (`valkyries.wnba.com`).
     - `KNEW 960 AM`: Athletics Bay Area English terrestrial affiliate (`mlb.com/athletics/schedule/affiliates`).
     - `KSFN 1510 AM / 99.3 FM`: SF Giants Spanish flagship (`mlb.com/giants/schedule/watch`).
     - `KZSF 1370 AM`: San Jose Earthquakes Spanish flagship (`sjearthquakes.com`).
   - **Verified non-terrestrial (digital/satellite-only, excluded from standard AM/FM conflicts):**
     - **San Jose Sharks (NHL):** Moved exclusively to digital `Sharks Audio Network` in January 2021 (<https://www.nhl.com/sharks/news/sharks-announce-launch-of-sharks-audio-network-320033246>).
     - **Stanford Men's Basketball (NCAAM):** Moved off `KNBR 1050 AM` in 2017–18 to `GoStanford.com` / Varsity Network / SiriusXM (<https://gostanford.com/news/2017/11/09/enhanced-basketball-coverage>).

---

## 2. Dataset-by-Dataset Line-by-Line Audit Summary

| Dataset | Rows | Scope | Official Source(s) | Audit Result |
| --- | ---: | --- | --- | --- |
| `site/data/mlb-2026.json` | 2,990 | All 30 MLB clubs (451 ST, 38 Exh/WBC, 2,459 Reg, 1 ASG, 41 Postseason; 384 SF/ATH priority) | `statsapi.mlb.com` | **Verified** — 4 `3:33 AM UTC` placeholder rows properly nulled (`start: null`). |
| `site/data/mlb-2027.json` | 2,901 | All 30 MLB clubs (465 ST, 5 Exh, 2,430 Reg, 1 ASG; 380 SF/ATH priority) | `statsapi.mlb.com` | **Verified** — Feb 19–Sep 26, 2027; 1,930 `3:33 AM UTC` rows properly nulled (`start: null`); 2027 Postseason not yet in API (flagged). |
| `site/data/mlb-2028.json` / `mlb-2029.json` | 0 / 0 | 2028–2029 MLB | `statsapi.mlb.com` (`totalGames: 0`) | **Verified empty** — flagged as unverified for 2028–2029 vacation windows. |
| `site/data/nfl-2026.json` | 321 | 49 Preseason + 272 Regular Season (20 SF 49ers priority) | `www.nfl.com/schedules/2026/...` | **Verified** — 24 flex-pool games (4 Wk 16 + 4 Wk 17 + 16 Wk 18) properly nulled (`date: null, start: null`). |
| `site/data/curated.json` | 87 | 46 WWO NFL, 1 WWO NCAAF, 10 49ers, 7 NFL Postseason dates, 5 Nov 2026 Cal/Stanford FB, 12 Cal 2027 FB, 6 Nov Warriors | `westwoodonesports.com`, `49ers.com`, `operations.nfl.com`, `calbears.com`, `gostanford.com`, `nba.com` | **Verified** — accurate for Nov 2026 subset, but incomplete across Aug–Oct 2026 NCAAF, WWO NCAAF/USSF, Dec–Apr Warriors, Cal/USF MBB, MLS, and Stanford/Cal 2027–2029 FB. |
| `site/data/expanded-official.json` | 176 | 66 Nov 18–Apr 11 Warriors + Cup/ASG, 32 Cal MBB, 32 USF MBB, 18 Aug–Oct Stanford/Cal FB, 5 WWO NCAAF, 1 WWO USSF, 1 SJ Earthquakes MLS, 1 MLB 2027 HR Derby, 18 Stanford/Cal 2027–2029 FB (plus Pro Bowl & 8-station matrix) | `nba.com/game/...`, `calbears.com`, `usfdons.com`, `westwoodonesports.com`, `sjearthquakes.com`, `gostanford.com`, `mlb.com`, `nfl.com` | **Verified line by line** — 0 inferred times, 0 inferred stations, 100% official URLs. |
| Legacy `assets/data.js` & `research/sources.md` | Legacy | Earlier session root prototype | Mixed primary + secondary (`fbschedules.com`, `espn.com`, `profootballnetwork.com`, `wikipedia.org`) | **Quarantined / Audited** — secondary sources and superseded Stanford 2023 ACC / July 14 / Feb 15–18 claims documented on Flagged for Review. |
