"""Import only official MLB records; fail visibly, never fabricate schedules."""
import json, urllib.request, datetime, pathlib, concurrent.futures
ROOT=pathlib.Path(__file__).resolve().parents[1]
D=ROOT/'site/data'
D.mkdir(parents=True,exist_ok=True)
def get(year):
    url=f'https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate={year}-01-01&endDate={year}-12-31'
    req=urllib.request.Request(url,headers={'User-Agent':'FreeTimeVacation/1.0'})
    checked=datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        with urllib.request.urlopen(req,timeout=90) as r: raw=json.load(r)
        games=[]
        for day in raw['dates']:
            for g in day['games']:
                a=g['teams']['away']['team'];h=g['teams']['home']['team']
                games.append(dict(id=f"mlb-{g['gamePk']}-{g['gameDate']}-{g['status']['statusCode']}",gameId=g['gamePk'],date=g['officialDate'],start=None if g['status'].get('startTimeTBD',True) else g['gameDate'],title=a['name']+' at '+h['name'],league='MLB',kind=g.get('seriesDescription',g['gameType']),priority=a['id'] in (137,133) or h['id'] in (137,133),teams=[a['name'],h['name']],source=f"https://statsapi.mlb.com/api/v1/schedule?gamePk={g['gamePk']}",status=g['status']['detailedState'],station=None,radioSource=None,timeBasis='First pitch',checked=checked))
        assert len(games)==raw['totalGames']
        (D/f'mlb-{year}.json').write_text(json.dumps(games,separators=(',',':')))
        return dict(year=year,count=len(games),source=url,checked=checked,status='imported' if games else 'empty response — not evidence of no games')
    except Exception as e:
        return dict(year=year,count=None,source=url,checked=checked,status='fetch failed',error=str(e))
if __name__=='__main__':
    results=list(concurrent.futures.ThreadPoolExecutor(4).map(get,range(2026,2030)))
    (D/'coverage.json').write_text(json.dumps(results,indent=2))
    print(json.dumps(results,indent=2))
