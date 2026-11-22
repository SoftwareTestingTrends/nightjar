It's a real bug. Importing the same CSV twice stores every night twice. I added a repro at `bugs/D-1-duplicate-csv-import/repro.py`, and it exits 1 right now:

```
BUG: imported the same 2-night CSV twice, diary holds 4 nights (expected 2)
```

**Cause:** in `src/nightjar/diary.py:70`, `Diary.add_nights` runs a plain `INSERT` for every row. Nothing checks whether a night is already there: the `nights` table has no unique constraint and no "already imported" check. The `/import` route in `web.py` calls it directly. Importing `data/sample_nights.csv` twice gave 42 nights instead of 21.

**Why it matters beyond the duplicate rows:** the extra copies change the usual-bedtime calculation. I imported a CSV with only 4 nights twice. That stored 8 rows, enough to pass the 7-night minimum, so `usual_bedtime` returned `23:18` when it should still have returned `None`. That breaks PR-21 item 2, which says no reminder with fewer than 7 nights. Duplicates also squeeze real nights out of the 14-night median.

**About the repro:**
- It uses a throwaway temp database and a 2-night CSV written inside the script, and prints one line saying what it saw.
- Run it with `uv run python bugs/D-1-duplicate-csv-import/repro.py`.
- I've only seen it exit 1. I haven't seen the 0 case, since there's no fix to test it against.
- I named the folder `D-1-duplicate-csv-import` rather than just a short name, to match the `bugs/D-<n>-<short-name>/` format in `docs/bug-bundles.md`. There was no ledger yet, so this is D-1.

**Not done:**
- I didn't write `report.md` or a `bugs/ledger.md` row; that format expects both, and the verify-fix skill reads the ledger. I can add them.
- I couldn't check the tracker for an existing ticket because it isn't running at http://127.0.0.1:8765. Start it with `make tracker`.
- I didn't change any app code.

When you fix it, you'll need to decide what counts as the same night. Bedtime plus wake time plus time zone seems sensible, and should the notes count too? You'll also need to decide whether a re-import skips duplicates or updates them.