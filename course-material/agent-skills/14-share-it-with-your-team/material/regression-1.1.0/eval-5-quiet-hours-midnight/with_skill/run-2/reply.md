I couldn't reproduce this, so I didn't write a repro script.

I posted quiet hours of 21:00 to 00:00 to `POST /settings` against a throwaway database, three times. This is the same call the Settings form makes.

- **Result:** Every run returned 303 (saved), and the Settings page showed `00:00` as the saved end time.
- **Other values:** `00:00:00` is also accepted. Only `24:00` is rejected, with HTTP 400.
- **Code:** I read the settings code in `web.py` and `diary.py` and found nothing that rejects midnight. `in_quiet_hours` handles a window that wraps past midnight.

I haven't tried it in a real browser. The settings page has no client-side validation, so I'd expect it to behave the same. `/nightjar-qa:browser-check` would confirm.

The tracker already has NJ-14, "Quiet hours can't end at midnight", which describes the same report. It may be stale. The reporter may also have entered `24:00`, which is rejected. Worth asking them which value and which browser they used.

I wrote `bugs/D-1-quiet-hours-midnight/report.md` and added a `not reproduced` row to `bugs/ledger.md`. I did not file anything in the tracker.

**Leftover file to delete:** `bugs/quiet-hours-midnight/repro.py`. I wrote it before running it, and the shell refused my attempt to delete it. It currently exits 0, so it isn't a valid repro. `/tmp/nj_probe_midnight.py` is a scratch file I also couldn't delete.