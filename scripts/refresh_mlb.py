"""Import only official MLB schedule fields. Empty years are not complete calendars."""
import json, urllib.request, datetime, pathlib, time
OUT=pathlib.Path('site/data'); OUT.mkdir(parents=True,exist_ok=True)
report=[]
for year in range(2026,2030):
    url=f'https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate={year}-01-01&endDate={year}-12-31'
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'VacationPlanner/1.0'})
        with urllib.request.urlopen(req,timeout=120) as r: raw=json.load(r)
        events=[]
        for day in raw.get('dates',[]):
            for g in day['games']:
                away=g['teams']['away']['team']; home=g['teams']['home']['team']
                tbd=g['status'].get('startTimeTBD',False)
                events.append(dict(id='mlb-'+str(g['gamePk']),date=g['officialDate'],start=None if tbd else g['gameDate'],away=away['name'],home=home['name'],awayId=away['id'],homeId=home['id'],sport='MLB',phase=g.get('seriesDescription',g['gameType']),priority=bool({away['id'],home['id']}&{133,137}),source=f"https://www.mlb.com/gameday/{g['gamePk']}/preview",status=g['status']['detailedState'],radio=None,radioSource=None,timeKind='TBD' if tbd else 'Scheduled start',checked=datetime.datetime.now(datetime.timezone.utc).isoformat()))
        (OUT/f'mlb-{year}.json').write_text(json.dumps(events,separators=(',',':'))+'\n')
        report.append(dict(year=year,count=len(events),tbd=sum(e['start'] is None for e in events),source=url,checked=datetime.datetime.now(datetime.timezone.utc).isoformat(),complete=False,note='API snapshot; not a guarantee that postseason, exhibitions or radio listings are complete.'))
        print(year,len(events),'games')
    except Exception as e:
        report.append(dict(year=year,count=None,source=url,error=str(e),complete=False))
        print(year,'FAILED',e)
(OUT/'mlb-coverage.json').write_text(json.dumps(report,indent=2)+'\n')
if all(r['count'] is None for r in report): raise SystemExit('All official MLB requests failed')
