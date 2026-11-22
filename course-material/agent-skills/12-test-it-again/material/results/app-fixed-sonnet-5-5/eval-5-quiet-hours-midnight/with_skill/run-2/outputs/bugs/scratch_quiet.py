import tempfile
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from fastapi.testclient import TestClient

from nightjar.coach import MockCoach
from nightjar.diary import Diary
from nightjar.web import create_app

d = Path(tempfile.mkdtemp())
c = TestClient(
    create_app(
        diary=Diary(d / "t.db"),
        coach=MockCoach(),
        clock=lambda: datetime(2026, 3, 20, 12, tzinfo=ZoneInfo("America/Toronto")),
        trace_path=d / "c.jsonl",
    ),
    follow_redirects=False,
)
for end in ["00:00", "23:59"]:
    r = c.post("/settings", data={"timezone": "America/Toronto", "quiet_start": "21:00", "quiet_end": end})
    print(end, r.status_code, "Invalid" in r.text)
    print(c.get("/").text.count("00:00"), Diary(d / "t.db").user())
