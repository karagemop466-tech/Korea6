# Free Time Vacation

A static GitHub Pages planner for Pacific Time. The daily scoreboard requests available MLB schedules from MLB's Stats API; manually researched football listings are a partial snapshot, not a complete feed. Empty results are **not** proof of free time. The site documents sources, assumptions, and known gaps on its Flagged for Review page.

Open `index.html` through a local HTTP server, for example `python3 -m http.server 8000`, or use the GitHub Pages site. Internet access and a browser that permits the MLB API request are required for live MLB listings. Run the local checks with `node --test tests/*.test.js` and `node tests/check-site.js`.
