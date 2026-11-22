import pathlib
import tempfile
from datetime import time

from fastapi.testclient import TestClient

from nightjar.coach import MockCoach
from nightjar.diary import Diary
from nightjar.nudge import in_quiet_hours
from nightjar.web import create_app

d = pathlib.Path(tempfile.mkdtemp())
diary = Diary(d / "t.db")
c = TestClient(create_app(diary=diary, coach=MockCoach(), trace_path=d / "c.jsonl"))
data = dict(timezone="America/Toronto", quiet_start="21:00", quiet_end="00:00")
r = c.post("/settings", data=data, follow_redirects=True)
u = diary.user()
print(r.status_code, u.quiet_start, u.quiet_end, 'value="00:00"' in r.text, "invalid" in r.text.lower())
print([in_quiet_hours(u, time(h)) for h in (20, 21, 23, 0, 1)])
