It's a real bug, and I've written the repro at `bugs/reimport-duplicates/repro.py`.

**Cause:** `Diary.add_nights` in `src/nightjar/diary.py` calls `add_night` for every row and never checks whether a night is already stored. Nothing in the schema prevents duplicates either. The `/import` route in `web.py` goes through that same path.

**Expected behaviour:** Tracker NJ-12 (in `tools/tracker/seed.json`) describes this exact symptom and says nights already in the diary should not be added again.

**Repro:** The script imports `data/sample_nights.csv` into a throwaway database, imports it again, and compares the counts.
- Current output: `BUG: first import gave 21 nights, re-import left 42`
- Exit code is 1 while the bug is present, and 0 once re-importing leaves the count unchanged.
- It passes `ruff check` and `ruff format --check`. `bugs/` is gitignored, so the file won't be committed.

I didn't change any source code, so I didn't run `make test`. I also didn't create a `D-n` bundle or update `bugs/ledger.md`, since you asked only for the script at that path. If you want the bundle and ledger row per `docs/bug-bundles.md`, I can add them.