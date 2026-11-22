# D-1: Importing the same CSV twice stores every night twice

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Start with an empty diary.
2. Import a CSV containing one night (`POST /import`, or `Diary.add_nights(parse_csv(...))`).
3. Import the same file again.
4. List the nights.

## Expected
Not specified. No requirement or story says what a repeated import should do.
Question for product: should re-importing skip nights already in the diary (matching on bedtime, wake time and timezone), warn the user, or add them again?

## Actual
Every night appears twice. `nights` has no uniqueness constraint (`src/nightjar/diary.py` schema) and `add_nights` always inserts. Duplicates also feed `usual_bedtime`, since the median is taken over stored nights.

## Reproducibility
3 of 3 runs.

## Repro
`uv run python bugs/D-1-csv-reimport-duplicates/repro.py`
Exits 1 while a 1-night CSV imported twice stores 2 nights; exits 0 once it stores 1. The script assumes "skip duplicates" as the fix. If product chooses differently, update the script.
