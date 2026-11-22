# D-1: Importing the same CSV twice duplicates every night in the diary

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Start with an empty diary.
2. Import a CSV with 2 nights (`bedtime,wake_time,timezone,notes`).
3. Import the same file again.
4. Look at the diary.

## Expected
Not specified. No requirement or story says what a re-import should do (S-117 AC6 only
covers importing an exported file into an *empty* diary).

Question for product: should re-importing a file skip nights already in the diary
(same bedtime, wake time and zone), add them again, or ask the user?

## Actual
Every row is inserted again: 2 nights imported twice gives 4 nights. `Diary.add_night`
is a plain `INSERT` and the `nights` table has no uniqueness constraint. The page
reports "Imported 2 nights." both times.

Likely knock-on (not checked): duplicated nights skew the 14-night usual bedtime
window in `sleep_window.py`, so the nudge time can shift.

## Reproducibility
3 of 3 runs.

## Repro
`uv run python bugs/D-1-csv-import-twice-duplicates/repro.py`

Exits 1 while a double import leaves duplicates (it prints the night count), and 0
once the diary holds only the 2 distinct nights. If product decides duplicates are
fine, update the script's expectation.
