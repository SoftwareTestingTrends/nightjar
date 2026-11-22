**Not reproduced, so I didn't write a repro script.** Setting quiet hours from 21:00 to 00:00 saves correctly in the current code.

**What I ran:** I posted the settings form (`POST /settings`) against a throwaway database, using the app's real `create_app` and a fixed clock. I tried 21:00→00:00 and three other quiet windows, including 23:00→00:00 and 00:00→07:00. Each returned 200, and reloading the page showed the end time as `00:00`. I repeated the run three times with the same result, 0 of 3 failures.

**Why I don't think the report matches the code:**
- Nothing in `src/` produces the text "Invalid time". The only error path is `time.fromisoformat` in `web.py`, which fails with a Python "Invalid isoformat string" message, and only for malformed input. A browser `<input type="time">` submits `00:00` as valid.
- The bug is recorded as a seeded ticket in `tools/tracker/seed.json` (item 46, "[Settings] Quiet hours can't end at midnight"). Its description matches your report exactly. I only read the seed file; I didn't check the live tracker, so I don't know whether that ticket is open.

**Ledger:** I created `bugs/ledger.md` with one row, `D-1`, status `not reproduced`, tracker `not filed`. Per the skill, I didn't create a bundle folder.

**Still unexplained:** the report came from a real user session. The most likely cause is something the form test doesn't cover, such as the browser UI, a different build, or a different value entered. If you can tell me the exact values and the browser, I'll rerun a browser check (`/browser-check`) on the settings form.