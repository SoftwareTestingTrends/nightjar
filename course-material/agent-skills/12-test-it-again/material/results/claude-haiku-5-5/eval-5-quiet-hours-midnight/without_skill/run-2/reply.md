This isn't a bug in this checkout, so I didn't write a `repro.py`.

**What I found**

- The settings form accepts `21:00` → `00:00`. The only save path is `POST /settings` in `src/nightjar/web.py`, which calls `time.fromisoformat("00:00")`. That parses fine, and `diary.save_user` stores it as `"00:00"`.
- The quiet-hours logic in `src/nightjar/nudge.py:in_quiet_hours` handles an end of `00:00` correctly. It wraps past midnight, so 21:00 to 24:00 is quiet.
- The string "Invalid time" does not appear anywhere in `src/`, templates, or tests. The settings-related errors are "Unknown time zone" and Python's own parse errors.
- I ran the form post through FastAPI's TestClient with a temporary database. `21:00`→`00:00` and `23:00`→`00:00` both saved, and the settings page re-rendered `00:00` as the end time. `21:00`→`23:59` also saved.

**About the ticket**

NJ-14 ("[Settings] Quiet hours can't end at midnight") describes a rejection with 'Invalid time' that this code doesn't produce. The tracker server isn't running here (connection refused), so I couldn't pull the ticket's comments. The steps may come from a different build, or the failure may be in the browser's time input or the running app. To settle it, I'd need the exact steps, the build or commit the app ran from, and ideally a screenshot or the response body from the failing save.

**Side note:** while probing, I accidentally ran a file that already existed at `/tmp/nj_probe/probe.py` (my `Write` to that path failed). It only posts the same form to a temp-database app, and I've read its contents. I didn't change or delete anything. The probe output above comes from that file.

I haven't changed any files, and I didn't create `bugs/` or a ledger entry.