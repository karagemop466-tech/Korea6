# Free Time Vacation

A static GitHub Pages planner for Pacific Time. The daily scoreboard requests available MLB schedules from MLB's Stats API; manually researched football listings are a partial snapshot, not a complete feed. Empty results are **not** proof of free time. The site documents sources, assumptions, and known gaps on its Flagged for Review page.

Open `index.html` through a local HTTP server, for example `python3 -m http.server 8000`, or use the GitHub Pages site. Internet access and a browser that permits the MLB API request are required for live MLB listings. Run the local checks with `node --test tests/*.test.js` and `node tests/check-site.js`.

## Additional verified analysis (session arena/fbb7cd8f-korea6)

- `calendar.html` — day-by-day free/busy model (Pacific time, Nov 2026 – Dec 2029) from `data/calendar.json` (generator: `tools/generate_calendar.py`).
- `windows.html` — vacation windows 2027–2029: **Feb 15–18, 2027 (verified)** and **Jul 12–14, 2027 (verified)** all-clear; 2028/2029 estimated and flagged.
- `summary.html`, `data-mlb.html`, `data-nfl.html`, `data-ncaaf.html` — executive summary and per-league tables, each row linked to an official source.
- `research/sources.md` — full verification log. Unverified items are never filled in; see the Flagged for Review page.
