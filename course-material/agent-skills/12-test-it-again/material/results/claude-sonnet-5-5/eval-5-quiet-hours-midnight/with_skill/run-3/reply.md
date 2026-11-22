I couldn't reproduce this, so I didn't write a `repro.py`. Quiet hours of 21:00 to 00:00 were accepted every time I tried.

**What I tried**, all against throwaway databases:
- **API:** I posted `quiet_start=21:00` and `quiet_end=00:00` to `/settings` three times. Each time it returned 303 and saved the end time as `00:00:00`.
- **Browser:** I filled the real Settings form with Playwright and Chromium three times. It redirected to `/` with no error, and the end time still read `00:00` afterwards.
- **Other values:**
  - `23:59` and `00:00:00` are also accepted.
  - Only `24:00` gets a 400, and that is not a valid time.

**Code:** `web.py` parses the value with `time.fromisoformat`, and `time(0, 0)` parses fine and is stored correctly. `in_quiet_hours` in `nudge.py` handles windows that wrap past midnight.

**Possible explanations**
- **Stale ticket:** `tools/tracker/seed.json` has NJ-14, "Quiet hours can't end at midnight", with the same "Invalid time" wording and status Open. The tracker wasn't running, so I only saw the seed data and couldn't check for comments or history. It may be stale or already fixed, or it may have come from a different build.
- **Different input:** you may have typed something other than `00:00`, such as `24:00`, or used a different browser or a different version of the app.

I added a `not reproduced` row (D-1) to `bugs/ledger.md`, since the triage steps ask for one. The bundle format says the ledger has one row per bundle, so this row has no bundle folder behind it.

If you can send the exact text you entered, or a screenshot of the error, I'll try again.