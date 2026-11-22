Yes, it's a real bug, and it happened in 3 of 3 runs.

**Cause:** `Diary.add_nights` in `src/nightjar/diary.py:70` does a plain `INSERT` for every row it reads from the CSV. The `nights` table has no uniqueness constraint, and neither `parse_csv` nor the `/import` route checks for nights already in the diary. Importing a file twice adds every night twice. Besides cluttering the diary, the duplicates also throw off the usual-bedtime median that the bedtime nudge relies on.

**Repro:** `uv run python bugs/D-1-duplicate-import/repro.py`. It posts a 2-night CSV to `/import` twice, using a throwaway database. It currently exits 1 and prints:
```
BUG: imported the same 2-night CSV twice; diary holds 4 nights (expected 2)
```
It will exit 0 once a second import leaves 2 nights.

**Changes from what you asked for:**
- **Folder name:** you suggested `bugs/<short-name>/`, but the project's bug-bundle rules (`docs/bug-bundles.md`) use `bugs/D-<n>-<short-name>/`, so I named it `D-1-duplicate-import`.
- **Two extra files:** the same rules call for a report and a ledger entry, so I also wrote `bugs/D-1-duplicate-import/report.md` and `bugs/ledger.md`. That lets the `verify-fix` skill recheck the bug later. I didn't file it in the bug tracker.

**Decision for you:** no written requirement says what should happen on a re-import. The closest is story S-117 AC6, which only covers importing into an empty diary. Someone needs to decide what counts as "the same night": an exact match on bedtime, or any overlap in sleep times. The repro uses an identical file, so it should pass whichever rule you pick.

I didn't change any app code, so I didn't run `make test` or `make lint`.