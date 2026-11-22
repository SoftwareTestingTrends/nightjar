"""End-to-end: a real browser adds the 7th night and the nudge appears.

Needs Chromium:  uv run playwright install chromium   (skipped if it's missing)
"""

import socket
import threading
import time
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
import uvicorn
from builders import nights_at

from nightjar.coach import MockCoach
from nightjar.diary import Diary
from nightjar.web import create_app

pytestmark = pytest.mark.e2e
playwright_api = pytest.importorskip("playwright.sync_api")
NOON_IN_TORONTO = datetime(2026, 3, 20, 12, 0, tzinfo=ZoneInfo("America/Toronto"))


@pytest.fixture
def base_url(tmp_path):
    diary = Diary(tmp_path / "e2e.db")
    diary.add_nights(nights_at("23:00", 6, first_night="2026-03-10"))  # one short of a nudge
    app = create_app(
        diary=diary,
        coach=MockCoach(),
        clock=lambda: NOON_IN_TORONTO,
        trace_path=tmp_path / "coach.jsonl",
    )
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(app, port=port, log_level="warning"))
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    while not server.started:
        time.sleep(0.05)
    yield f"http://127.0.0.1:{port}"
    server.should_exit = True
    thread.join(timeout=5)


@pytest.fixture
def page():
    with playwright_api.sync_playwright() as playwright:
        try:
            browser = playwright.chromium.launch()
        except playwright_api.Error as error:
            pytest.skip(f"Chromium not installed ({error.message.splitlines()[0]})")
        yield browser.new_page()
        browser.close()


def test_T_114_1_e2e_adding_the_seventh_night_shows_the_nudge(page, base_url):
    page.goto(base_url)
    expect = playwright_api.expect
    expect(page.get_by_test_id("nudge-cold-start")).to_contain_text("Log 1 more night")

    page.get_by_test_id("bedtime-input").fill("2026-03-16T23:00")
    page.get_by_test_id("wake-input").fill("2026-03-17T07:00")
    page.get_by_test_id("notes-input").fill("Read a book, lights out at 11.")
    page.get_by_test_id("add-night-submit").click()

    expect(page.get_by_test_id("diary-row")).to_have_count(7)
    expect(page.get_by_test_id("nudge-time")).to_have_text("22:15")
