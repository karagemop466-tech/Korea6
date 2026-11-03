"""Read NFL's rendered schedule state; only game cards with explicit ISO times.
Unknown card layouts are a coverage failure, not proof of a free day.
"""
import json,re,datetime,urllib.request,pathlib,concurrent.futures
from zoneinfo import ZoneInfo
D=pathlib.Path(__file__).resolve().parents[1]/'site/data'
def walk(o):
 if isinstance(o,dict):
  yield o
  for v in o.values():yield from walk(v)
 elif isinstance(o,list):
  for v in o:yield from walk(v)
def extract(raw,url):
 texts=[]
 for m in re.finditer(r'self\.__next_f\.push\((.*?)\)</script>',raw):
  try:
   val=json.loads(m[1]);texts.append(val[1] if len(val)>1 and isinstance(val[1],str) else '')
  except (ValueError,TypeError):pass
 records={}
 roots={}
 for line in ''.join(texts).splitlines():
  try:
   key,value=line.split(':',1);roots[key]=json.loads(value)
  except (ValueError,IndexError):pass
 def resolve(v):
  for _ in range(12):
   if not isinstance(v,str) or not v.startswith('$') or ':' not in v:break
   try:
    keys=v[1:].split(':');v=roots[keys[0]]
    for k in keys[1:]:v=v[int(k)] if isinstance(v,list) else v[k]
   except (KeyError,IndexError,ValueError,TypeError):return None
  return v
 for line in ''.join(texts).splitlines():
  try:root=json.loads(line.split(':',1)[1])
  except (ValueError,IndexError):continue
  for o in walk(root):
   if all(k in o for k in ('id','time','homeTeam','awayTeam','seasonType','externalIds')):
    home=resolve(o['homeTeam']);away=resolve(o['awayTeam'])
    if not isinstance(home,dict) or not isinstance(away,dict):continue
    home=resolve(home.get('fullName'));away=resolve(away.get('fullName'))
    if not home or not away:continue
    stamp=o.get('time');dt=None
    try:dt=datetime.datetime.fromisoformat(stamp.replace('Z','+00:00'))
    except (AttributeError,ValueError):pass
    if dt and not dt.tzinfo:dt=None
    ext=resolve(o['externalIds']) or []
    slug=next((x['id'] for x in ext if isinstance(x,dict) and x.get('source')=='slug'),None)
    if not slug:continue
    records[o['id']]=dict(id='nfl-'+o['id'],date=dt.astimezone(ZoneInfo('America/Los_Angeles')).date().isoformat() if dt else None,start=stamp if dt else None,title=away+' at '+home,league='NFL',kind='Preseason' if o['seasonType']=='PRE' else 'Regular season',priority='49ers' in away+home,teams=[away,home],source='https://www.nfl.com/games/'+slug,station=None,radioSource=None,timeBasis='Kickoff',status=o.get('status','Unknown'),checked=datetime.datetime.now(datetime.timezone.utc).isoformat(),note='Official NFL schedule record; local radio carriage unverified.')
    continue
   if not all(k in o for k in ('gameTime','homeTeam','awayTeam','href','gameId')):continue
   a=o['awayTeam'];h=o['homeTeam']
   if not isinstance(a,dict) or not isinstance(h,dict):continue
   away=a.get('abbreviationScreenReaderText');home=h.get('abbreviationScreenReaderText')
   if not away or not home:continue
   href=o['href']
   if not isinstance(href,str) or not href.startswith('/games/'):continue
   stamp=o['gameTime'];dt=None
   try:dt=datetime.datetime.fromisoformat(stamp.replace('Z','+00:00'))
   except (AttributeError,ValueError):pass
   # Only explicit, timezone-aware times; don't invent a date for unplaced cards.
   if dt and not dt.tzinfo:dt=None
   tbd=any(o.get(k) is True for k in ('isTimeTBD','isDateTBD','timeTbd','dateTbd')) or 'TBD' in str(o.get('variant',''))
   records[o['gameId']]=dict(id='nfl-'+o['gameId'],date=dt.astimezone(ZoneInfo('America/Los_Angeles')).date().isoformat() if dt else None,start=stamp if dt and not tbd else None,title=away+' at '+home,league='NFL',kind='Preseason' if '-pre-' in href else 'Regular season',priority='49ers' in away+home,teams=[away,home],source='https://www.nfl.com'+href,station=None,radioSource=None,timeBasis='Kickoff',status=o.get('variant','Unknown'),checked=datetime.datetime.now(datetime.timezone.utc).isoformat(),note='Official NFL game card; local radio carriage unverified.')
 return list(records.values())
def get(slug):
 url='https://www.nfl.com/schedules/2026/by-week/'+slug
 try:
  raw=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=60).read().decode()
  rows=extract(raw,url)
  # Score-strip records may repeat other weeks; IDs deduplicate across all pages.
  return rows,dict(source=url,count=len(rows),status='parsed' if rows else 'no supported cards — needs review')
 except Exception as e:return [],dict(source=url,count=None,status='failed',error=str(e))
if __name__=='__main__':
 slugs=['hall-of-fame-game']+[f'preseason-week-{i}' for i in range(1,4)]+[f'week-{i}' for i in range(1,19)]
 rows={};audit=[]
 for games,info in concurrent.futures.ThreadPoolExecutor(4).map(get,slugs):
  audit.append(info)
  for g in games:rows[g['id']]=g
 (D/'nfl-2026.json').write_text(json.dumps(list(rows.values()),separators=(',',':')))
 (D/'nfl-coverage.json').write_text(json.dumps(audit,indent=2))
 print(len(rows),'NFL game cards imported')
