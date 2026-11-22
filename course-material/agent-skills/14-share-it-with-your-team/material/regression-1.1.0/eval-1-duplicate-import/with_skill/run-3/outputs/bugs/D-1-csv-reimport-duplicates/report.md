# D-1: Importing the same CSV twice stores every night twice

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Start with an empty diary.
2. Import a CSV with 2 nights (`bedtime,wake_time,timezone,notes`).
3. Import the exact same CSV again.
4. List the nights.

## Expected
Not specified. No requirement or story says what a re-import should do (S-114 and S-117 only cover import into an empty diary).

Question for product: should re-importing skip nights already in the diary (same bedtime, wake time and zone), warn the user, or add them again?

## Actual
4 nights are stored. The diary has no uniqueness rule: `Diary.add_night` always INSERTs, and the `nights` table has no unique constraint. Duplicate nights also skew the usual bedtime (median of the last 14 nights, minimum 7), so the nudge time can shift.

## Reproducibility
3 of 3 runs. This was reproduced at the `Diary` layer. I did not go through the web upload form, which calls the same import code.

## Repro
`uv run python bugs/D-1-csv-reimport-duplicates/repro.py`

Exits 1 while a 2-night CSV imported twice stores more than 2 nights, and 0 once only 2 are stored. If product decides that duplicates are acceptable, close this bug and delete the repro.
