It's a real bug. Importing the same CSV twice stores every night twice, and the repro script confirms it.

**Cause:** `Diary.add_nights` in `src/nightjar/diary.py` calls `add_night`, which does a plain `INSERT`. The `nights` table has no uniqueness constraint, and nothing checks for existing rows. I found no requirement or story that says duplicates should be allowed.

**Repro:** `bugs/duplicate-csv-import/repro.py` imports a 2-night CSV twice into a throwaway database.
- **Current behaviour:** it prints `BUG: expected 2 nights after importing a 2-night CSV twice, found 4` and exits 1.
- **When fixed:** it should exit 0.
- **How to run it:** `uv run python bugs/duplicate-csv-import/repro.py` from the repo root.

- **Folder name:** I used the path you gave. `docs/bug-bundles.md` expects `bugs/D-<n>-<name>/` plus a `report.md` and a ledger row. I didn't create those, so say if you want it converted.
- **Fix:** I didn't make one. The likely fix is a `UNIQUE(bedtime_utc, wake_time_utc, timezone)` constraint with `INSERT OR IGNORE`, or a skip-if-exists check in `add_nights`. Both change what `add_nights` returns (the count of nights actually added), so the API and page copy would need checking too.