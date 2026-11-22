# D-1: Importing the same CSV twice stores every night twice

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Start with an empty diary.
2. Import a CSV with 2 distinct nights (`POST /import`, or `Diary.add_nights(parse_csv(...))`).
3. Import the same CSV again.

## Expected
Nights already in the diary are not added again: 2 nights stored.

## Actual
4 nights stored; every night appears twice. Cause: `Diary.add_nights` / `add_night` in `src/nightjar/diary.py` do a plain `INSERT`, and the `nights` table has no uniqueness constraint or duplicate check. The docs don't state a rule for re-imports; the expectation comes from the report and the seeded tracker ticket's wording.

## Reproducibility
3 of 3 runs

## Repro
`uv run python bugs/D-1-csv-reimport-duplicates/repro.py`

Uses a throwaway temp database. Exits 1 while duplicates are stored (prints the count seen), 0 once the second import adds nothing.
