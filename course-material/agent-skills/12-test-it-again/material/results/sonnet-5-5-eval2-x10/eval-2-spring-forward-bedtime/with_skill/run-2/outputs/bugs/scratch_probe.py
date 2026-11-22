import os
import re
import tempfile

from fastapi.testclient import TestClient

from nightjar.diary import Diary
from nightjar.web import create_app

d = Diary(os.path.join(tempfile.mkdtemp(), "t.db"))
c = TestClient(create_app(diary=d))
r = c.post(
    "/nights",
    data={
        "bedtime": "2026-03-08T02:30",
        "wake_time": "2026-03-08T09:30",
        "timezone": "America/Toronto",
    },
    follow_redirects=False,
)
print(r.status_code)
n = d.nights()[0]
print(n.bedtime, n.local_bedtime, n.duration)
print(re.findall(r"\d\d:\d\d", c.get("/").text)[:6])
