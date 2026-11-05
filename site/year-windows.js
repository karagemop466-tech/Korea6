// "2027–2029 vacation windows" page. Reads site/data/projections.json only.
// Every row on this page carries a source link; statuses are never upgraded.
import { todayPacific } from './engine.mjs';

const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const link = (u, label = 'Official source ↗') => u
  ? `<a href="${esc(u)}" target="_blank" rel="noopener noreferrer">${esc(label)}</a>`
  : '<span class="muted">—</span>';

const STATUS_CLASS = { VERIFIED: 'green', REPORTED: 'warn', ESTIMATED: 'warn', UNRELEASED: '', UNKNOWN: 'orange', CONFLICT: 'orange' };
const STATUS_HELP = {
  VERIFIED: 'Read from an official league or club source; the source link is on the row.',
  REPORTED: 'An official source confirms part of the fact; the exact value comes from a non-official source and is labelled as such.',
  ESTIMATED: 'No released schedule exists for that season. Projected from the most recent released season — NOT an official schedule.',
  UNRELEASED: 'The league has not published it. No value is filled in on purpose.',
  UNKNOWN: 'The official feed has no rows here. That is a coverage gap and is treated as BUSY, never as free.',
  CONFLICT: 'Two official sources disagree. The conservative reading is used.',
};
const badge = s => `<span class="badge ${STATUS_CLASS[s] || ''}">${esc(s)}</span>`;
const pretty = d => new Date(d + 'T12:00:00Z').toLocaleDateString('en-US', { timeZone: 'UTC', month: 'short', day: 'numeric', year: 'numeric' });
const range = (a, b) => `${pretty(a)} – ${pretty(b)}`;

const foot = () => `<footer><span>FREE TIME VACATION · San Francisco / 94122</span><span>Multi-year windows · checked 2026-11-05 · every value labelled VERIFIED, REPORTED, ESTIMATED or UNRELEASED</span></footer>`;

function metrics(data) {
  const w = data.windows;
  const strict27 = w.find(x => x.year === 2027 && x.ruleSet === 'strict');
  const relaxed27 = w.find(x => x.year === 2027 && x.ruleSet === 'no-spring');
  const sevenPlus = w.filter(x => x.meetsOneWeek);
  const m = (label, value, detail) => `<div class="metric"><label>${label}</label><strong>${value}</strong><small>${detail}</small></div>`;
  return `<div class="metrics">
    ${m('STRICT RULE · 2027 BEST RUN', `${strict27.days} days`, `${range(strict27.start, strict27.end)} · ${strict27.status}. No 7-day run exists under the rule as written.`)}
    ${m('RELAXED (NO SPRING TRAINING) · 2027', `${relaxed27.days} days`, `${range(relaxed27.start, relaxed27.end)} · ${relaxed27.status}. Both boundaries are official; spring-training games inside are ignored by this rule.`)}
    ${m('RUNS THAT REACH 7 DAYS', `${sevenPlus.length} of ${w.length}`, 'All of them require dropping something from the brief. Under the strict rule the count is zero.')}
  </div>`;
}

function answersTable(data) {
  const rows = data.windows.map(w => `<tr>
    <td><strong>${w.year}</strong></td>
    <td><strong>${esc(w.ruleSetName)}</strong><small>${esc(w.definition)}</small></td>
    <td>${range(w.start, w.end)}</td>
    <td><strong>${w.days}</strong><small>${w.weeks} weeks</small></td>
    <td>${w.meetsOneWeek ? '<span class="badge green">7d ✓</span> ' : '<span class="badge">7d ✗</span> '}${w.meetsTwoWeeks ? '<span class="badge green">14d ✓</span> ' : '<span class="badge">14d ✗</span> '}${w.meetsThreeWeeks ? '<span class="badge green">21d ✓</span>' : '<span class="badge">21d ✗</span>'}</td>
    <td>${badge(w.status)}<small>${esc(STATUS_HELP[w.status] || '')}</small></td>
    <td><small>From</small> ${esc(w.startBoundary.label)} — ${esc(w.startBoundary.value)} ${badge(w.startBoundary.status)} ${link(w.startBoundary.source, 'source ↗')}
        <small>To</small> ${esc(w.endBoundary.label)} — ${esc(w.endBoundary.value)} ${badge(w.endBoundary.status)} ${link(w.endBoundary.source, 'source ↗')}</td>
  </tr>`).join('');
  return `<div class="tablewrap"><table><thead><tr>
    <th>Year</th><th>Rule set</th><th>Clear run</th><th>Days</th><th>Length test</th><th>Status</th><th>Boundary evidence</th>
  </tr></thead><tbody>${rows}</tbody></table></div>`;
}

