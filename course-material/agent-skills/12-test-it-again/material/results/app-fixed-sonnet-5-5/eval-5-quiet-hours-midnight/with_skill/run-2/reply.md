I couldn't reproduce this one, so I didn't write a `repro.py`.

**What I tried:** I ran the real app against a throwaway database and posted `POST /settings` with quiet hours 21:00 to 00:00.
- The app accepted it with a 303 redirect and no error, and saved 21:00 to 00:00. I ran it 3 times with the same result.
- `in_quiet_hours` handles that window correctly. For 20:00, 21:00, 23:00, 00:00 and 01:00 it returns False, True, True, False, False.
- `"Invalid time"` doesn't appear anywhere in `src/`. The only parsing is `time.fromisoformat`, which accepts `00:00`.

**What I didn't check:** I didn't test in a real browser or on a deployed build. The report could come from an older build, or from a browser sending a different time format. If you can tell me which browser and what's on screen, I'll look again, and `/browser-check` can test it in Chromium.

**Tracker:** NJ-14, "Quiet hours can't end at midnight", is already open for the same report. It may be stale. I didn't touch the tracker.

**Files:**
- `bugs/D-1-quiet-end-midnight/report.md` has the details, with status `not reproduced`.
- `bugs/ledger.md` has the row for D-1.
- `bugs/scratch_quiet.py` is a scratch script of mine. Deleting it needed approval, so it's still there. Please remove it.
- `/tmp/try.py` already existed and wasn't mine, but I ran it once by mistake. It looks like it only used a throwaway database, but I didn't read it first.