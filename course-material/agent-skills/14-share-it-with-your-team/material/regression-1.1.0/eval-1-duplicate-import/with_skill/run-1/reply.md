Importing the same CSV twice does store every night twice. I confirmed it and logged it as D-1. The repro script exited 1 in 3 of 3 runs, each against a throwaway database.

**Cause:** `Diary.add_nights` (`src/nightjar/diary.py:70`) inserts every row without checking for existing ones. The `nights` table also has no uniqueness constraint. A CSV with 2 nights imported twice leaves 4 rows.

**Spec gap:** No requirement or story says what a re-import should do, so the report's Expected section reads "Not specified". It includes a question for product: should a re-import skip matching nights, replace them, or warn? And what counts as the same night? The report notes that the seeded tracker ticket expects duplicates to be skipped.

**Files**
- `bugs/D-1-csv-reimport-duplicates/repro.py` imports a 2-night CSV twice and exits 1 while more than 2 nights are stored.
- `bugs/D-1-csv-reimport-duplicates/report.md`
- `bugs/ledger.md` has one row: `confirmed`, tracker `not filed`.

The repro lives in the `D-1-…` folder rather than `bugs/<short-name>/`, because `docs/bug-bundles.md` requires that naming.

I didn't run `make test` or `make lint`, since I changed no source or tests.

**Next step:** filing in the tracker is yours to start. Run:

`/nightjar-qa:file-bug bugs/D-1-csv-reimport-duplicates`