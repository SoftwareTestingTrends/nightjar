I couldn't reproduce this one, so I didn't treat it as a bug. I ran the repro script I'd drafted 3 times, and it passed each time, so I wrote no repro for the bundle.

- **What I tried:** I sent `POST /settings` with `quiet_start=21:00` and `quiet_end=00:00` to a fresh throwaway database, the same values the Settings form sends. Each run returned HTTP 303 and saved `quiet_end=00:00:00`. I never saw an "invalid time" error.
- **Logic check:** `in_quiet_hours` (`nudge.py:59`) handles a 21:00–00:00 window correctly because it wraps midnight. The string "Invalid time" doesn't appear anywhere in `src/`.
- **Not tested:** I only tested through the API. I didn't drive the form in a browser.
- **Existing ticket:** The tracker already has NJ-14, "Quiet hours can't end at midnight" (Open). It says 00:00 is rejected and 23:59 works, which doesn't match what the current code does. The ledger row says not filed because I didn't file or comment on anything.
- **Ledger:** I added D-1 with status `not reproduced`.
- **Report:** `bugs/D-1-quiet-hours-midnight/report.md` has the details.

**Leftover file:** `bugs/quiet-hours-midnight/repro.py` is still on disk. The command to delete it needed your approval, so please run `rm -r bugs/quiet-hours-midnight`. It exits 0 today, so it isn't a real repro.

**Where to look next:**
- Does the browser submit something other than `00:00`, such as `24:00`? A browser run with `/browser-check` would settle it.
- Is the report from a different build?
- Is NJ-14 stale?

If you can tell me what you did in the browser, I'll triage again.