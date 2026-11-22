# D-1: Importing the same CSV twice stores every night twice

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Start with an empty diary.
2. Import a CSV with one night (`bedtime,wake_time,timezone,notes` header plus one row).
3. Import the same file again.
4. List the nights: the one night is stored twice.

Cause: the `nights` table has no uniqueness constraint, and `Diary.add_night` / `add_nights` (`src/nightjar/diary.py`) always INSERT. The `/import` handler in `web.py` doesn't check for existing nights.

## Expected
Not specified. No requirement or story says what a re-import should do (skip duplicates, replace, or add). Only S-117 AC6 touches import, and only for an empty diary.

Question for product: should re-importing a file skip nights already in the diary, and if so, what makes two nights "the same" (bedtime + wake time? bedtime only?)?

## Actual
Every night in the file is stored again. Duplicates feed `usual_bedtime` (median of the last 14 nights), so they skew the nudge time.

## Reproducibility
3 of 3 runs.

## Repro
`uv run python bugs/D-1-csv-reimport-duplicates/repro.py` exits 1 while a 1-night CSV imported twice gives 2 nights, and 0 once it gives 1. It uses a temporary database.
