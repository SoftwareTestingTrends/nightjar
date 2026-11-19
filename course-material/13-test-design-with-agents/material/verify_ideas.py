import sys; sys.path.insert(0,"tests")
from datetime import datetime, time, timezone
from zoneinfo import ZoneInfo
from builders import nights_at
from nightjar.models import User
from nightjar.nudge import next_nudge
import nightjar.nudge as nm
T=ZoneInfo("America/Toronto"); L=ZoneInfo("Europe/London")
def loc(z,*a): return datetime(*a,tzinfo=z)
tu=lambda **k: User(name="S",timezone="America/Toronto",**k)
# 1 quiet hours vs DST-shifted nudge
n=next_nudge(tu(quiet_start=time(3,0),quiet_end=time(7,0)), nights_at("02:45",7,first_night="2026-02-01"), loc(T,2026,3,7,12,0))
print("#1 at",n.at.isoformat(),"silent",n.silent)
n=next_nudge(tu(quiet_start=time(1,0),quiet_end=time(2,30)), nights_at("02:45",7,first_night="2026-02-01"), loc(T,2026,3,7,12,0))
print("#1 mirror at",n.at.isoformat(),"silent",n.silent)
# 2 fall-back repeated hour
n=next_nudge(tu(), nights_at("02:15",7,first_night="2026-10-01"), loc(T,2026,10,31,12,0))
print("#2 at",n.at.isoformat(), n.at.astimezone(timezone.utc).isoformat(), "fold",n.at.fold)
n2=next_nudge(tu(), nights_at("02:15",7,first_night="2026-10-01"), datetime(2026,11,1,6,0,tzinfo=timezone.utc))
print("#2b at",n2.at.isoformat())
# 4
n=next_nudge(tu(), nights_at("00:10",7), loc(T,2026,3,20,12,0)); print("#4",n.at.isoformat(), n.text)
# 6
ns=nights_at("23:30",4)+nights_at("00:30",4,first_night="2026-03-05")
n=next_nudge(tu(), ns, loc(T,2026,3,20,12,0)); print("#6",n.at.time())
# 7
for s in [(22,15,0),(22,14,59),(22,15,1)]:
    n=next_nudge(tu(), nights_at("23:00",7), loc(T,2026,3,20,*s)); print("#7",s,n.at.isoformat())
# 8
n=next_nudge(tu(), nights_at("23:00",7), datetime(2026,3,21,2,0,tzinfo=timezone.utc)); print("#8",n.at.isoformat())
# 9
for qs,qe in [(time(22,15),time(7,0)),(time(20,0),time(22,15))]:
    n=next_nudge(tu(quiet_start=qs,quiet_end=qe), nights_at("23:00",7), loc(T,2026,3,20,12)); print("#9",qs,qe,n.silent)
# 10
n=next_nudge(tu(quiet_start=time(22,0)), nights_at("23:00",7), loc(T,2026,3,20,12)); print("#10 start only",n.silent)
n=next_nudge(tu(quiet_start=time(22,0),quiet_end=time(22,0)), nights_at("23:00",7), loc(T,2026,3,20,12)); print("#10 equal",n.silent)
# 18
nm.load_register=lambda: {"nudge_copy":[]}
try: next_nudge(tu(), nights_at("23:00",7), loc(T,2026,3,20,12))
except Exception as e: print("#18", type(e).__name__, e)
