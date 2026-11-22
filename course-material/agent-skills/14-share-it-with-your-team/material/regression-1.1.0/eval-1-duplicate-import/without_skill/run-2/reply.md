It's a real bug. Importing the same CSV twice stores every night twice.

I ran the repro and it exited 1 with `2 distinct nights imported twice -> 4 stored (expected 2)`.

**Cause:** nothing in the import path checks for duplicates.
- `Diary.add_nights` in `src/nightjar/diary.py:70` calls `add_night` for each row.
- `add_night` does a plain `INSERT`.
- The `nights` table (`diary.py:23`) has no unique constraint on `bedtime_utc`, `wake_time_utc` and `timezone`.
- The `/import` route in `web.py` goes through the same path, so uploading the file twice in the browser does the same.

**Repro:** `bugs/duplicate-import/repro.py` uses a throwaway temp database and imports a 2-night CSV twice. It exits 1 while the nights are duplicated and 0 once the count is 2. Run it from the repo root with `uv run python bugs/duplicate-import/repro.py`.

**Fix:** I haven't made one, since you asked only for the investigation. The usual approach is a unique index on `(bedtime_utc, wake_time_utc, timezone)` and `INSERT OR IGNORE`, with the import count reporting only the rows actually inserted. Whether an identical night should be skipped or rejected is a product decision, though.

I put the script at the path you gave, `bugs/duplicate-import/`. `docs/bug-bundles.md` describes a `bugs/D-<n>-<short-name>/` layout with a `report.md` and a ledger entry. I didn't create those, but I can if you want it filed that way.

I didn't run `make test` or `make lint`, because I changed no source or tests.