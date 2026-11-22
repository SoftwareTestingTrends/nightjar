import os
import tempfile

from fastapi.testclient import TestClient

from nightjar.diary import Diary
from nightjar.web import create_app

diary = Diary(os.path.join(tempfile.mkdtemp(), "t.db"))
c = TestClient(create_app(diary=diary))
csv = (
    "bedtime,wake_time,timezone,notes\n"
    "2026-03-18T23:00:00-04:00,2026-03-19T07:00:00-04:00,America/Toronto,a\n"
    "2026-03-19T23:30:00-04:00,2026-03-20T07:00:00-04:00,America/Toronto,b\n"
)
for _ in range(2):
    r = c.post("/import", files={"file": ("d.csv", csv, "text/csv")}, follow_redirects=False)
    print(r.headers["location"], len(diary.nights()))
