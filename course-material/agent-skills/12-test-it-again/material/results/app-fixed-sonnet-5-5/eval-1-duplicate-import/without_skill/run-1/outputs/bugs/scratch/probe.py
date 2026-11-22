import sys, tempfile
from pathlib import Path
sys.path.insert(0, "src")
from fastapi.testclient import TestClient
from nightjar.diary import Diary
from nightjar.web import create_app

tmp = Path(tempfile.mkdtemp())
d = Diary(tmp / "d.db")
c = TestClient(create_app(diary=d, trace_path=tmp / "t.jsonl"))
data = Path("data/sample_nights.csv").read_bytes()
for _ in range(2):
    r = c.post("/import", files=dict(file=("n.csv", data)), follow_redirects=False)
    print(r.status_code, r.headers.get("location"), len(d.nights()))
