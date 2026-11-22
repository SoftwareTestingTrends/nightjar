# D-1: Importing the same CSV twice duplicates every night

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Start with an empty diary.
2. Import a CSV with 2 nights (`bedtime,wake_time,timezone,notes`) via Import CSV.
3. Import the exact same file again.

## Expected
Not specified. No requirement or story says what a repeat import should do
(S-117 AC6 only covers importing an export into an *empty* diary).

Question for product: should re-importing skip nights that already exist
(same bedtime, wake time and timezone), import them again, or warn the user?

## Actual
Every row is inserted again: 2 nights imported twice gives 4 rows. `nights` has no
uniqueness constraint (`src/nightjar/diary.py`, `add_night` is a plain INSERT) and
`/import` reports "Imported 2 nights." both times. Duplicates also weigh double in
`usual_bedtime` (median of the last 14 nights, min 7), so the nudge time can shift.
The last point is from reading the code and was not tested.

## Reproducibility
3 of 3 runs

## Repro
`uv run python bugs/D-1-csv-reimport-duplicates/repro.py`
Exit 1 while the diary holds duplicates (defect present); exit 0 once a repeat import leaves 2 rows.
Note: if product decides duplicates are acceptable, the repro's exit code should be revisited.
