Yes, it's a real bug. Importing the same CSV twice stores every night twice, and I wrote a repro for it.

**Cause:** `Diary.add_nights` in `src/nightjar/diary.py:70` calls `add_night` for each row. That is a plain `INSERT`, and the `nights` table has no uniqueness constraint. Nothing checks for an existing night, so a second import, or a double-submit of the form, inserts every row again.

**Why it matters:** `usual_bedtime` takes the median bedtime of the last 14 nights. Duplicate rows fill that window with repeated nights, which skews the usual bedtime and the nudge. The app also reports "Imported N nights" as if they were all new. The docs don't say what re-importing should do, so I judged this by what a user would expect. If you want re-imports to add duplicates on purpose, tell me and I'll drop the repro.

**Repro:** `bugs/duplicate-csv-import/repro.py` imports a 2-night CSV twice into a throwaway database. It currently prints `2 distinct nights imported twice -> 4 stored (expected 2)` and exits 1. It exits 0 once the duplicates are gone. I ran it only against the current code, so the exit-0 path is untested.

I used the path you gave, not the `bugs/D-<n>-<name>/` layout from `docs/bug-bundles.md`. I didn't write a `report.md` or a ledger row. I also didn't change any app code.

For a fix, the likely route is a unique key on `(bedtime_utc, wake_time_utc, timezone)` with `INSERT OR IGNORE`. `add_nights` would then return the number of rows actually inserted.