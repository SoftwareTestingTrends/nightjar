Yes, it's a real bug. Importing the same CSV twice stores every night twice.

**Cause:** `Diary.add_nights` (`src/nightjar/diary.py:70`) calls `add_night`, which does a plain `INSERT`. The `nights` table has no uniqueness constraint, and `/import` in `web.py:85` doesn't check for existing rows either. A second import therefore adds a second copy of each night.

**Why it matters:** `usual_bedtime` takes the median bedtime over the last 14 nights. Duplicated rows skew that median and the nudge time built on it.

**Caveat:** The docs don't say what a re-import should do. I treated "no duplicates" as the expected behavior. If you'd rather allow identical nights on purpose, the repro's expectation would need to change.

**Repro:** `bugs/duplicate-import/repro.py` uses a throwaway temp database and imports a 2-night CSV twice. I ran it with `uv run python bugs/duplicate-import/repro.py`. It printed `BUG: 2-night CSV imported twice stored 4 nights, expected 2` and exited 1. It exits 0 once a re-import stores no duplicates.

**Not done:**
- I didn't fix the bug.
- I didn't write a ledger row or `report.md`, because you asked only for the repro.
- I couldn't file it in the tracker, because it isn't running.
- `bugs/` is gitignored, so the script won't show up in `git status`.

A fix would add a unique key on `(bedtime_utc, wake_time_utc, timezone)` with `INSERT OR IGNORE`, or skip existing nights in `add_nights`. I'd also make `add_nights` return the number actually inserted, so the "imported N" message stays accurate.