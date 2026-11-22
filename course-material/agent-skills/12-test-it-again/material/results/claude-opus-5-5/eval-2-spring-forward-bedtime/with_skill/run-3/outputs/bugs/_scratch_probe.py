import re
import tempfile
from datetime import UTC, datetime
from pathlib import Path

from fastapi.testclient import TestClient

from nightjar.coach import MockCoach
from nightjar.diary import Diary
from nightjar.web import create_app

d = tempfile.mkdtemp()
diary = Diary(Path(d) / "t.db")
app = create_app(diary, MockCoach(), lambda: datetime(2026, 3, 9, 12, tzinfo=UTC))
c = TestClient(app)
r = c.post(
    "/nights",
    data={"bedtime": "2026-03-08T02:30", "wake_time": "2026-03-08T09:30", "timezone": "America/Toronto"},
    follow_redirects=True,
)
print(r.status_code)
n = diary.nights()[0]
print(n.bedtime, "| utc", n.bedtime.astimezone(UTC), "| local", n.local_bedtime, "| dur", n.duration)
print(re.findall(r"<td>[^<]*</td>", r.text)[:4])
