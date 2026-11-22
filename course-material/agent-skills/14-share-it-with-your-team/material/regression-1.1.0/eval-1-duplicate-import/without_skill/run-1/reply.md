Yes, this is a real bug. Importing the same CSV twice stores every night twice.

**Cause:** the import has no duplicate check.
- `POST /import` in `src/nightjar/web.py` calls `parse_csv` and then `Diary.add_nights`.
- `add_nights` in `src/nightjar/diary.py` calls `add_night` once per row, and each call is a plain `INSERT`.
- The `nights` table has only an auto-increment `id`. It has no unique constraint on `(bedtime_utc, wake_time_utc, timezone)`.

**Effect:** duplicated nights skew `usual_bedtime` (the median over the last 14 nights) and the nudge that depends on it. No doc says re-imports are meant to add duplicates.

**Repro:** `bugs/csv-reimport-duplicates/repro.py` imports a 2-night CSV twice into a throwaway database. I ran it and it exits 1 with `BUG: 2-night CSV imported twice stored 4 nights (expected 2)`. It will exit 0 once the import skips nights that are already stored.

- **Folder name:** I used the path you asked for. `docs/bug-bundles.md` expects `bugs/D-<n>-<short-name>/` with a `report.md` and a row in `bugs/ledger.md`. I didn't create those, so say if you want the bundle converted.
- **Not run:** I haven't run `make test`, because I changed no source code.
- **Not fixed:** I didn't touch the bug itself.