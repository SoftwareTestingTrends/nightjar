"""Try to forge a log line through the search box (run from a clone with uv)."""
import json, tempfile
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from fastapi.testclient import TestClient
from nightjar.coach import MockCoach
from nightjar.diary import Diary
from nightjar.web import create_app
tmp = Path(tempfile.mkdtemp()); log = tmp / "search.log"
c = TestClient(create_app(diary=Diary(tmp / "t.db"), coach=MockCoach(), clock=lambda: datetime(2026, 3, 20, 12, tzinfo=ZoneInfo("America/Toronto")),
                          trace_path=tmp / "t.jsonl", search_log_path=log))
forged = 'tea\n{"at": "2026-03-20T12:00:01-04:00", "query": "support login ok", "results": 999}'
c.get("/api/search", params={"q": forged})
lines = log.read_text().splitlines()
print(json.dumps({"log lines after one search": len(lines), "forged entry appears as its own line": any(l.startswith('{"at": "2026-03-20T12:00:01') for l in lines)}))
