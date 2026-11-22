This is a real bug. It reproduced 3 of 3 times. A 2-night CSV imported twice leaves 4 nights stored, and `repro.py` exits 1 each time.

**Cause:** `Diary.add_nights` in `src/nightjar/diary.py` inserts every row without checking for existing ones. The `nights` table has no uniqueness constraint. The `/import` endpoint reports the full file count each time. Duplicate nights would also skew the usual-bedtime median that the nudge relies on.

**Expected behaviour is not specified.** No requirement or story says how re-imports should work. I wrote "Not specified" under Expected and added a question for product: should an identical night be skipped, replaced or kept, and should the user be told how many were skipped?

**Files written:**
- `bugs/D-1-csv-reimport-duplicates/repro.py`
- `bugs/D-1-csv-reimport-duplicates/report.md`
- `bugs/ledger.md`, with a new row D-1 (`confirmed`, tracker `not filed`)

I didn't run `make test` or `make lint`, because I changed no code or tests.

**Next step:** filing makes it visible to the team, so you'll need to run it yourself:

`/file-bug bugs/D-1-csv-reimport-duplicates`