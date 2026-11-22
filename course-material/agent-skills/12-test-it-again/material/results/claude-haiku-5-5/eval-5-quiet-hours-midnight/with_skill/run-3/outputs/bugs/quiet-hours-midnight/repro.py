"""Repro: quiet hours ending at midnight (00:00) are rejected by Settings.

Exits 1 while the defect is present, 0 once it is fixed.
Uses a throwaway database in a temporary directory.
"""

import re
import sys
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

from nightjar.diary import Diary
from nightjar.web import create_app


def main() -> int:
    db = Path(tempfile.mkdtemp()) / "repro.db"
    client = TestClient(create_app(Diary(str(db))))
    response = client.post(
        "/settings",
        data={"timezone": "America/Toronto", "quiet_start": "21:00", "quiet_end": "00:00"},
        follow_redirects=False,
    )
    if response.status_code != 303:
        error = re.search(r'class="error"[^>]*>(.*?)<', response.text, re.S)
        detail = error.group(1).strip() if error else response.text[:120]
        print(f"BUG PRESENT: 21:00-00:00 rejected with HTTP {response.status_code}: {detail}")
        return 1
    print("FIXED: 21:00-00:00 accepted")
    return 0


if __name__ == "__main__":
    sys.exit(main())
