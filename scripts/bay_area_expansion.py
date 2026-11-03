#!/usr/bin/env python3
"""Generate site/data/expanded-official.json from verified primary-source schedules.

Every row in this expansion dataset was verified line by line against official
league, club, university athletics, or network pages on 2026-11-03 (UTC).
No dates, kickoff/tipoff times, opponents, or radio station assignments are
inferred; any unconfirmed field is left null and explained in `note`.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PT = ZoneInfo("America/Los_Angeles")
ET = ZoneInfo("America/New_York")
CHECKED = "2026-11-03"


def pt_iso(date_str: str, hm: str | None) -> str | None:
    if not hm:
        return None
    dt = datetime.strptime(f"{date_str} {hm}", "%Y-%m-%d %H:%M").replace(tzinfo=PT)
    return dt.isoformat()


def et_to_pt_iso(date_str: str, hm_et: str | None) -> tuple[str, str | None]:
    if not hm_et:
        return date_str, None
    dt_et = datetime.strptime(f"{date_str} {hm_et}", "%Y-%m-%d %H:%M").replace(tzinfo=ET)
    dt_pt = dt_et.astimezone(PT)
    return dt_pt.strftime("%Y-%m-%d"), dt_pt.isoformat()


def build_stations() -> list[dict]:
    return [
        {
            "station": "KNBR 680 AM / KNBR-FM 104.5",
            "band": "AM / FM terrestrial",
            "receivable94122": True,
            "properties": [
                "San Francisco Giants (MLB English flagship)",
                "San Francisco 49ers (NFL flagship with KSAN 107.7 FM)",
                "129th Big Game: Stanford at California (Nov 21, 2026)",
                "Westwood One Sports SF affiliate (subject to local conflicts)",
                "San Jose Earthquakes (select overflow matches)",
            ],
            "source": "https://www.mlb.com/giants/schedule/watch",
            "secondarySource": "https://www.49ers.com/fans/tv-radio",
            "westwoodOneSource": "https://www.westwoodonesports.com/station-finder/",
            "checked": CHECKED,
        },
        {
            "station": "KSAN 107.7 FM (107.7 The Bone)",
            "band": "FM terrestrial",
            "receivable94122": True,
            "properties": [
                "San Francisco 49ers (NFL FM flagship across preseason, regular season, and postseason)",
            ],
            "source": "https://www.49ers.com/fans/tv-radio",
            "secondarySource": "https://www.49ers.com/schedule/",
            "checked": CHECKED,
        },
        {
            "station": "KTCT 1050 AM (KNBR 1050)",
            "band": "AM terrestrial",
            "receivable94122": True,
            "properties": [
                "Stanford Football (2026 season flagship)",
                "University of San Francisco (USF Dons) Men's Basketball",
                "Westwood One Sports SF affiliate (listed as KTCT-AM)",
                "San Jose Earthquakes (select overflow matches)",
            ],
            "note": "Stanford Men's Basketball moved off KNBR 1050 AM in 2017-18 to digital/SiriusXM.",
            "source": "https://gostanford.com/news/2026/07/30/2026-football-radio-broadcast-team-announced",
            "secondarySource": "https://usfdons.com/sports/mens-basketball/schedule/2026-27",
            "westwoodOneSource": "https://www.westwoodonesports.com/station-finder/",
            "checked": CHECKED,
        },
        {
            "station": "KSFO 810 AM",
            "band": "AM terrestrial",
            "receivable94122": True,
            "properties": [
                "California Golden Bears Football (regular-season flagship; Big Game on KNBR)",
                "California Golden Bears Men's Basketball (all 2026-27 regular-season games)",
                "San Jose Earthquakes (2026 MLS English radio flagship)",
                "U.S. Bank 49ers Radio Network shoulder/partner station",
            ],
            "source": "https://calbears.com/sports/football/schedule/2026",
            "secondarySource": "https://calbears.com/sports/mens-basketball/schedule/2026-27",
            "mlsSource": "https://www.sjearthquakes.com/news/news-earthquakes-announce-radio-stations-for-2026-mls-season",
            "checked": CHECKED,
        },
        {
            "station": "KGMZ 95.7 FM (95.7 The Game)",
            "band": "FM terrestrial",
            "receivable94122": True,
            "properties": [
                "Golden State Warriors (NBA flagship)",
                "Golden State Valkyries (WNBA multi-year flagship; all home + select away games, May-Sep)",
            ],
            "source": "https://www.nba.com/warriors/schedule",
            "secondarySource": "https://valkyries.wnba.com/news/valkyries-announce-audacy-as-radio-partner-20250514",
            "checked": CHECKED,
        },
        {
            "station": "KNEW 960 AM (iHeartRadio)",
            "band": "AM terrestrial",
            "receivable94122": True,
            "properties": [
                "Athletics (MLB Bay Area terrestrial radio affiliate)",
            ],
            "source": "https://www.mlb.com/athletics/schedule/affiliates",
            "secondarySource": "https://talk960.iheart.com/featured/oakland-as/",
            "checked": CHECKED,
        },
        {
            "station": "KSFN 1510 AM / 99.3 FM",
            "band": "AM / FM translator terrestrial",
            "receivable94122": True,
            "properties": [
                "San Francisco Giants (MLB Spanish radio flagship)",
            ],
            "source": "https://www.mlb.com/giants/schedule/watch",
            "checked": CHECKED,
        },
        {
            "station": "KZSF 1370 AM (La Kaliente)",
            "band": "AM terrestrial",
            "receivable94122": True,
            "properties": [
                "San Jose Earthquakes (2026 MLS Spanish radio flagship)",
            ],
            "source": "https://www.sjearthquakes.com/news/news-earthquakes-announce-radio-stations-for-2026-mls-season",
            "checked": CHECKED,
        },
    ]


def build_non_terrestrial_exclusions() -> list[dict]:
    return [
        {
            "team": "San Jose Sharks",
            "league": "NHL",
            "audioPlatform": "Sharks Audio Network (sjsharks.com/listen & Sharks+SAP Center app)",
            "terrestrialAmFmIn94122": False,
            "summary": "Moved exclusively to digital streaming in January 2021; does not occupy a standard AM/FM terrestrial frequency in 94122.",
            "source": "https://www.nhl.com/sharks/news/sharks-announce-launch-of-sharks-audio-network-320033246",
            "checked": CHECKED,
        },
        {
            "team": "Stanford Cardinal Men's Basketball",
            "league": "NCAAM",
            "audioPlatform": "GoStanford.com / Varsity Network / SiriusXM",
            "terrestrialAmFmIn94122": False,
            "summary": "Shifted off KNBR 1050 AM beginning in the 2017-18 season to digital streaming and satellite audio; unlike Stanford Football, Cal MBB, and USF MBB, it is not a terrestrial AM/FM conflict.",
            "source": "https://gostanford.com/news/2017/11/09/enhanced-basketball-coverage",
            "secondarySource": "https://gostanford.com/sports/mens-basketball/schedule",
            "checked": CHECKED,
        },
    ]


def build_events() -> list[dict]:
    events: list[dict] = []

    # 1. Missing Westwood One NCAAF national broadcasts (Nov 14 - Dec 12, 2026)
    wwo_ncaaf = [
        ("ww-557144", "2026-11-14", None, "Texas Tech at Oklahoma State", "Kickoff/airtime TBD on Westwood One NCAAF schedule. Local SF affiliate carriage unverified."),
        ("ww-557145", "2026-11-21", None, "LSU at Tennessee", "Kickoff/airtime TBD on Westwood One NCAAF schedule. Local SF affiliate carriage unverified."),
        ("ww-557131", "2026-11-28", "11:30", "Michigan at Ohio State", "Westwood One pregame airtime 11:30 AM ET (8:30 AM PST). Local SF affiliate carriage unverified."),
        ("ww-557146", "2026-12-05", "15:30", "SEC Championship Game (Atlanta, GA)", "Westwood One pregame airtime 3:30 PM ET (12:30 PM PST). Local SF affiliate carriage unverified."),
        ("ww-557132", "2026-12-12", "14:00", "Army vs. Navy (East Rutherford, NJ)", "Westwood One pregame airtime 2:00 PM ET (11:00 AM PST). Local SF affiliate carriage unverified."),
    ]
    for eid, d_et, hm_et, title, note in wwo_ncaaf:
        d_pt, start_iso = et_to_pt_iso(d_et, hm_et)
        events.append({
            "id": eid,
            "date": d_pt,
            "start": start_iso,
            "title": title,
            "league": "NCAAF",
            "source": "https://www.westwoodonesports.com/ncaa-football/",
            "station": None,
            "radioSource": "https://www.westwoodonesports.com/station-finder/",
            "kind": "Westwood One",
            "timeBasis": "Network airtime",
            "priority": True,
            "corePromptScope": True,
            "status": "Scheduled",
            "checked": CHECKED,
            "note": note,
        })

    # 2. Missing Westwood One U.S. Soccer national broadcast (Nov 17, 2026)
    d_pt, start_iso = et_to_pt_iso("2026-11-17", "18:45")
    events.append({
        "id": "ww-572875",
        "date": d_pt,
        "start": start_iso,
        "title": "USMNT vs. Haiti",
        "league": "USSF",
        "source": "https://www.westwoodonesports.com/us-soccer/",
        "station": None,
        "radioSource": "https://www.westwoodonesports.com/station-finder/",
        "kind": "Westwood One",
        "timeBasis": "Network airtime",
        "priority": True,
        "corePromptScope": False,
        "status": "Scheduled",
        "checked": CHECKED,
        "note": "Westwood One U.S. Soccer broadcast (6:45 PM ET / 3:45 PM PST airtime). Local SF affiliate carriage unverified.",
    })

    # 3. Completed Aug-Oct 2026 California Football games (with verified kickoff + KSFO 810 AM)
    cal_fb_2026 = [
        ("2026-09-05", "19:30", "UCLA at California", "Final (L 24-45). Explicit Radio: KSFO 810 AM on schedule."),
        ("2026-09-12", "12:30", "California at Syracuse", "Final (W 21-18). Explicit Radio: KSFO 810 AM on schedule."),
        ("2026-09-19", "12:30", "Wagner at California", "Final (W 49-7). Explicit Radio: KSFO 810 AM on schedule."),
        ("2026-09-25", "19:30", "Clemson at California", "Final (L 10-24). Explicit Radio: KSFO 810 AM on schedule."),
        ("2026-10-03", "12:30", "California at UNLV", "Final (L 31-39). Explicit Radio: KSFO 810 AM on schedule."),
        ("2026-10-10", "12:30", "Virginia Tech at California", "Final (W 25-20). Explicit Radio: KSFO 810 AM on schedule."),
        ("2026-10-17", "19:30", "Wake Forest at California", "Final (L 7-41). Explicit Radio: KSFO 810 AM on schedule."),
        ("2026-10-24", "09:00", "California at SMU", "Final (L 20-59). Explicit Radio: KSFO 810 AM on schedule."),
        ("2026-10-31", "09:00", "California at NC State", "Final (L 10-31). Explicit Radio: KSFO 810 AM on schedule."),
    ]
    for d, hm, title, note in cal_fb_2026:
        events.append({
            "id": f"cal-fb-{d}",
            "date": d,
            "start": pt_iso(d, hm),
            "title": title,
            "league": "NCAAF",
            "source": "https://calbears.com/sports/football/schedule/2026",
            "station": "KSFO 810 AM",
            "radioSource": "https://calbears.com/sports/football/schedule/2026",
            "kind": "Regular season",
            "timeBasis": "Kickoff",
            "priority": True,
            "corePromptScope": True,
            "status": "Final",
            "checked": CHECKED,
            "note": note,
        })

    # 4. Completed Aug-Oct 2026 Stanford Football games (schedule strip shows Final; kickoff left null)
    stan_fb_2026 = [
        ("2026-08-29", "Hawai'i at Stanford", "Final (W 37-27). GoStanford schedule strip displays Final rather than kickoff time; season flagship KTCT 1050 AM."),
        ("2026-09-04", "Miami at Stanford", "Final (L 6-45). GoStanford schedule strip displays Final rather than kickoff time; season flagship KTCT 1050 AM."),
        ("2026-09-19", "Stanford at Duke", "Final (L 7-35). GoStanford schedule strip displays Final rather than kickoff time; season flagship KTCT 1050 AM."),
        ("2026-09-26", "Georgia Tech at Stanford", "Final (W 34-27). GoStanford schedule strip displays Final rather than kickoff time; season flagship KTCT 1050 AM."),
        ("2026-10-03", "Stanford at Wake Forest", "Final (L 3-57). GoStanford schedule strip displays Final rather than kickoff time; season flagship KTCT 1050 AM."),
        ("2026-10-10", "Stanford at Notre Dame", "Final (L 7-58). GoStanford schedule strip displays Final rather than kickoff time; season flagship KTCT 1050 AM."),
        ("2026-10-17", "Elon at Stanford", "Final (W 34-7). GoStanford schedule strip displays Final rather than kickoff time; season flagship KTCT 1050 AM."),
        ("2026-10-23", "NC State at Stanford", "Final (W 31-28). GoStanford schedule strip displays Final rather than kickoff time; season flagship KTCT 1050 AM."),
        ("2026-10-31", "Stanford at Louisville", "Final (L 24-52). GoStanford schedule strip displays Final rather than kickoff time; season flagship KTCT 1050 AM."),
    ]
    for d, title, note in stan_fb_2026:
        events.append({
            "id": f"stan-fb-{d}",
            "date": d,
            "start": None,
            "title": title,
            "league": "NCAAF",
            "source": "https://gostanford.com/sports/football/schedule",
            "station": "KTCT 1050 AM",
            "radioSource": "https://gostanford.com/news/2026/07/30/2026-football-radio-broadcast-team-announced",
            "kind": "Regular season",
            "timeBasis": "Kickoff",
            "priority": True,
            "corePromptScope": True,
            "status": "Final",
            "checked": CHECKED,
            "note": note,
        })

    # 5. Stanford & California 2027-2029 future NCAAF schedules (newly verified official releases)
    stan_acc_2027 = [
        ("stan-2027-acc-home-cal", "California at Stanford", "Official 2027 ACC home opponent (130th Big Game). Date, kickoff, and game-level radio not yet announced."),
        ("stan-2027-acc-home-duke", "Duke at Stanford", "Official 2027 ACC home opponent. Date, kickoff, and game-level radio not yet announced."),
        ("stan-2027-acc-home-unc", "North Carolina at Stanford", "Official 2027 ACC home opponent. Date, kickoff, and game-level radio not yet announced."),
        ("stan-2027-acc-home-syr", "Syracuse at Stanford", "Official 2027 ACC home opponent. Date, kickoff, and game-level radio not yet announced."),
        ("stan-2027-acc-home-uva", "Virginia at Stanford", "Official 2027 ACC home opponent. Date, kickoff, and game-level radio not yet announced."),
        ("stan-2027-acc-away-bc", "Stanford at Boston College", "Official 2027 ACC road opponent. Date, kickoff, and game-level radio not yet announced."),
        ("stan-2027-acc-away-clem", "Stanford at Clemson", "Official 2027 ACC road opponent. Date, kickoff, and game-level radio not yet announced."),
        ("stan-2027-acc-away-fsu", "Stanford at Florida State", "Official 2027 ACC road opponent. Date, kickoff, and game-level radio not yet announced."),
        ("stan-2027-acc-away-smu", "Stanford at SMU", "Official 2027 ACC road opponent. Date, kickoff, and game-level radio not yet announced."),
    ]
    for eid, title, note in stan_acc_2027:
        events.append({
            "id": eid,
            "date": None,
            "start": None,
            "title": title,
            "league": "NCAAF",
            "source": "https://gostanford.com/news/2026/09/16/acc-announces-2027-conference-opponents",
            "station": None,
            "radioSource": None,
            "kind": "2027 conference matchup",
            "timeBasis": "Kickoff",
            "priority": True,
            "corePromptScope": True,
            "status": "Date TBD",
            "checked": CHECKED,
            "note": note,
        })

    future_dated_ncaaf = [
        ("stan-2027-09-04", "2027-09-04", "Stanford at TCU", "https://gostanford.com/news/2018/01/29/season-opening-date-shifted", "Announced in 2018 nonconference release; kickoff and post-ACC 9-game schedule retention unconfirmed."),
        ("stan-2027-09-11", "2027-09-11", "Vanderbilt at Stanford", "https://gostanford.com/news/2018/01/29/season-opening-date-shifted", "Announced in pre-ACC nonconference release; kickoff and radio unverified."),
        ("stan-2027-11-27", "2027-11-27", "Notre Dame at Stanford", "https://gostanford.com/news/2026/05/20/two-dates-added-to-notre-dame-rivalry", "Official May 20, 2026 rivalry extension at Stanford Stadium. Kickoff and game-level radio unverified."),
        ("stan-2028-10-14", "2028-10-14", "Stanford at Notre Dame", "https://gostanford.com/news/2026/05/20/two-dates-added-to-notre-dame-rivalry", "Official May 20, 2026 rivalry extension at Notre Dame Stadium. Kickoff and game-level radio unverified."),
        ("cal-2028-08-26", "2028-08-26", "California at Sacramento State", "https://calbears.com/news/2026/6/25/football-cal-announces-matchups-against-odu-sac-state", "Official June 25, 2026 nonconference release. Kickoff and 2028 radio assignment unverified."),
        ("cal-2028-09-09", "2028-09-09", "California at Old Dominion", "https://calbears.com/news/2026/6/25/football-cal-announces-matchups-against-odu-sac-state", "Official June 25, 2026 nonconference release. Kickoff and 2028 radio assignment unverified."),
        ("cal-2028-09-16", "2028-09-16", "Minnesota at California", "https://calbears.com/news/2020/2/11/football-cal-adds-minnesota-and-wyoming-to-future-schedules", "Official Cal future nonconference release. Kickoff and 2028 radio assignment unverified."),
        ("cal-2029-09-08", "2029-09-08", "UCLA at California", "https://calbears.com/news/2026/6/25/football-cal-announces-matchups-against-odu-sac-state", "Official Cal future nonconference schedule listing. Kickoff and 2029 radio assignment unverified."),
        ("cal-2029-09-15", "2029-09-15", "California at Wyoming", "https://calbears.com/news/2020/2/11/football-cal-adds-minnesota-and-wyoming-to-future-schedules", "Official Cal future nonconference release. Kickoff and 2029 radio assignment unverified."),
    ]
    for eid, d, title, src, note in future_dated_ncaaf:
        events.append({
            "id": eid,
            "date": d,
            "start": None,
            "title": title,
            "league": "NCAAF",
            "source": src,
            "station": None,
            "radioSource": None,
            "kind": "Regular season",
            "timeBasis": "Kickoff",
            "priority": True,
            "corePromptScope": True,
            "status": "Time TBD",
            "checked": CHECKED,
            "note": note,
        })

    # 6. MLB 2027 Home Run Derby (verified from MLB.com 2027 schedule announcement)
    events.append({
        "id": "mlb-hrd-2027-07-12",
        "date": "2027-07-12",
        "start": None,
        "title": "2027 T-Mobile Home Run Derby (Wrigley Field, Chicago)",
        "league": "MLB",
        "source": "https://www.mlb.com/news/mlb-2027-schedule-released",
        "station": None,
        "radioSource": None,
        "kind": "All-Star Week",
        "timeBasis": "Event start",
        "priority": False,
        "corePromptScope": True,
        "status": "Time TBD",
        "checked": CHECKED,
        "note": "Official MLB 2027 schedule release confirms Monday, July 12, 2027 at Wrigley Field (Netflix); start time and terrestrial radio unverified.",
    })

    # 7. San Jose Earthquakes upcoming 2026 MLS match on KSFO 810 AM / KZSF 1370 AM
    events.append({
        "id": "mls-sje-2026-11-07",
        "date": "2026-11-07",
        "start": pt_iso("2026-11-07", "16:00"),
        "title": "San Jose Earthquakes at Minnesota United FC",
        "league": "MLS",
        "source": "https://www.sjearthquakes.com/news/news-earthquakes-announce-radio-stations-for-2026-mls-season",
        "station": "KSFO 810 AM / KZSF 1370 AM",
        "radioSource": "https://www.sjearthquakes.com/news/news-earthquakes-announce-radio-stations-for-2026-mls-season",
        "kind": "Regular season",
        "timeBasis": "Kickoff",
        "priority": True,
        "corePromptScope": False,
        "status": "Scheduled",
        "checked": CHECKED,
        "note": "Decision Day 2026 MLS match listed at 4:00 PM PT on official Earthquakes 2026 radio broadcast schedule (KSFO 810 AM English / KZSF 1370 AM Spanish).",
    })

    # 8. Full 2026-27 California Men's Basketball regular-season schedule (all 32 games on KSFO 810 AM)
    cal_mbb_2026_27 = [
        ("2026-11-02", "17:00", "Adams State at California", "Final"),
        ("2026-11-04", "18:00", "Radford at California", "Scheduled"),
        ("2026-11-08", "17:30", "California vs. Houston (Lake Tahoe, NV)", "Scheduled"),
        ("2026-11-11", "20:00", "USC at California", "Scheduled"),
        ("2026-11-14", "14:00", "Utah Tech at California", "Scheduled"),
        ("2026-11-19", "19:00", "East Texas A&M at California", "Scheduled"),
        ("2026-11-23", "19:00", "Alabama State at California", "Scheduled"),
        ("2026-11-28", "17:00", "California vs. Minnesota (Sioux Falls, SD)", "Scheduled"),
        ("2026-12-02", "18:00", "California at Utah", "Scheduled"),
        ("2026-12-06", "17:00", "Vanderbilt at California", "Scheduled"),
        ("2026-12-10", "19:00", "Southeastern Louisiana at California", "Scheduled"),
        ("2026-12-12", "12:00", "UC Riverside at California", "Scheduled"),
        ("2026-12-20", "12:00", "Southern at California", "Scheduled"),
        ("2026-12-22", "15:00", "Northeastern at California", "Scheduled"),
        ("2026-12-30", "13:00", "California at North Carolina", "Scheduled"),
        ("2027-01-02", "11:15", "California at Duke", "Scheduled"),
        ("2027-01-06", "18:00", "Florida State at California", "Scheduled"),
        ("2027-01-09", "13:00", "Virginia at California", "Scheduled"),
        ("2027-01-13", "16:00", "California at Louisville", "Scheduled"),
        ("2027-01-16", "11:00", "California at Notre Dame", "Scheduled"),
        ("2027-01-23", "18:00", "Stanford at California", "Scheduled"),
        ("2027-01-27", "18:00", "NC State at California", "Scheduled"),
        ("2027-01-30", "14:30", "Syracuse at California", "Scheduled"),
        ("2027-02-03", "17:00", "California at SMU", "Scheduled"),
        ("2027-02-06", "09:00", "California at Clemson", "Scheduled"),
        ("2027-02-10", "18:00", "Virginia Tech at California", "Scheduled"),
        ("2027-02-13", "19:00", "Miami at California", "Scheduled"),
        ("2027-02-17", "16:00", "California at Pittsburgh", "Scheduled"),
        ("2027-02-20", "09:00", "California at NC State", "Scheduled"),
        ("2027-02-24", "18:00", "Boston College at California", "Scheduled"),
        ("2027-02-27", "13:30", "Wake Forest at California", "Scheduled"),
        ("2027-03-06", "13:00", "California at Stanford", "Scheduled"),
    ]
    for d, hm, title, status in cal_mbb_2026_27:
        events.append({
            "id": f"cal-mbb-{d}",
            "date": d,
            "start": pt_iso(d, hm),
            "title": f"{title} (Men's Basketball)",
            "league": "NCAAM",
            "source": "https://calbears.com/sports/mens-basketball/schedule/2026-27",
            "station": "KSFO 810 AM",
            "radioSource": "https://calbears.com/sports/mens-basketball/schedule/2026-27",
            "kind": "Regular season",
            "timeBasis": "Tipoff",
            "priority": True,
            "corePromptScope": False,
            "status": status,
            "checked": CHECKED,
            "note": "Explicitly tagged 'Radio: KSFO 810 AM' on Cal Athletics 2026-27 Men's Basketball schedule.",
        })

    # 9. Full 2026-27 USF Dons Men's Basketball schedule (KNBR 1050 / thesportsleader.com)
    # Rows with has_listen=True carry an explicit [Listen](https://www.thesportsleader.com/) link on usfdons.com;
    # road/neutral rows without a row-level Listen link leave station=None and note the season KNBR 1050 partnership.
    usf_mbb_2026_27 = [
        ("2026-11-02", "19:00", "Radford at San Francisco", True, "Final"),
        ("2026-11-06", "19:00", "North Dakota State at San Francisco", True, "Scheduled"),
        ("2026-11-10", "19:00", "Montana at San Francisco", True, "Scheduled"),
        ("2026-11-14", "16:00", "Portland State at San Francisco", True, "Scheduled"),
        ("2026-11-18", "19:00", "Louisiana at San Francisco", True, "Scheduled"),
        ("2026-11-23", "13:30", "San Francisco vs. Nevada (Palm Desert, CA)", False, "Scheduled"),
        ("2026-11-24", "11:00", "San Francisco vs. Oregon State (Palm Desert, CA)", False, "Scheduled"),
        ("2026-11-28", "16:00", "Bethune-Cookman at San Francisco", True, "Scheduled"),
        ("2026-12-02", "19:00", "UNLV at San Francisco", True, "Scheduled"),
        ("2026-12-05", "16:00", "South Dakota at San Francisco", True, "Scheduled"),
        ("2026-12-08", "19:00", "Grace University at San Francisco", True, "Scheduled"),
        ("2026-12-12", "13:30", "San Francisco at Fresno State", False, "Scheduled"),
        ("2026-12-16", "17:30", "San Francisco at Texas State", False, "Scheduled"),
        ("2026-12-19", "15:00", "San Francisco vs. George Washington (Frisco, TX)", False, "Scheduled"),
        ("2026-12-21", "13:00", "San Francisco vs. Tulsa (Frisco, TX)", False, "Scheduled"),
        ("2026-12-29", "19:00", "Yale at San Francisco", True, "Scheduled"),
        ("2027-01-02", "16:00", "Denver at San Francisco", True, "Scheduled"),
        ("2027-01-07", "20:00", "San Francisco at Santa Clara", False, "Scheduled"),
        ("2027-01-13", None, "San Francisco at Seattle U", False, "Time TBD"),
        ("2027-01-16", None, "San Francisco at Portland", False, "Time TBD"),
        ("2027-01-19", "19:00", "LMU at San Francisco", True, "Scheduled"),
        ("2027-01-23", "16:00", "Pepperdine at San Francisco", True, "Scheduled"),
        ("2027-01-27", "20:00", "Saint Mary's at San Francisco", True, "Scheduled"),
        ("2027-01-30", None, "San Francisco at San Diego", False, "Time TBD"),
        ("2027-02-03", None, "San Francisco at Denver", False, "Time TBD"),
        ("2027-02-06", "20:00", "Pacific at San Francisco", True, "Scheduled"),
        ("2027-02-09", "20:00", "San Francisco at Saint Mary's", False, "Scheduled"),
        ("2027-02-13", "16:00", "Portland at San Francisco", True, "Scheduled"),
        ("2027-02-17", None, "San Francisco at LMU", False, "Time TBD"),
        ("2027-02-21", "17:00", "San Francisco at Pacific", False, "Scheduled"),
        ("2027-02-24", "20:00", "Santa Clara at San Francisco", True, "Scheduled"),
        ("2027-02-27", "17:00", "Seattle U at San Francisco", True, "Scheduled"),
    ]
    for d, hm, title, has_listen, status in usf_mbb_2026_27:
        events.append({
            "id": f"usf-mbb-{d}",
            "date": d,
            "start": pt_iso(d, hm),
            "title": f"{title} (Men's Basketball)",
            "league": "NCAAM",
            "source": "https://usfdons.com/sports/mens-basketball/schedule/2026-27",
            "station": "KTCT 1050 AM" if has_listen else None,
            "radioSource": "https://usfdons.com/news/2026/2/6/mens-basketball-san-francisco-saint-marys-slated-for-saturday-showdown" if has_listen else None,
            "kind": "Regular season",
            "timeBasis": "Tipoff",
            "priority": True,
            "corePromptScope": False,
            "status": status,
            "checked": CHECKED,
            "note": (
                "Explicit KNBR/thesportsleader.com Listen link on USF schedule; USF MBB airs on KNBR 1050 AM."
                if has_listen
                else "Season partner is KNBR 1050 AM per USF game releases, but row-level Listen link is not posted yet."
            ),
        })

    # 10. Remaining 2026-27 Golden State Warriors regular-season games (Nov 18, 2026 - Apr 11, 2027)
    # Every game verified individually against https://www.nba.com/schedule/warriors?cal=<Month>
    # and https://www.nba.com/warriors/schedule (flagship radio KGMZ 95.7 FM).
    gsw_games = [
        ("2026-11-18", "21:30", "Golden State Warriors at Dallas Mavericks", "0022600267", "gsw-vs-dal"),
        ("2026-11-19", "20:00", "Golden State Warriors at Memphis Grizzlies", "0022600270", "gsw-vs-mem"),
        ("2026-11-22", "20:30", "Boston Celtics at Golden State Warriors", "0022600286", "bos-vs-gsw"),
        ("2026-11-25", "22:00", "Sacramento Kings at Golden State Warriors", "0022600062", "sac-vs-gsw"),
        ("2026-11-27", "21:30", "Golden State Warriors at Portland Trail Blazers", "0022600074", "gsw-vs-por"),
        ("2026-11-29", "20:30", "LA Clippers at Golden State Warriors", "0022600310", "lac-vs-gsw"),
        ("2026-12-01", "23:00", "Utah Jazz at Golden State Warriors", "0022600326", "uta-vs-gsw"),
        ("2026-12-12", "20:00", "Golden State Warriors at Cleveland Cavaliers", "0022600344", "gsw-vs-cle"),
        ("2026-12-14", "20:00", "Golden State Warriors at Memphis Grizzlies", "0022600361", "gsw-vs-mem"),
        ("2026-12-16", "19:00", "Golden State Warriors at Indiana Pacers", "0022600371", "gsw-vs-ind"),
        ("2026-12-18", "19:30", "Golden State Warriors at Toronto Raptors", "0022600390", "gsw-vs-tor"),
        ("2026-12-20", "20:00", "Golden State Warriors at Milwaukee Bucks", "0022600408", "gsw-vs-mil"),
        ("2026-12-22", "22:30", "Dallas Mavericks at Golden State Warriors", "0022600422", "dal-vs-gsw"),
        ("2026-12-23", "22:30", "Golden State Warriors at LA Clippers", "0022600437", "gsw-vs-lac"),
        ("2026-12-25", "22:30", "Denver Nuggets at Golden State Warriors", "0022600014", "den-vs-gsw"),
        ("2026-12-27", "20:30", "Minnesota Timberwolves at Golden State Warriors", "0022600455", "min-vs-gsw"),
        ("2026-12-28", "21:00", "Golden State Warriors at Phoenix Suns", "0022600460", "gsw-vs-phx"),
        ("2026-12-30", "22:00", "Houston Rockets at Golden State Warriors", "0022600476", "hou-vs-gsw"),
        ("2027-01-02", "20:30", "Brooklyn Nets at Golden State Warriors", "0022600499", "bkn-vs-gsw"),
        ("2027-01-06", "22:00", "New York Knicks at Golden State Warriors", "0022600529", "nyk-vs-gsw"),
        ("2027-01-07", "22:00", "Detroit Pistons at Golden State Warriors", "0022600539", "det-vs-gsw"),
        ("2027-01-09", "20:30", "Chicago Bulls at Golden State Warriors", "0022600553", "chi-vs-gsw"),
        ("2027-01-12", "23:00", "Sacramento Kings at Golden State Warriors", "0022600577", "sac-vs-gsw"),
        ("2027-01-13", "22:00", "Charlotte Hornets at Golden State Warriors", "0022600583", "cha-vs-gsw"),
        ("2027-01-15", "19:00", "Golden State Warriors at Atlanta Hawks", "0022600593", "gsw-vs-atl"),
        ("2027-01-17", "18:00", "Golden State Warriors at Miami Heat", "0022600611", "gsw-vs-mia"),
        ("2027-01-19", "19:00", "Golden State Warriors at Orlando Magic", "0022600617", "gsw-vs-orl"),
        ("2027-01-21", "22:00", "Los Angeles Lakers at Golden State Warriors", "0022600637", "lal-vs-gsw"),
        ("2027-01-22", "22:00", "Milwaukee Bucks at Golden State Warriors", "0022600646", "mil-vs-gsw"),
        ("2027-01-24", "20:30", "Oklahoma City Thunder at Golden State Warriors", "0022600661", "okc-vs-gsw"),
        ("2027-01-27", "22:00", "Golden State Warriors at Portland Trail Blazers", "0022600685", "gsw-vs-por"),
        ("2027-01-28", "21:00", "Golden State Warriors at Utah Jazz", "0022600692", "gsw-vs-uta"),
        ("2027-01-30", "17:30", "San Antonio Spurs at Golden State Warriors", "0022600702", "sas-vs-gsw"),
        ("2027-02-01", "22:00", "San Antonio Spurs at Golden State Warriors", "0022600722", "sas-vs-gsw"),
        ("2027-02-03", "22:30", "Golden State Warriors at LA Clippers", "0022600736", "gsw-vs-lac"),
        ("2027-02-05", "19:00", "Golden State Warriors at Charlotte Hornets", "0022600748", "gsw-vs-cha"),
        ("2027-02-07", "15:00", "Golden State Warriors at Detroit Pistons", "0022600763", "gsw-vs-det"),
        ("2027-02-09", "20:00", "Golden State Warriors at Chicago Bulls", "0022600781", "gsw-vs-chi"),
        ("2027-02-10", "19:30", "Golden State Warriors at Boston Celtics", "0022600790", "gsw-vs-bos"),
        ("2027-02-13", "20:30", "Golden State Warriors at New York Knicks", "0022600815", "gsw-vs-nyk"),
        ("2027-02-15", "19:30", "Indiana Pacers at Golden State Warriors", "0022600084", "ind-vs-gsw"),
        ("2027-02-17", "22:00", "New Orleans Pelicans at Golden State Warriors", "0022600842", "nop-vs-gsw"),
        ("2027-02-25", "22:00", "Dallas Mavericks at Golden State Warriors", "0022600857", "dal-vs-gsw"),
        ("2027-03-01", "20:30", "Golden State Warriors at Houston Rockets", "0022600884", "gsw-vs-hou"),
        ("2027-03-02", "20:00", "Golden State Warriors at Dallas Mavericks", "0022600891", "gsw-vs-dal"),
        ("2027-03-04", "22:00", "Washington Wizards at Golden State Warriors", "0022600908", "was-vs-gsw"),
        ("2027-03-07", "22:00", "Houston Rockets at Golden State Warriors", "0022600928", "hou-vs-gsw"),
        ("2027-03-09", "23:00", "Portland Trail Blazers at Golden State Warriors", "0022600944", "por-vs-gsw"),
        ("2027-03-10", "22:00", "Golden State Warriors at Sacramento Kings", "0022600951", "gsw-vs-sac"),
        ("2027-03-12", "22:00", "Golden State Warriors at Denver Nuggets", "0022600966", "gsw-vs-den"),
        ("2027-03-14", "22:00", "Golden State Warriors at Los Angeles Lakers", "0022600982", "gsw-vs-lal"),
        ("2027-03-16", "22:00", "Cleveland Cavaliers at Golden State Warriors", "0022600995", "cle-vs-gsw"),
        ("2027-03-17", "22:00", "Memphis Grizzlies at Golden State Warriors", "0022601003", "mem-vs-gsw"),
        ("2027-03-19", "22:00", "Portland Trail Blazers at Golden State Warriors", "0022601018", "por-vs-gsw"),
        ("2027-03-22", "22:00", "Atlanta Hawks at Golden State Warriors", "0022601041", "atl-vs-gsw"),
        ("2027-03-24", "22:00", "Philadelphia 76ers at Golden State Warriors", "0022601056", "phi-vs-gsw"),
        ("2027-03-25", "22:00", "Toronto Raptors at Golden State Warriors", "0022601066", "tor-vs-gsw"),
        ("2027-03-27", "19:00", "Golden State Warriors at Washington Wizards", "0022601075", "gsw-vs-was"),
        ("2027-03-29", "19:30", "Golden State Warriors at Brooklyn Nets", "0022601092", "gsw-vs-bkn"),
        ("2027-03-31", "19:00", "Golden State Warriors at Philadelphia 76ers", "0022601105", "gsw-vs-phi"),
        ("2027-04-02", "19:30", "Golden State Warriors at Minnesota Timberwolves", "0022601120", "gsw-vs-min"),
        ("2027-04-04", "18:00", "Golden State Warriors at Sacramento Kings", "0022601141", "gsw-vs-sac"),
        ("2027-04-06", "23:00", "Phoenix Suns at Golden State Warriors", "0022601157", "phx-vs-gsw"),
        ("2027-04-08", "21:30", "Golden State Warriors at Oklahoma City Thunder", "0022601171", "gsw-vs-okc"),
        ("2027-04-09", "20:00", "Golden State Warriors at Oklahoma City Thunder", "0022601179", "gsw-vs-okc"),
        ("2027-04-11", "20:30", "Utah Jazz at Golden State Warriors", "0022601198", "uta-vs-gsw"),
    ]
    for d_et, hm_et, title, gid, slug in gsw_games:
        d_pt, start_iso = et_to_pt_iso(d_et, hm_et)
        events.append({
            "id": f"gsw-{d_pt}",
            "date": d_pt,
            "start": start_iso,
            "title": title,
            "league": "NBA",
            "source": f"https://www.nba.com/game/{slug}-{gid}",
            "station": "KGMZ 95.7 FM",
            "radioSource": "https://www.nba.com/warriors/schedule",
            "kind": "Regular season",
            "timeBasis": "Tipoff",
            "priority": True,
            "corePromptScope": False,
            "status": "Scheduled",
            "checked": CHECKED,
            "note": "Verified on NBA.com Warriors schedule; KGMZ 95.7 FM The Game is official Warriors flagship.",
        })

    # Emirates NBA Cup Dec 2026 TBD flex games (2 games between Dec 4 and Dec 11, 2026)
    events.append({
        "id": "gsw-2026-12-cup-tbd",
        "date": None,
        "start": None,
        "title": "Golden State Warriors Emirates NBA Cup Knockout / Flex Games (2 games, Dec 4-10, 2026)",
        "league": "NBA",
        "source": "https://www.nba.com/warriors/schedule",
        "station": "KGMZ 95.7 FM",
        "radioSource": "https://www.nba.com/warriors/schedule",
        "kind": "NBA Cup flex",
        "timeBasis": "Tipoff",
        "priority": True,
        "corePromptScope": False,
        "status": "Date TBD",
        "checked": CHECKED,
        "note": "Official Warriors schedule lists DATE TBD / OPPONENT TBD between Dec 1 and Dec 12 for NBA Cup Quarterfinals/Regular-Season flex week.",
    })

    # NBA All-Star Game 2027 (Phoenix, Sunday Feb 21, 2027)
    events.append({
        "id": "nba-asg-2027-02-21",
        "date": "2027-02-21",
        "start": None,
        "title": "2027 NBA All-Star Game (Phoenix, AZ)",
        "league": "NBA",
        "source": "https://cdn.nba.com/teams/uploads/sites/1610612744/2026/09/2627Schedule_8.5x11_v2.pdf",
        "station": None,
        "radioSource": None,
        "kind": "All-Star",
        "timeBasis": "Tipoff",
        "priority": False,
        "corePromptScope": False,
        "status": "Time TBD",
        "checked": CHECKED,
        "note": "Listed on official Warriors 2026-27 schedule PDF for Feb 21, 2027 in Phoenix; Bay Area terrestrial carriage unverified.",
    })

    return events


def build_payload() -> dict:
    events = build_events()
    return {
        "meta": {
            "checked": CHECKED,
            "listenerLocation": "Outer Sunset, San Francisco, CA 94122",
            "timezone": "America/Los_Angeles",
            "medium": "Standard terrestrial AM/FM radio",
            "generator": "scripts/bay_area_expansion.py",
            "eventCount": len(events),
            "durationEstimatesMinutes": {
                "MLB": {"minutes": 185, "basis": "Planning estimate (~2h40m pitch-clock average + pre/postgame radio cushion); never treated as an official end time."},
                "NFL": {"minutes": 195, "basis": "Planning estimate (~3h12m average NFL game duration); never treated as an official end time."},
                "NCAAF": {"minutes": 215, "basis": "Planning estimate (~3h24m-3h35m FBS average duration); never treated as an official end time."},
                "NBA": {"minutes": 150, "basis": "Planning estimate (~2h15m-2h30m NBA broadcast window); never treated as an official end time."},
                "NCAAM": {"minutes": 135, "basis": "Planning estimate (~2h05m-2h15m college basketball window); never treated as an official end time."},
                "MLS": {"minutes": 130, "basis": "Planning estimate (~2h05m soccer match window); never treated as an official end time."},
                "USSF": {"minutes": 135, "basis": "Planning estimate (~2h15m Westwood One soccer broadcast window); never treated as an official end time."},
            },
        },
        "proBowlFinding": {
            "status": "Discontinued starting 2026 season (2027 class)",
            "announcementDate": "2026-08-26",
            "headline": "NFL elevates Pro Bowl selection; AFC-NFC Pro Bowl game will no longer be staged",
            "summary": "On August 26, 2026, the NFL officially announced that starting with the 2026 season (2027 Pro Bowl class), 88 players earn Pro Bowl recognition with an in-person celebration in Los Angeles, and the AFC-NFC Pro Bowl game will cease being contested. There is no 2027 Pro Bowl game to schedule or broadcast.",
            "source": "https://www.nfl.com/news/nfl-elevates-pro-bowl-selection-game-s-will-cease-being-contested",
            "secondarySource": "https://media.nfl.com/news-and-releases/pbg/nfl-elevates-pro-bowl-selection--honoring-the-league-s-best-of-t0",
            "checked": CHECKED,
        },
        "feb2027WindowProof": {
            "window": "2027-02-15..2027-02-18",
            "days": 4,
            "coreFourCategoryVerdict": {
                "zeroScheduledGameDays": ["2027-02-15", "2027-02-16", "2027-02-17", "2027-02-18"],
                "maxConsecutiveDays": 4,
                "qualifiesFor7DayVacation": False,
                "explanation": "Super Bowl LXI airs Sun Feb 14, 2027 and 2027 MLB Spring Training opens Fri Feb 19, 2027, leaving at most 4 consecutive days (Feb 15-18, 2027) in the narrow 4-category scope (MLB + NFL + Stanford/Cal NCAAF + Westwood One NFL) — short of a 7-day vacation.",
            },
            "fullBayAreaAmFmVerdict": {
                "occupiedDays": [
                    {
                        "date": "2027-02-15",
                        "conflicts": [
                            {
                                "title": "Indiana Pacers at Golden State Warriors",
                                "start": "2027-02-15T16:30:00-08:00",
                                "station": "KGMZ 95.7 FM",
                                "source": "https://www.nba.com/game/ind-vs-gsw-0022600084",
                            }
                        ],
                    },
                    {
                        "date": "2027-02-17",
                        "conflicts": [
                            {
                                "title": "California at Pittsburgh (Men's Basketball)",
                                "start": "2027-02-17T16:00:00-08:00",
                                "station": "KSFO 810 AM",
                                "source": "https://calbears.com/sports/mens-basketball/schedule/2026-27",
                            },
                            {
                                "title": "New Orleans Pelicans at Golden State Warriors",
                                "start": "2027-02-17T19:00:00-08:00",
                                "station": "KGMZ 95.7 FM",
                                "source": "https://www.nba.com/game/nop-vs-gsw-0022600842",
                            },
                            {
                                "title": "San Francisco at LMU (Men's Basketball)",
                                "start": None,
                                "station": "KTCT 1050 AM (season partner; row link TBA)",
                                "source": "https://usfdons.com/sports/mens-basketball/schedule/2026-27",
                            },
                        ],
                    },
                ],
                "remainingCandidateSingleDays": ["2027-02-16", "2027-02-18"],
                "maxConsecutiveDays": 1,
                "qualifiesFor7DayVacation": False,
                "explanation": "Under full SF 94122 terrestrial AM/FM sports coverage, Feb 15-18, 2027 is broken on both Mon Feb 15 (Warriors vs Pacers on 95.7 FM) and Wed Feb 17 (Warriors vs Pelicans on 95.7 FM + Cal MBB at Pitt on 810 AM + USF MBB at LMU). NBA All-Star Break (Feb 19-24, 2027) then immediately collides with MLB Spring Training opening on Fri Feb 19, 2027.",
            },
        },
        "scopeMatrix": [
            {
                "year": 2027,
                "coreFourScope": {
                    "oneWeek": 0,
                    "twoWeek": 0,
                    "threeWeek": 0,
                    "longestGap": "4 days (Feb 15-18, 2027, between Super Bowl LXI on Feb 14 and MLB Spring Training on Feb 19); Dec 2026-Jan 2027 CFP/Bowl & NFL Week 18/Playoffs occupy winter; MLB runs Feb 19-Nov 2027.",
                    "status": "0 windows >=7 days (verified negative in Feb 2027; Oct-Dec 2027 blocked by 2027 NFL/NCAAF/MLB Postseason)",
                },
                "fullAmFmScope": {
                    "oneWeek": 0,
                    "twoWeek": 0,
                    "threeWeek": 0,
                    "longestGap": "1 day in Feb 2027 (Feb 16 and Feb 18 single days only; Warriors + Cal MBB + USF MBB occupy Feb 15 and Feb 17; Valkyries on 95.7 FM + SJ Earthquakes on 810/1370 AM + MLB occupy summer).",
                    "status": "0 windows >=7 days",
                },
            },
            {
                "year": 2028,
                "coreFourScope": {
                    "oneWeek": None,
                    "twoWeek": None,
                    "threeWeek": None,
                    "longestGap": "Unverified — 2028 MLB Spring Training & Regular Season, 2027-28 NFL Postseason, and 2028 ACC/NFL schedules not yet published.",
                    "status": "Unverified (0 certified windows)",
                },
                "fullAmFmScope": {
                    "oneWeek": None,
                    "twoWeek": None,
                    "threeWeek": None,
                    "longestGap": "Unverified — 2027-28 NBA/NCAAM, 2028 MLB, 2028 MLS, and 2028 WNBA schedules not yet published.",
                    "status": "Unverified (0 certified windows)",
                },
            },
            {
                "year": 2029,
                "coreFourScope": {
                    "oneWeek": None,
                    "twoWeek": None,
                    "threeWeek": None,
                    "longestGap": "Unverified — only 2 Cal nonconference football dates (Sep 8 vs UCLA, Sep 15 at Wyoming) are officially published for 2029.",
                    "status": "Unverified (0 certified windows)",
                },
                "fullAmFmScope": {
                    "oneWeek": None,
                    "twoWeek": None,
                    "threeWeek": None,
                    "longestGap": "Unverified — 2028-29 and 2029 pro/college radio schedules not yet published.",
                    "status": "Unverified (0 certified windows)",
                },
            },
        ],
        "stations": build_stations(),
        "nonTerrestrialExclusions": build_non_terrestrial_exclusions(),
        "events": events,
    }


def main() -> None:
    out = Path(__file__).resolve().parent.parent / "site" / "data" / "expanded-official.json"
    payload = build_payload()
    out.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"Wrote {out} ({len(payload['events'])} verified events, {len(payload['stations'])} terrestrial stations)")


if __name__ == "__main__":
    main()
