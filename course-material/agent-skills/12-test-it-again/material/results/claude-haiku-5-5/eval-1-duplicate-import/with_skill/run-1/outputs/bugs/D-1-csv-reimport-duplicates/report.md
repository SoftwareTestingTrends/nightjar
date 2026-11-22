# D-1: Importing the same CSV twice stores every night twice

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Start with an empty diary.
2. Import a CSV with one night through Import CSV (`POST /import`):
   `2026-03-01T23:00:00-05:00,2026-03-02T07:00:00-05:00,America/Toronto,`
3. Import the same file again.
4. Count the nights in the diary.

The same happens with `data/sample_nights.csv`: the first import stores 21 nights and the
second stores 21 more, giving 42 rows. Both responses say `Imported 21 nights.`

## Expected
Not specified. No requirement or story says what a repeat import should do. The repro
assumes one copy of the night should remain. Product needs to confirm this (see questions).

## Actual
The second import adds every night again. The diary ends up with two copies of each night.
The app reports success both times (redirect to `/?imported=N`, status 303).

## Reproducibility
3 of 3 runs. Sample CSV: 21 rows, then 42 rows. Repro CSV: 1 night, then 2 nights.

## Repro
From the repository root: `uv run python bugs/D-1-csv-reimport-duplicates/repro.py`

- Exit 1: the defect is present. It prints `BUG: importing the same CSV twice left 2 nights in the diary (expected 1)`.
- Exit 0: the diary holds one copy after a repeat import, whatever the fix does (skip, replace or reject).

The script uses a temporary database, not `nightjar.db`.

## Questions for product
- When a CSV contains a night already in the diary, should the import skip it, replace the
  stored copy, or reject the file? (The import message currently reports the full row count.)
- What counts as the same night: same bedtime instant, or same bedtime and timezone?
- Should the import message count only the nights actually added?

## Why it matters (not verified)
`usual_bedtime` in `sleep_window.py` takes the median over the last 14 nights, so duplicate
rows probably shift the usual bedtime and the nudge time. Not checked yet.
