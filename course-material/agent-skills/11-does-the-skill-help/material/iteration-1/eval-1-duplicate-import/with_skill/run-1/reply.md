Importing the same CSV twice does store every night twice, so I treated it as a bug (D-1). The repro script exited 1 on all 3 runs, each against a throwaway database.

**What happens:** `Diary.add_night` in `src/nightjar/diary.py` does a plain `INSERT`, and the `nights` table has no uniqueness rule. A 2-night CSV imported twice leaves 4 rows. `/import` then reports `imported=<count>` as if every row were new. Duplicate nights also feed the usual-bedtime median, so they can skew the nudge.

**Open question:** nothing in `docs/` says what a re-import should do, such as skip silently or warn. I called it a defect anyway, because silently doubling the diary can't be intended. The fix does need a product decision on that behavior.

**Files written:**
- `bugs/D-1-csv-reimport-duplicates/repro.py` exits 1 while the bug is present and 0 once each night is stored once.
- `bugs/D-1-csv-reimport-duplicates/report.md`
- `bugs/ledger.md`, with a new row for D-1 (confirmed, not filed). The ledger didn't exist before, so I created it.

I didn't file anything with the tracker. To file it, run:

`/file-bug bugs/D-1-csv-reimport-duplicates`