The report is real: importing the same CSV twice stores every night twice. `repro.py` exited 1 on all 3 runs, each time with "importing a 2-night CSV twice stored 4 nights (expected 2)".

The `nights` table has no uniqueness constraint. `Diary.add_night` and `add_nights` in `src/nightjar/diary.py` always INSERT, and the `/import` route uses that same path.

No requirement or story says what a re-import should do, so the bundle says "Not specified" under Expected. It also has a question for product: should a re-import skip, replace or add duplicate nights? Duplicates matter because the usual bedtime is the median of the last 14 nights, so they can shift the nudge time.

I ran `repro.py` against `Diary` directly with a temporary database, not through the web upload. I didn't check the tracker for an existing ticket, because the shell command for that needed approval.

Files are in `bugs/`:
- `D-1-csv-reimport-duplicates/repro.py`
- `D-1-csv-reimport-duplicates/report.md`
- `ledger.md` has one new row: status `confirmed`, tracker `not filed`.

To file it, run `/file-bug bugs/D-1-csv-reimport-duplicates`.