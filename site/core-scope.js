const PT = 'America/Los_Angeles';
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmtTime = iso => iso ? new Intl.DateTimeFormat('en-US', {timeZone: PT, hour: 'numeric', minute: '2-digit', timeZoneName: 'short'}).format(new Date(iso)) : '— (TBD / unverified)';
const fmtWindow = (iso, mins) => {
  if (!iso || !mins) return '— (start time unverified)';
  const s = new Date(iso);
  const e = new Date(s.getTime() + mins * 60000);
  const f = new Intl.DateTimeFormat('en-US', {timeZone: PT, hour: 'numeric', minute: '2-digit'});
  const tz = new Intl.DateTimeFormat('en-US', {timeZone: PT, timeZoneName: 'short'}).formatToParts(s).find(p => p.type === 'timeZoneName')?.value || 'PT';
  return `${f.format(s)} – ~${f.format(e)} ${tz} (est. ${mins}m)`;
};

async function boot() {
  const root = document.getElementById('content');
  try {
    const res = await fetch('data/expanded-official.json');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    const durations = data.meta.durationEstimatesMinutes || {};

    const matrixRows = data.scopeMatrix.map(row => `
      <tr>
        <td><strong>${row.year}</strong></td>
        <td><span class="badge ${row.coreFourScope.oneWeek === 0 ? 'orange' : 'warn'}">Unverified (0 certified)</span><small>Incomplete schedule coverage; annual maximum unknown</small></td>
        <td><span class="badge ${row.fullAmFmScope.oneWeek === 0 ? 'orange' : 'warn'}">Unverified (0 certified)</span><small>Incomplete station and schedule coverage; annual maximum unknown</small></td>
        <td><a href="vacations.html">Open ${row.year} finder</a></td>
      </tr>
    `).join('');

    const febDays = [
      {date:'2027-02-14 (Sun)', core:'Super Bowl LXI (NFL Postseason)', full:'Super Bowl LXI (NFL / Westwood One)', station:'KSAN / KNBR / Westwood One (carriage TBA)', src:'https://operations.nfl.com/calendar-events/nfl-important-dates', badge:'orange', status:'Scheduled; local carriage requires review'},
      {date:'2027-02-15 (Mon)', core:'No core game confirmed in this partial snapshot', full:'Indiana Pacers at Golden State Warriors (4:30 PM PST)', station:'KGMZ 95.7 FM', src:'https://www.nba.com/game/ind-vs-gsw-0022600084', badge:'orange', status:'Occupied on 95.7 FM'},
      {date:'2027-02-16 (Tue)', core:'No core game confirmed in this partial snapshot', full:'No verified local game; Westwood One NCAAM national slate unposted', station:'—', src:'https://www.westwoodonesports.com/ncaa-basketball/', badge:'warn', status:'Unverified; WWO NCAAM unposted'},
      {date:'2027-02-17 (Wed)', core:'No core game confirmed in this partial snapshot', full:'Cal MBB at Pitt (4:00 PM PST) + Pelicans at Warriors (7:00 PM PST) + USF MBB at LMU (TBA)', station:'KSFO 810 AM · KGMZ 95.7 FM · KTCT 1050 AM (partner)', src:'https://calbears.com/sports/mens-basketball/schedule/2026-27', badge:'orange', status:'Listed games; individual carriage needs review'},
      {date:'2027-02-18 (Thu)', core:'No core game confirmed in this partial snapshot', full:'No verified local game; Westwood One NCAAM national slate unposted', station:'—', src:'https://www.westwoodonesports.com/ncaa-basketball/', badge:'warn', status:'Unverified; WWO NCAAM unposted'},
      {date:'2027-02-19 (Fri)', core:'2027 MLB Spring Training Opening Day (3 games)', full:'2027 MLB Spring Training Opening Day + NBA All-Star Weekend', station:'MLB club flagships', src:'https://statsapi.mlb.com/api/v1/schedule?sportId=1&season=2027&startDate=2027-02-19&endDate=2027-02-19', badge:'orange', status:'MLB games listed; AM/FM carriage unverified'},
      {date:'2027-02-20 (Sat)', core:'2027 MLB Spring Training (SF Giants at Mariners; Athletics vs White Sox + full slate)', full:'Giants and Athletics spring games; Cal MBB at NC State (9:00 AM PST, KSFO 810 AM)', station:'MLB game-specific carriage unverified · KSFO 810 listed for Cal', src:'https://calbears.com/sports/mens-basketball/schedule/2026-27', badge:'orange', status:'Scheduled; local carriage requires review'},
    ].map(d => `
      <tr>
        <td><strong>${esc(d.date)}</strong></td>
        <td>${esc(d.core)}</td>
        <td>${esc(d.full)}<small>${esc(d.station)}</small></td>
        <td><span class="badge ${d.badge}">${esc(d.status)}</span></td>
        <td><a href="${esc(d.src)}" target="_blank" rel="noopener">Official source ↗</a></td>
      </tr>
    `).join('');

    const stationRows = data.stations.map(s => `
      <tr>
        <td><strong>${esc(s.station)}</strong><small>${esc(s.band)}</small></td>
        <td>${s.properties.map(p => `<div>• ${esc(p)}</div>`).join('')}${s.note ? `<small>${esc(s.note)}</small>` : ''}</td>
        <td><span class="badge green">Reception unverified</span></td>
        <td>
          <a href="${esc(s.source)}" target="_blank" rel="noopener">Primary ↗</a>
          ${s.secondarySource ? ` · <a href="${esc(s.secondarySource)}" target="_blank" rel="noopener">Partner ↗</a>` : ''}
        </td>
      </tr>
    `).join('');

    const exclusionRows = data.nonTerrestrialExclusions.map(x => `
      <tr>
        <td><strong>${esc(x.team)}</strong> <span class="badge">${esc(x.league)}</span></td>
        <td>${esc(x.audioPlatform)}<small>${esc(x.summary)}</small></td>
        <td><span class="badge">Digital / Satellite only</span></td>
        <td><a href="${esc(x.source)}" target="_blank" rel="noopener">Official announcement ↗</a></td>
      </tr>
    `).join('');

    root.innerHTML = `
      <div class="eyebrow">LINE-BY-LINE PRIMARY SOURCE EXPANSION · 94122</div>
      <div class="headrow">
        <div>
          <h1>Two-scope evidence &amp; Bay Area AM/FM review</h1>
          <p class="lede">Side-by-side analysis separating the narrow 4-category prompt scope (All 30 MLB, NFL, Stanford/Cal NCAAF, Westwood One NFL) from a partial inventory of Outer Sunset 94122 terrestrial AM/FM sports — backed by ${data.events.length} newly verified primary-source records.</p>
        </div>
        <span class="badge green">Checked ${esc(data.meta.checked)} · 0 inferred values</span>
      </div>

      <div class="metrics">
        <div class="metric">
          <label>1–3 WEEK CONFLICT-FREE WINDOWS (2027)</label>
          <strong>Unknown</strong>
          <small>No windows certified; incomplete evidence does not prove that none exist.</small>
        </div>
        <div class="metric">
          <label>2027 NFL PRO BOWL GAME</label>
          <strong>Canceled</strong>
          <small>Officially discontinued Aug 26, 2026 by NFL.com starting with the 2026 season.</small>
        </div>
        <div class="metric">
          <label>NEWLY VERIFIED PRIMARY RECORDS</label>
          <strong>${data.events.length}</strong>
          <small>68 NBA · 64 NCAAM · 41 NCAAF · 1 MLS · 1 U.S. Soccer · 1 MLB HR Derby</small>
        </div>
      </div>

      <div class="note info">
        <strong>Official NFL Pro Bowl Verification (${esc(data.proBowlFinding.announcementDate)}):</strong>
        ${esc(data.proBowlFinding.summary)}
        <a href="${esc(data.proBowlFinding.source)}" target="_blank" rel="noopener">NFL.com release ↗</a> ·
        <a href="${esc(data.proBowlFinding.secondarySource)}" target="_blank" rel="noopener">NFL Media release ↗</a>
      </div>

      <div class="note">Coverage is incomplete. February 15–18 is only a candidate between league milestones, not proof of a free interval or an annual maximum. National schedules and flagship partnerships do not prove individual game carriage or reception in 94122. The historical generated data contains broader assertions that remain under review. <a href="review.html">See review flags</a>.</div>
      <div class="section-head"><h2>1. 2027–2029 Vacation Window Verdict by Scope (1, 2 &amp; 3 Weeks)</h2></div>
      <div class="panel tablewrap">
        <table>
          <thead>
            <tr>
              <th>Year</th>
              <th>Core 4-Category Scope (MLB + NFL + Stanford/Cal FB + WWO NFL)</th>
              <th>Full SF 94122 Terrestrial AM/FM Scope (+ NBA, NCAAM, WNBA, MLS, WWO NCAA)</th>
              <th>Planner</th>
            </tr>
          </thead>
          <tbody>${matrixRows}</tbody>
        </table>
      </div>

      <div class="section-head"><h2>2. Partial Day-by-Day Snapshot: February 14–20, 2027 (Super Bowl LXI to MLB Spring Training)</h2></div>
      <div class="panel tablewrap">
        <table>
          <thead>
            <tr>
              <th>Date (PT)</th>
              <th>Core 4-Category Scope</th>
              <th>Partial Bay Area AM/FM evidence</th>
              <th>Status</th>
              <th>Verified Source</th>
            </tr>
          </thead>
          <tbody>${febDays}</tbody>
        </table>
      </div>

      <div class="section-head"><h2>3. Selected Bay Area Terrestrial AM/FM Sports Stations</h2></div>
      <div class="panel tablewrap">
        <table>
          <thead>
            <tr>
              <th>Station</th>
              <th>Reported sports properties</th>
              <th>94122 Reception</th>
              <th>Official Sources</th>
            </tr>
          </thead>
          <tbody>${stationRows}${exclusionRows}</tbody>
        </table>
      </div>

      <div class="section-head"><h2>4. Expanded Primary-Source Broadcast &amp; Schedule Ledger (${data.events.length} rows)</h2></div>
      <div class="panel panel-pad">
        <div class="toolbar">
          <label for="exp-league">League</label>
          <select id="exp-league">
            <option value="ALL">All (${data.events.length})</option>
            <option value="NBA">NBA — Warriors / ASG (68)</option>
            <option value="NCAAM">NCAAM — Cal &amp; USF MBB (64)</option>
            <option value="NCAAF">NCAAF — Stanford, Cal &amp; WWO (41)</option>
            <option value="MLS">MLS — SJ Earthquakes (1)</option>
            <option value="USSF">U.S. Soccer — Westwood One (1)</option>
            <option value="MLB">MLB — 2027 Home Run Derby (1)</option>
          </select>
          <label for="exp-scope">Scope</label>
          <select id="exp-scope">
            <option value="ALL">All verified expansion rows</option>
            <option value="CORE">Core 4-Category Prompt Scope only</option>
            <option value="AMFM">Additional 94122 AM/FM Radio Sports</option>
          </select>
          <input id="exp-search" type="search" placeholder="Search team, station, date (e.g. 2027-02-17, KSFO, Notre Dame)…">
          <span id="exp-count" class="badge"></span>
        </div>
      </div>
      <div class="panel tablewrap">
        <table>
          <thead>
            <tr>
              <th>Date (PT)</th>
              <th>Pacific Start &amp; Planning Window</th>
              <th>Event &amp; Category</th>
              <th>Verified Terrestrial Station</th>
              <th>Official Source</th>
            </tr>
          </thead>
          <tbody id="exp-tbody"></tbody>
        </table>
      </div>
      <footer>
        <span>All start times normalized to America/Los_Angeles (PST/PDT). Unconfirmed times and game-specific station assignments are left blank (—) rather than inferred.</span>
        <span><a href="../research/line-by-line-audit-f8a21d11.md">Read full line-by-line audit report</a></span>
      </footer>
    `;

    const tbody = document.getElementById('exp-tbody');
    const selLeague = document.getElementById('exp-league');
    const selScope = document.getElementById('exp-scope');
    const inpSearch = document.getElementById('exp-search');
    const countEl = document.getElementById('exp-count');

    function renderRows() {
      const lg = selLeague.value;
      const sc = selScope.value;
      const q = inpSearch.value.trim().toLowerCase();
      const rows = data.events.filter(e => {
        if (lg !== 'ALL' && e.league !== lg) return false;
        if (sc === 'CORE' && !e.corePromptScope) return false;
        if (sc === 'AMFM' && e.corePromptScope) return false;
        if (q) {
          const hay = `${e.date || 'tbd'} ${e.title} ${e.league} ${e.station || ''} ${e.kind} ${e.note || ''}`.toLowerCase();
          if (!hay.includes(q)) return false;
        }
        return true;
      });
      countEl.textContent = `${rows.length} shown`;
      tbody.innerHTML = rows.map(e => {
        const mins = durations[e.league]?.minutes;
        return `
          <tr>
            <td><strong>${esc(e.date || 'Date TBD')}</strong><small>${esc(e.status)}</small></td>
            <td><strong>${esc(fmtTime(e.start))}</strong><small>${esc(e.start ? fmtWindow(e.start, mins) : e.timeBasis + ' unverified')}</small></td>
            <td>
              <strong>${e.priority ? '<span class="priority" title="High priority">★</span>' : ''}${esc(e.title)}</strong>
              <small><span class="badge">${esc(e.league)}</span> · ${esc(e.kind)}${e.note ? ' — ' + esc(e.note) : ''}</small>
            </td>
            <td>${e.station ? `<strong>${esc(e.station)}</strong>` : '<span class="muted">— (unverified)</span>'}${e.radioSource ? `<small><a href="${esc(e.radioSource)}" target="_blank" rel="noopener">Radio source ↗</a></small>` : ''}</td>
            <td><a href="${esc(e.source)}" target="_blank" rel="noopener">Official source ↗</a></td>
          </tr>
        `;
      }).join('') || '<tr><td colspan="5" class="empty">No matching verified rows.</td></tr>';
    }

    selLeague.addEventListener('change', renderRows);
    selScope.addEventListener('change', renderRows);
    inpSearch.addEventListener('input', renderRows);
    renderRows();
  } catch (err) {
    root.innerHTML = `<div class="note">Failed to load official expansion dataset: ${esc(err.message)}</div>`;
  }
}
boot();
