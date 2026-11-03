import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const DATA_DIR = path.join(ROOT, 'site', 'data');

const OFFICIAL_HOSTS = new Set([
  'www.nba.com',
  'cdn.nba.com',
  'calbears.com',
  'usfdons.com',
  'gostanford.com',
  'www.westwoodonesports.com',
  'www.sjearthquakes.com',
  'valkyries.wnba.com',
  'www.nhl.com',
  'www.mlb.com',
  'statsapi.mlb.com',
  'www.nfl.com',
  'media.nfl.com',
  'operations.nfl.com',
  'www.49ers.com',
  'www.thesportsleader.com',
  'talk960.iheart.com',
]);

const loadJson = name => JSON.parse(fs.readFileSync(path.join(DATA_DIR, name), 'utf8'));

test('expanded-official.json uses only trusted primary sources and unique global IDs', () => {
  const exp = loadJson('expanded-official.json');
  assert.ok(exp.events.length >= 170, 'expected >=170 verified expansion events');
  assert.equal(exp.meta.eventCount, exp.events.length);

  const baselineIds = new Set();
  for (const fname of ['mlb-2026.json', 'mlb-2027.json', 'nfl-2026.json', 'curated.json']) {
    for (const row of loadJson(fname)) baselineIds.add(row.id);
  }

  const seenExp = new Set();
  const ptFmt = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'America/Los_Angeles',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  });

  for (const r of exp.events) {
    assert.ok(r.id && !seenExp.has(r.id), `duplicate expansion id: ${r.id}`);
    assert.ok(!baselineIds.has(r.id), `collision with baseline dataset id: ${r.id}`);
    seenExp.add(r.id);

    const srcHost = new URL(r.source).hostname;
    assert.ok(OFFICIAL_HOSTS.has(srcHost), `non-primary source host ${srcHost} on ${r.id}`);

    if (r.station !== null) {
      assert.ok(r.radioSource, `missing radioSource when station is set on ${r.id}`);
      const radioHost = new URL(r.radioSource).hostname;
      assert.ok(OFFICIAL_HOSTS.has(radioHost), `non-primary radioSource host ${radioHost} on ${r.id}`);
    }

    if (r.start !== null) {
      assert.match(r.start, /(-08:00|-07:00)$/, `expected Pacific offset on ${r.id}: ${r.start}`);
      const d = new Date(r.start);
      assert.ok(!Number.isNaN(d.getTime()), `invalid ISO start on ${r.id}`);
      assert.equal(ptFmt.format(d), r.date, `Pacific date mismatch on ${r.id}: ${r.start} vs ${r.date}`);
    }
  }
});

test('Pacific DST offset transitions are exact across Nov 2026 and Mar 14, 2027', () => {
  const exp = loadJson('expanded-official.json');
  const byId = new Map(exp.events.map(e => [e.id, e]));

  // Oct 31, 2026 is PDT (-07:00); Nov 2, 2026 is PST (-08:00)
  assert.match(byId.get('cal-fb-2026-10-31').start, /-07:00$/);
  assert.match(byId.get('cal-mbb-2026-11-02').start, /-08:00$/);

  // Mar 12, 2027 is PST (-08:00); Mar 14, 2027 evening is PDT (-07:00)
  assert.match(byId.get('gsw-2027-03-12').start, /-08:00$/);
  assert.match(byId.get('gsw-2027-03-14').start, /-07:00$/);
});

test('Feb 14-20, 2027 two-scope proof holds across MLB + NFL + NCAAF + NBA + NCAAM', () => {
  const mlb27 = loadJson('mlb-2027.json');
  const curated = loadJson('curated.json');
  const exp = loadJson('expanded-official.json');

  const coreEvents = [
    ...mlb27,
    ...curated.filter(r => r.league !== 'NBA'),
    ...exp.events.filter(r => r.corePromptScope),
  ];
  const fullEvents = [...mlb27, ...curated, ...exp.events];

  // Super Bowl LXI on 2027-02-14 and MLB Spring Training Opening Day on 2027-02-19
  assert.ok(coreEvents.some(r => r.date === '2027-02-14' && r.title.includes('Super Bowl LXI')));
  assert.ok(coreEvents.some(r => r.date === '2027-02-19' && r.league === 'MLB'));

  // Core 4-category scope has 0 scheduled games on Feb 15-18 (4 days < 7 days)
  for (const d of ['2027-02-15', '2027-02-16', '2027-02-17', '2027-02-18']) {
    assert.equal(coreEvents.filter(r => r.date === d).length, 0, `expected 0 core games on ${d}`);
  }

  // Full SF 94122 AM/FM scope has verified radio conflicts on Feb 15 and Feb 17
  const feb15 = fullEvents.filter(r => r.date === '2027-02-15');
  assert.ok(feb15.some(r => r.id === 'gsw-2027-02-15' && r.station === 'KGMZ 95.7 FM'));

  const feb17 = fullEvents.filter(r => r.date === '2027-02-17');
  assert.ok(feb17.some(r => r.id === 'cal-mbb-2027-02-17' && r.station === 'KSFO 810 AM'));
  assert.ok(feb17.some(r => r.id === 'gsw-2027-02-17' && r.station === 'KGMZ 95.7 FM'));
  assert.ok(feb17.some(r => r.id === 'usf-mbb-2027-02-17'));
});

test('Pro Bowl discontinuation, 8 terrestrial stations, and digital exclusions are primary-sourced', () => {
  const exp = loadJson('expanded-official.json');
  assert.equal(exp.proBowlFinding.announcementDate, '2026-08-26');
  assert.ok(OFFICIAL_HOSTS.has(new URL(exp.proBowlFinding.source).hostname));
  assert.equal(exp.stations.length, 8);
  for (const s of exp.stations) {
    assert.equal(s.receivable94122, true);
    assert.ok(OFFICIAL_HOSTS.has(new URL(s.source).hostname));
  }
  assert.equal(exp.nonTerrestrialExclusions.length, 2);
  for (const x of exp.nonTerrestrialExclusions) {
    assert.equal(x.terrestrialAmFmIn94122, false);
    assert.ok(OFFICIAL_HOSTS.has(new URL(x.source).hostname));
  }
});
