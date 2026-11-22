It's a real bug. Importing the same CSV twice stores every night twice.

- **Cause:** `/import` in `web.py` calls `Diary.add_nights()`, which calls `add_night()` for each row. Each call is a plain `INSERT`. The `nights` table has no unique constraint, and nothing checks for an existing night, so a second import adds every row again.
- **Is it intended?** I found no requirement or doc that says duplicates are expected. The page also reports "Imported N nights" both times. Duplicated nights would skew the usual-bedtime median that the nudge and coach rely on.
- **Repro:** `bugs/D-1-csv-reimport-duplicates/repro.py` imports a 2-night CSV twice into a throwaway database. It exits 1 while the bug is present and 0 once only 2 nights are stored. I ran it and it exited 1 with `BUG: 4 nights stored after importing a 2-night CSV twice (expected 2)`.
- **Folder name:** I used `D-1-csv-reimport-duplicates` instead of `bugs/<short-name>` because `docs/bug-bundles.md` requires the `D-<n>-` prefix. Tell me if you want it renamed.

I didn't write `report.md` or `bugs/ledger.md`, and I haven't filed a ticket. I also didn't change any app code.

A likely fix is a unique index on `(bedtime_utc, timezone)` with `INSERT OR IGNORE`. `add_nights` would then return the number of rows actually added. You'd need to decide whether a re-import of a row with edited notes should update that row.