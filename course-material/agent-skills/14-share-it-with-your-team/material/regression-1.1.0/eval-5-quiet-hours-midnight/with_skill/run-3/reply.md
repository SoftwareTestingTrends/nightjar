I can't reproduce this, so it isn't confirmed as a bug and I haven't written a repro. I can't tidy up either: the shell blocked my `rm` of the repro script I drafted and my write of the ledger row, and I stopped there. Please run these two steps, or tell me to retry:

```
rm -r bugs/quiet-hours-midnight
```

Then create `bugs/ledger.md` with this content:

```
| ID | Summary | Status | Tracker | Last checked |
|---|---|---|---|---|
| D-1 | Settings rejects quiet hours 21:00 to 00:00 as invalid time | not reproduced | not filed | 2026-11-22, POST /settings accepted and saved 00:00 (3 of 3) |
```

**What I tried:** I posted quiet hours 21:00 to 00:00 to `/settings` against a throwaway database. It succeeded three times in a row (303 redirect), and `quiet_end` was saved as `00:00:00`. The script exited 0 each time, so it can't serve as a repro for a bug that isn't there.

**Code check:**
- `web.py` parses the times with `time.fromisoformat`, which accepts `00:00`.
- Storage round-trips midnight correctly.
- `in_quiet_hours` handles a window that wraps past midnight, so 21:00 to 00:00 is treated correctly.

**Tracker:** `tools/tracker/seed.json` has NJ-14 ("Quiet hours can't end at midnight") as Open, with the same symptom. It matches your report, but I couldn't reproduce it against the current code. I haven't commented on it or filed anything.

**Possible causes:**
- The message may come from a different input path, such as a browser sending an unusual time format. I tested only the API, not the page.
- You may be running an older build or an old `nightjar.db`.

If you can tell me which browser you used, or the exact text of the error, I'll try again through the page.