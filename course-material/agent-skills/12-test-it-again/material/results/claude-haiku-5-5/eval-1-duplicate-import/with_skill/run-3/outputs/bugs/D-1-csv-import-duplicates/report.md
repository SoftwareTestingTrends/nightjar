# D-1: Importing the same CSV twice stores every night twice

Status: confirmed
Tracker: not filed

## Steps to reproduce

1. Start with an empty diary.
2. Import `data/sample_nights.csv` (21 nights). The diary now holds 21 nights.
3. Import the same file again.
4. Count the nights in the diary.

## Expected

Not specified. No requirement or story says what a repeated import should do.
The likely expectation is that the diary still holds 21 nights (the file's nights are
not added a second time), but that is a product decision.

## Actual

The diary holds 42 nights. Every night from the file is stored twice. The page reports
"Imported 21 nights" on the second import as well.

Cause: `nightjar.diary.Diary.add_nights` inserts every night unconditionally. The `nights`
table has no unique constraint, and nothing compares the incoming nights with the stored
ones. The `/import` route in `nightjar.web` calls `add_nights` directly.

## Reproducibility

3 of 3 runs (3 of 3 with the repro script, and 3 of 3 through the `/import` route in a
temporary database).

## Repro

Command, from the repository root:

```
uv run python bugs/D-1-csv-import-duplicates/repro.py
```

- Exit 1: the defect is present. The script prints `BUG: 42 nights after importing the same 21-night file twice`.
- Exit 0: the defect is fixed. The script prints `OK: 21 nights ...`.

The script uses a temporary database and never touches `nightjar.db`.

## Questions for product

- After a repeated import of the same file, should the diary keep 21 nights (skip
  duplicates), or should it replace the earlier copies? What counts as "the same night":
  the same bedtime and wake time, or the same night of with any times?
- Should the import message report how many nights were new, not how many rows were read?
