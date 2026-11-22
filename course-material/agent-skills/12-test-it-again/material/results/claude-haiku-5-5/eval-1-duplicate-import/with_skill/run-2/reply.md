This is a real bug, and it's already in the tracker as NJ-12. I wrote a bundle at `bugs/D-1-csv-reimport-duplicates/` and created `bugs/ledger.md`.

**What happens:** The `/import` route calls `Diary.add_nights`, which runs a plain `INSERT` for every row with no check for existing nights (`src/nightjar/diary.py:57-73`). Importing `data/sample_nights.csv` twice stores 42 nights, not 21.

**Is it a requirement?** No requirement or story in `docs/` covers re-importing. The expected behaviour ("nights already in the diary are not added again") comes from NJ-12. I read that from `tools/tracker/seed.json`, not from the live tracker, so its current state may differ. The report records a question for product: what makes two nights "the same", and should a partly overlapping file add only its new nights?

**Repro:** `bugs/D-1-csv-reimport-duplicates/repro.py` uploads the sample CSV twice through the real route, in a temp database. It exits 1 while the bug is present and 0 once it's fixed. It exited 1 on all 3 runs with `defect: re-importing the same file stored 21 more nights (42 total, expected 21)`.

**Choices I made:**
- I put the bundle under `bugs/D-1-csv-reimport-duplicates/`, not `bugs/<short-name>/`, because `docs/bug-bundles.md` requires the `D-<n>-` prefix.
- The repro compares counts before and after the second upload, so it doesn't depend on how a fix defines "same night".
- The ledger row says `not filed`, as the skill requires.

**Next step:** run `/file-bug bugs/D-1-csv-reimport-duplicates`. NJ-12 already covers this, so the filing step should record it as a duplicate of NJ-12 rather than create a new ticket.

I didn't run `make test` or `make lint`, since I made no changes under `src/` or `tests/`.