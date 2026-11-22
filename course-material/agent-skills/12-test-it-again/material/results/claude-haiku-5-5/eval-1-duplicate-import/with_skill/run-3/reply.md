It's a real bug, and it reproduces every time. Importing the same CSV twice takes the diary from 21 nights to 42.

**What's happening:** `Diary.add_nights` in `src/nightjar/diary.py` inserts every night unconditionally. The `nights` table has no unique constraint, and nothing compares incoming nights with stored ones. The `/import` route calls it directly, so the page reports "Imported 21 nights" on the second import too.

**Bundle written:**
- `bugs/D-1-csv-import-duplicates/repro.py`: exits 1 while the defect is present and 0 once it's fixed. It uses a temporary database. I ran it 3 times and got exit 1 each time.
- `bugs/D-1-csv-import-duplicates/report.md`: steps, actual behaviour, and reproducibility (3 of 3).
- `bugs/ledger.md`: created with one row, D-1, status `confirmed`, tracker `not filed`.

**Two deviations from your request:**
- I put the script in `bugs/D-1-csv-import-duplicates/`, not `bugs/<short-name>/`. The bundle contract in `docs/bug-bundles.md` uses the `D-<n>-<short-name>` form, and `/file-bug` expects it.
- The ledger didn't exist yet, so D-1 is the first entry.

**Open question for product:** the docs don't say what a repeated import should do, so Expected is "Not specified" in the report. The likely answer is that the diary keeps 21 nights, but the rules for what counts as "the same night" are a product decision. The report lists the questions.

**Next step:** to file it with the team, run `/file-bug bugs/D-1-csv-import-duplicates`. I haven't filed anything.