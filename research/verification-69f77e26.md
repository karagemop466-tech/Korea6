# Final verification log — session `arena/69f77e26-korea6` (2026-11-03)

Line-by-line re-verification of the load-bearing claims behind the vacation-window analysis, against official or official-carried sources. Rule: **verified = confirmed on the linked source today; otherwise blank/flagged ESTIMATED. No inferred values presented as verified.** All times Pacific (PST/PDT) unless noted.

## 1. MLB (all 30 clubs; Giants & A's high priority)

| # | Claim in repo | Re-verification result | Source |
|---|---|---|---|
| 1.1 | 2027 regular-season schedule released Thu Jul 16, 2026 | VERIFIED — MLB announced the 2027 schedule Jul 16, 2026 | [mlb.com news](https://www.mlb.com/news/mlb-2027-schedule-released); corroborated by [USA TODAY via centraloregondaily](https://www.centraloregondaily.com/sports/mlb-2027-schedule-revealed-when-is-opening-day-will-there-even-be-a-season/article_f66030aa-8e73-5be9-84ee-37b1d37209bd.html) and [The Athletic via NYT](https://www.nytimes.com/athletic/7450665/2026/07/16/mlb-2027-schedule-earliest-opening-day-ever-labor-battle/) |
| 1.2 | Opening Night Wed Mar 24, 2027 (single game, Netflix, matchup TBA); traditional Opening Day Thu Mar 25, 2027 (14 games); season ends Sun Sep 26, 2027 | VERIFIED | same sources as 1.1 |
| 1.3 | Home Run Derby Mon Jul 12, 2027 (Netflix); 97th All-Star Game Tue Jul 13, 2027, Wrigley Field (FOX); off day Jul 14; second half opens Thu Jul 15, 2027 with a single ESPN game | VERIFIED (press) — see flag F18: the official Stats API feed contains the ASG on 2027-07-13 and NO game rows on Jul 14 or Jul 15 (next full slate Jul 16), so the Jul 15 single game is not present in the imported feed | [mlb.com news](https://www.mlb.com/news/mlb-2027-schedule-released); [KTAL](https://www.ktalnews.com/sports/mlb/mlb-2027-schedule/); feed: [statsapi.mlb.com 2027](https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate=2027-01-01&endDate=2027-12-31) |
| 1.4 | 2027 Spring Training opens Fri Feb 19, 2027, all 30 clubs (announced Sep 4, 2026) | VERIFIED — official club press releases on mlb.com/press-release (Brewers, Dodgers, Orioles, Padres) all open Fri Feb 19, 2027; imported feed's earliest 2027 rows are 2027-02-19 | [mlb.com Brewers release](https://www.mlb.com/press-release/press-release-brewers-announce-2027-spring-training-schedule); [Dodgers](https://www.mlb.com/press-release/dodgers-announce-2027-spring-training-schedule); [Orioles](https://www.mlb.com/press-release/press-release-orioles-announce-2027-spring-training-schedule) |
| 1.5 | Imported 2027 feed: 2,901 records; 30 clubs in Regular Season; kinds = 2,430 RS + 465 ST + 5 exhibition + 1 ASG; 1,930 rows without a start time (TBD) | VERIFIED against `site/data/mlb-2027.json` (this session) | [statsapi.mlb.com 2027](https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate=2027-01-01&endDate=2027-12-31) |
| 1.6 | 2028/2029 MLB feeds return 0 records | VERIFIED as an empty API response — **not** evidence of no games; schedules not yet released | [statsapi.mlb.com 2028–2029](https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate=2028-01-01&endDate=2029-12-31) |
| 1.7 | MLB average nine-inning game 2025 = 2 h 38 m (third straight year ≤ 2:40) | VERIFIED — official MLB.com report | [mlb.com news](https://www.mlb.com/news/mlb-average-game-time-under-three-hours-third-straight-year) |
| 1.8 | Giants English flagship = KNBR 680 AM / 104.5 FM SF; Spanish flagship KSFN 1510 | VERIFIED — official broadcast-partners page | [mlb.com/giants/schedule/watch](https://www.mlb.com/giants/schedule/watch) |
| 1.9 | A's Bay Area terrestrial affiliate listed as KNEW 960 AM | Carried as listed on the official affiliates page; game-by-game carriage unverified (F11) | [mlb.com/athletics/schedule/affiliates](https://www.mlb.com/athletics/schedule/affiliates) |

## 2. NFL (all; 49ers high priority) & Westwood One Sports

| # | Claim in repo | Re-verification result | Source |
|---|---|---|---|
| 2.1 | 2026 season: Kickoff Wed Sep 9, 2026 (Patriots at Seahawks, Lumen Field); 18 weeks / 272 games; Week 18 Jan 9–10, 2027; Wild Card Jan 16–18; Divisional Jan 23–24; Championships Sun Jan 31, 2027; **Super Bowl LXI Sun Feb 14, 2027, SoFi Stadium, Inglewood** | VERIFIED — NFL "Important Dates for 2026–2027" release (Jul 7, 2026) carried on official team sites | [seahawks.com (NFL release)](https://www.seahawks.com/news/nfl-announces-important-dates-for-2026-2027); [operations.nfl.com important dates](https://operations.nfl.com/calendar-events/nfl-important-dates) |
| 2.2 | Imported 2026 NFL data: 321 records = 272 regular + 49 preseason; 20 49ers games | VERIFIED against `site/data/nfl-2026.json` (this session) | [nfl.com/schedules/2026](https://www.nfl.com/schedules/2026/by-week/week-1) |
| 2.3 | Westwood One 2026 NFL radio package: Kickoff game, TNF, SNF, MNF, 8 international games, Thanksgiving, Black Friday, Christmas, late-season Saturdays, full postseason, **Super Bowl LXI Feb 14, 2027 on Westwood One radio** | VERIFIED — network's 40th-season NFL coverage announcement; 46 upcoming slots transcribed in `site/data/curated.json` with per-event source URLs | [westwoodonesports.com/nfl-schedule](https://www.westwoodonesports.com/nfl-schedule/); [news.radio-online.com](https://news.radio-online.com/articles/n49383/Westwood-One-Sets-40th-Season-of-NFL-Coverage); [insideradio](https://www.insideradio.com/free/westwood-one-marks-40-years-of-nfl-coverage/article_cb5945c2-c687-43a1-a5db-3a678c9ef88a.html) |
| 2.4 | 49ers flagship = KNBR 680 AM / 104.5 FM (also KSAN 107.7 FM, KSFO 810 AM); partnership extended multi-year **through the 2030 season** (announced Apr 15, 2026) | VERIFIED — official Cumulus/49ers release | [cumulusmedia.com Apr 15, 2026](https://www.cumulusmedia.com/2026/04/15/san-francisco-49ers-announce-multi-year-partnership-extension-with-cumulus-medias-knbr/); [49ers.com/schedule](https://www.49ers.com/schedule/) |
| 2.5 | **Super Bowl LXII: Sun Feb 13, 2028, Mercedes-Benz Stadium, Atlanta** — announced by the NFL Oct 15, 2024 | VERIFIED (upgrades the earlier "estimated Feb 13, 2028" to an officially announced anchor; see flag F19) | [media.nfl.com Oct 15, 2024](https://media.nfl.com/news-and-releases/corporate-communications/atlanta-to-host-super-bowl-lxii-in-2028) |
| 2.6 | Super Bowl LXIII 2029: Allegiant Stadium, Las Vegas — **exact date not yet announced** | VERIFIED as TBD (venue announced; date pending) — all 2029 windows stay ESTIMATED | [media.nfl.com](https://media.nfl.com/news-and-releases/corporate-communications/atlanta-to-host-super-bowl-lxii-in-2028) |
| 2.7 | 2027 NFL full slate unreleased (release cycle ~May 2027); 2027 kickoff ~Sep 2027 | UNVERIFIED — structural estimate only, flagged | — |
| 2.8 | NFL average game length 3:03 (2025, nflverse play-by-play); site planning overlay uses 180 min incl. halftime | Overlay is a labeled assumption, not a verified average (F05) — retained as such | [upintherafters](https://www.upintherafters.com/nfl/how-long-is-a-football-game) |

## 3. NCAAF — Stanford & Cal (high priority)

| # | Claim in repo | Re-verification result | Source |
|---|---|---|---|
| 3.1 | Cal 2027 nonconference: **Aug 28 vs Sacramento State; Sep 4 at UCLA; Sep 11 vs Old Dominion** | VERIFIED — official calbears.com releases Jun 25 / Sep 16, 2026 | [calbears.com Sep 16, 2026](https://calbears.com/news/2026/9/16/california-football-announces-2027-conference-opponents) |
| 3.2 | Cal 2027 ACC opponents: home BC, Florida State, Louisville, SMU; away Georgia Tech, Miami, Pitt, Stanford, Wake Forest; dates/times TBD (ACC announces full grid ~late Jan 2027) | VERIFIED (opponents only) | same as 3.1 |
| 3.3 | Stanford 2027 ACC opponents — **corrected**: per the ACC's Sep 16, 2026 announcement (nine-game model), home = California, Duke, UNC, Syracuse, **Virginia**; away = Boston College, Clemson, SMU, **Florida State**. The earlier root `research/sources.md` line (from the 2023 eight-game model: "away Virginia Tech") is superseded — see flag F17. 130th Big Game at Stanford in 2027 | VERIFIED (opponents only; dates TBD) | [gostanford.com Sep 16, 2026](https://gostanford.com/news/2026/09/16/acc-announces-2027-conference-opponents) |
| 3.4 | Cal football flagship = KGO 810 AM (KSFO); Big Game on KNBR 680/104.5 | VERIFIED — official calbears.com | [calbears.com schedule](https://calbears.com/sports/football/schedule/2026); [calbears.com 2020 KGO release](https://calbears.com/news/2020/6/15/athletics-news-cal-extends-partnership-with-kgo-radio) |
| 3.5 | Stanford football flagship = KNBR 1050 AM (KTCT); note Cumulus describes 1050 carriage as "HD3 channel KTCT/1050" — HD3 subchannel vs main AM carrier is a reception nuance for 94122 (see F20) | VERIFIED as affiliate; HD3 nuance flagged | [gostanford.com Jul 30, 2026 broadcast team](https://gostanford.com/news/2026/07/30/2026-football-radio-broadcast-team-announced); [thesportsleader.com](https://www.thesportsleader.com/stanfordfootball/); [cumulusmedia.com Apr 15, 2026](https://www.cumulusmedia.com/2026/04/15/san-francisco-49ers-announce-multi-year-partnership-extension-with-cumulus-medias-knbr/) |
| 3.6 | NCAAF average game ~3 h 26 m (2025) | Secondary analysis; site keeps 180-min planning overlay labeled as assumption (F05) | [SI](https://www.si.com/fannation/college/cfb-hq/ncaa-football/how-long-are-college-football-games-what-you-need-to-know) |

## 4. Vacation-window conclusions (strict definition: no MLB, no NFL incl. Westwood One national, no Stanford/Cal)

| # | Conclusion | Basis |
|---|---|---|
| 4.1 | **2027: Feb 15–18 (4 days)** sits between verified Super Bowl LXI (Feb 14, 2027) and verified first 2027 MLB spring-training games (Feb 19, 2027); NFL postseason ends with the Super Bowl; NCAAF bowl season ends January | Items 1.4, 2.1 — verified anchors, but not certified against every other radio sport (Warriors etc.), so the site correctly does NOT label it "free" (F01) |
| 4.2 | **2027 All-Star week**: feed shows games through Jul 11, ASG Jul 13, no feed games Jul 14–15, full slate Jul 16. The only fully game-free feed date is **Jul 14**; Jul 13 is busy (ASG). The earlier session's "Jul 12–14 all-clear" claim remains contradicted (F15/F18) | Item 1.3 |
| 4.3 | **No 7/14/21-day all-clear window exists in 2027, 2028, or 2029** under the strict definition: NFL runs continuously Sep → mid-Feb and overlaps MLB (late Feb/Mar–Oct) and NCAAF (Aug–Jan) | Items 1.1–1.4, 2.1, 2.5, 3.1–3.3 |
| 4.4 | **2028**: best gap ≈ **Feb 14–17, 2028** (between verified Super Bowl LXII Feb 13, 2028 and estimated 2028 spring-training start ~mid-Feb 2028) — ESTIMATED on the MLB side, VERIFIED on the NFL side | Items 1.6, 2.5 |
| 4.5 | **2029**: best gap ≈ **mid-February 2029** after Super Bowl LXIII (date TBD; venue Las Vegas) — entirely ESTIMATED until the NFL releases 2028-important-dates and MLB releases the 2029 schedule | Items 1.6, 2.6 |

## 5. Irregularities found during this pass (added to `site/data/research.json` as F17–F20)

- **F17** Stanford 2027 opponent list in the preserved root `research/sources.md` (2023 eight-game ACC model) is superseded by the ACC's Sep 16, 2026 nine-game announcement.
- **F18** Official 2027 MLB feed has no rows on Jul 14–15, 2027 while press coverage says the second half opens Thu Jul 15 with one ESPN game; treated conservatively (Jul 13 busy, Jul 14 game-free in feed, Jul 15 uncertain).
- **F19** Super Bowl LXII date (Feb 13, 2028) is now officially announced, upgrading the 2028 gap's NFL anchor from estimated to verified; 2029 SB date still TBD.
- **F20** KNBR 1050 (Stanford) is described by Cumulus as an HD3 subchannel (KTCT/1050); ordinary AM/FM reception nuance for 94122 stays flagged under F10.
- **F21** 2027 MLB game-level start times remain mostly TBD (1,930 of 2,901 feed rows lack a start) — already covered by F07; possible MLB CBA stoppage (CBA expires Dec 2026) could shift 2027 dates — press-flagged.

## 6. Tests run this session

- `node --test tests/core.test.js tests/engine.test.mjs` → 14/14 pass
- `python3 tests/validate.py` → 6/6 pass (source URLs, unique IDs, coverage counts, 30 clubs, 46 Westwood One rows, research register)
- `node tests/check-site.js` → all root pages, nav targets and local assets found
