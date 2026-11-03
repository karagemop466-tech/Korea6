# COORDINATION.md — Shared Task Board (Korea6 / Free-Time Vacation project)

Project: Build a GitHub Pages site that identifies "free time" (no live radio sports in the SF Bay Area)
for MLB (all 30 clubs; Giants/A's high priority), NFL (all; 49ers high priority), Stanford & Cal NCAAF
(high priority), and Westwood One Sports national NFL broadcasts. Target vacation windows in 2027, 2028, 2029.

## Session log

### Session: arena/fbb7cd8f-korea6 (this session) — 2026-11-03
- [x] INIT — Repo reviewed (only README.md present). COORDINATION.md created.
- [x] RESEARCH — Official sources verified (full log in research/sources.md). Key findings:
  MLB 2027 schedule VERIFIED released Jul 16, 2026 (Mar 24 opener; ASG Jul 13; ends Sep 26);
  2027 Spring Training VERIFIED opens Feb 19, 2027; NFL 2026 VERIFIED (Super Bowl LXI Feb 14, 2027,
  SoFi); NFL 2027+ / MLB 2028+ / NCAAF 2027 dates NOT released → estimated & flagged;
  Cal 2027 nonconference + ACC opponents VERIFIED; Stanford 2027 ACC opponents VERIFIED;
  Westwood One 2026 NFL package VERIFIED; Bay Area radio map VERIFIED (KNBR 680 Giants/49ers/W1 NFL,
  KNBR 1050 Stanford, KGO 810 Cal, Bloomberg 960 A's, KSTE 650 A's-Sacramento flagged);
  durations VERIFIED: MLB 2:38, NFL 3:03 (12-min HT), NCAAF ~3:26.
- [x] DATA — data/calendar.json generated (tools/generate_calendar.py), 1155 days Nov 2026–Dec 2029,
  per-day verified/estimated flags. All-clear runs: 2027-02-15..18 (4d, VERIFIED), 2027-07-12..14
  (3d, VERIFIED), 2028-02-14..17 (4d, est.), 2029-02-12..16 (5d, est.).
- [x] SITE — index/calendar/windows/summary/data-mlb/data-nfl/data-ncaaf/radio/flagged built (assets/).
- [x] VERIFY — JS syntax checked (node --check OK); calendar.json spot-checked at anchor dates;
  every data row has an official source link or an ESTIMATED/NOT RELEASED flag (flagged.html lists 10 items).
- [in progress] PR — Open PR to main, merge, enable/confirm GitHub Pages deploy, record PR link here.

## Task claims
| Task | Status | Owner session | Files touched |
|---|---|---|---|
| INIT + COORDINATION.md | done | arena/fbb7cd8f-korea6 | COORDINATION.md, README.md |
| RESEARCH official sources | in progress | arena/fbb7cd8f-korea6 | research/notes.md |
| DATA tables (verified vs estimated) | unclaimed | — | data/*.json, data/*.md |
| SITE build (pages + nav + calendar) | unclaimed | — | site/ (index + subpages) |
| VERIFY line-by-line | unclaimed | — | site/, research/ |
| PR + merge + Pages deploy | unclaimed | — | COORDINATION.md |

## Rules
- Never present an unverified/estimated value as verified. Blank + flag instead.
- Small, frequent commits on this branch; `git pull --rebase` before every push.
- Shared outputs (site index/nav, combined tables) are finalized by the integration step at the end.

## Session log — arena/fbb7cd8f-korea6 (2026-11-03)
- Claimed: RESEARCH/DATA/SITE/VERIFY for the verified free-time window analysis (scope: research/sources.md, tools/generate_calendar.py, data/calendar.json, assets/free-time.css, assets/calendar.js, calendar.html, windows.html, summary.html, data-mlb.html, data-nfl.html, data-ncaaf.html; additive nav entries in assets/app.js).
- Verified from official sources (full log in research/sources.md): MLB 2027 schedule released 2026-07-16 (mlb.com) — opener Mar 24-25 2027, ASG Jul 13 2027, season ends Sep 26 2027; 2027 Spring Training opens Feb 19 2027 (mlb.com press release); NFL 2026 season key dates incl. Super Bowl LXI Feb 14 2027 SoFi (Westwood One/Cumulus, nfl.com via press); Westwood One 2026 NFL radio package (westwoodonesports.com/nfl-schedule); Cal 2027 nonconference (Aug 28 Sac State, Sep 4 at UCLA, Sep 11 ODU) and ACC opponents (calbears.com); Stanford 2027 ACC opponents (gostanford.com); radio flagships KNBR 680 (Giants/49ers/Westwood One NFL SF), KNBR 1050 (Stanford), KGO 810 (Cal), Bloomberg 960 + KSTE 650 (A's); durations MLB 2:38 (mlb.com), NFL 3:03 (2025 play-by-play), NCAAF ~3:26 (NCAA stats).
- Findings: all-clear (no MLB/NFL/Stanford/Cal/Westwood One) runs: 2027-02-15..18 (4 days, VERIFIED anchors), 2027-07-12..14 (3 days, VERIFIED), 2028-02-14..17 (4 days, ESTIMATED), 2029-02-12..16 (5 days, ESTIMATED). No 1-3 week all-clear window exists in 2027-2029 because the NFL season continuously overlaps MLB/NCAAF.
- Irregularities flagged (published on the site's Flagged page + research/sources.md): 2027 MLB game times TBD; 2027 NFL slate unreleased (May 2027); all 2028-2029 schedules unreleased; possible MLB CBA stoppage Dec 2026; KSTE 650/KHTK 1140 reception in 94122 unverified; estimated typical daily broadcast windows used for the day calendar.
- Conflict resolution: main had advanced (PR #2/#3 from arena-99e24d1c with a JS site). Rebased; kept that session's index/radio/flagged/style/COORDINATION content and integrated this session's pages additively (own stylesheet free-time.css; no shared file overwritten except additive nav entries in assets/app.js). Their work was not discarded.
- PR #4 updated with this integration; merged to main; Pages deploy re-confirmed (see PR #4).
