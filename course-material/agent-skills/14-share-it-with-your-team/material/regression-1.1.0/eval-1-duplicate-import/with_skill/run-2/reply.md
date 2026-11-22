Importing the same CSV twice does store every night twice. I confirmed it as D-1, and the repro exited 1 in 3 of 3 runs.

**Cause:** the `nights` table in `src/nightjar/diary.py` has no uniqueness constraint, and `add_nights` always inserts. The duplicates also skew `usual_bedtime`, because the median runs over the stored nights.

**Product question:** no requirement or story says what a repeated import should do, so the report's Expected section reads "Not specified". The question for product is whether a re-import should skip nights already in the diary, warn the user, or add them again. The repro assumes "skip duplicates" (1 night stored after two imports). If product picks something else, the script needs updating.

I didn't run `make test` or `make lint`, because I changed no source code.

**Files:**
- `bugs/D-1-csv-reimport-duplicates/repro.py` imports a 1-night CSV twice into a throwaway database. It exits 1 while 2 nights are stored and 0 once only 1 is.
- `bugs/D-1-csv-reimport-duplicates/report.md`
- `bugs/ledger.md`, with a D-1 row marked `confirmed` and tracker `not filed`.

I put the bundle under `bugs/D-1-csv-reimport-duplicates/` rather than the `bugs/<short-name>/` path you suggested, because `docs/bug-bundles.md` requires the `D-<n>-` prefix.

**Next step:** filing changes something the team sees, so I haven't done it. To file it, run:

`/nightjar-qa:file-bug bugs/D-1-csv-reimport-duplicates`