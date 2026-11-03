import urllib.request,pathlib
for name,url in [('nfl','https://www.nfl.com/schedules/2026/reg1/'),('49ers','https://www.49ers.com/schedule/'),('nba','https://cdn.nba.com/static/json/staticData/scheduleLeagueV2.json')]:
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  raw=urllib.request.urlopen(req,timeout=30).read().decode()
  pathlib.Path(f'site/data/probe-{name}.txt').write_text(raw)
 except Exception as e:pathlib.Path(f'site/data/probe-{name}.txt').write_text(str(e))
