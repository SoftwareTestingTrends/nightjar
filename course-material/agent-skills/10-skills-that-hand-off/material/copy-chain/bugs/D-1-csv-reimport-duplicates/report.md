# D-1: Importing the same CSV twice stores every night twice

Status: fixed
Tracker: duplicate of NJ-12 (open)

## Steps to reproduce
1. Start with an empty diary.
2. Import a diary CSV (for example `data/sample_nights.csv`) via `POST /import`.
3. Import the same file again.

## Expected
Nights already in the diary are not added again. The diary has one entry per night.

## Actual
Every night is stored a second time. A 2-night file gives 4 nights after two imports.
The cause is in `src/nightjar/diary.py`. `add_nights` calls `add_night` for every
parsed row, and the `nights` table has no uniqueness constraint or duplicate check.
`web.py` `import_csv` then reports the full count as imported.

## Reproducibility
3 of 3 runs

## Repro
`uv run python bugs/D-1-csv-reimport-duplicates/repro.py`

Exit 1 means the defect is present (prints the night count it saw). Exit 0 means it is fixed.

Note: the tracker seed data contains a ticket that appears to describe this same defect
(the "uploaded it again by mistake" report). `/file-bug` should search for it first and
record "duplicate of NJ-n" if it is still open.
