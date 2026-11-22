# D-1: Importing the same CSV twice stores every night twice

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Start with an empty diary.
2. Import a CSV (for example `data/sample_nights.csv`) with **Import CSV**.
3. Import the same file again.
4. The diary now holds every night twice.

Cause: `Diary.add_nights` (`src/nightjar/diary.py`) inserts every row. The `nights` table has no
uniqueness constraint, and nothing checks for existing nights.

## Expected
Not specified. No requirement or story says what a repeated import should do (skip duplicates,
replace, warn, or allow them).

Question for product: should re-importing a night that already exists be ignored, replaced, or
reported to the user? And what makes two nights "the same" (same bedtime and wake time in UTC)?

## Actual
Each import adds all its rows again. A 1-night CSV imported twice gives 2 stored nights. The
page says "Imported N nights" both times. Duplicated nights are counted twice by the
usual-bedtime median, so the nudge can be skewed.

## Reproducibility
3 of 3 runs

## Repro
`uv run python bugs/D-1-csv-reimport-duplicates/repro.py`

Exits 1 while a second import of the same CSV stores duplicates, and 0 once it stores each night
only once. The repro asserts "1 night", which is one possible product decision; if product picks
another behaviour, update the repro.
