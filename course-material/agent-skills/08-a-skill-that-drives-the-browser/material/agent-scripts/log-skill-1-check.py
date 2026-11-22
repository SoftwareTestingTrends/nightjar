import sys, os
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright

url = sys.argv[1]
ev = "evidence/log-night"
os.makedirs(ev, exist_ok=True)
today = datetime.now().date()
y = today - timedelta(days=1)
bed = f"{y}T23:00"
wake = f"{today}T06:30"
note = "Slept well, woke once"
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto(url)
    pg.screenshot(path=f"{ev}/01-home.png", full_page=True)
    print("1 banner:", pg.get_by_test_id("nudge-cold-start").inner_text())
    print("1 rows:", pg.get_by_test_id("diary-row").count())
    pg.get_by_test_id("bedtime-input").fill(bed)
    pg.get_by_test_id("wake-input").fill(wake)
    pg.get_by_test_id("timezone-input").fill("America/Toronto")
    pg.get_by_test_id("notes-input").fill(note)
    pg.screenshot(path=f"{ev}/02-filled.png", full_page=True)
    print("2 values:", bed, wake, pg.get_by_test_id("timezone-input").input_value())
    pg.get_by_test_id("add-night-submit").click()
    pg.wait_for_load_state()
    pg.screenshot(path=f"{ev}/03-after-save.png", full_page=True)
    print("3 error:", pg.get_by_test_id("error-message").all_inner_texts())
    print("3 rows:", pg.get_by_test_id("diary-row").all_inner_texts())
    print("3 table:", pg.get_by_test_id("diary-table").inner_text())
    print("3 banner:", pg.get_by_test_id("nudge-panel").inner_text())
    b.close()
