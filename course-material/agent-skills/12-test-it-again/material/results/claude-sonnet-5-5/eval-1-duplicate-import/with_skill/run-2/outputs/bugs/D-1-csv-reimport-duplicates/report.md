# D-1: Importing the same CSV twice stores every night twice

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Start with an empty diary.
2. Import a CSV with one night (`bedtime,wake_time,timezone,notes` header plus one row).
3. Import the exact same CSV again.
4. List the nights.

## Expected
Not specified. No requirement or story says whether re-importing should skip, merge or
duplicate nights (S-117 AC6 only covers import of an export into an *empty* diary).

Question for product: should a re-import skip nights that already exist (same bedtime,
wake time and timezone), and should the import report how many were skipped?

## Actual
Every row is inserted again. The diary holds 2 nights after importing a 1-night CSV twice.
Cause: `Diary.add_night` (`src/nightjar/diary.py`) is a plain `INSERT`, and the `nights`
table has no uniqueness constraint, so `add_nights` never checks for existing rows.
Duplicates also skew `usual_bedtime` (median of the last 14 nights, so duplicated nights
count twice).

## Reproducibility
3 of 3 runs

## Repro
`uv run python bugs/D-1-csv-reimport-duplicates/repro.py`

Exits 1 while a second import of the same CSV leaves duplicate nights, 0 once the diary
holds each night once. Because "Expected" is not specified, the script encodes the
reporter's expectation (no duplicates); product should confirm it.
