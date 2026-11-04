# Independent integration audit — 2026-11-04

This is a targeted audit, not a line-by-line certification of all records or a comprehensive link check. Earlier logs and generated data retain their historical claims and must not be treated as independently reverified here.

| Finding | Evidence and review status |
|---|---|
| National radio schedule | [Westwood One NFL schedule](https://www.westwoodonesports.com/nfl-schedule/) lists upcoming national broadcasts, e.g. Jacksonville at Baltimore on November 5. It does not establish local carriage of each event or reception at a particular address. |
| 49ers radio | [49ers radio partners](https://www.49ers.com/fans/tv-radio) list KNBR 680 and KSAN 107.7 as flagship stations and describe a three-hour pregame show. This does not prove reception at an individual home or every future station assignment. |
| Vacation findings | Incomplete future and radio schedules cannot establish zero 7-, 14-, or 21-day windows, annual longest gaps, or a confirmed February 15–18, 2027 all-clear. Compare [NFL important dates](https://operations.nfl.com/calendar-events/nfl-important-dates) and [MLB schedule API](https://statsapi.mlb.com/api/v1/schedule?sportId=1&season=2027&startDate=2027-02-19&endDate=2027-02-19); milestone boundaries alone do not prove absence between them. Scope page and README corrected. Review flag F27 records the raw historical data issue. |
| Official link irregularity | The attempted URL https://www.mlb.com/news/mlb-2027-spring-training-schedule-released returned an MLB 404 during review; do not use it as evidence. This was a test URL, not a comprehensive external-link audit. |
| Open work | Full verified 2027–2029 schedules, game-by-game local AM/FM carriage, station reception, exact broadcast ends, and comprehensive independent row verification remain incomplete. Estimates are not confirmed schedules. |

Local automated tests check software behavior, not the correctness of all source data. See the dashboard review page and earlier logs for additional unresolved issues.
