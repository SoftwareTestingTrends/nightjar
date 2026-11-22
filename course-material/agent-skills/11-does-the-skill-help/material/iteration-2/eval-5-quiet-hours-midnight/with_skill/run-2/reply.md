I couldn't reproduce this one, so I didn't treat it as a confirmed bug. Quiet hours of 21:00 to 00:00 saved without any error.

**What I tried:** I posted the settings form (`POST /settings`) with `quiet_start=21:00` and `quiet_end=00:00` three times. Each run used a throwaway database and the in-process app. Each time it returned HTTP 303 (success) and saved `quiet_end=00:00:00`. The code agrees:
- `time.fromisoformat("00:00")` parses fine.
- `time(0, 0)` counts as true in Python 3.12, so `_format_time` in `src/nightjar/diary.py` doesn't drop it.
- I didn't run a browser check of the form.

**Ledger:** I added D-1 to `bugs/ledger.md` with status `not reproduced` and tracker `not filed`.

**Cleanup:** My attempt to delete `bugs/quiet-end-midnight/repro.py` was blocked and needs your approval. That script exits 0, so it doesn't show a defect. Please delete the `bugs/quiet-end-midnight/` folder, or tell me to retry the delete.

**Tracker ticket:** NJ-14 in the tracker (`tools/tracker/seed.json`) already describes this symptom: "rejected with 'Invalid time'; 23:59 works". It's marked Open, and the current code doesn't show it. It may already be fixed, or it may depend on something I didn't try.

**Reporter details that would help:**
- Which browser did they use?
- Did they type the time or use the picker?
- What was the exact error text?
- Did the entry have seconds, or a `24:00`-style value? `24:00` is rejected with "hour must be in 0..23", so a user typing it would see an error like this.

I'm not filing anything. If you want to keep investigating, rerun the repro with the reporter's exact input.