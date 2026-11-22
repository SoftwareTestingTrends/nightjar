Yes, it's a real bug. I reproduced it: importing a two-night CSV twice stores 4 nights instead of 2.

**Cause:** `Diary.add_nights` in `src/nightjar/diary.py:70` inserts every row it's given. The `nights` table has no uniqueness constraint, and nothing checks for existing nights. The `/import` handler in `web.py` goes straight from `parse_csv` to `add_nights`.

The tracker already has this as NJ-12, "Re-uploading a CSV adds the same nights again", still open. Its description says nights already in the diary should not be added again.

**Repro:** `bugs/reimport-duplicates/repro.py` uses a throwaway temp database. It imports the same CSV twice and prints what it saw. It exits 1 while the count is wrong and 0 once it's 2. I ran it with `uv run python bugs/reimport-duplicates/repro.py`, and it exited 1 with "2 nights imported twice -> 4 stored (expected 2)".

- **Folder name:** I used the path you gave. `docs/bug-bundles.md` expects `bugs/D-<n>-<short-name>/` with a `report.md` and a ledger row. I haven't created those. I can rename the folder and add them if you want this to work with the other testing skills.
- **Fix:** I haven't changed any code. The simplest fix is a unique index on `(bedtime_utc, timezone)` plus `INSERT OR IGNORE`. The import count should then report only the nights actually added.