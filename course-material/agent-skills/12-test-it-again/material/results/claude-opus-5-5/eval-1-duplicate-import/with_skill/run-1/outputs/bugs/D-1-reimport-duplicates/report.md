# D-1: Importing the same CSV twice stores every night twice

Status: confirmed
Tracker: not filed

## Steps to reproduce

1. Start with an empty diary.
2. POST a 2-night CSV (`bedtime,wake_time,timezone,notes`) to `/import`.
3. POST the same file to `/import` again.
4. Count the nights in the diary.

## Expected

Not specified. No requirement or story (PR-21, S-114, S-116, S-117) says what
re-importing nights that are already in the diary should do. S-117 AC6 only covers
importing into an *empty* diary.

Question for product: when an imported row matches a night already in the diary
(same bedtime instant, for example), should NightJar skip it, update it, or keep both?
And should the "Imported N nights." message count only the new ones?

## Actual

The diary holds 4 nights: every row is inserted again. `Diary.add_nights` calls
`add_night` (a plain `INSERT`) for each row, and the `nights` table has no uniqueness
constraint, so nothing detects the duplicates. The page reports "Imported 2 nights."
both times.

Possible impact: the usual bedtime is the median of the last 14 rows (PR-21 §1). With
duplicates, those 14 rows cover only 7 real nights. With `data/sample_nights.csv`
imported twice (42 rows) the nudge stayed at 22:15, so the sample data doesn't show a
visible change. Other diaries could see one.

## Reproducibility

3 of 3 runs.

## Repro

`uv run python bugs/D-1-reimport-duplicates/repro.py`

Uses a throwaway temp database and the real `/import` endpoint. Exits 1 while the
defect is present (the diary holds 4 nights), and 0 once re-importing leaves 2.
