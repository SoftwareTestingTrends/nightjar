Importing the same CSV twice does store every night twice. I confirmed it as D-1.

- **Repro:** `uv run python bugs/D-1-csv-reimport-duplicates/repro.py` imports a one-night CSV twice into a throwaway database. It printed `2 nights stored (expected 1)` and exited 1 in 3 of 3 runs. It should exit 0 once a re-import no longer duplicates nights.
- **Cause:** the `nights` table has no uniqueness rule. `Diary.add_night` in `src/nightjar/diary.py` always inserts, and the `/import` handler in `web.py` never checks for existing nights.
- **Impact:** duplicates feed `usual_bedtime`, which takes the median of the last 14 nights, so they can skew the nudge time. I reasoned this from the code and didn't test it.
- **Expected behaviour is not specified.** No story or requirement says what a re-import should do. The report says "Not specified" and asks product whether re-imports should skip nights already in the diary, and what makes two nights the same.

I wrote the report at `bugs/D-1-csv-reimport-duplicates/report.md` and added the ledger row (`confirmed`, tracker `not filed`) in `bugs/ledger.md`. I didn't run `make test` or `make lint`, since I only added files under the gitignored `bugs/`.

To file it, run: `/file-bug bugs/D-1-csv-reimport-duplicates`