# D-1: Importing the same CSV twice stores every night twice

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Start with an empty diary.
2. Import a CSV with 2 nights (`bedtime,wake_time,timezone,notes`).
3. Import the exact same CSV again.
4. List the nights.

## Expected
Not specified. No requirement or story says what a re-import should do (`docs/` has nothing on duplicates).

Question for product: should re-importing skip nights already stored (same bedtime, wake time and timezone), replace them, or add them again? Duplicated nights skew the usual bedtime (median of the last 14 nights), so the nudge time can shift.

## Actual
Every night is stored again: a 2-night CSV imported twice gives 4 nights. Cause: the `nights` table has no uniqueness constraint, and `Diary.add_night` / `add_nights` (`src/nightjar/diary.py`) always INSERT. The web `/import` route calls the same path.

## Reproducibility
3 of 3 runs

## Repro
`uv run python bugs/D-1-csv-reimport-duplicates/repro.py` exits 1 while a double import stores 4 nights, and 0 once it stores 2. It uses a throwaway temp database. It exercises `Diary` directly, the same code the `/import` route uses.
