import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const read = p => JSON.parse(readFileSync(resolve(root, p), 'utf8'));

const data = read('site/data/projections.json');
const STATUSES = new Set(['VERIFIED', 'REPORTED', 'ESTIMATED', 'UNRELEASED', 'UNKNOWN', 'CONFLICT']);
const iso = /^\d{4}-\d{2}-\d{2}$/;

test('every anchor carries a source, a known status and parseable dates', () => {
  assert.ok(data.anchors.length >= 20);
  const ids = new Set();
  for (const a of data.anchors) {
    assert.ok(a.id, 'anchor id');
    assert.ok(!ids.has(a.id), `duplicate anchor id ${a.id}`);
    ids.add(a.id);
    assert.ok(STATUSES.has(a.status), `${a.id} status ${a.status}`);
    assert.ok(a.source && a.source.startsWith('https://'), `${a.id} source`);
    assert.ok(a.statusNote, `${a.id} statusNote`);
    if (a.date !== null) assert.match(a.date, iso, `${a.id} date`);
    if (a.endDate) assert.match(a.endDate, iso, `${a.id} endDate`);
    // UNRELEASED anchors must never carry a value.
    if (a.status === 'UNRELEASED') assert.equal(a.value, null, `${a.id} must stay blank`);
  }
});

test('no ESTIMATED or REPORTED value is presented as verified', () => {
  for (const a of data.anchors) {
    if (a.status === 'ESTIMATED' || a.status === 'REPORTED') {
      assert.ok(a.statusNote.length > 40, `${a.id} must explain why it is ${a.status}`);
    }
  }
});

test('windows are consistent with their boundaries', () => {
  assert.equal(data.windows.length, 15); // 3 years x 5 rule sets
  for (const w of data.windows) {
    const start = new Date(w.start + 'T12:00:00Z');
    const end = new Date(w.end + 'T12:00:00Z');
    assert.equal(w.days, Math.round((end - start) / 86400000) + 1, `${w.year}/${w.ruleSet} day count`);
    assert.ok(w.startBoundary.source.startsWith('https://'));
    assert.ok(w.endBoundary.source.startsWith('https://'));
    assert.ok(STATUSES.has(w.status));
    // The strict rule must never produce a 7-day run in any year.
    if (w.ruleSet === 'strict') assert.equal(w.meetsOneWeek, false, `${w.year} strict must not reach a week`);
  }
});

test('the 2027 strict window is Feb 15-18 and is bounded by verified official dates', () => {
  const w = data.windows.find(x => x.year === 2027 && x.ruleSet === 'strict');
  assert.equal(w.start, '2027-02-15');
  assert.equal(w.end, '2027-02-18');
  assert.equal(w.days, 4);
  assert.equal(w.status, 'VERIFIED');
  assert.equal(w.startBoundary.value, '2027-02-14'); // Super Bowl LXI
  assert.equal(w.endBoundary.value, '2027-02-19');   // MLB spring training opens
});

test('the relaxed 2027 window runs from Super Bowl LXI to MLB Opening Night', () => {
  const w = data.windows.find(x => x.year === 2027 && x.ruleSet === 'no-spring');
  assert.equal(w.start, '2027-02-15');
  assert.equal(w.end, '2027-03-23');
  assert.equal(w.days, 37);
  assert.equal(w.status, 'VERIFIED');
  assert.equal(w.endBoundary.value, '2027-03-24'); // MLB Opening Night
  assert.equal(w.meetsOneWeek, true);
});

test('day-by-day table matches the stored official MLB 2027 snapshot', () => {
  const mlb = read('site/data/mlb-2027.json');
  const counts = new Map();
  for (const g of mlb) if (g.date) counts.set(g.date, (counts.get(g.date) || 0) + 1);
  const d = data.ladder2027DayByDay;
  assert.equal(d.window.start, '2027-02-15');
  assert.equal(d.window.end, '2027-03-23');
  assert.equal(d.window.days, 37);
  for (const row of d.days) {
    assert.equal(row.mlbGames, counts.get(row.date) || 0, `${row.date} MLB game count`);
    if (row.mlbGames > 0) assert.ok(row.source.startsWith('https://statsapi.mlb.com/'));
  }
  // Feb 15-18 must be the only zero-game days at the head of the window.
  assert.equal(d.days.slice(0, 4).every(x => x.mlbGames === 0), true);
  assert.equal(d.daysWithZeroMlbGames, 4);
  assert.equal(d.daysWithGiantsOrAthletics + 4 <= 37, true);
});

test('quiet-run table flags the postseason coverage gap rather than calling it free', () => {
  const runs = data.mlbOnlyQuietRuns2027;
  const tail = runs.find(r => r.end === '2027-12-31');
  assert.ok(tail, 'the Sep 27 - Dec 31 run must be present');
  assert.equal(tail.status, 'UNKNOWN');
  assert.match(tail.note, /postseason/i);
  // Jul 13 is the All-Star Game and must never appear inside a quiet run.
  for (const r of runs) {
    assert.ok(!(r.start <= '2027-07-13' && '2027-07-13' <= r.end), 'All-Star Game date leaked into a quiet run');
  }
});
