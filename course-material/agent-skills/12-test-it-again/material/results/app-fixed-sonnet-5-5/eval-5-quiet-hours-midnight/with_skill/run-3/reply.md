I couldn't reproduce this, so I didn't write a `repro.py`.

**What I tried:** I ran the real app against a throwaway database and posted quiet hours 21:00 to 00:00 to `/settings`, three times. Each time it returned a 303 redirect (accepted), and the saved end time read back as `00:00:00`. 23:59 was accepted as well.

**What the code shows:** `time.fromisoformat("00:00")` parses fine in `web.py:106-107`. `_format_time` and `_parse_time` in `diary.py` store and reload midnight correctly. `in_quiet_hours` handles a 21:00 to 00:00 window correctly.

**Where the message might come from:** There is no "invalid time" text anywhere in `src/`. If you saw that message in a browser, it could be coming from the browser's own time input rather than NightJar. I didn't check that in a browser.

**Possible duplicate:** The tracker seed (`tools/tracker/seed.json:46`) already has a ticket, "[Settings] Quiet hours can't end at midnight". It describes the same symptom. The tracker wasn't running, so I couldn't check whether that ticket is still open.

I added a ledger row at `bugs/ledger.md`: D-1, `not reproduced`, tracker `not filed`.

**To go further, tell me:**
- Which browser you used and what exactly the message said.
- Or run `make e2e` or `/browser-check` on the settings form. That would test the browser behaviour, which I haven't.