#!/usr/bin/env python3
"""Generate site/data/season-estimates.json — clearly labeled ESTIMATED schedules.

Purpose
-------
The project brief requires vacation analysis for 2027, 2028 and 2029. Official
league schedules exist only for some of those seasons:

  * MLB 2026 + 2027 …… official (statsapi.mlb.com feed; refreshed by scripts/refresh.py)
  * NFL 2026 season …… official (scripts/nfl.py), postseason anchors curated
  * 2028+ ……………… NOT RELEASED by the leagues (see research flags).

Per the brief ("If there are none, then estimate the schedule and make sure to
note that it is an estimation and not a real verified released schedule for that
year"), this script synthesizes **day-level estimated league-wide broadcast
windows** for the seasons that are not yet released, plus a small number of
**verified anchor rows** (Super Bowl LXII/LXIII, 2028 All-Star Game, LA28
Olympic baseball). Every synthesized row is marked:

  * status = "Estimate — not an officially released schedule"
  * timeBasis = "ESTIMATED typical window"
  * estimation = True
  * note explains the basis and the uncertainty.

Verified anchor rows use status "Scheduled"/"Official announcement" and are
linked to the official announcement in `source`. Nothing here is presented as a
released fixture list.

Estimated daily broadcast windows (America/Los_Angeles; PST/PDT applied
per date via zoneinfo):

  MLB spring training   10:00-19:30
  MLB regular season    10:05-22:35
  MLB postseason        12:00-23:00
  NFL Sunday            09:00-23:30   (London games can begin 06:30 PT; see flag)
  NFL Thursday/Monday   17:00-23:30
  NFL Saturday          10:00-23:30
  NCAAF (Stanford/Cal)  09:00-23:30
  Westwood One NFL      17:30-23:30   (Thu/Mon national windows)
  Olympic baseball      10:00-22:00

These windows are conservative planning overlays (league-wide slates can run
earlier and later), never official end times. The generator is deterministic:
same inputs -> same output. Run: python3 scripts/season_estimates.py
"""
from __future__ import annotations

import json
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site" / "data" / "season-estimates.json"
PT = ZoneInfo("America/Los_Angeles")
CHECKED = "2026-11-05"

# ---------------------------------------------------------------------------
# Official anchors (verified on 2026-11-05; see research logs for citations).
# ---------------------------------------------------------------------------
SRC_NFL_DATES = "https://operations.nfl.com/calendar-events/nfl-important-dates"
SRC_SB_LXII = "https://media.nfl.com/news-and-releases/corporate-communications/atlanta-to-host-super-bowl-lxii-in-2028"
SRC_SB_LXIII = "https://www.prnewswire.com/news-releases/super-bowl-returns-to-las-vegas-in-2029-302729218.html"
SRC_MLB_ASG_2028 = "https://www.mlb.com/news/release-mlb-awards-the-2028-all-star-game-presented-by-mastercard-to-the-san-francisco-giants"
SRC_MLB_SCHEDULE = "https://www.mlb.com/schedules"
SRC_MLB_2027 = "https://www.mlb.com/news/mlb-2027-schedule-released"
SRC_NFL_SCHEDULES = "https://www.nfl.com/schedules/"
SRC_OLY = "https://www.nbcolympics.com/news/baseball-2028-los-angeles-olympics"
SRC_WW = "https://www.westwoodonesports.com/nfl-schedule/"
SRC_STANFORD = "https://gostanford.com/sports/football/schedule"
SRC_CAL = "https://calbears.com/sports/football/schedule/2026"

EST_NOTE_MLB = ("Estimated league-wide broadcast window: MLB has not released this "
                "season's schedule. Typical first-pitch-to-last-out span only; "
                "not a released fixture.")
EST_NOTE_NFL = ("Estimated league-wide broadcast window: the NFL has not released this "
                "season's schedule. Typical game-day slate span only; not a released fixture.")
EST_NOTE_NCAAF = ("Estimated Stanford/Cal football game day (dates, opponents and kickoffs "
                  "not yet announced for this season). Some Saturdays are bye weeks.")
EST_NOTE_WW = ("Estimated Westwood One national NFL window (Thursday/Monday night "
               "packages). Specific games and airtimes unverified until Westwood One "
               "publishes the season schedule; Bay Area affiliate carriage unverified.")

