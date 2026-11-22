"""Repro: saving quiet hours 21:00-00:00 via the settings form is rejected.

Exits 1 while the bug is present, 0 once fixed.
Run: uv run python bugs/quiet-hours-midnight/repro.py
"""

import sys
import tempfile
from datetime import time
from pathlib import Path

from fastapi.testclient import TestClient

from nightjar.diary import Diary
from nightjar.web import create_app


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        diary = Diary(Path(tmp) / "repro.db")
        client = TestClient(create_app(diary=diary))
        response = client.post(
            "/settings",
            data={"timezone": "America/Toronto", "quiet_start": "21:00", "quiet_end": "00:00"},
            follow_redirects=False,
        )
        user = diary.user()
        saved = user.quiet_start == time(21, 0) and user.quiet_end == time(0, 0)
        if response.status_code == 303 and saved:
            print("OK: quiet hours 21:00-00:00 saved")
            return 0
        print(
            f"BUG: status={response.status_code}, saved="
            f"{user.quiet_start}-{user.quiet_end}"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
