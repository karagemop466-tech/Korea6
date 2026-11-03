#!/usr/bin/env python3
"""Generate data/calendar.json — day-level free/busy model for the Free-Time Vacation site.

Honesty rules encoded here:
- Season WINDOWS for 2026/2027 are anchored to verified official dates (see research/sources.md).
- 2028/2029 windows are structural ESTIMATES (schedules not yet released) -> verified:false.
- Per-day broadcast windows are ESTIMATED typical windows (avg durations: MLB 2:38, NFL 3:03,
  NCAAF ~3:26) because official per-game times for future seasons are not released.
"""
import json, datetime as dt

START = dt.date(2026, 11, 3)
END = dt.date(2029, 12, 31)

# Season windows: (start, end_inclusive, category, phase, verified, source_note)
WINDOWS = [
    # ---- 2026 (verified anchors) ----
    ("2026-11-03", "2026-11-04", "mlb", "postseason", False, "2026 postseason final days (end date estimated; 2026 WS concluded early Nov 2026)"),
    ("2026-09-09", "2027-02-14", "nfl", "season", True, "Kickoff Sep 9 2026 (verified) .. Super Bowl LXI Feb 14 2027 (verified)"),
    ("2026-08-29", "2027-01-10", "ncaaf", "season", False, "Stanford opener Aug 29 2026 (verified); bowl-season end Jan 10 2027 estimated"),
    # ---- 2027 ----
    ("2027-02-19", "2027-03-23", "mlb", "spring", True, "2027 Spring Training opens Feb 19 2027 (MLB press release, verified)"),
    ("2027-03-24", "2027-09-26", "mlb", "regular", True, "2027 regular season Mar 24 - Sep 26 2027 (MLB, verified)"),
    ("2027-09-27", "2027-10-30", "mlb", "postseason", False, "Postseason after Sep 26 (verified end); WS window Oct 22-30 possible Game 7 (reported)"),
    ("2027-02-15", "2027-02-18", "mlb", "off", True, "VERIFIED all-clear gap: after Super Bowl LXI (Feb 14 2027, verified) and before 2027 Spring Training (Feb 19 2027, verified); NFL/NCAAF also off"),
    ("2027-07-12", "2027-07-14", "mlb", "allstar", True, "2027 All-Star break: HR Derby Jul 12, ASG Jul 13 (verified), second half resumes Jul 15 (verified) - no regular-season games Jul 12-14"),
    ("2027-09-09", "2028-02-13", "nfl", "season", False, "ESTIMATED: 2027 NFL schedule not released (expected May 2027); kickoff ~Sep 9 2027, Super Bowl LXII ~Feb 13 2028"),
    ("2027-08-28", "2028-01-10", "ncaaf", "season", False, "Cal Week 0 Aug 28 2027 (verified); remainder of 2027 slate dates TBD; bowl end estimated"),
    # ---- 2028 (all estimated) ----
    ("2028-02-18", "2028-03-22", "mlb", "spring", False, "ESTIMATED 2028 spring training window"),
    ("2028-03-23", "2028-09-24", "mlb", "regular", False, "ESTIMATED 2028 regular season window"),
    ("2028-09-25", "2028-10-29", "mlb", "postseason", False, "ESTIMATED 2028 postseason window"),
    ("2028-09-07", "2029-02-11", "nfl", "season", False, "ESTIMATED 2028 NFL season (kickoff ~Sep 7 2028; Super Bowl LXIII ~Feb 11 2029)"),
    ("2028-08-26", "2029-01-08", "ncaaf", "season", False, "ESTIMATED 2028 NCAAF season"),
    # ---- 2029 (all estimated) ----
    ("2029-02-17", "2029-03-21", "mlb", "spring", False, "ESTIMATED 2029 spring training window"),
    ("2029-03-22", "2029-09-23", "mlb", "regular", False, "ESTIMATED 2029 regular season window"),
    ("2029-09-24", "2029-10-28", "mlb", "postseason", False, "ESTIMATED 2029 postseason window"),
    ("2029-09-06", "2030-02-10", "nfl", "season", False, "ESTIMATED 2029 NFL season (kickoff ~Sep 6 2029; Super Bowl LXIV ~Feb 10 2030)"),
    ("2029-08-25", "2030-01-13", "ncaaf", "season", False, "ESTIMATED 2029 NCAAF season"),
]