WINDOWS = {
    "mlb_st": ("10:00", "19:30"),
    "mlb_rs": ("10:05", "22:35"),
    "mlb_ps": ("12:00", "23:00"),
    "nfl_sun": ("09:00", "23:30"),
    "nfl_wknd": ("10:00", "23:30"),
    "nfl_tnf_mnf": ("17:00", "23:30"),
    "ncaaf": ("09:00", "23:30"),
    "ww": ("17:30", "23:30"),
    "oly": ("10:00", "22:00"),
}


def iso_pair(d: str, window: tuple[str, str]) -> tuple[str, str]:
    start_hm, end_hm = window
    s = datetime.strptime(f"{d} {start_hm}", "%Y-%m-%d %H:%M").replace(tzinfo=PT)
    e = datetime.strptime(f"{d} {end_hm}", "%Y-%m-%d %H:%M").replace(tzinfo=PT)
    return s.isoformat(), e.isoformat()


def daterange(a: str, b: str):
    cur = date.fromisoformat(a)
    end = date.fromisoformat(b)
    while cur <= end:
        yield cur.isoformat()
        cur += timedelta(days=1)


def row(rid, d, window, title, league, kind, source, note, *,
        priority=False, start=None, window_end=None, status=None,
        time_basis=None, conditional=False) -> dict:
    if window and start is None:
        start, window_end = iso_pair(d, window)
    return {
        "id": rid,
        "date": d,
        "start": start,
        "windowEnd": window_end,
        "title": title,
        "league": league,
        "kind": kind,
        "priority": priority,
        "source": source,
        "status": status or "Estimate — not an officially released schedule",
        "station": None,
        "radioSource": None,
        "timeBasis": time_basis or "ESTIMATED typical window",
        "checked": CHECKED,
        "note": note,
        "estimation": True,
        **({"conditional": True} if conditional else {}),
    }


def load_existing_ncaaf_dates() -> set[str]:
    """Dates that already carry a verified Stanford/Cal (NCAAF) record."""
    dates: set[str] = set()
    for name in ("expanded-official.json", "curated.json"):
        p = ROOT / "site" / "data" / name
        if not p.exists():
            continue
        data = json.loads(p.read_text())
        rows = data["events"] if isinstance(data, dict) else data
        for r in rows:
            if r.get("league") == "NCAAF" and r.get("date"):
                dates.add(r["date"])
    return dates


