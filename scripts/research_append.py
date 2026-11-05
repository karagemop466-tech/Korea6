"""Idempotent, additive merge of session arena/63ee3d13-korea6's source and flag rows
into site/data/research.json.

Nothing is ever overwritten: sources are merged by URL (the new claim text is appended
to an existing entry when the URL is already registered), and flags are merged by id.
Run: python3 scripts/research_append.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "site/data/research.json"
CHECKED = "2026-11-05"

NFL_DATES = "https://operations.nfl.com/calendar-events/nfl-important-dates"
FORTYNINERS = "https://www.49ers.com/schedule/"
MLB_2027_NEWS = "https://www.mlb.com/news/mlb-2027-schedule-released"
MLB_API = "https://statsapi.mlb.com/api/v1/schedule?sportId=1"
SB62 = "https://www.nfl.com/news/mercedes-benz-stadium-in-atlanta-to-host-super-bowl-lxii-in-2028"
SB63 = "https://www.nfl.com/news/las-vegas-to-host-super-bowl-lxiii-in-2029"

SOURCES = [
    {"name": "MLB 2027 schedule release (milestones)",
     "claim": "Read 2026-11-05: 2027 Opening Night Wed Mar 24 (Netflix, matchup TBD); traditional Opening Day Thu Mar 25 with 14 games; first full slate Sat Mar 27; 97th All-Star Game Tue Jul 13 at Wrigley Field; Home Run Derby Mon Jul 12; second half begins Thu Jul 15; final regular-season day Sun Sep 26. Labor Day Mon Sep 6 is a full-slate day.",
     "source": MLB_2027_NEWS},
    {"name": "MLB Stats API — 2027 spring-training opener evidence",
     "claim": "Read 2026-11-05: the official feed returns 17 spring-training games on 2027-02-19 and zero for 2027-02-15..2027-02-18, which is the game-level basis for the Feb 15-18, 2027 gap.",
     "source": f"{MLB_API}&startDate=2027-02-15&endDate=2027-02-22"},
    {"name": "MLB Stats API — 2028 returns no rows",
     "claim": "Read 2026-11-05: totalItems 0 for 2028. An empty official response is unknown coverage, not an empty season. Every 2028 date used anywhere on the site is a labelled projection.",
     "source": f"{MLB_API}&startDate=2028-01-01&endDate=2028-12-31"},
    {"name": "MLB Stats API — 2029 returns no rows",
     "claim": "Read 2026-11-05: totalItems 0 for 2029. Same treatment as 2028: unknown coverage, never 'free'.",
     "source": f"{MLB_API}&startDate=2029-01-01&endDate=2029-12-31"},
    {"name": "NFL Football Operations — 2026-27 postseason and Week 18",
     "claim": "Read 2026-11-05: Week 18 is Jan 9-10, 2027; Wild Card Jan 16-18; Divisional Jan 23-24; AFC/NFC Championships Jan 31; Super Bowl LXI Sun Feb 14, 2027 at SoFi Stadium, Inglewood. Also lists the Nov 22, 2026 Vikings-49ers international game at Estadio Banorte (Mexico City, 8:20 PM ET).",
     "source": NFL_DATES},
    {"name": "49ers official 2026 schedule — Week 18 TBD and per-game radio",
     "claim": "Read 2026-11-05: 49ers.com lists Week 18 (at Arizona Cardinals) as TBD for both date and TV, while every game on the page lists radio as 'KSAN 107.7 FM / KNBR 104.5 FM / 680 AM'. Week 1 was played at the Melbourne Cricket Ground. Week 8 was the bye.",
     "source": FORTYNINERS},
    {"name": "NFL.com — Atlanta to host Super Bowl LXII (date still TBA on NFL.com)",
     "claim": "Read 2026-11-05: NFL.com confirms Mercedes-Benz Stadium, Atlanta as the LXII host, but its own 'Upcoming Super Bowls' table lists the LXII date as TBA. The Feb 13, 2028 date is therefore reported, not officially tabled.",
     "source": SB62},
    {"name": "NFL.com — Las Vegas to host Super Bowl LXIII in 2029",
     "claim": "Read 2026-11-05: NFL.com confirms Allegiant Stadium, Las Vegas as the LXIII host. The announcement gives no firm date ('February 2029'), so Feb 11, 2029 is a projection.",
     "source": SB63},
    {"name": "Non-official: Super Bowl LXII date reported as Feb 13, 2028",
     "claim": "NOT an official source. Pro Football Talk (Yahoo Sports) reported that the NFL set Super Bowl LXII for Feb 13, 2028, which also rules out an 18-game 2027 regular season. Used only to label a REPORTED value; never promoted to VERIFIED.",
     "source": "https://sports.yahoo.com/articles/nfl-sends-message-2028-super-153037714.html"},
]

FLAGS = [
    {"id": "F27",
     "title": "Stored NFL 2026 snapshot is missing Week 18 and 24 flexed games",
     "detail": "The imported nfl-2026.json stops at Jan 3-4, 2027, but NFL Football Operations lists Week 18 as Jan 9-10, 2027 and 49ers.com lists San Francisco's Week 18 game at Arizona as TBD. 24 imported rows (including that 49ers game) carry a null date and null start because their kickoffs are flexed. Jan 9-10, 2027 must be treated as BUSY even though the dashboard shows no rows.",
     "source": NFL_DATES},
    {"id": "F28",
     "title": "2027 MLB postseason is absent from the official feed",
     "detail": "The MLB 2027 snapshot ends at the last regular-season day, Sep 26, 2027, and contains no Wild Card, Division Series, Championship Series or World Series rows. The 2026 snapshot did contain them, so this is a coverage gap. October 2027 is scored BUSY UNKNOWN, never free.",
     "source": f"{MLB_API}&startDate=2027-10-01&endDate=2027-11-30"},
    {"id": "F29",
     "title": "2027 Opening Night (Mar 24) is missing from the official feed",
     "detail": "MLB.com announces a Mar 24, 2027 Opening Night game on Netflix with the matchup TBD. The MLB Stats API snapshot has no game on 2027-03-24, so a naive gap scan reports that day as empty. It is treated as BUSY.",
     "source": MLB_2027_NEWS},
    {"id": "F30",
     "title": "Super Bowl LXII date is reported, not officially tabled",
     "detail": "NFL.com confirms Atlanta as the LXII host but lists the date as TBA. The Feb 13, 2028 date comes from non-official reporting (ESPN/Pro Football Talk). A previously registered source row in this file asserted that the Oct 15, 2024 NFL release announced Feb 13, 2028; the official media.nfl.com release does not state a date, so that earlier claim is corrected here.",
     "source": SB62},
    {"id": "F31",
     "title": "Super Bowl LXIII date is not announced",
     "detail": "NFL.com confirms Las Vegas / Allegiant Stadium as the LXIII host but the announcement gives no firm date beyond February 2029. Feb 11, 2029 is a projection published as ESTIMATED.",
     "source": SB63},
    {"id": "F32",
     "title": "MLB 2028 and 2029 schedules do not exist yet",
     "detail": "The MLB Stats API returns totalItems 0 for both 2028 and 2029. Every 2028 and 2029 baseball date on the site — spring-training openers and Opening Day — is a projection derived from the 2026/2027 pattern and is labelled ESTIMATED. They are not released schedules.",
     "source": f"{MLB_API}&startDate=2028-01-01&endDate=2028-12-31"},
    {"id": "F33",
     "title": "Official sources disagree about whether Jul 15, 2027 has MLB games",
     "detail": "MLB.com states the 2027 second half begins Thursday, July 15, but the MLB Stats API snapshot has no game on 2027-07-15 (nor on 2027-07-12 or 2027-07-14, while 2027-07-13 holds the All-Star Game). The conservative reading — Jul 15 is busy — is used, which caps the All-Star break at one isolated clear day (Jul 12 or Jul 14), not a vacation window.",
     "source": MLB_2027_NEWS},
    {"id": "F34",
     "title": "Withdrawn claim: there is no verified Jul 12-14, 2027 all-clear window",
     "detail": "A stale, unmerged pull request and older page wording described 'Mon Jul 12 - Wed Jul 14, 2027' as a verified 3-day window. Tue Jul 13, 2027 is the 97th MLB All-Star Game, so that period is not clear. The corrected reading is a single isolated day: Jul 12 (Home Run Derby, no game) or Jul 14. Those pull requests (#1 and #13) were closed unmerged rather than republished; #13 also asserted VERIFIED status against non-official sources (topendsports, sportsbrackets.net, academicjobs.com, upintherafters, Wikipedia).",
     "source": MLB_2027_NEWS},
    {"id": "F36",
     "title": "Cal football's 810 AM call sign was KGO, now KSFO",
     "detail": "Cumulus moved the KSFO call sign from 560 AM to the 810 AM facility on Nov 18, 2024, and the call transfer completed Jan 1, 2025; the KGO call letters were retired and 560 AM (later KZAC) went dark in 2025-26. Official UC Berkeley event listings now read 'Radio: KSFO 810 AM'. The legacy data-ncaaf.html row that said 'KGO 810 AM' was corrected on 2026-11-05; site/data/research.json already used KSFO.",
     "source": "https://events.berkeley.edu/sports/event/315720-california-football-vs-pittsburgh"},
    {"id": "F37",
     "title": "Athletics flagship is KNEW 960 AM (Bay Area), with KSTE 650 AM as the Sacramento flagship",
     "detail": "Read 2026-11-05 from the official Athletics affiliates page: terrestrial radio lists '960 AM KNEW, Bay Area' and '650 AM KSTE, Sacramento'; everything else (A's Cast, iHeartRadio, MLB At Bat) is streaming, not AM/FM. Older 'Bloomberg 960 AM' branding is stale — KNEW flipped to an iHeart sports-talk format in Oct 2024. Reception of a 960 kHz Oakland signal in Outer Sunset 94122 remains unverified.",
     "source": "https://www.mlb.com/athletics/schedule/affiliates"},
    {"id": "F38",
     "title": "Giants flagships confirmed on the official MLB broadcast-partners page",
     "detail": "Read 2026-11-05: KNBR 680 AM / 104.5 FM is the English flagship and KSFN 1510 AM / 99.3 FM the Spanish flagship. This confirms the existing station register entries but does not by itself prove reception at a specific address in 94122.",
     "source": "https://www.mlb.com/giants/schedule/broadcast-partners"},
    {"id": "F35",
     "title": "No 1-, 2- or 3-week window exists under the rule exactly as written",
     "detail": "Confirmed against the official boundaries: the longest clean run is 4 days in 2027 (Feb 15-18, between Super Bowl LXI and the first spring-training games), with the 2028 and 2029 equivalents estimated at 4 days each. The only relaxation that produces a multi-week window is ignoring MLB spring training, which opens Feb 15 - Mar 23, 2027 (37 days) with official dates at both ends. That run contains 32 days with a Giants or Athletics spring-training game, and Golden State Warriors and Cal basketball broadcasts remain on Bay Area AM/FM throughout.",
     "source": NFL_DATES},
]


def main():
    data = json.loads(TARGET.read_text())

    by_url = {s["source"]: s for s in data["sources"]}
    added = merged = 0
    for row in SOURCES:
        existing = by_url.get(row["source"])
        if existing:
            if row["claim"] not in existing["claim"]:
                existing["claim"] = existing["claim"].rstrip() + " " + row["claim"]
                merged += 1
        else:
            data["sources"].append({"name": row["name"], "claim": row["claim"], "source": row["source"]})
            by_url[row["source"]] = data["sources"][-1]
            added += 1

    by_id = {f["id"]: f for f in data["flags"]}
    f_added = f_kept = 0
    for row in FLAGS:
        if row["id"] in by_id:
            f_kept += 1
            continue
        data["flags"].append(row)
        f_added += 1

    TARGET.write_text(json.dumps(data, indent=1) + "\n")
    print(f"research.json: {added} source rows added, {merged} merged into existing URLs; "
          f"{f_added} flags added, {f_kept} flag ids already present (left untouched).")


if __name__ == "__main__":
    main()
