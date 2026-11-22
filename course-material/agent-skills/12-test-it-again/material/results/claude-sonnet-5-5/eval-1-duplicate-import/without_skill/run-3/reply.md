Yes, it's a real bug. Importing the same CSV twice stores every night twice.

**Cause:** nothing checks for existing nights. `POST /import` in `web.py` calls `Diary.add_nights`, which loops over `add_night` in `diary.py`. That runs a plain `INSERT` into `nights`. The table has no uniqueness constraint on `(bedtime_utc, wake_time_utc, timezone)`.

**Evidence:**
- **Repro result:** I imported a 2-night CSV twice into a throwaway database. The diary held 4 nights, and the script exited 1.
- **Existing ticket:** the seeded tracker data describes the same symptom (`data/sample_nights.csv` uploaded twice gives 42 rows).
- **Impact:** duplicate nights skew the usual-bedtime median that the nudge and the coach use.
- **Requirements:** they don't say what a re-import should do, so skipping duplicates is my reading of the expected behavior.

**Repro:** `bugs/D-1-duplicate-csv-import/repro.py`. I named the folder `D-1-…` to follow `docs/bug-bundles.md`. Run it with `uv run python bugs/D-1-duplicate-csv-import/repro.py`. It prints one line and exits 1 while the bug is present, 0 once it's fixed.

I wrote only the script. There is no `report.md`, no `bugs/ledger.md` row, and nothing filed in the tracker. I haven't changed any product code.

A fix would add a unique index on those three columns and use `INSERT OR IGNORE`. `add_nights` would then return the number of rows actually inserted, so the "Imported N nights" notice stays accurate. I can do that, or write the report and ledger row, if you'd like.