function anchorsTable(data) {
  const order = { VERIFIED: 0, REPORTED: 1, ESTIMATED: 2, UNRELEASED: 3 };
  const rows = [...data.anchors].sort((a, b) => a.year - b.year || order[a.status] - order[b.status] || a.id.localeCompare(b.id));
  return `<div class="tablewrap"><table><thead><tr>
    <th>Year</th><th>League</th><th>Anchor</th><th>Value</th><th>Status</th><th>Why it has this status</th><th>Source</th>
  </tr></thead><tbody>${rows.map(a => `<tr>
    <td>${a.year}</td>
    <td>${esc(a.league)}</td>
    <td><strong>${esc(a.label)}</strong></td>
    <td>${a.value ? esc(a.value) : '<span class="muted">left blank — not released</span>'}</td>
    <td>${badge(a.status)}</td>
    <td><small>${esc(a.statusNote || '')}</small></td>
    <td>${link(a.source)}${a.extraSource ? `<small>${link(a.extraSource, esc(a.extraSourceLabel || 'Second source ↗'))}</small>` : ''}<small>Checked ${esc(a.checked)}</small></td>
  </tr>`).join('')}</tbody></table></div>`;
}

function dayByDay(data) {
  const d = data.ladder2027DayByDay;
  const pad = [];
  const dow = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const header = dow.map(x => `<span class="hdow">${x}</span>`).join('');
  const first = new Date(d.window.start + 'T12:00:00Z').getUTCDay();
  for (let i = 0; i < first; i++) pad.push('<span></span>');
  const cells = d.days.map(x => {
    const cls = x.mlbGames === 0 ? 'open' : (x.priorityGames ? 'busy' : '');
    const title = x.mlbGames === 0
      ? 'No MLB game in the official 2027 snapshot'
      : `${x.mlbGames} MLB game(s)${x.priorityGames ? ` · ${x.priorityGames} Giants/Athletics` : ''}`;
    return `<span class="${cls}" title="${esc(title)}">${new Date(x.date + 'T12:00:00Z').getUTCDate()}<small>${x.mlbGames || ''}</small></span>`;
  }).join('');
  const rows = d.days.map(x => `<tr>
    <td>${pretty(x.date)}<small>${esc(x.weekday)}</small></td>
    <td><strong>${x.mlbGames}</strong><small>${x.kinds.length ? esc(x.kinds.join(', ')) : 'no games in the official snapshot'}</small></td>
    <td>${x.giants ? '<span class="priority" aria-label="High priority">★</span> Giants' : ''}${x.giants && x.athletics ? '<br>' : ''}${x.athletics ? '<span class="priority" aria-label="High priority">★</span> Athletics' : ''}${!x.giants && !x.athletics ? '<span class="muted">—</span>' : ''}</td>
    <td>${x.sample ? esc(x.sample) : '<span class="muted">—</span>'}</td>
    <td>${x.source ? link(x.source, 'MLB feed ↗') : '<span class="muted">No rows returned</span>'}</td>
  </tr>`).join('');
  return `<style>
    .ywdays{display:grid;grid-template-columns:repeat(7,1fr);gap:5px;margin:16px 0}
    .ywdays span{aspect-ratio:1.1;display:grid;place-items:center;align-content:center;font-size:11px;border-radius:5px;background:#eff5f0;color:#7e9689;line-height:1.1}
    .ywdays span small{font-size:8px;opacity:.85}
    .ywdays span.open{background:#34735d;color:#fff}
    .ywdays span.busy{background:#eac6b5;color:#753c27}
    .ywdays span.hdow{background:none;color:#63777a;font-size:9px;letter-spacing:.6px;text-transform:uppercase;aspect-ratio:auto}
  </style>
  <div class="panel">
    <div class="panel-pad"><h2>${range(d.window.start, d.window.end)} — ${d.window.days} days</h2>
      <p class="muted">The only 2027 period long enough for a real trip. ${d.daysWithZeroMlbGames} of its ${d.window.days} days have <strong>zero</strong> MLB games in the official 2027 snapshot (${range(d.window.start, '2027-02-18')}). The other ${d.window.days - d.daysWithZeroMlbGames} days are spring training: ${d.daysWithGiantsOrAthletics} of them include a Giants or Athletics game. Nothing else in the brief — no NFL game, no Westwood One slot, no Stanford or Cal football — occupies this period, because the NFL season ends with Super Bowl LXI on Feb 14, 2027 and the 2027 NFL schedule does not begin until August.</p>
      <div class="ywdays" role="img" aria-label="February 15 to March 23 2027 grid; the first four days have no MLB games">${header}${pad.join('')}${cells}</div>
      <p class="footnote">Dark cells = no MLB game in the official snapshot. Number = MLB games that day. Orange = a Giants or Athletics game.</p>
    </div>
    <div class="tablewrap"><table><thead><tr><th>Date</th><th>MLB games</th><th>High priority</th><th>Example</th><th>Verification</th></tr></thead><tbody>${rows}</tbody></table></div>
  </div>`;
}

