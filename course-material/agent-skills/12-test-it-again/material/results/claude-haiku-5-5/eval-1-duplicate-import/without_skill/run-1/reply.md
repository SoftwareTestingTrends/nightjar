Yes, this is a real bug. Importing the same CSV twice stores every night twice.

I reproduced it through the `/import` route against an empty temporary database. The sample file has 21 nights. After the first import there were 21 rows. After the second there were 42, and the page still said "Imported 21 nights" both times.

The cause is in `src/nightjar/diary.py`. `add_nights` inserts every parsed row with a plain `INSERT`, and the `nights` table has no unique constraint on the night's times, so nothing stops a duplicate.

The docs don't say whether re-importing should be a no-op, so I took that reading myself. I think duplicates are wrong here because the usual-bedtime median uses the last 14 nights, so doubled rows shift which nights count, and the summary story (S-116) counts logged nights.

**Repro:** `bugs/reimport-duplicates/repro.py`. It imports `data/sample_nights.csv` twice into a throwaway database. It exits 1 while the bug is present (currently prints `BUG: after importing twice there are 42 nights, not 21`) and exits 0 once a second import adds no rows. Run it from the repo root with `uv run python bugs/reimport-duplicates/repro.py`.

I used the path you gave rather than the `bugs/D-<n>-<short-name>/` layout in `docs/bug-bundles.md`. I didn't add `report.md` or a ledger row, since you only asked for the script. Tell me if you want those added to match the convention.

I didn't change the application code. `make test` gives `66 passed, 1 deselected` and `make lint` gives `All checks passed!`. `bugs/` is gitignored, so the new script won't show in `git status`. I also left a scratch file at `/tmp/nj_probe.py`, which I couldn't delete because the command needed approval. It's outside the repo and harmless.