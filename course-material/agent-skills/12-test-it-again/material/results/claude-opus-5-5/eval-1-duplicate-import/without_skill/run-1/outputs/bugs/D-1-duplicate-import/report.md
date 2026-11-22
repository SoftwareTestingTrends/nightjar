# D-1: Importing the same CSV twice stores every night twice

Status: confirmed
Tracker: not filed

## Steps to reproduce

1. Start with an empty diary.
2. POST a 2-night CSV to `/import`.
3. POST the same CSV to `/import` again.
4. Count the nights in the diary.

## Expected

2 nights. Re-importing a night that is already in the diary should not add a second copy
(the same bedtime can't happen twice).

## Actual

4 nights. `Diary.add_nights` (`src/nightjar/diary.py`) inserts every parsed row with a
plain `INSERT`, and the `nights` table has no uniqueness constraint, so nothing stops a
duplicate. Duplicates also skew the usual-bedtime median that the nudge (S-114) relies on.

Note: no written requirement covers re-import explicitly (S-117 AC6 only covers importing
into an empty diary), so the exact rule for "same night" (same bedtime? overlapping
times?) is a product decision.

## Reproducibility

3 of 3 runs.

## Repro

`uv run python bugs/D-1-duplicate-import/repro.py` exits 1 while the defect is present
(prints the duplicated count) and 0 once importing the same file twice leaves 2 nights.
