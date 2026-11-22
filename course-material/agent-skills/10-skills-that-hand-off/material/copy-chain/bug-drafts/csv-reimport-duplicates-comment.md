## New evidence for NJ-12

Reproduced on current main with a minimal script (bug bundle D-1): importing a 2-night CSV twice via `POST /import` on an empty diary gives 4 nights (expected 2). 3 of 3 runs.

## Steps to reproduce

1. Start with an empty diary.
2. `POST /import` with a diary CSV (test data, e.g. `data/sample_nights.csv`).
3. `POST /import` the same file again.

## Cause (from reading the code)

- `src/nightjar/diary.py`: `add_nights` calls `add_night` for every parsed row. The `nights` table has no uniqueness constraint or duplicate check.
- `web.py` `import_csv` then reports the full count as imported, so the user is told the duplicates were added.

## Evidence

`uv run python bugs/D-1-csv-reimport-duplicates/repro.py` exits 1 and prints
`DEFECT: 4 nights after importing a 2-night file twice (expected 2)`.

## Notes

Expected result matches NJ-12: nights already in the diary are not added again. No requirement says what the import message should show for skipped rows. Question for product.
