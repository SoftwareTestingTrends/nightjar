The bug is real: importing the same CSV twice stores every night twice. I've written the bundle as D-1.

The repro, `bugs/D-1-csv-reimport-duplicates/repro.py`, exited 1 in 3 of 3 runs. It imports a one-night CSV twice into a throwaway database and gets 2 nights instead of 1. I haven't run it against a fix, so the exit-0 path is untested.

- **Cause:** `Diary.add_nights` in `src/nightjar/diary.py` inserts every row. The `nights` table has no uniqueness constraint, and nothing checks for existing nights.
- **Side effect:** duplicates are counted twice in the usual-bedtime median, so they can skew the nudge.
- **Expected behaviour:** no requirement or story says what a repeat import should do, so the report says "Not specified". The question for product is whether to skip, replace or warn, and what makes two nights "the same". The repro assumes the diary should keep 1 night. Update it if product picks something else.

The report is `bugs/D-1-csv-reimport-duplicates/report.md`, and the row is in `bugs/ledger.md` with status `confirmed`, tracker `not filed`.

I couldn't confirm that `bugs/` is gitignored, because the `git check-ignore` command needed approval.

To file it, run: `/file-bug bugs/D-1-csv-reimport-duplicates`