"""Log a 02:30 bedtime on 2026-03-08 (Toronto spring-forward gap) and read the diary row back.

Exit 1 while an accepted bedtime is shown as a different time than entered; exit 0 if it
is rejected or shown as entered.
"""

import re
import sys
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

from nightjar.diary import Diary
from nightjar.web import create_app

with tempfile.TemporaryDirectory() as tmp:
    client = TestClient(create_app(diary=Diary(Path(tmp) / "repro.db")))
    response = client.post(
        "/nights",
        data={
            "bedtime": "2026-03-08T02:30",
            "wake_time": "2026-03-08T09:30",
            "timezone": "America/Toronto",
        },
        follow_redirects=False,
    )
    if response.status_code != 303:
        print(f"bedtime rejected ({response.status_code}); not silently shifted")
        sys.exit(0)
    page = client.get("/").text
    row = re.search(r'<tr data-testid="diary-row">\s*<td>[^<]*</td>\s*<td>(\d\d:\d\d)</td>', page)
    shown = row.group(1) if row else None
    if shown == "02:30":
        print("diary shows 02:30, as entered")
        sys.exit(0)
    print(f"entered 02:30, diary shows {shown}")
    sys.exit(1)
