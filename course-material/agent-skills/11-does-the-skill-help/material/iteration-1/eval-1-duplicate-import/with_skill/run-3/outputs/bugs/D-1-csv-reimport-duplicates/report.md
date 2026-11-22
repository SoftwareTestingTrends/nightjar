# D-1: Importing the same CSV twice stores every night twice

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Start with an empty diary.
2. Import a CSV with 2 nights (`POST /import`, or `parse_csv` then `Diary.add_nights`).
3. Import the same CSV again.
4. List the nights.

## Expected
Nights already in the diary are not added again: 2 nights stored.

## Actual
Every night is stored a second time: 4 stored. `Diary.add_nights` (`src/nightjar/diary.py`) inserts each row unconditionally. The `nights` table has no uniqueness constraint, so nothing rejects a repeat.

## Reproducibility
3 of 3 runs

## Repro
`uv run python bugs/D-1-csv-reimport-duplicates/repro.py`

Exits 1 while the bug is present (prints `... -> 4 stored (expected 2)`) and 0 once re-importing leaves 2 nights.
