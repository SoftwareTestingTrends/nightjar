"""Drive the real home page in Chromium: log one night on an empty diary."""

import socket
import sys
import tempfile
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import uvicorn
from playwright.sync_api import expect, sync_playwright

from nightjar.coach import MockCoach
from nightjar.diary import Diary
from nightjar.web import create_app

ZONE = "America/Toronto"
today = datetime.now(ZoneInfo(ZONE)).date()
yesterday = today - timedelta(days=1)
NOTE = "Slept well, woke once"

tmp = Path(tempfile.mkdtemp())
app = create_app(diary=Diary(tmp / "check.db"), coach=MockCoach(), trace_path=tmp / "c.jsonl")
with socket.socket() as s:
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
server = uvicorn.Server(uvicorn.Config(app, port=port, log_level="warning"))
threading.Thread(target=server.run, daemon=True).start()
while not server.started:
    time.sleep(0.05)
url = f"http://127.0.0.1:{port}"

out = Path(sys.argv[1])
out.mkdir(exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url)
    print("before banner:", page.get_by_test_id("nudge-cold-start").inner_text())
    print("before rows:", page.get_by_test_id("diary-row").count())
    page.screenshot(path=str(out / "1-before.png"), full_page=True)

    page.get_by_test_id("bedtime-input").fill(f"{yesterday}T23:00")
    page.get_by_test_id("wake-input").fill(f"{today}T06:30")
    page.get_by_test_id("timezone-input").fill(ZONE)
    page.get_by_test_id("notes-input").fill(NOTE)
    page.screenshot(path=str(out / "2-filled.png"), full_page=True)
    page.get_by_test_id("add-night-submit").click()

    expect(page.get_by_test_id("diary-row")).to_have_count(1)
    row = page.get_by_test_id("diary-row")
    print("row cells:", [c.inner_text() for c in row.locator("td").all()])
    print("after banner:", page.get_by_test_id("nudge-cold-start").inner_text())
    page.screenshot(path=str(out / "3-after.png"), full_page=True)

    expect(row).to_contain_text("7h 30m")
    expect(row).to_contain_text(NOTE)
    expect(row).to_contain_text(ZONE)
    expect(page.get_by_test_id("nudge-cold-start")).to_contain_text("Log 6 more nights")
    print("ALL ASSERTIONS PASSED")
    browser.close()
server.should_exit = True
