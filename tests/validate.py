import pathlib,json,datetime,urllib.parse,unittest,re
R=pathlib.Path(__file__).resolve().parents[1]
ALLOWED=[
 'statsapi.mlb.com','www.mlb.com','www.nfl.com','media.nfl.com','operations.nfl.com',
 'www.49ers.com','www.westwoodonesports.com','calbears.com','gostanford.com','usfdons.com',
 'www.nba.com','cdn.nba.com','www.sjearthquakes.com','valkyries.wnba.com','www.nhl.com',
 'www.thesportsleader.com','talk960.iheart.com',
]
class Validate(unittest.TestCase):
 def _check_event_row(self,row,ids):
  self.assertTrue(row['source'].startswith('https://'))
  if 'id' not in row:return
  self.assertNotIn(row['id'],ids);ids.add(row['id'])
  if row['start']:self.assertIsNotNone(datetime.datetime.fromisoformat(row['start'].replace('Z','+00:00')).tzinfo)
  if row['date']:datetime.date.fromisoformat(row['date'])
  self.assertIn(urllib.parse.urlparse(row['source']).hostname,ALLOWED)
  if row['station']:self.assertTrue(row['radioSource'])
 def test_data(self):
  ids=set()
  for file in sorted((R/'site/data').glob('*.json')):
   rows=json.loads(file.read_text())
   if isinstance(rows,list):
    for row in rows:self._check_event_row(row,ids)
   elif file.name=='expanded-official.json':
    for row in rows['events']:self._check_event_row(row,ids)
 def test_internal_links(self):
  for file in (R/'site').glob('*.html'):
   for url in re.findall(r'(?:href|src)="([^"]+)"',file.read_text()):
    if url.startswith(('http','#')):continue
    self.assertTrue((file.parent/url.split('?')[0].split('#')[0]).is_file(),f'{file}: {url}')
 def test_counts(self):
  for c in json.loads((R/'site/data/coverage.json').read_text()):
   if c['count'] is not None:self.assertEqual(c['count'],len(json.loads((R/f"site/data/mlb-{c['year']}.json").read_text())))
 def test_clubs(self):
  rows=json.loads((R/'site/data/mlb-2027.json').read_text());clubs={t for r in rows if r['kind']=='Regular Season' for t in r['teams']}
  self.assertEqual(len(clubs),30)
 def test_westwood(self):
  rows=json.loads((R/'site/data/curated.json').read_text())
  self.assertEqual(len([r for r in rows if r['kind']=='Westwood One' and r['league']=='NFL']),46)
 def test_research(self):
  data=json.loads((R/'site/data/research.json').read_text())
  for kind in ['sources','stations','flags']:
   for row in data[kind]:self.assertTrue(row['source'].startswith('https://'))
if __name__=='__main__':unittest.main()
