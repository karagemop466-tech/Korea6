"""Transcribed official records reviewed 2026-11-03. Unknown fields stay null."""
import json,pathlib,datetime
from zoneinfo import ZoneInfo
D=pathlib.Path(__file__).resolve().parents[1]/'site/data'
rows=[]
def add(id,date,time,title,league,source,station=None,radio=None,kind='Regular season',basis='Kickoff',priority=True,note=''):
 start=datetime.datetime.fromisoformat(date+'T'+time).replace(tzinfo=ZoneInfo('America/Los_Angeles')).isoformat() if date and time else None
 rows.append(dict(id=id,date=date,start=start,title=title,league=league,source=source,station=station,radioSource=radio or (source if station else None),kind=kind,timeBasis=basis,priority=priority,status='Scheduled',checked='2026-11-03',note=note))
ww='https://www.westwoodonesports.com/events/'
# Times below are network airtimes converted from ET to PT, NOT kickoff.
wwrows='''1105|16:30|Jacksonville Jaguars at Baltimore Ravens|548561
1108|16:30|Tampa Bay Buccaneers at Chicago Bears|548500
1112|16:30|Washington Commanders at New York Giants|548562
1115|16:30|Pittsburgh Steelers at Cincinnati Bengals|548501
1119|16:30|Indianapolis Colts at Houston Texans|548564
1123|16:00|Cincinnati Bengals at Washington Commanders|548543
1126|09:30|Chicago Bears at Detroit Lions|548512
1126|17:00|Kansas City Chiefs at Buffalo Bills|548514
1129|16:30|New England Patriots at Los Angeles Chargers|548502
1203|16:30|Kansas City Chiefs at Los Angeles Rams|548566
1207|16:00|Dallas Cowboys at Seattle Seahawks|548545
1213|16:30|Buffalo Bills at Green Bay Packers|548505
1217|16:30|San Francisco 49ers at Los Angeles Chargers|548568
1219|17:00|Chicago Bears at Buffalo Bills|548518
1221|16:00|New England Patriots at Kansas City Chiefs|548548
1225|09:30|Green Bay Packers at Chicago Bears|548528
1225|17:00|Los Angeles Rams at Seattle Seahawks|548534
1226|17:00|Week 16 Saturday Doubleheader TBA|548520
1228|16:00|New York Giants at Detroit Lions|548550
0102|13:00|Week 17 Saturday Doubleheader TBA|548521
0103|16:30|Philadelphia Eagles at San Francisco 49ers|548509
0109|09:30|Week 18 Saturday Tripleheader TBA|548523
0109|17:00|Week 18 Saturday Tripleheader TBA|548526
1108|06:15|Cincinnati Bengals vs Atlanta Falcons|548489
1109|16:00|Buffalo Bills at Minnesota Vikings|548541
1115|06:15|New England Patriots vs Detroit Lions|548490
1116|16:00|Los Angeles Chargers at Baltimore Ravens|548542
1122|16:30|Minnesota Vikings vs San Francisco 49ers|548491
1125|16:30|Green Bay Packers at Los Angeles Rams|548511
1126|13:15|Philadelphia Eagles at Dallas Cowboys|548513
1127|11:30|Denver Broncos at Pittsburgh Steelers|548515
1130|16:00|Carolina Panthers at Tampa Bay Buccaneers|548544
1206|16:30|Houston Texans at Pittsburgh Steelers|548503
1210|16:30|Minnesota Vikings at New England Patriots|548567
1214|16:00|Pittsburgh Steelers at Jacksonville Jaguars|548546
1219|13:30|Seattle Seahawks at Philadelphia Eagles|548517
1220|16:30|Detroit Lions at Minnesota Vikings|548506
1224|16:30|Houston Texans at Philadelphia Eagles|548569
1225|13:15|Buffalo Bills at Denver Broncos|548531
1226|13:00|Week 16 Saturday Doubleheader TBA|548519
1227|16:30|Jacksonville Jaguars at Dallas Cowboys|548507
1231|16:30|Baltimore Ravens at Cincinnati Bengals|548570
0102|17:00|Week 17 Saturday NFL Doubleheader TBA|548522
0104|16:00|Houston Texans at Green Bay Packers|548552
0109|13:15|Week 18 Saturday Tripleheader TBA|548524
0110|16:30|Week 18 Sunday Night Football - Teams TBA|548510'''
for line in wwrows.splitlines():
 md,t,title,id=line.split('|');date=('2027' if md[:2]=='01' else '2026')+'-'+md[:2]+'-'+md[2:]
 add('ww-'+id,date,t,title,'NFL',ww+id,kind='Westwood One',basis='Network airtime',note='National broadcast verified; Bay Area game-specific carriage unverified. Not a kickoff time.')
