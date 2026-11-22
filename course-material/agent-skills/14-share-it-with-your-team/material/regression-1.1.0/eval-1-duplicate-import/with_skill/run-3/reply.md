The report holds up. Importing the same CSV twice stores every night twice, and I wrote a repro script for it.

**What I found:** `Diary.add_night` in `src/nightjar/diary.py` always does a plain INSERT, and the `nights` table has no uniqueness constraint. A repeat import therefore doubles the rows. This also skews the usual-bedtime median, so the nudge time can shift. I reproduced it at the `Diary` layer, not through the web upload form, which calls the same import code.

**Expected behaviour is not specified.** No requirement or story says what a re-import should do, so the report's Expected section says "Not specified". It also carries a question for product: skip existing nights, warn, or add them again?

**Repro:** `bugs/D-1-csv-reimport-duplicates/repro.py` imports a 2-night CSV twice into a throwaway database and prints `2-night CSV imported twice -> 4 nights stored (expected 2)`. It exited 1 on all 3 runs, and it should exit 0 once only 2 nights are stored.

I put the bundle at `bugs/D-1-csv-reimport-duplicates/` rather than the `bugs/<short-name>/` you asked for, because `docs/bug-bundles.md` requires the `D-<n>-` prefix. I also created `bugs/ledger.md` with the D-1 row (`confirmed`, `not filed`), since it didn't exist yet.

**Next step:** filing changes something the team sees, so I haven't done it. To file it, run:

`/nightjar-qa:file-bug bugs/D-1-csv-reimport-duplicates`