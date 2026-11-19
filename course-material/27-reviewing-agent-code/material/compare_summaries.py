"""Call one clone's GET /api/summary on the sample diary at several moments. Run from the clone with uv."""
import json, sys, tempfile
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from fastapi.testclient import TestClient
from nightjar.coach import MockCoach
from nightjar.diary import Diary
from nightjar.web import create_app
TZ = ZoneInfo("America/Toronto")
MOMENTS = {"Fri 20 Mar 12:00": datetime(2026, 3, 20, 12, 0, tzinfo=TZ),
           "Fri 20 Mar 23:30": datetime(2026, 3, 20, 23, 30, tzinfo=TZ),
           "Sat 21 Mar 09:00": datetime(2026, 3, 21, 9, 0, tzinfo=TZ),
           "Tue 24 Mar 09:00": datetime(2026, 3, 24, 9, 0, tzinfo=TZ)}
out = {}
for label, now in MOMENTS.items():
    tmp = Path(tempfile.mkdtemp())
    c = TestClient(create_app(diary=Diary(tmp / "t.db"), coach=MockCoach(), clock=lambda now=now: now, trace_path=tmp / "t.jsonl"))
    with open("data/sample_nights.csv", "rb") as f: c.post("/import", files={"file": ("n.csv", f, "text/csv")})
    s = c.get("/api/summary").json()
    avg = s.get("average_sleep_minutes", s.get("average_sleep_hours"))
    out[label] = {"nights_logged": s["nights_logged"], "average": avg}
print(json.dumps(out))