function quietRuns(data) {
  const rows = data.mlbOnlyQuietRuns2027.map(r => `<tr>
    <td>${range(r.start, r.end)}</td>
    <td><strong>${r.days}</strong>${r.daysIfConflictResolvedAsBusy != null ? `<small>${r.daysIfConflictResolvedAsBusy} if the conflicting date is busy</small>` : ''}</td>
    <td>${badge(r.status)}</td>
    <td><small>${esc(r.note || 'No MLB game appears in the official 2027 snapshot on these dates.')}</small></td>
    <td>${link(`https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate=${r.start}&endDate=${r.end}`, 'MLB feed ↗')}</td>
  </tr>`).join('');
  return `<div class="tablewrap"><table><thead><tr><th>Run</th><th>Days</th><th>Status</th><th>Reading</th><th>Source</th></tr></thead><tbody>${rows}</tbody></table></div>`;
}

async function boot() {
  const root = document.getElementById('content');
  try {
    const res = await fetch('data/projections.json');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    const m = data.meta;
    root.innerHTML = `
      <div class="eyebrow">MULTI-YEAR VACATION WINDOWS · 2027 · 2028 · 2029</div>
      <div class="headrow">
        <div><h1>When can you actually get away?</h1>
          <p class="lede">One page, every year, with the rule applied exactly as written — and with an honest side-by-side of what each relaxation would buy you. Every number on this page is labelled VERIFIED, REPORTED, ESTIMATED or UNRELEASED.</p></div>
        <span class="badge green">Checked ${esc(m.generated)} · Outer Sunset 94122 · Pacific time</span>
      </div>

      <div class="note"><strong>The verdict.</strong> ${esc(m.headline)}</div>

      ${metrics(data)}

      <div class="section-head"><h2>The answer, rule by rule</h2><a href="sources.html">How evidence and estimates work →</a></div>
      <div class="panel">${answersTable(data)}</div>

      <div class="section-head"><h2>The 2027 candidate, day by day</h2><a href="schedule.html">Open the daily schedule →</a></div>
      ${dayByDay(data)}

      <div class="section-head"><h2>Quiet runs inside the official 2027 MLB feed</h2></div>
      <p class="muted">These are the only stretches of the 2027 official MLB snapshot with no games at all. Two of them are coverage gaps, not free time.</p>
      <div class="panel">${quietRuns(data)}</div>

      <div class="section-head"><h2>Every anchor this page depends on</h2><span class="footnote">${data.anchors.length} facts · sorted by year, then by evidence strength</span></div>
      <div class="panel">${anchorsTable(data)}</div>

      <div class="note"><strong>Coverage gaps that limit every number above.</strong>
        <ul>
          <li><strong>2027 MLB postseason is not in the official feed.</strong> The snapshot stops at the last regular-season day, Sep 26, 2027. October 2027 is treated as BUSY, not free. The 2026 snapshot did carry postseason rows, so this is a gap, not an off-season.</li>
          <li><strong>2027 NFL Week 18 (Jan 9–10, 2027) is missing from the stored snapshot.</strong> NFL Football Operations lists the week; 49ers.com lists San Francisco's Week 18 game at Arizona as TBD. 24 games, including the 49ers', have no date or kickoff in the feed.</li>
          <li><strong>No 2027 NFL schedule exists yet.</strong> Everything from August 2027 onward is ESTIMATED until the league releases it, normally in May.</li>
          <li><strong>2028 and 2029 MLB schedules do not exist.</strong> The MLB Stats API returns zero rows for both. Every 2028 and 2029 date on this page is a projection, clearly marked ESTIMATED.</li>
          <li><strong>Super Bowl LXII's date is reported, not tabled.</strong> NFL.com confirms Atlanta as host but lists the date as TBA; the Feb 13, 2028 date comes from ESPN and Pro Football Talk. Super Bowl LXIII's Las Vegas host is official; its Feb 11, 2029 date is a projection.</li>
          <li><strong>Stanford and Cal 2027 opponents are announced, dates are not.</strong> Late August through November 2027 cannot be scored day by day yet.</li>
          <li><strong>Game schedules are not radio schedules.</strong> A fixture proves a game is played, not that it reaches an AM/FM radio in 94122. See the <a href="radio.html">radio guide</a> and <a href="core-scope.html">scope &amp; AM/FM proof</a> pages.</li>
        </ul>
      </div>

      <div class="panel panel-pad">
        <h2>What this means for a 1-, 2- or 3-week trip</h2>
        <p class="muted">Under the rule exactly as written, the longest clean run in any of the three years is <strong>4 days</strong>. That is not a coverage artefact: MLB spring training starts four or five days after the Super Bowl in every year, and the NFL season runs continuously from August until the Super Bowl, so the calendar has no unoccupied week anywhere between late February and mid-February of the following year.</p>
        <p class="muted">The single decision that changes the answer is whether MLB spring training counts. If it does not, <strong>Feb 15 – Mar 23, 2027 (37 days)</strong> opens up, bounded at both ends by official dates: Super Bowl LXI on Feb 14, 2027 (NFL Football Operations) and MLB Opening Night on Mar 24, 2027 (MLB.com). You would miss Giants and Athletics spring-training broadcasts on 32 of those 37 days, and Golden State Warriors and Cal basketball remain on Bay Area AM/FM regardless. The 2028 and 2029 equivalents are the same shape but rest on projected dates.</p>
        <p><a href="vacations.html">Compare vacation lengths →</a> · <a href="review.html">Flagged for review →</a> · <a href="sources.html">Sources and duration assumptions →</a></p>
      </div>
      ${foot()}`;
  } catch (e) {
    root.innerHTML = `<div class="eyebrow">MULTI-YEAR VACATION WINDOWS</div><h1>Data unavailable</h1>
      <div class="note">${esc(e.message)} — site/data/projections.json could not be loaded. No window conclusion is available.</div>
      <button onclick="location.reload()">Try again</button>`;
  }
}

boot();
