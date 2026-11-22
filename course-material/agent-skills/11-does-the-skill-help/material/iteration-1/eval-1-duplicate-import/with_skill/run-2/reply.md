It's a real bug. Importing the same CSV twice stores every night twice, and the repro fails every time.

- **Cause:** `Diary.add_nights` and `add_night` in `src/nightjar/diary.py` do a plain `INSERT`. The `nights` table has no uniqueness constraint and the code doesn't check for duplicates.
- **Expected behaviour:** The docs don't say what a re-import should do. "Nights already in the diary aren't added again" comes from your report and the seeded tracker ticket, so confirm that's the intended rule.
- **Repro:** `bugs/D-1-csv-reimport-duplicates/repro.py` imports 2 distinct nights twice into a temp database. It stores 4 and exits 1. It exits 0 once the count stays at 2. I ran it 3 times and got exit 1 each time.
- **Not run:** I didn't run `make test` or `make lint`, because I changed no source or test files.
- **Bundle:** I wrote `report.md` in the same folder and created `bugs/ledger.md` with row D-1 (`confirmed`, tracker `not filed`). The `bugs/` folder didn't exist before, and it's gitignored.

Filing changes something the team sees, so I haven't done it. To file it, run:

`/file-bug bugs/D-1-csv-reimport-duplicates`