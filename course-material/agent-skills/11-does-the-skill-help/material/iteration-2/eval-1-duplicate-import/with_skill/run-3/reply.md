Importing the same CSV twice does store every night twice. It reproduced 3 of 3 runs. I've logged it as D-1, status `confirmed`.

**Cause:** the `nights` table has no uniqueness constraint, and `Diary.add_night` always inserts a new row (`src/nightjar/diary.py:57`). The web `POST /import` goes through the same path. I reproduced it at the `Diary` level against a throwaway database, not through the web endpoint.

**Expected behavior isn't specified.** No requirement or story says what a re-import should do, so the report says "Not specified". The question for product is whether an existing night (same bedtime, wake time and timezone) should be skipped, replaced or added again. Duplicates also skew the usual-bedtime median that drives the nudge.

**Repro script:** `bugs/D-1-csv-reimport-duplicates/repro.py`. It exits 1 while the second import adds a duplicate and 0 once the diary holds one night. It assumes the fix is to skip duplicates, so update it if product decides otherwise.

**Files written:**
- `bugs/D-1-csv-reimport-duplicates/report.md`
- `bugs/ledger.md` (new, with one row)

To file it in the tracker, run `/file-bug bugs/D-1-csv-reimport-duplicates`. I can't start that step myself.