# D-1: Importing the same CSV twice stores every night twice

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Start with an empty diary.
2. Import a CSV with one night (`bedtime,wake_time,timezone,notes` header).
3. Import the exact same CSV again.
4. List the nights.

The same path goes through the web `POST /import`, which calls `parse_csv` then `Diary.add_nights`. The `nights` table has no uniqueness constraint and `add_night` always INSERTs.

## Expected
Not specified. No requirement or story says what a re-import should do (skip duplicates, replace, or add). Question for product: should importing a night that already exists (same bedtime, wake time and timezone) be skipped, or is a repeated import meant to add rows? A duplicate night also skews the usual-bedtime median that drives the nudge.

## Actual
Every night in the file is stored again. A 1-night CSV imported twice gives 2 nights.

## Reproducibility
3 of 3 runs

## Repro
`uv run python bugs/D-1-csv-reimport-duplicates/repro.py`

Exits 1 while the second import adds duplicates, 0 once the diary holds 1 night. It assumes the fix is to skip duplicates. If product decides otherwise, update the script.
