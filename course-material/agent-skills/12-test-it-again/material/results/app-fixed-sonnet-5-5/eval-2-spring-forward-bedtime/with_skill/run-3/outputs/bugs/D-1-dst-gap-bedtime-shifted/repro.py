"""D-1: a bedtime inside the spring-forward gap is silently shown an hour later.

Exit 1 while a 02:30 bedtime on 2026-03-08 (America/Toronto) is accepted and shown as
03:30 with no notice; exit 0 once the app rejects it or tells the user.
"""

import re
import sys
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

from nightjar.diary import Diary
from nightjar.web import create_app

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    client = TestClient(create_app(diary=diary))
    resp = client.post(
        "/nights",
        data={
            "bedtime": "2026-03-08T02:30",
            "wake_time": "2026-03-08T08:00",
            "timezone": "America/Toronto",
        },
        follow_redirects=False,
    )
    nights = diary.nights()
    shown = nights[0].local_bedtime.strftime("%H:%M") if nights else None
    page = client.get("/").text
    told = resp.status_code != 303 or bool(re.search(r"daylight|DST|adjust|skipp", page, re.I))
    if shown == "03:30" and not told:
        print("Entered 02:30 on 2026-03-08 (Toronto); diary shows 03:30 and gives no notice")
        sys.exit(1)
    print(f"status={resp.status_code} shown={shown} told_user={told}")
    sys.exit(0)
