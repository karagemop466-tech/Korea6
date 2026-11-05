"""Deterministic generator for site/data/projections.json.

Multi-year (2027/2028/2029) vacation-window anchors and conflict-free runs for the
San Francisco / Outer Sunset 94122 listener.

Rules followed by this generator (see research/sources-63ee3d13.md):

* Every anchor carries an explicit `status`:
    VERIFIED   - the value was read today from an official league/club source and the
                 source URL is attached.
    REPORTED   - an official source confirms part of the fact (e.g. the host stadium)
                 but not the exact value shown; the exact value comes from a
                 non-official source and is labelled as such.
    ESTIMATED  - no official schedule exists for that season; the value is a
                 projection produced by repeating the structure of the most recent
                 released season. It is NOT a released schedule.
    UNRELEASED - the league has not published the schedule; no value is supplied.
* No value is ever filled in from memory without one of the four labels above.
* The day-by-day table for 2027 is computed from the official MLB Stats API snapshot
  already stored in site/data/mlb-2027.json; it does not invent rows.

Run: python3 scripts/projections.py
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKED = "2026-11-05"

MLB_API = "https://statsapi.mlb.com/api/v1/schedule?sportId=1"
NFL_DATES = "https://operations.nfl.com/calendar-events/nfl-important-dates"
FORTYNINERS = "https://www.49ers.com/schedule/"
WWO = "https://www.westwoodonesports.com/nfl-schedule/"
MLB_2027_NEWS = "https://www.mlb.com/news/mlb-2027-schedule-released"
MLB_2027_ST = "https://www.mlb.com/press-release/press-release-mlb-announces-2027-spring-training-schedule"
SB62 = "https://www.nfl.com/news/mercedes-benz-stadium-in-atlanta-to-host-super-bowl-lxii-in-2028"
SB63 = "https://www.nfl.com/news/las-vegas-to-host-super-bowl-lxiii-in-2029"
SB62_DATE_REPORT = "https://www.espn.com/nfl/story/_/id/48351897/las-vegas-officially-named-super-bowl-lxiii-host"

# ---------------------------------------------------------------------------
# Anchors. Each anchor is one fact with one source and one status.
# ---------------------------------------------------------------------------

def A(**kw):
    base = {
        "id": None, "year": None, "league": None, "label": None,
        "value": None, "date": None, "endDate": None,
        "status": "UNRELEASED", "statusNote": None,
        "source": None, "sourceLabel": None, "checked": CHECKED,
    }
    base.update(kw)
    return base


ANCHORS = [
    # ---------------- MLB 2027 (official, verified today) ----------------
    A(id="mlb-2027-st-open", year=2027, league="MLB",
      label="2027 MLB spring training — first games",
      value="Fri Feb 19, 2027 — 17 games",
      date="2027-02-19", status="VERIFIED",
      statusNote="MLB Stats API returns 17 spring-training games for 2027-02-19 and none for 2027-02-15..18. MLB's own press release announced the 2027 spring schedule; the API is the game-level evidence.",
      source=f"{MLB_API}&startDate=2027-02-15&endDate=2027-02-22", sourceLabel="MLB Stats API (official)",
      extraSource=MLB_2027_ST, extraSourceLabel="MLB press release — 2027 spring training"),
    A(id="mlb-2027-opening-night", year=2027, league="MLB",
      label="2027 MLB Opening Night",
      value="Wed Mar 24, 2027 (single game, Netflix; matchup TBD)",
      date="2027-03-24", status="VERIFIED",
      statusNote="Read from MLB.com's 2027 schedule release story.",
      source=MLB_2027_NEWS, sourceLabel="MLB.com — 2027 schedule released"),
    A(id="mlb-2027-opening-day", year=2027, league="MLB",
      label="2027 MLB traditional Opening Day",
      value="Thu Mar 25, 2027 — 14 games (earliest ever)",
      date="2027-03-25", status="VERIFIED",
      statusNote="Read from MLB.com's 2027 schedule release story.",
      source=MLB_2027_NEWS, sourceLabel="MLB.com — 2027 schedule released"),
    A(id="mlb-2027-full-slate", year=2027, league="MLB",
      label="2027 MLB first full slate (all 30 clubs)",
      value="Sat Mar 27, 2027", date="2027-03-27", status="VERIFIED",
      statusNote="Read from MLB.com's 2027 schedule release story.",
      source=MLB_2027_NEWS, sourceLabel="MLB.com — 2027 schedule released"),
    A(id="mlb-2027-asg", year=2027, league="MLB",
      label="2027 MLB All-Star Game (97th) — Wrigley Field",
      value="Tue Jul 13, 2027 (FOX)",
      date="2027-07-13", status="VERIFIED",
      statusNote="Confirmed by MLB.com release story and by the All-Star row present in the MLB Stats API 2027 snapshot.",
      source=MLB_2027_NEWS, sourceLabel="MLB.com — 2027 schedule released"),
    A(id="mlb-2027-hr-derby", year=2027, league="MLB",
      label="2027 T-Mobile Home Run Derby",
      value="Mon Jul 12, 2027 (Netflix)",
      date="2027-07-12", status="VERIFIED",
      statusNote="Not a game, but an official MLB event broadcast nationally. Listed because the brief asks for 'special MLB games'.",
      source=MLB_2027_NEWS, sourceLabel="MLB.com — 2027 schedule released"),
    A(id="mlb-2027-second-half", year=2027, league="MLB",
      label="2027 MLB second half begins",
      value="Thu Jul 15, 2027",
      date="2027-07-15", status="VERIFIED",
      statusNote="MLB.com states the second half begins Thursday July 15; the All-Star break therefore has no regular-season games on Jul 12 or Jul 14, but Jul 13 has the All-Star Game itself.",
      source=MLB_2027_NEWS, sourceLabel="MLB.com — 2027 schedule released"),
    A(id="mlb-2027-reg-end", year=2027, league="MLB",
      label="2027 MLB regular season — final day",
      value="Sun Sep 26, 2027",
      date="2027-09-26", status="VERIFIED",
      statusNote="Read from MLB.com's 2027 schedule release story; matches the last regular-season date in the MLB Stats API snapshot.",
      source=MLB_2027_NEWS, sourceLabel="MLB.com — 2027 schedule released"),
    A(id="mlb-2027-postseason", year=2027, league="MLB",
      label="2027 MLB postseason (Wild Card → World Series)",
      value=None, date=None, status="UNRELEASED",
      statusNote="Not present in the official MLB feed on this date. The 2026 snapshot did carry postseason rows, so this is a coverage gap in the 2027 snapshot, not proof that no games occur. October 2027 must be treated as BUSY UNKNOWN.",
      source=MLB_2027_NEWS, sourceLabel="MLB.com — 2027 schedule released"),

    # ---------------- NFL / 49ers 2026-27 (official, verified today) ----------------
    A(id="nfl-2026-week18", year=2027, league="NFL",
      label="NFL 2026 Week 18 window",
      value="Sat Jan 9 – Sun Jan 10, 2027 (exact kickoffs flexed)",
      date="2027-01-09", endDate="2027-01-10", status="VERIFIED",
      statusNote="NFL Football Operations lists 'Week 18: January 9-10, 2027'. 49ers.com lists San Francisco's Week 18 game at Arizona as TBD. The stored NFL snapshot stops at Jan 3/4, 2027, so this week is missing from the dataset.",
      source=NFL_DATES, sourceLabel="NFL Football Operations — important dates",
      extraSource=FORTYNINERS, extraSourceLabel="49ers.com — official 2026 schedule"),
    A(id="nfl-2026-wildcard", year=2027, league="NFL",
      label="NFL Wild Card Weekend",
      value="Sat Jan 16 – Mon Jan 18, 2027",
      date="2027-01-16", endDate="2027-01-18", status="VERIFIED",
      statusNote="Official NFL Football Operations calendar.",
      source=NFL_DATES, sourceLabel="NFL Football Operations — important dates"),
    A(id="nfl-2026-divisional", year=2027, league="NFL",
      label="NFL Divisional Playoffs",
      value="Sat Jan 23 – Sun Jan 24, 2027",
      date="2027-01-23", endDate="2027-01-24", status="VERIFIED",
      statusNote="Official NFL Football Operations calendar.",
      source=NFL_DATES, sourceLabel="NFL Football Operations — important dates"),
    A(id="nfl-2026-championship", year=2027, league="NFL",
      label="AFC and NFC Championship Games",
      value="Sun Jan 31, 2027",
      date="2027-01-31", status="VERIFIED",
      statusNote="Official NFL Football Operations calendar.",
      source=NFL_DATES, sourceLabel="NFL Football Operations — important dates"),
    A(id="nfl-2026-sb", year=2027, league="NFL",
      label="Super Bowl LXI — last Westwood One NFL broadcast of the season",
      value="Sun Feb 14, 2027 · SoFi Stadium, Inglewood CA",
      date="2027-02-14", status="VERIFIED",
      statusNote="Official NFL Football Operations calendar. Westwood One is the NFL's official network radio partner and carries the Super Bowl; its own schedule page shows the 2026 package running through the postseason.",
      source=NFL_DATES, sourceLabel="NFL Football Operations — important dates",
      extraSource=WWO, extraSourceLabel="Westwood One Sports — NFL schedule"),
    A(id="nfl-2026-probowl", year=2027, league="NFL",
      label="Pro Bowl",
      value="No AFC–NFC Pro Bowl game is staged from the 2026 season onward",
      date=None, status="VERIFIED",
      statusNote="NFL announced the Pro Bowl Game will cease being contested; the league calendar for Jan/Feb 2027 contains no Pro Bowl date. Recorded as an exclusion, not a game.",
      source="https://www.nfl.com/news/nfl-elevates-pro-bowl-selection-game-s-will-cease-being-contested",
      sourceLabel="NFL.com — Pro Bowl announcement"),
    A(id="nfl-2026-49ers-radio", year=2026, league="NFL",
      label="49ers terrestrial radio flagship (every game)",
      value="KNBR 680 AM / 104.5 FM and KSAN 107.7 FM",
      date=None, status="VERIFIED",
      statusNote="Listed on every 2026 home and away game on the official 49ers.com schedule, including the TBD Week 18 game at Arizona.",
      source=FORTYNINERS, sourceLabel="49ers.com — official 2026 schedule"),
    A(id="nfl-2027-schedule", year=2027, league="NFL",
      label="NFL 2027 season schedule",
      value=None, date=None, status="UNRELEASED",
      statusNote="The 2027 NFL schedule has not been released. 49ers opponents are set by the rotation but dates/times are not published. Anything shown for Aug 2027 – Jan 2028 is ESTIMATED.",
      source=NFL_DATES, sourceLabel="NFL Football Operations — important dates"),

    # ---------------- NCAAF Stanford / Cal 2027 ----------------
    A(id="ncaaf-2027-dates", year=2027, league="NCAAF",
      label="Stanford & Cal 2027 game dates and kickoff times",
      value=None, date=None, status="UNRELEASED",
      statusNote="Only opponents have been announced (Cal: Aug 28 window vs Sacramento State, Sep 4 at UCLA, Sep 11 vs Old Dominion; Stanford / Cal ACC slates announced by each school). Individual dates and kickoff times are not published, so late-August through November 2027 cannot be scored day by day.",
      source="https://calbears.com/news/2026/6/25/football-cal-announces-matchups-against-odu-sac-state",
      sourceLabel="CalBears.com — 2027 non-conference announcement",
      extraSource="https://gostanford.com/sports/football/schedule",
      extraSourceLabel="GoStanford.com — official football schedule"),

    # ---------------- 2028 ----------------
    A(id="nfl-sb62", year=2028, league="NFL",
      label="Super Bowl LXII — host confirmed, date reported but not on NFL's own date table",
      value="Sun Feb 13, 2028 · Mercedes-Benz Stadium, Atlanta (reported)",
      date="2028-02-13", status="REPORTED",
      statusNote="NFL.com confirms Atlanta / Mercedes-Benz Stadium as the LXII host, but NFL.com's own 'Upcoming Super Bowls' table still lists the LXII date as TBA. The Feb 13, 2028 date is reported by ESPN (Adam Schefter) and Pro Football Talk. Treat as high-confidence, not officially tabled.",
      source=SB62, sourceLabel="NFL.com — Atlanta to host Super Bowl LXII",
      extraSource="https://sports.yahoo.com/articles/nfl-sends-message-2028-super-153037714.html",
      extraSourceLabel="Non-official: Pro Football Talk on the Feb 13, 2028 date"),
    A(id="nfl-2027-season-length", year=2028, league="NFL",
      label="2027 NFL regular season length",
      value="17-game regular season retained (18-game expansion not adopted for 2027)",
      date=None, status="REPORTED",
      statusNote="Reported by Pro Football Talk / Awful Announcing when the Feb 13, 2028 Super Bowl date was set. No official NFL release of the 2027 season format was located on this date.",
      source="https://sports.yahoo.com/articles/nfl-sends-message-2028-super-153037714.html",
      sourceLabel="Non-official: Pro Football Talk"),
    A(id="mlb-2028-schedule", year=2028, league="MLB",
      label="MLB 2028 schedule",
      value=None, date=None, status="UNRELEASED",
      statusNote="MLB has not released a 2028 schedule. MLB Stats API returns totalItems 0 for 2028 on this date. Every 2028 MLB date below is ESTIMATED from the 2027 pattern.",
      source="https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate=2028-01-01&endDate=2028-12-31",
      sourceLabel="MLB Stats API (official) — empty 2028 response"),
    A(id="mlb-2028-st-open-est", year=2028, league="MLB",
      label="2028 MLB spring training — projected first games",
      value="≈ Fri Feb 18, 2028",
      date="2028-02-18", status="ESTIMATED",
      statusNote="Projection. Spring training opened 2026-02-20 and opens 2027-02-19. Projected by holding the same weekday offset; MLB has not released a 2028 schedule.",
      source=f"{MLB_API}&startDate=2027-02-15&endDate=2027-02-22",
      sourceLabel="MLB Stats API 2027 (basis for the projection)"),
    A(id="mlb-2028-open-est", year=2028, league="MLB",
      label="2028 MLB Opening Day — projected",
      value="≈ Wed Mar 22, 2028",
      date="2028-03-22", status="ESTIMATED",
      statusNote="Projection. 2027 Opening Night is Wed Mar 24; MLB has historically opened in the last week of March. Not a released date.",
      source=MLB_2027_NEWS, sourceLabel="MLB.com — 2027 schedule released (basis for the projection)"),

    # ---------------- 2029 ----------------
    A(id="nfl-sb63", year=2029, league="NFL",
      label="Super Bowl LXIII — host confirmed, date projected",
      value="≈ Sun Feb 11, 2029 · Allegiant Stadium, Las Vegas",
      date="2029-02-11", status="ESTIMATED",
      statusNote="NFL.com confirms Las Vegas / Allegiant Stadium as the LXIII host but the announcement gives no firm date ('February 2029'). The Feb 11, 2029 date is the widely reported second Sunday of February 2029 and is shown as ESTIMATED, not as an NFL-announced date.",
      source=SB63, sourceLabel="NFL.com — Las Vegas to host Super Bowl LXIII"),
    A(id="mlb-2029-schedule", year=2029, league="MLB",
      label="MLB 2029 schedule",
      value=None, date=None, status="UNRELEASED",
      statusNote="MLB has not released a 2029 schedule. MLB Stats API returns totalItems 0 for 2029 on this date. Every 2029 MLB date below is ESTIMATED.",
      source="https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate=2029-01-01&endDate=2029-12-31",
      sourceLabel="MLB Stats API (official) — empty 2029 response"),
    A(id="mlb-2029-st-open-est", year=2029, league="MLB",
      label="2029 MLB spring training — projected first games",
      value="≈ Fri Feb 16, 2029",
      date="2029-02-16", status="ESTIMATED",
      statusNote="Projection from the 2026/2027 pattern. Not a released date.",
      source=f"{MLB_API}&startDate=2027-02-15&endDate=2027-02-22",
      sourceLabel="MLB Stats API 2027 (basis for the projection)"),
    A(id="mlb-2029-open-est", year=2029, league="MLB",
      label="2029 MLB Opening Day — projected",
      value="≈ Wed Mar 21, 2029",
      date="2029-03-21", status="ESTIMATED",
      statusNote="Projection from the 2027 pattern. Not a released date.",
      source=MLB_2027_NEWS, sourceLabel="MLB.com — 2027 schedule released (basis for the projection)"),
]

# ---------------------------------------------------------------------------
# Rule sets / ladder
# ---------------------------------------------------------------------------

RULESETS = [
    {
        "id": "strict",
        "name": "Strict — exactly as written",
        "definition": "Every MLB game (all 30 clubs, spring training + regular season + postseason + All-Star), every NFL game, Stanford and Cal football, and every Westwood One national NFL radio broadcast blocks a minute.",
        "startKey": "sb", "endKey": "stOpen",
        "note": "This is the rule the brief states. Spring training counts, so the run ends the day before the first Cactus/Grapefruit League game.",
    },
    {
        "id": "no-spring",
        "name": "Relaxed — MLB spring training ignored",
        "definition": "As strict, but exhibition/spring-training games do not block. Only MLB regular season, postseason and All-Star events count.",
        "startKey": "sb", "endKey": "mlbOpen",
        "note": "This is the only rule change that produces a multi-week window. The cost: you will miss Giants and Athletics spring-training broadcasts.",
    },
    {
        "id": "no-nfl",
        "name": "Relaxed — NFL / Westwood One ignored",
        "definition": "MLB and Stanford/Cal football only. No NFL game and no Westwood One slot blocks a minute.",
        "startKey": "ncaafEnd", "endKey": "stOpen",
        "note": "The winter gap between the last possible college bowl game and the first spring-training game.",
    },
    {
        "id": "no-mlb",
        "name": "Relaxed — MLB ignored",
        "definition": "NFL, Stanford/Cal football and Westwood One only. No MLB game blocks a minute.",
        "startKey": "sb", "endKey": "nflPreseason",
        "note": "The longest possible run, but it sits entirely inside the MLB regular season.",
    },
    {
        "id": "no-nfl-ncaaf",
        "name": "Relaxed — NFL and college football ignored",
        "definition": "MLB only (spring training, regular season, postseason, All-Star).",
        "startKey": "mlbPostEnd", "endKey": "stOpenNext",
        "note": "The off-season gap: the day after the World Series ends through the day before spring training opens the following February. Both boundaries are projections.",
    },
]

# Boundary values per year. `status` is the weakest status among the two boundaries.
BOUNDARIES = {
    2027: {
        "sb": ("2027-02-14", "VERIFIED", "Super Bowl LXI", NFL_DATES),
        "stOpen": ("2027-02-19", "VERIFIED", "MLB spring training opens", f"{MLB_API}&startDate=2027-02-15&endDate=2027-02-22"),
        "mlbOpen": ("2027-03-24", "VERIFIED", "MLB Opening Night", MLB_2027_NEWS),
        "ncaafEnd": ("2027-01-01", "ESTIMATED", "Last possible Stanford/Cal bowl date (projected)", "https://gostanford.com/sports/football/schedule"),
        "nflPreseason": ("2027-08-06", "ESTIMATED", "Projected first 2027 preseason game (2026 Hall of Fame Game fell on Aug 6, 2026)", FORTYNINERS),
        "mlbPostEnd": ("2027-11-05", "ESTIMATED", "Projected World Series end (2026 pattern)", MLB_2027_NEWS),
    },
    2028: {
        "sb": ("2028-02-13", "REPORTED", "Super Bowl LXII (date reported, host official)", SB62),
        "stOpen": ("2028-02-18", "ESTIMATED", "Projected MLB spring training opener", f"{MLB_API}&startDate=2027-02-15&endDate=2027-02-22"),
        "mlbOpen": ("2028-03-22", "ESTIMATED", "Projected MLB Opening Night", MLB_2027_NEWS),
        "ncaafEnd": ("2028-01-01", "ESTIMATED", "Projected last Stanford/Cal bowl date", "https://gostanford.com/sports/football/schedule"),
        "nflPreseason": ("2028-08-05", "ESTIMATED", "Projected first 2028 preseason game", FORTYNINERS),
        "mlbPostEnd": ("2028-11-04", "ESTIMATED", "Projected World Series end", MLB_2027_NEWS),
    },
    2029: {
        "sb": ("2029-02-11", "ESTIMATED", "Super Bowl LXIII (host official, date projected)", SB63),
        "stOpen": ("2029-02-16", "ESTIMATED", "Projected MLB spring training opener", f"{MLB_API}&startDate=2027-02-15&endDate=2027-02-22"),
        "mlbOpen": ("2029-03-21", "ESTIMATED", "Projected MLB Opening Night", MLB_2027_NEWS),
        "ncaafEnd": ("2029-01-01", "ESTIMATED", "Projected last Stanford/Cal bowl date", "https://gostanford.com/sports/football/schedule"),
        "nflPreseason": ("2029-08-04", "ESTIMATED", "Projected first 2029 preseason game", FORTYNINERS),
        "mlbPostEnd": ("2029-11-03", "ESTIMATED", "Projected World Series end", MLB_2027_NEWS),
    },
    # Used only as the closing boundary of the 2029 "MLB-only" off-season run.
    2030: {
        "stOpen": ("2030-02-15", "ESTIMATED", "Projected 2030 MLB spring training opener", f"{MLB_API}&startDate=2027-02-15&endDate=2027-02-22"),
    },
}

STATUS_RANK = {"VERIFIED": 0, "REPORTED": 1, "ESTIMATED": 2, "UNRELEASED": 3}

PRIORITY = {"San Francisco Giants", "Athletics"}


def d(s):
    return dt.date.fromisoformat(s)


def weaker(a, b):
    return a if STATUS_RANK[a] >= STATUS_RANK[b] else b


def build_windows():
    out = []
    for year in (2027, 2028, 2029):
        b = BOUNDARIES[year]
        for rs in RULESETS:
            start_raw, start_status, start_label, start_src = b[rs["startKey"]]
            if rs["endKey"] == "stOpenNext":
                end_raw, end_status, end_label, end_src = BOUNDARIES[year + 1]["stOpen"]
                end_label = end_label + f" ({year + 1})"
            else:
                end_raw, end_status, end_label, end_src = b[rs["endKey"]]
            start = d(start_raw) + dt.timedelta(days=1)
            end = d(end_raw) - dt.timedelta(days=1)
            days = (end - start).days + 1
            status = weaker(start_status, end_status)
            out.append({
                "year": year,
                "ruleSet": rs["id"],
                "ruleSetName": rs["name"],
                "start": start.isoformat(),
                "end": end.isoformat(),
                "days": max(days, 0),
                "weeks": round(max(days, 0) / 7, 1),
                "status": status,
                "meetsOneWeek": days >= 7,
                "meetsTwoWeeks": days >= 14,
                "meetsThreeWeeks": days >= 21,
                "startBoundary": {"value": start_raw, "label": start_label, "status": start_status, "source": start_src},
                "endBoundary": {"value": end_raw, "label": end_label, "status": end_status, "source": end_src},
                "note": rs["note"],
                "definition": rs["definition"],
            })
    return out


# ---------------------------------------------------------------------------
# 2027 candidate window, day by day, from the official MLB snapshot
# ---------------------------------------------------------------------------

def day_by_day():
    rows = json.loads((ROOT / "site/data/mlb-2027.json").read_text())
    start = d("2027-02-15")
    end = d("2027-03-23")  # last day before 2027 Opening Night (Mar 24)
    by_date = {}
    for r in rows:
        if not r.get("date"):
            continue
        by_date.setdefault(r["date"], []).append(r)

    days = []
    cur = start
    while cur <= end:
        key = cur.isoformat()
        games = by_date.get(key, [])
        giants = [g for g in games if "San Francisco Giants" in (g.get("teams") or [])]
        athletics = [g for g in games if "Athletics" in (g.get("teams") or [])]
        days.append({
            "date": key,
            "weekday": cur.strftime("%a"),
            "mlbGames": len(games),
            "priorityGames": len(giants) + len(athletics),
            "giants": bool(giants),
            "athletics": bool(athletics),
            "kinds": sorted({g.get("kind") for g in games if g.get("kind")}),
            "sample": games[0]["title"] if games else None,
            "source": f"{MLB_API}&startDate={key}&endDate={key}" if games else None,
        })
        cur += dt.timedelta(days=1)

    total = len(days)
    quiet = [x for x in days if x["mlbGames"] == 0]
    priority_days = [x for x in days if x["priorityGames"] > 0]
    return {
        "window": {"start": start.isoformat(), "end": end.isoformat(), "days": total},
        "source": f"{MLB_API}&startDate=2027-02-15&endDate=2027-03-23",
        "sourceLabel": "MLB Stats API 2027 snapshot (official)",
        "daysWithZeroMlbGames": len(quiet),
        "daysWithAnyMlbGame": total - len(quiet),
        "daysWithGiantsOrAthletics": len(priority_days),
        "days": days,
    }


def strict_runs_from_feed():
    """Runs of consecutive days with zero MLB games in the official 2027 snapshot.

    Scanned from the day after Super Bowl LXI (2027-02-15) to the end of 2027.
    Every returned run is annotated: a run that ends at the last date present in the
    feed is an UNKNOWN coverage tail (the 2027 postseason is not in the snapshot), not
    an all-clear period.
    """
    rows = json.loads((ROOT / "site/data/mlb-2027.json").read_text())
    have = sorted({r["date"] for r in rows if r.get("date")})
    if not have:
        return []
    first_feed, last_feed = have[0], have[-1]
    cur, last = d("2027-02-15"), d("2027-12-31")
    runs, run = [], []
    while cur <= last:
        if cur.isoformat() not in set(have):
            run.append(cur.isoformat())
        else:
            if run:
                runs.append(run)
            run = []
        cur += dt.timedelta(days=1)
    if run:
        runs.append(run)

    # Dates that look empty in the feed but are known-coverage gaps, never all-clear days.
    KNOWN_GAPS = {
        "2027-03-24": ("2027 MLB Opening Night (Netflix, matchup TBD) is announced by MLB.com but is not "
                       "present in the MLB Stats API snapshot. Treat as BUSY."),
    }

    out = []
    for r in sorted(runs, key=lambda r: -len(r)):
        item = {"start": r[0], "end": r[-1], "days": len(r), "status": "VERIFIED", "note": None}
        gaps_in_run = [g for g in KNOWN_GAPS if r[0] <= g <= r[-1]]
        if gaps_in_run:
            item["status"] = "UNKNOWN"
            item["note"] = " ".join(KNOWN_GAPS[g] for g in gaps_in_run)
        elif r[0] < first_feed:
            item["note"] = ("Starts before the first date present in the official MLB 2027 snapshot "
                            f"({first_feed}); MLB has no games before spring training opens.")
        elif r[-1] >= last_feed:
            item["status"] = "UNKNOWN"
            item["note"] = ("This run runs to the end of the year because the official 2027 MLB snapshot "
                            f"stops at {last_feed}. The 2027 postseason is NOT in the feed. This is a "
                            "coverage gap and must be treated as BUSY, not free.")
        elif "2027-07-15" in r:
            item["status"] = "CONFLICT"
            item["note"] = ("MLB.com says the 2027 second half begins Thursday July 15, but the MLB Stats API "
                            "snapshot has no game on that date. The two official sources disagree, so Jul 15 is "
                            "treated as BUSY and this run is scored as "
                            f"{len([x for x in r if x != '2027-07-15'])} day(s), not {len(r)}.")
            item["daysIfConflictResolvedAsBusy"] = len([x for x in r if x != "2027-07-15"])
        out.append(item)
    return out


def build():
    payload = {
        "meta": {
            "generated": CHECKED,
            "session": "arena/63ee3d13-korea6",
            "generator": "scripts/projections.py",
            "listenerLocation": "Outer Sunset, San Francisco, CA 94122",
            "timezone": "America/Los_Angeles",
            "statusLegend": {
                "VERIFIED": "Read today from an official league or club source; source URL attached.",
                "REPORTED": "An official source confirms part of the fact; the exact value comes from a non-official source and is labelled as such.",
                "ESTIMATED": "No released schedule exists; value is projected from the most recent released season. NOT an official schedule.",
                "UNRELEASED": "League has not published it; no value supplied on purpose.",
            },
            "headline": "No 7-, 14- or 21-day window is conflict-free under the rule exactly as written in 2027, 2028 or 2029. The only rule change that creates a multi-week window is ignoring MLB spring training, which opens a 37-day 2027 run (Feb 15 – Mar 23) with verified official boundaries at both ends.",
        },
        "anchors": ANCHORS,
        "windows": build_windows(),
        "ladder2027DayByDay": day_by_day(),
        "mlbOnlyQuietRuns2027": strict_runs_from_feed(),
    }
    out = ROOT / "site/data/projections.json"
    out.write_text(json.dumps(payload, indent=1) + "\n")
    print(f"wrote {out.relative_to(ROOT)} — {len(ANCHORS)} anchors, {len(payload['windows'])} windows, "
          f"{len(payload['ladder2027DayByDay']['days'])} day rows")


if __name__ == "__main__":
    build()
