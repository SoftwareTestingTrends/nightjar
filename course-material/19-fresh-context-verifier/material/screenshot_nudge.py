"""Screenshot the nudge panel in a given state.

    uv run python scripts/screenshot_nudge.py silent out.png
    states: silent (quiet hours cover the nudge), loud (no quiet hours), cold (6 nights)
"""
import socket, sys, tempfile, threading, time
from datetime import datetime, time as clock_time
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tests"))
import uvicorn
from builders import nights_at
from playwright.sync_api import sync_playwright

from nightjar.coach import MockCoach
from nightjar.diary import Diary
from nightjar.models import User
from nightjar.web import create_app

state, out = sys.argv[1], sys.argv[2]
tmp = Path(tempfile.mkdtemp())
diary = Diary(tmp / "shot.db")
diary.add_nights(nights_at("23:00", 6 if state == "cold" else 8, first_night="2026-03-10"))
quiet = (clock_time(22, 0), clock_time(7, 0)) if state == "silent" else (None, None)
diary.save_user(User(name="Sam", timezone="America/Toronto", quiet_start=quiet[0], quiet_end=quiet[1]))
app = create_app(diary=diary, coach=MockCoach(), clock=lambda: datetime(2026, 3, 20, 12, 0, tzinfo=ZoneInfo("America/Toronto")), trace_path=tmp / "t.jsonl")
with socket.socket() as s:
    s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]
server = uvicorn.Server(uvicorn.Config(app, port=port, log_level="warning"))
threading.Thread(target=server.run, daemon=True).start()
while not server.started:
    time.sleep(0.05)
with sync_playwright() as p:
    page = p.chromium.launch().new_page(viewport={"width": int(sys.argv[3]) if len(sys.argv) > 3 else 1280, "height": 900})
    page.goto(f"http://127.0.0.1:{port}/")
    page.locator('[data-testid="nudge-panel"]').screenshot(path=out)
server.should_exit = True
print("saved", out)