# Typical daily broadcast windows (minutes from midnight, Pacific local clock) — ESTIMATED typical patterns
TYPICAL = {
    "mlb": [(12*60+5, 15*60+5, "MLB game window (est. start 12:05p PT, avg 2h38m)"),
            (16*60+5, 19*60+5, "MLB game window (est. start 4:05p PT)"),
            (18*60+5, 21*60+5, "MLB game window (est. start 6:05p PT)"),
            (19*60+10, 22*60+10, "MLB game window (est. start 7:10p PT)")],
    "nfl_sun": [(10*60, 19*60+30, "NFL Sunday slate (est. 10:00a-7:30p PT, games avg 3h03m)"),
                (17*60+15, 20*60+45, "NFL Sunday/Monday/Thursday night (est. 5:15-8:45p PT)")],
    "nfl_other": [(13*60, 19*60+30, "NFL Saturday/holiday slate (est. 1:00-7:30p PT)"),
                  (12*60, 16*60, "NFL holiday afternoon games (est. 12:00-4:00p PT)"),
                  (17*60+15, 20*60+45, "NFL primetime (est. 5:15-8:45p PT)")],
    "ncaaf_sat": [(9*60, 22*60+30, "NCAAF Saturday slate (est. 9:00a-10:30p PT, games avg ~3h26m)")],
    "ncaaf_fri": [(16*60, 20*60+30, "NCAAF Friday night (est. 4:00-8:30p PT)")],
}

def parse(s): return dt.date.fromisoformat(s)

days = []
d = START
while d <= END:
    cats = {"mlb": "off", "nfl": "off", "ncaaf": "off"}
    covered = False
    verified = True
    notes = []
    for ws, we, cat, phase, ver, note in WINDOWS:
        if parse(ws) <= d <= parse(we):
            cats[cat] = phase
            covered = True
            verified = verified and ver
            if not ver:
                notes.append(note)
    if not covered:
        verified = False
    dow = d.weekday()  # 0=Mon
    busy = []
    def add(cat, minutes_list):
        for s, e, label in minutes_list:
            busy.append({"start": s, "end": e, "label": label, "cat": cat})
    if cats["mlb"] in ("spring", "regular", "postseason"):  # 'allstar' break = no games
        add("mlb", TYPICAL["mlb"])
    if cats["nfl"] == "season":
        if dow == 6:
            add("nfl", TYPICAL["nfl_sun"])
        elif dow in (3, 0):  # Thu, Mon
            add("nfl", [TYPICAL["nfl_sun"][1]])
        else:
            add("nfl", TYPICAL["nfl_other"])
        # Westwood One national NFL (TNF/MNF/SNF/holidays/playoffs/Super Bowl) rides KNBR 680 — same windows
        busy.append({"start": 17*60+15 if dow in (0,3,6) else 10*60, "end": 20*60+45 if dow in (0,3,6) else 19*60+30,
                     "label": "Westwood One national NFL broadcast (KNBR 680) — same games as NFL windows", "cat": "westwood"})
    if cats["ncaaf"] == "season":
        add("ncaaf", TYPICAL["ncaaf_sat"] if dow == 5 else (TYPICAL["ncaaf_fri"] if dow == 4 else [(12*60, 22*60+30, "NCAAF weekday slate (est. 12:00-10:30p PT)")]))
    # merge busy -> free blocks
    busy.sort(key=lambda b: b["start"])
    merged = []
    for b in busy:
        if merged and b["start"] <= merged[-1]["end"]:
            merged[-1]["end"] = max(merged[-1]["end"], b["end"])
        else:
            merged.append(dict(b))
    free = []
    cursor = 0
    for b in merged:
        if b["start"] > cursor:
            free.append({"start": cursor, "end": b["start"]})
        cursor = max(cursor, b["end"])
    if cursor < 24*60:
        free.append({"start": cursor, "end": 24*60})
    free_hours = sum(f["end"] - f["start"] for f in free) / 60.0
    overall = "FREE" if not merged else ("PARTIAL" if free_hours > 0 else "BUSY")
    days.append({
        "date": d.isoformat(), "dow": d.strftime("%a"),
        "cats": cats, "overall": overall, "freeHours": round(free_hours, 2),
        "busy": merged, "free": free, "verified": verified,
        "note": "; ".join(sorted(set(notes))) if notes else ""
    })
    d += dt.timedelta(days=1)

out = {"generated": "2026-11-03", "tz": "America/Los_Angeles (Pacific)", "days": days}
with open("/home/user/Korea6/data/calendar.json", "w") as f:
    json.dump(out, f)
print(f"wrote {len(days)} days")
