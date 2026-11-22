# D-1: Re-importing the same CSV stores every night a second time

Status: confirmed
Tracker: not filed

## Steps to reproduce

1. Start from an empty diary (a new database).
2. On the home page, choose `data/sample_nights.csv` and click Import. The diary shows 21 nights.
3. Import the same file again.
4. Look at the diary.

## Expected

Nights already in the diary are not added again: the diary still holds 21 nights.
(Source: NJ-12 in the tracker, "Re-uploading a CSV adds the same nights again". No
requirement or story in `docs/` covers re-importing.)

Question for product: what makes two nights "the same"? Options are the same bedtime and
wake time, or the same bedtime alone. Should a file that overlaps the diary add only its new nights?

## Actual

The second import stores all 21 nights again. The diary holds 42 nights, and every night
appears twice. `Diary.add_nights` in `src/nightjar/diary.py` runs a plain `INSERT` for every
row and never checks for an existing night.

## Reproducibility

3 of 3 runs (`uv run python bugs/D-1-csv-reimport-duplicates/repro.py` printed
`defect: re-importing the same file stored 21 more nights (42 total, expected 21)` each time).

## Repro

Command, run from the repository root:

    uv run python bugs/D-1-csv-reimport-duplicates/repro.py

It uploads `data/sample_nights.csv` to `/import` twice, in a temporary database, and
compares the night count after each upload.

- Exit 1: the defect is present (the second upload added nights).
- Exit 0: fixed (the count stayed the same after the second upload).
