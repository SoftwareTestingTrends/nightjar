# D-1: Importing the same CSV twice stores every night twice

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Start with an empty diary.
2. Import a CSV (for example `data/sample_nights.csv`).
3. Import the same file again.

## Expected
The second import adds nothing (or tells the user the nights already exist). The
diary holds each night once.

## Actual
Every night is stored again, so the diary has 2x the rows. `Diary.add_night` does a plain
`INSERT` and the `nights` table has no uniqueness rule on (bedtime, wake time, timezone).
`/import` then reports `imported=<count>` as if all rows were new. Duplicates also feed the
usual-bedtime median in `sleep_window.py`, so they can skew the nudge.

No requirement in `docs/` states a dedupe rule, so the intended behavior (skip silently vs.
warn) needs a product decision. Either way, silently doubling the diary is a defect.

## Reproducibility
3 of 3 runs.

## Repro
`uv run python bugs/D-1-csv-reimport-duplicates/repro.py` uses a throwaway temp database,
imports a 2-night CSV twice and counts stored nights. Exit 1 = duplicates stored (bug
present); exit 0 = each night stored once (fixed).
