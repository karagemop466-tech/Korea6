# Westwood One NFL / NCAAF national radio — line-by-line re-verification (2026-11-06)

Session: `arena/92bf4127-korea6`. Claimed on [COORDINATION.md](../COORDINATION.md). This file is a verification report only; it does not change any shared data file (`site/data/*.json`). Shared-data follow-ups are listed in section 5 for the final integration session.

## 1. Method

- Official source: [Westwood One NFL schedule](https://www.westwoodonesports.com/nfl-schedule/) (Upcoming tab, fetched 2026-11-06, 3 pages of content). Its per-game links are on westwoodonesports.com/events/<id>.
- Each official entry (event ID, date, matchup, kickoff time printed as **ET**) was transcribed and compared with the stored rows in `site/data/curated.json` where `kind == "Westwood One"`, matched by event ID.
- ET was converted to Pacific by subtracting 3 hours. This is valid for all listed dates, since US daylight saving time ended on Nov 1, 2026 and PST applies through January 2027.
- Checked fields: date, start date, and Pacific start time. Matchup titles were compared as displayed.
- Comparison script output is reproduced in section 3. The script was run locally; no values were inferred.

## 2. Result

- Official entries checked: **46** (45 NFL + 1 NCAAF `Oregon at Ohio State`).
- Matched to a stored row on event ID, date and Pacific time: **46 / 46**.
- Stored Westwood One rows NOT on the official Upcoming list: **1** — `ww-548561` Jacksonville Jaguars at Baltimore Ravens, 2026-11-05 (see section 4, item 1).
- Local Bay Area carriage: **not verified for any row**. Every stored Westwood One row has `station: null`; the national feed listing is not a claim about KNBR/KGO/other Bay Area affiliates.
- Postseason: the network's announcement says it carries every postseason contest and Super Bowl LXI (Feb 14, 2027). **No postseason game-level rows exist** in the stored data, and none appear on the Upcoming list yet (see section 4, item 2).

## 3. Row-by-row check (official entry → stored row)

| Event ID | Official date | Matchup (as listed) | Official ET | Pacific (converted) | Official label | Stored date & Pacific start | Result | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 548489 | 2026-11-08 | Cincinnati Bengals vs Atlanta Falcons | 09:15 | 06:15 | 2026 NFL Madrid Game | 2026-11-08 06:15 | Match | [event 548489](https://www.westwoodonesports.com/events/548489) |
| 548541 | 2026-11-09 | Buffalo Bills at Minnesota Vikings | 19:00 | 16:00 | Monday Night Football | 2026-11-09 16:00 | Match | [event 548541](https://www.westwoodonesports.com/events/548541) |
| 548490 | 2026-11-15 | New England Patriots vs Detroit Lions | 09:15 | 06:15 | 2026 NFL Munich Game | 2026-11-15 06:15 | Match | [event 548490](https://www.westwoodonesports.com/events/548490) |
| 548542 | 2026-11-16 | Los Angeles Chargers at Baltimore Ravens | 19:00 | 16:00 | Monday Night Football | 2026-11-16 16:00 | Match | [event 548542](https://www.westwoodonesports.com/events/548542) |
| 548491 | 2026-11-22 | Minnesota Vikings vs San Francisco 49ers | 19:30 | 16:30 | 2026 NFL Mexico City Game | 2026-11-22 16:30 | Match | [event 548491](https://www.westwoodonesports.com/events/548491) |
| 548511 | 2026-11-25 | Green Bay Packers at Los Angeles Rams | 19:30 | 16:30 | Thanksgiving Wednesday | 2026-11-25 16:30 | Match | [event 548511](https://www.westwoodonesports.com/events/548511) |
| 548513 | 2026-11-26 | Philadelphia Eagles at Dallas Cowboys | 16:15 | 13:15 | NFL Thanksgiving Day Tripleheader | 2026-11-26 13:15 | Match | [event 548513](https://www.westwoodonesports.com/events/548513) |
| 548515 | 2026-11-27 | Denver Broncos at Pittsburgh Steelers | 14:30 | 11:30 | NFL Black Friday Game | 2026-11-27 11:30 | Match | [event 548515](https://www.westwoodonesports.com/events/548515) |
| 548544 | 2026-11-30 | Carolina Panthers at Tampa Bay Buccaneers | 19:00 | 16:00 | Monday Night Football | 2026-11-30 16:00 | Match | [event 548544](https://www.westwoodonesports.com/events/548544) |
| 548503 | 2026-12-06 | Houston Texans at Pittsburgh Steelers | 19:30 | 16:30 | Sunday Night Football | 2026-12-06 16:30 | Match | [event 548503](https://www.westwoodonesports.com/events/548503) |
| 548567 | 2026-12-10 | Minnesota Vikings at New England Patriots | 19:30 | 16:30 | Thursday Night Football | 2026-12-10 16:30 | Match | [event 548567](https://www.westwoodonesports.com/events/548567) |
| 548546 | 2026-12-14 | Pittsburgh Steelers at Jacksonville Jaguars | 19:00 | 16:00 | Monday Night Football | 2026-12-14 16:00 | Match | [event 548546](https://www.westwoodonesports.com/events/548546) |
| 548517 | 2026-12-19 | Seattle Seahawks at Philadelphia Eagles | 16:30 | 13:30 | Week 15 Saturday NFL Doubleheader | 2026-12-19 13:30 | Match | [event 548517](https://www.westwoodonesports.com/events/548517) |
| 548506 | 2026-12-20 | Detroit Lions at Minnesota Vikings | 19:30 | 16:30 | Sunday Night Football | 2026-12-20 16:30 | Match | [event 548506](https://www.westwoodonesports.com/events/548506) |
| 548569 | 2026-12-24 | Houston Texans at Philadelphia Eagles | 19:30 | 16:30 | Thursday Night Football | 2026-12-24 16:30 | Match | [event 548569](https://www.westwoodonesports.com/events/548569) |
| 548531 | 2026-12-25 | Buffalo Bills at Denver Broncos | 16:15 | 13:15 | Christmas Day NFL Tripleheader | 2026-12-25 13:15 | Match | [event 548531](https://www.westwoodonesports.com/events/548531) |
| 548519 | 2026-12-26 | Week 16 Saturday Doubleheader TBA | 16:00 | 13:00 | Week 16 Saturday NFL Doubleheader | 2026-12-26 13:00 | Match | [event 548519](https://www.westwoodonesports.com/events/548519) |
| 548507 | 2026-12-27 | Jacksonville Jaguars at Dallas Cowboys | 19:30 | 16:30 | Sunday Night Football | 2026-12-27 16:30 | Match | [event 548507](https://www.westwoodonesports.com/events/548507) |
| 548570 | 2026-12-31 | Baltimore Ravens at Cincinnati Bengals | 19:30 | 16:30 | Thursday Night Football | 2026-12-31 16:30 | Match | [event 548570](https://www.westwoodonesports.com/events/548570) |
| 548522 | 2027-01-02 | Week 17 Saturday NFL Doubleheader TBA | 20:00 | 17:00 | Week 17 Saturday NFL Doubleheader | 2027-01-02 17:00 | Match | [event 548522](https://www.westwoodonesports.com/events/548522) |
| 548552 | 2027-01-04 | Houston Texans at Green Bay Packers | 19:00 | 16:00 | Monday Night Football | 2027-01-04 16:00 | Match | [event 548552](https://www.westwoodonesports.com/events/548552) |
| 548524 | 2027-01-09 | Week 18 Saturday Tripleheader TBA | 16:15 | 13:15 | Week 18 Saturday NFL Tripleheader | 2027-01-09 13:15 | Match | [event 548524](https://www.westwoodonesports.com/events/548524) |
| 548510 | 2027-01-10 | Week 18 Sunday Night Football - Teams TBA | 19:30 | 16:30 | Sunday Night Football | 2027-01-10 16:30 | Match | [event 548510](https://www.westwoodonesports.com/events/548510) |
| 548500 | 2026-11-08 | Tampa Bay Buccaneers at Chicago Bears | 19:30 | 16:30 | Sunday Night Football | 2026-11-08 16:30 | Match | [event 548500](https://www.westwoodonesports.com/events/548500) |
| 548562 | 2026-11-12 | Washington Commanders at New York Giants | 19:30 | 16:30 | Thursday Night Football | 2026-11-12 16:30 | Match | [event 548562](https://www.westwoodonesports.com/events/548562) |
| 548501 | 2026-11-15 | Pittsburgh Steelers at Cincinnati Bengals | 19:30 | 16:30 | Sunday Night Football | 2026-11-15 16:30 | Match | [event 548501](https://www.westwoodonesports.com/events/548501) |
| 548564 | 2026-11-19 | Indianapolis Colts at Houston Texans | 19:30 | 16:30 | Thursday Night Football | 2026-11-19 16:30 | Match | [event 548564](https://www.westwoodonesports.com/events/548564) |
| 548543 | 2026-11-23 | Cincinnati Bengals at Washington Commanders | 19:00 | 16:00 | Monday Night Football | 2026-11-23 16:00 | Match | [event 548543](https://www.westwoodonesports.com/events/548543) |
| 548512 | 2026-11-26 | Chicago Bears at Detroit Lions | 12:30 | 09:30 | NFL Thanksgiving Day Tripleheader | 2026-11-26 09:30 | Match | [event 548512](https://www.westwoodonesports.com/events/548512) |
| 548514 | 2026-11-26 | Kansas City Chiefs at Buffalo Bills | 20:00 | 17:00 | NFL Thanksgiving Day Tripleheader | 2026-11-26 17:00 | Match | [event 548514](https://www.westwoodonesports.com/events/548514) |
| 548502 | 2026-11-29 | New England Patriots at Los Angeles Chargers | 19:30 | 16:30 | Sunday Night Football | 2026-11-29 16:30 | Match | [event 548502](https://www.westwoodonesports.com/events/548502) |
| 548566 | 2026-12-03 | Kansas City Chiefs at Los Angeles Rams | 19:30 | 16:30 | Thursday Night Football | 2026-12-03 16:30 | Match | [event 548566](https://www.westwoodonesports.com/events/548566) |
| 548545 | 2026-12-07 | Dallas Cowboys at Seattle Seahawks | 19:00 | 16:00 | Monday Night Football | 2026-12-07 16:00 | Match | [event 548545](https://www.westwoodonesports.com/events/548545) |
| 548505 | 2026-12-13 | Buffalo Bills at Green Bay Packers | 19:30 | 16:30 | Sunday Night Football | 2026-12-13 16:30 | Match | [event 548505](https://www.westwoodonesports.com/events/548505) |
| 548568 | 2026-12-17 | San Francisco 49ers at Los Angeles Chargers | 19:30 | 16:30 | Thursday Night Football | 2026-12-17 16:30 | Match | [event 548568](https://www.westwoodonesports.com/events/548568) |
| 548518 | 2026-12-19 | Chicago Bears at Buffalo Bills | 20:00 | 17:00 | Week 15 Saturday NFL Doubleheader | 2026-12-19 17:00 | Match | [event 548518](https://www.westwoodonesports.com/events/548518) |
| 548548 | 2026-12-21 | New England Patriots at Kansas City Chiefs | 19:00 | 16:00 | Monday Night Football | 2026-12-21 16:00 | Match | [event 548548](https://www.westwoodonesports.com/events/548548) |
| 548528 | 2026-12-25 | Green Bay Packers at Chicago Bears | 12:30 | 09:30 | Christmas Day NFL Tripleheader | 2026-12-25 09:30 | Match | [event 548528](https://www.westwoodonesports.com/events/548528) |
| 548534 | 2026-12-25 | Los Angeles Rams at Seattle Seahawks | 20:00 | 17:00 | Christmas Day NFL Tripleheader | 2026-12-25 17:00 | Match | [event 548534](https://www.westwoodonesports.com/events/548534) |
| 548520 | 2026-12-26 | Week 16 Saturday Doubleheader TBA | 20:00 | 17:00 | Week 16 Saturday NFL Doubleheader | 2026-12-26 17:00 | Match | [event 548520](https://www.westwoodonesports.com/events/548520) |
| 548550 | 2026-12-28 | New York Giants at Detroit Lions | 19:00 | 16:00 | Monday Night Football | 2026-12-28 16:00 | Match | [event 548550](https://www.westwoodonesports.com/events/548550) |
| 548521 | 2027-01-02 | Week 17 Saturday Doubleheader TBA | 16:00 | 13:00 | Week 17 Saturday NFL Doubleheader | 2027-01-02 13:00 | Match | [event 548521](https://www.westwoodonesports.com/events/548521) |
| 548509 | 2027-01-03 | Philadelphia Eagles at San Francisco 49ers | 19:30 | 16:30 | Sunday Night Football | 2027-01-03 16:30 | Match | [event 548509](https://www.westwoodonesports.com/events/548509) |
| 548523 | 2027-01-09 | Week 18 Saturday Tripleheader TBA | 12:30 | 09:30 | Week 18 Saturday NFL Tripleheader | 2027-01-09 09:30 | Match | [event 548523](https://www.westwoodonesports.com/events/548523) |
| 548526 | 2027-01-09 | Week 18 Saturday Tripleheader TBA | 20:00 | 17:00 | Week 18 Saturday NFL Tripleheader | 2027-01-09 17:00 | Match | [event 548526](https://www.westwoodonesports.com/events/548526) |
| 557143 | 2026-11-07 | Oregon at Ohio State | 15:00 | 12:00 | NCAAF (Announcers: Danny Reed and Derek Rackley) | 2026-11-07 12:00 | Match | [event 557143](https://www.westwoodonesports.com/events/557143) |

## 4. Irregularities and open items (flagged, not corrected)

1. **`ww-548561` (Nov 5, 2026, Jaguars at Ravens)** is stored as a Westwood One row with start `2026-11-05T16:30:00-08:00`, but it does not appear on the fetched Upcoming list (the list begins Nov 8). It is a past date relative to 2026-11-06. The stored note says "Not a kickoff time". It could not be confirmed from the Upcoming tab; check the Past tab of the official schedule page. Status: **unverified**.
2. **Postseason gap.** The official announcements state Westwood One carries every NFL postseason game and Super Bowl LXI (Feb 14, 2027, SoFi Stadium). Sources: [Radio Ink, Sep 9, 2026](https://radioink.com/2026/09/09/radio-welcomes-back-football-westwood-one-compass-ready/), [Radio-Online, 40th season](https://news.radio-online.com/articles/n49383/Westwood-One-Sets-40th-Season-of-NFL-Coverage), [Westwood One, Aug 3 2026 release](https://www.westwoodone.com/blog/2026/08/03/westwood-ones-nfl-play-by-play-broadcasts-reach-64-million-fans-who-are-more-passionate-and-engaged-than-tv-audiences/). The matchups are not yet set, so no postseason rows can be verified. Do not infer them. The NFL postseason date windows in `curated.json` (Jan 16–24 and Feb 14, 2027) are NFL calendar windows, not Westwood One game listings.
3. **Duplicate event listing on the official page.** `548500` (Bucs at Bears, Nov 8) and `548489` (Bengals vs Falcons, Madrid, Nov 8) are shown in both the NFL block and the 'Upcoming Broadcasts' block of the page. Stored rows are not duplicated, which is correct.
4. **TBA matchups.** Several rows are listed as `TBA` (`548519`, `548520`, `548521`, `548522`, `548523`, `548524`, `548526`, and `548510` 'Teams TBA'). These are present on the official page with dates and times, but the matchups are not confirmed. The stored titles reflect the official wording, and the rows are not filled in.
5. **Time basis.** Official times are printed in ET. Stored `start` values are Pacific and match the ET-minus-3h conversion for every matched row. Stored `timeBasis` is 'Network airtime'; the official page does not use that phrase, so this basis label is unverified and is not a kickoff claim.

## 5. Requests for the final integration session (shared data — not edited here)

- Re-check `ww-548561` against the Past tab of https://www.westwoodonesports.com/nfl-schedule/ and either confirm or remove it.
- Do not add postseason Westwood One rows until matchups are published on westwoodonesports.com; keep the postseason as a labeled note, as above.
- Bay Area carriage (KNBR 680/104.5, KGO 810, KTCT 1050, and others) for each Westwood One NFL row remains unverified; verify against the [Westwood One station finder](https://www.westwoodonesports.com/station-finder) before marking any row as receivable in SF 94122.

## 6. Sources

- [Westwood One NFL schedule (official)](https://www.westwoodonesports.com/nfl-schedule/)
- [Westwood One station finder (official)](https://www.westwoodonesports.com/station-finder)
- [Westwood One 40th-season NFL announcement, Radio-Online](https://news.radio-online.com/articles/n49383/Westwood-One-Sets-40th-Season-of-NFL-Coverage)
- [Westwood One NFL coverage release, Aug 3 2026](https://www.westwoodone.com/blog/2026/08/03/westwood-ones-nfl-play-by-play-broadcasts-reach-64-million-fans-who-are-more-passionate-and-engaged-than-tv-audiences/)
- [Radio Ink, Sep 9 2026](https://radioink.com/2026/09/09/radio-welcomes-back-football-westwood-one-compass-ready/)

