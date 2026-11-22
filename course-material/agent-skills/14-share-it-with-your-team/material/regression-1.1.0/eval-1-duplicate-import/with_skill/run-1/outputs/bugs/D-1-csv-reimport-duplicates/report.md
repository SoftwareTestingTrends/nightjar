# D-1: Importing the same CSV twice stores every night twice

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Start with an empty diary.
2. Import a CSV with 2 nights (`POST /import`, or `parse_csv` + `Diary.add_nights`).
3. Import the identical CSV again.
4. List the nights.

## Expected
Not specified. No requirement or story says what a re-import should do. The reporter's
expectation (and the seeded tracker ticket's) is that nights already in the diary are not
added again.

Question for product: should a re-import skip nights that match an existing one (same
bedtime, wake time and zone), replace them, or warn the user? What counts as "the same night"?

## Actual
Every night is stored a second time: 2 distinct nights imported twice give 4 rows.
Cause: `nights` has no uniqueness constraint and `Diary.add_nights` (`src/nightjar/diary.py:70`)
inserts every row unconditionally.

## Reproducibility
3 of 3 runs.

## Repro
`uv run python bugs/D-1-csv-reimport-duplicates/repro.py` from the repository root.
Exit 1 while duplicates are stored; exit 0 once a re-import leaves 2 nights.