add('ww-557143','2026-11-07','12:00','Oregon at Ohio State','NCAAF',ww+'557143',kind='Westwood One',basis='Network airtime',note='Local carriage unverified.')
sf='https://www.49ers.com/schedule/'
for md,t,title in [('1108','13:25','Las Vegas Raiders at San Francisco 49ers'),('1115','13:25','San Francisco 49ers at Dallas Cowboys'),('1122','17:20','Minnesota Vikings vs San Francisco 49ers'),('1129','13:25','Seattle Seahawks at San Francisco 49ers'),('1206','10:00','San Francisco 49ers at New York Giants'),('1213','13:25','Los Angeles Rams at San Francisco 49ers'),('1217','17:15','San Francisco 49ers at Los Angeles Chargers'),('1227','13:25','San Francisco 49ers at Kansas City Chiefs'),('0103','17:20','Philadelphia Eagles at San Francisco 49ers')]:
 date=('2027' if md[:2]=='01' else '2026')+'-'+md[:2]+'-'+md[2:]
 add('sf-'+md,date,t,title,'NFL',sf,'KSAN 107.7 FM / KNBR 104.5 FM / 680 AM')
add('sf-week18',None,None,'San Francisco 49ers at Arizona Cardinals','NFL',sf,'KSAN 107.7 FM / KNBR 104.5 FM / 680 AM',note='Week 18: date and time TBD; cannot place on a day.')
cal='https://calbears.com/sports/football/schedule/2026'
stan='https://gostanford.com/sports/football/schedule'
stanradio='https://gostanford.com/news/2026/07/30/2026-football-radio-broadcast-team-announced'
for date,time,title,station in [('2026-11-14','12:30','California at Virginia','KSFO 810 AM'),('2026-11-21',None,'Stanford at California','KNBR 104.5 FM / 680 AM'),('2026-11-28',None,'Pittsburgh at California','KSFO 810 AM')]:
 add('cal-'+date,date,time,title,'NCAAF',cal,station)
for date,title,note in [('2026-11-14','Stanford at Virginia Tech','Source says 4 OR 4:30 P.M.; single kickoff not confirmed.'),('2026-11-28','SMU at Stanford','Kickoff TBA.')]:
 add('stan-'+date,date,None,title,'NCAAF',stan,kind='Regular season',note=note+' Season radio partner: KTCT 1050 AM; game-level assignment not confirmed.')
ops='https://operations.nfl.com/calendar-events/nfl-important-dates'
for date,title in [('2027-01-16','Wild Card Weekend'),('2027-01-17','Wild Card Weekend'),('2027-01-18','Wild Card Weekend'),('2027-01-23','Divisional Playoffs'),('2027-01-24','Divisional Playoffs'),('2027-01-31','AFC and NFC Championship Games'),('2027-02-14','Super Bowl LXI')]:
 add('nfl-date-'+date,date,None,title,'NFL',ops,kind='Postseason date window',note='Official date/window only. Matchups, game count, kickoff and local station not verified.')
nba='https://www.nba.com/warriors/schedule'
for date,time,title in [('2026-11-05','19:00','Miami Heat at Golden State Warriors'),('2026-11-07','17:30','Orlando Magic at Golden State Warriors'),('2026-11-09','19:00','New Orleans Pelicans at Golden State Warriors'),('2026-11-11','18:30','Golden State Warriors at Houston Rockets'),('2026-11-13','18:30','Golden State Warriors at San Antonio Spurs'),('2026-11-16','17:00','Golden State Warriors at New Orleans Pelicans')]:
 add('gsw-'+date,date,time,title,'NBA',nba,'KGMZ 95.7 FM',basis='Tipoff',note='Partial Warriors schedule only; remaining games not yet imported.')
D.mkdir(exist_ok=True,parents=True)
(D/'curated.json').write_text(json.dumps(rows,indent=2))
