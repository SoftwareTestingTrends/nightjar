"""Security tests a reviewer runs against the journal-search change (run from a clone with uv)."""
import json, random, tempfile, time
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo
from fastapi.testclient import TestClient
from nightjar.coach import MockCoach
from nightjar.diary import Diary
from nightjar.models import Night
from nightjar.web import create_app
TZ = "America/Toronto"
def app_with(notes):
    tmp = Path(tempfile.mkdtemp()); d = Diary(tmp / "t.db")
    start = datetime(2025, 3, 1, 23, 0, tzinfo=ZoneInfo(TZ))
    d.add_nights([Night(bedtime=start + timedelta(days=i), wake_time=start + timedelta(days=i, hours=8), timezone=TZ, notes=n) for i, n in enumerate(notes)])
    return TestClient(create_app(diary=d, coach=MockCoach(), clock=lambda: datetime(2026, 3, 20, 12, tzinfo=ZoneInfo(TZ)), trace_path=tmp / "t.jsonl"))
out = {}
c = app_with(["Herbal tea before bed.", "<img src=x onerror=alert(1)> stressful day"])
page = c.get("/", params={"q": "<script>alert(1)</script>"}).text
out["script tag in the search text is escaped"] = "<script>alert(1)</script>" not in page
page = c.get("/", params={"q": "stressful"}).text
out["markup in a journal note is escaped"] = "<img src=x onerror" not in page
r = c.get("/api/search", params={"q": "' OR '1'='1"})
out["SQL-style quote: status 200, no rows"] = (r.status_code, len(r.json().get("nights", r.json().get("results", []))))
random.seed(1)
words = ["tea", "walk", "stress", "shower", "journal", "late", "work", "coffee", "travel", "tired", "relaxed", "river"]
year = app_with([" ".join(random.choice(words) for _ in range(25)) for _ in range(365)])
for n in (5, 200, 2000):
    q = " ".join(random.choice(["teaa", "wlak", "stres", "showr"]) for _ in range(n))
    t = time.time(); r = year.get("/api/search", params={"q": q}); out[f"{n}-word query on 365 nights: seconds"] = round(time.time() - t, 2)
print(json.dumps(out))
