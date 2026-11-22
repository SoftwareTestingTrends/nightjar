# D-1: Importing the same CSV twice stores every night twice

Status: confirmed
Tracker: not filed

## Steps to reproduce

1. Start with an empty diary.
2. Import a CSV (e.g. `data/sample_nights.csv`) via **Import CSV** (`POST /import`).
3. Import the same file again.

## Expected

Each night appears once; re-importing a night that is already in the diary does not
add another row.

## Actual

Every night is stored twice. `Diary.add_nights` (`src/nightjar/diary.py`) does a plain
`INSERT` per row, and the `nights` table has no uniqueness constraint, so nothing
detects that a night already exists.

Impact beyond a cluttered diary: `usual_bedtime` takes the last 14 *rows*, so duplicates
halve the real window to 7 distinct nights, and 4 distinct nights imported twice pass
the 7-night cold-start minimum (PR-21 / S-114 edge T-114-5), so a nudge appears when it
shouldn't.

## Reproducibility

Deterministic (no clock or randomness involved).

## Repro

`uv run python bugs/D-1-csv-reimport-duplicates/repro.py`: imports a 2-night CSV twice
into a throwaway diary. Exit 1 = bug present (4 nights stored); exit 0 = fixed (2 nights).
