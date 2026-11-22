I couldn't reproduce this, so I didn't write a `repro.py`.

**What I tried:** I ran the real app against a throwaway database, posting to `/settings` with `quiet_start=21:00` and `quiet_end=00:00`. I ran it 3 times. Each run returned a 303 redirect with no error, and the settings page showed 00:00 as the saved end. I used `23:59` as a control, and it behaved the same way.

**Why it works:** `web.py` parses the times with `time.fromisoformat`, which accepts `00:00`. Saving and reloading also keep midnight, because on Python 3.12 `time(0, 0)` counts as truthy. A 21:00–00:00 window is treated as wrapping past midnight in `nudge.in_quiet_hours`.

**What I didn't test:** I only exercised the server, not a real browser. The form has no JavaScript or validation pattern that would reject midnight, so I'd expect a browser to post `00:00` as well. If you still see "invalid time", tell me which browser you used and the exact text you typed. `/browser-check` could then confirm it on the page.

**Possible stale ticket:** the tracker's seed data has a ticket, "[Settings] Quiet hours can't end at midnight", describing the same symptom. It may be out of date.

**Files written:**
- `bugs/ledger.md` has one row, D-1, with status `not reproduced`.
- `bugs/D-1-quiet-hours-midnight-end/report.md` is the bundle report. The bundle has no repro script.

Nothing was filed.