def estimate_rows() -> list[dict]:
    rows: list[dict] = []
    have_ncaaf = load_existing_ncaaf_dates()

    # ---- MLB 2027 postseason (regular season official feed ends 2027-09-26) ----
    for d in daterange("2027-09-29", "2027-11-05"):
        rows.append(row(
            f"est-mlb-ps-{d}", d, WINDOWS["mlb_ps"],
            "MLB postseason — estimated league-wide game window",
            "MLB", "Estimated postseason window", SRC_MLB_SCHEDULE,
            "Estimated MLB 2027 postseason window (Wild Card through World Series). "
            "Postseason matchups and times are set only after the regular season. "
            "Bounds derived from the official 2027 season end date (Sep 26) and "
            "recent postseason calendars.",
            priority=True))

    # ---- MLB 2028 season (schedule not released; Olympic-break scenario) ----
    # Spring training estimated to open ~Feb 18-25; used 2027's official Feb 19
    # opener as the anchor plus one day for a Friday-before-weekend style start.
    for d in daterange("2028-02-18", "2028-03-28"):
        rows.append(row(
            f"est-mlb-st-{d}", d, WINDOWS["mlb_st"],
            "MLB spring training — estimated league-wide game window",
            "MLB", "Estimated spring training window", SRC_MLB_SCHEDULE,
            EST_NOTE_MLB + " Spring-training bound estimated from recent seasons "
            "(2027 official opener: Feb 19)."))
    for d in list(daterange("2028-03-29", "2028-07-09")) + list(daterange("2028-07-21", "2028-09-24")):
        rows.append(row(
            f"est-mlb-rs-{d}", d, WINDOWS["mlb_rs"],
            "MLB regular season — estimated league-wide game window",
            "MLB", "Estimated regular-season window", SRC_MLB_SCHEDULE,
            EST_NOTE_MLB))
    for d in daterange("2028-09-28", "2028-11-03"):
        rows.append(row(
            f"est-mlb-ps-{d}", d, WINDOWS["mlb_ps"],
            "MLB postseason — estimated league-wide game window",
            "MLB", "Estimated postseason window", SRC_MLB_SCHEDULE,
            EST_NOTE_MLB, priority=True))

    # 2028 All-Star Week anchors — venue/date announced Aug 14, 2026 (Oracle Park).
    rows.append(row(
        "anchor-mlb-asg2028-derby", "2028-07-10", None,
        "MLB Home Run Derby (All-Star Week, Oracle Park) — date estimated",
        "MLB", "All-Star Week", SRC_MLB_ASG_2028,
        "All-Star Week is awarded to the Giants/Oracle Park (official MLB release, "
        "Aug 14, 2026). Derby is customarily the night before the game; exact date "
        "not yet announced.",
        priority=True, status="Official venue — date estimated"))
    for d, label in (("2028-07-11", "reported Jul 11"), ("2028-07-12", "reported Jul 12")):
        rows.append(row(
            f"anchor-mlb-asg2028-{d}", d, None,
            "MLB All-Star Game (Oracle Park, San Francisco) — date tentative",
            "MLB", "MLB All-Star Game", SRC_MLB_ASG_2028,
            f"Official MLB release awards the 2028 All-Star Game to the Giants at "
            f"Oracle Park (Aug 14, 2026). Game date not finalized in the release; "
            f"press reports give {label}. Both candidate dates are blocked pending "
            f"the official date.",
            priority=True, status="Official venue — date tentative"))

    # LA28 Olympic baseball (announced schedule; MLB participation still pending).
    for d in daterange("2028-07-13", "2028-07-20"):
        rows.append(row(
            f"est-oly-baseball-{d}", d, WINDOWS["oly"],
            "LA28 Olympic baseball (Dodger Stadium) — announced schedule",
            "Olympics", "Olympic baseball (LA28)", SRC_OLY,
            "Olympic baseball at Dodger Stadium is scheduled around Jul 13-20, 2028 "
            "(LA28/WBSC published schedules differ on the exact first/last day). "
            "Whether MLB pauses its season for player participation is NOT decided; "
            "SF terrestrial radio carriage of Olympic baseball is unverified. This "
            "is not an MLB game and is excluded from the core 4-category scope.",
            priority=True, status="Scheduled (LA28 published) — carriage unverified",
            time_basis="Announced session window (times estimated)"))

    # ---- MLB 2029 season (schedule not released) ----
    for d in daterange("2029-02-16", "2029-03-27"):
        rows.append(row(
            f"est-mlb-st-{d}", d, WINDOWS["mlb_st"],
            "MLB spring training — estimated league-wide game window",
            "MLB", "Estimated spring training window", SRC_MLB_SCHEDULE,
            EST_NOTE_MLB))
    for d in list(daterange("2029-03-28", "2029-07-09")) + list(daterange("2029-07-11", "2029-09-23")):
        rows.append(row(
            f"est-mlb-rs-{d}", d, WINDOWS["mlb_rs"],
            "MLB regular season — estimated league-wide game window",
            "MLB", "Estimated regular-season window", SRC_MLB_SCHEDULE,
            EST_NOTE_MLB))
    for d in daterange("2029-09-27", "2029-11-01"):
        rows.append(row(
            f"est-mlb-ps-{d}", d, WINDOWS["mlb_ps"],
            "MLB postseason — estimated league-wide game window",
            "MLB", "Estimated postseason window", SRC_MLB_SCHEDULE,
            EST_NOTE_MLB, priority=True))
    rows.append(row(
        "est-mlb-asg2029-derby", "2029-07-09", None,
        "MLB Home Run Derby (2029 All-Star Week) — date estimated",
        "MLB", "All-Star Week", SRC_MLB_SCHEDULE,
        "No 2029 All-Star host has been announced. Model assumes the customary "
        "mid-July Tuesday pattern; verify when MLB announces.",
        priority=True, status="Estimate — host and date not announced"))
    rows.append(row(
        "est-mlb-asg2029-game", "2029-07-10", None,
        "MLB All-Star Game (2029) — date estimated",
        "MLB", "MLB All-Star Game", SRC_MLB_SCHEDULE,
        "No 2029 All-Star date has been announced. Model assumes the customary "
        "mid-July Tuesday; verify when MLB announces.",
        priority=True, status="Estimate — date not announced"))

    # ---- NFL seasons 2027 / 2028 / 2029 (schedules not released) ----
    # Model: kickoff = Thursday after Labor Day; 18 regular Sundays; Mon/Thu
    # national windows; Saturdays in the final weeks; postseason early January.
    nfl_seasons = [
        # (kickoff Thu, first Sunday, last Sunday (wk18), preseason start, preseason end,
        #  playoff Saturdays, playoff Sundays, conference-championship Sunday, SB row)
        dict(kickoff="2027-09-09", sun1="2027-09-12", sun18="2028-01-09",
             pre_a="2027-08-05", pre_b="2027-08-28",
             sat=("2027-12-25", "2028-01-01", "2028-01-08", "2028-01-15", "2028-01-22", "2028-01-29"),
             playoff_sun=("2028-01-16", "2028-01-23", "2028-01-30")),
        dict(kickoff="2028-09-07", sun1="2028-09-10", sun18="2029-01-07",
             pre_a="2028-08-03", pre_b="2028-08-26",
             sat=("2028-12-23", "2028-12-30", "2029-01-06", "2029-01-13", "2029-01-20", "2029-01-27"),
             playoff_sun=("2029-01-14", "2029-01-21", "2029-01-28")),
        dict(kickoff="2029-09-06", sun1="2029-09-09", sun18="2030-01-06",
             pre_a="2029-08-02", pre_b="2029-08-25",
             sat=("2029-12-22", "2029-12-29"),
             playoff_sun=()),
    ]
    for season in nfl_seasons:
        tag = season["kickoff"][:4]
        for d in daterange(season["pre_a"], season["pre_b"]):
            wd = date.fromisoformat(d).weekday()
            if wd in (3, 5, 6, 0):  # Thu, Sat, Sun, Mon
                rows.append(row(
                    f"est-nfl-pre-{d}", d, WINDOWS["nfl_sun"] if wd in (5, 6) else WINDOWS["nfl_tnf_mnf"],
                    "NFL preseason — estimated game day",
                    "NFL", "Estimated preseason window", SRC_NFL_SCHEDULES,
                    EST_NOTE_NFL, priority=True))
        # Regular Sundays
        for d in daterange(season["sun1"], min(season["sun18"], "2029-12-31")):
            if date.fromisoformat(d).weekday() != 6:
                continue
            rows.append(row(
                f"est-nfl-sun-{d}", d, WINDOWS["nfl_sun"],
                "NFL Sunday — estimated league-wide game slate",
                "NFL", "Estimated regular-season window", SRC_NFL_SCHEDULES,
                EST_NOTE_NFL, priority=True))
        # Thursdays (kickoff + TNF; skip after week 18 Sunday minus 5 days)
        thu_end = (date.fromisoformat(season["sun18"]) - timedelta(days=5)).isoformat()
        for d in daterange(season["kickoff"], min(thu_end, "2029-12-31")):
            if date.fromisoformat(d).weekday() == 3:
                rows.append(row(
                    f"est-nfl-thu-{d}", d, WINDOWS["nfl_tnf_mnf"],
                    "NFL Thursday — estimated national window (TNF/kickoff)",
                    "NFL", "Estimated regular-season window", SRC_NFL_SCHEDULES,
                    EST_NOTE_NFL, priority=True))
        # Mondays (MNF)
        mon_end = (date.fromisoformat(season["sun18"]) - timedelta(days=6)).isoformat()
        for d in daterange(season["sun1"], min(mon_end, "2029-12-31")):
            if date.fromisoformat(d).weekday() == 0:
                rows.append(row(
                    f"est-nfl-mon-{d}", d, WINDOWS["nfl_tnf_mnf"],
                    "NFL Monday — estimated national window (MNF)",
                    "NFL", "Estimated regular-season window", SRC_NFL_SCHEDULES,
                    EST_NOTE_NFL, priority=True))
        for d in season["sat"]:
            if d <= "2029-12-31":
                rows.append(row(
                    f"est-nfl-sat-{d}", d, WINDOWS["nfl_wknd"],
                    "NFL Saturday — estimated game slate (late season / playoffs)",
                    "NFL", "Estimated postseason window", SRC_NFL_SCHEDULES,
                    EST_NOTE_NFL, priority=True))
        for d in season["playoff_sun"]:
            if d <= "2029-12-31":
                rows.append(row(
                    f"est-nfl-po-{d}", d, WINDOWS["nfl_sun"],
                    "NFL playoff Sunday — estimated slate (divisional / conference)",
                    "NFL", "Estimated postseason window", SRC_NFL_SCHEDULES,
                    EST_NOTE_NFL, priority=True))
        # Westwood One estimated national windows (Thu + Mon) during the season.
        for d in daterange(season["kickoff"], min(thu_end, "2029-12-31")):
            if date.fromisoformat(d).weekday() == 3:
                rows.append(row(
                    f"est-ww-thu-{d}", d, WINDOWS["ww"],
                    "Westwood One Thursday Night Football — estimated window",
                    "NFL", "Westwood One (estimated)", SRC_WW, EST_NOTE_WW,
                    priority=True))
        for d in daterange(season["sun1"], min(mon_end, "2029-12-31")):
            if date.fromisoformat(d).weekday() == 0:
                rows.append(row(
                    f"est-ww-mon-{d}", d, WINDOWS["ww"],
                    "Westwood One Monday Night Football — estimated window",
                    "NFL", "Westwood One (estimated)", SRC_WW, EST_NOTE_WW,
                    priority=True))

    # ---- Super Bowl anchors ----
    rows.append(row(
        "anchor-nfl-sb-lxii", "2028-02-13", None,
        "Super Bowl LXII (Mercedes-Benz Stadium, Atlanta)",
        "NFL", "Super Bowl (official date)", SRC_SB_LXII,
        "Host venue officially announced by the NFL Oct 15, 2024 (media.nfl.com "
        "release). The game date Feb 13, 2028 was announced Jul 24, 2026 by the "
        "host stadium (Mercedes-Benz Stadium) and ESPN's Adam Schefter; nfl.com's "
        "Super Bowl table still showed TBA on 2026-11-05 (flag F24). Kickoff time "
        "not set. Westwood One carries the national radio broadcast.",
        priority=True, status="Scheduled (official date)", time_basis="Official date; kickoff TBD"))
    rows.append(row(
        "anchor-nfl-sb-lxiii", "2029-02-11", None,
        "Super Bowl LXIII (Allegiant Stadium, Las Vegas) — date estimated",
        "NFL", "Super Bowl (venue official)", SRC_SB_LXIII,
        "NFL announced Las Vegas/Allegiant Stadium as the host on Mar 30, 2026. "
        "The game date is NOT yet officially set; Feb 11, 2029 follows the "
        "customary second-Sunday-of-February pattern and is an ESTIMATE.",
        priority=True, status="Venue official — date estimated", time_basis="ESTIMATED date; kickoff TBD"))

    # ---- Stanford / Cal football (est Saturdays + conditional bowl window) ----
    for a, b in (("2026-08-29", "2026-11-28"), ("2027-08-28", "2027-11-27"),
                 ("2028-08-26", "2028-11-25"), ("2029-08-25", "2029-11-24")):
        for d in daterange(a, b):
            if date.fromisoformat(d).weekday() != 5 or d in have_ncaaf:
                continue
            rows.append(row(
                f"est-ncaaf-{d}", d, WINDOWS["ncaaf"],
                "Stanford / California football — estimated game day",
                "NCAAF", "Estimated game day", SRC_STANFORD,
                EST_NOTE_NCAAF + " Cal schedule source: " + SRC_CAL,
                priority=True))
    for a, b in (("2026-12-20", "2027-01-02"), ("2027-12-20", "2028-01-02"),
                 ("2028-12-20", "2029-01-02"), ("2029-12-20", "2029-12-31")):
        for d in daterange(a, b):
            rows.append(row(
                f"est-ncaaf-bowl-{d}", d, WINDOWS["ncaaf"],
                "Stanford / California — possible bowl game (conditional)",
                "NCAAF", "Estimated bowl window (conditional)", SRC_STANFORD,
                "Conditional estimate: applies only if Stanford or Cal accepts a bowl "
                "invitation this season. Bowl assignments are decided in early "
                "December; treated as a possible game day for conservative planning.",
                priority=True, conditional=True))

    rows.sort(key=lambda r: (r["date"], r["id"]))
    return rows


def main() -> None:
    rows = estimate_rows()
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids)), "duplicate ids"
    for r in rows:
        date.fromisoformat(r["date"])
        if r["start"]:
            datetime.fromisoformat(r["start"].replace("Z", "+00:00")).tzinfo
        assert r["source"].startswith("https://")
    OUT.write_text(json.dumps(rows, indent=1) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(rows)} rows")


if __name__ == "__main__":
    main()
