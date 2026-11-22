# D-1: Importing the same CSV twice stores every night twice

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Start with an empty diary.
2. Import a CSV (e.g. `data/sample_nights.csv`) via Import CSV, or `Diary.add_nights(parse_csv(text))`.
3. Import the same file again.

## Expected
Not specified. No requirement or story says how re-imports or duplicate nights are handled.
Question for product: should an identical night (same bedtime, wake time, timezone) be skipped on import, replaced, or kept? Should the user be told how many were skipped?

## Actual
Every night is stored twice. `Diary.add_nights` inserts every row unconditionally and the `nights` table has no uniqueness constraint (`src/nightjar/diary.py`). The page reports `imported=<count>` for the full file each time. Duplicates also skew the usual-bedtime median (`sleep_window.py`), which could shift the nudge.

## Reproducibility
3 of 3 runs

## Repro
`uv run python bugs/D-1-csv-reimport-duplicates/repro.py` exits 1 while the nights are duplicated and 0 once a re-import stores no extra nights.
