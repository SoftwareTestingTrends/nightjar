Importing the same CSV twice does store every night twice. I confirmed it, so I wrote a bug bundle for it as D-1. I did not file it in the tracker.

- **Cause:** `Diary.add_night` in `src/nightjar/diary.py` is a plain `INSERT`, and the `nights` table has no uniqueness constraint. A second import therefore adds every row again. The duplicates also count twice in `usual_bedtime`, which takes the median of the last 14 nights.
- **Repro:** `uv run python bugs/D-1-csv-reimport-duplicates/repro.py` prints `diary holds 2 night(s) (expected 1)` and exits 1. It did this on 3 of 3 runs, against a temporary database. It will exit 0 once a second import leaves each night stored once.
- **Expected behaviour is not specified.** No story says what a re-import should do. S-117 AC6 only covers importing an export into an empty diary. The report says "Not specified" and carries a question for product: should a re-import skip nights that already exist, and should it report how many it skipped? The repro script assumes the reporter's expectation of no duplicates, so product should confirm that.
- **Files:** `report.md` and `repro.py` are in `bugs/D-1-csv-reimport-duplicates/`, and `bugs/ledger.md` has a `confirmed` / `not filed` row.

I ran the repro three separate times rather than in a loop, because the loop command was blocked by a permission check. I did not run `make test` or `make lint`, since no code changed.

To file it, run: `/file-bug bugs/D-1-csv-reimport-duplicates`