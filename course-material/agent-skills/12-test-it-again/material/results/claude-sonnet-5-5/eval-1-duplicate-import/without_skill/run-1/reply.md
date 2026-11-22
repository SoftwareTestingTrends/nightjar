Yes, it's a real bug. Importing the same CSV twice stores every night twice.

I imported a 2-night CSV twice into an empty database and got 4 nights back instead of 2.

**Cause:** `Diary.add_nights` in `src/nightjar/diary.py` inserts every row with a plain `INSERT`. The `nights` table has only an auto-increment `id`. Nothing in the schema or the import code checks whether a night is already stored. The docs don't say what a re-import should do, but a diary holding duplicate nights is wrong. It also skews the 14-night median that the usual bedtime and the nudge are built on.

**Repro:** `bugs/duplicate-import/repro.py`. It builds a throwaway database, imports a 2-night CSV twice and counts the nights. It exits 1 while the bug is present and 0 once only 2 nights are stored. I ran it and it exited 1 with the "BUG: 4 nights stored…" line.

I haven't fixed the bug. One likely fix is a unique constraint on `(bedtime_utc, wake_time_utc, timezone)` with `INSERT OR IGNORE`. Before choosing it, decide whether a re-import should skip duplicates silently or report how many it skipped.

I wrote only the repro script, not the full bundle from `docs/bug-bundles.md`. There is no `report.md` or `bugs/ledger.md`, and the folder is `bugs/duplicate-import/` rather than `D-<n>-…`, as you asked. I can add those if you want it in the ledger.