# D-1: Importing the same CSV twice stores every night twice

Status: confirmed
Tracker: not filed

## Steps to reproduce

1. Start with an empty diary.
2. `POST /import` with a CSV of 2 nights (America/Toronto, 2026-03-18 and 2026-03-19).
3. `POST /import` the exact same file again.
4. List the diary's nights.

## Expected

Not specified. No requirement or story (BR-07, PR-21, S-114, S-116, S-117) says what
re-importing nights that are already in the diary should do: skip them, replace them,
or reject the file.

There is a knock-on effect that *is* specified. Duplicate rows count as separate nights
in `usual_bedtime()`:
- PR-21 §2 says fewer than 7 nights is a cold start with no reminder. Importing 4 real
  nights twice gives 8 rows, so the nudge turns on.
- PR-21 §1 says the window is the last 14 nights. With duplicates it covers only 7
  distinct nights.

**Question for product:** if an imported night is already in the diary (same bedtime
instant and time zone), should it be skipped, replace the stored one, or fail the
import? And what should the "imported N nights" message say in that case?

## Actual

Both imports succeed (303, `?imported=2` each time) and the diary ends up with 4 nights:
each night is stored twice. `Diary.add_nights` (`src/nightjar/diary.py`) inserts every
parsed row, and the `nights` table has no uniqueness constraint.

## Reproducibility

3 of 3 runs (2026-11-21).

## Repro

`uv run python bugs/D-1-double-import/repro.py`

It imports a 2-night CSV twice through the real `/import` endpoint against a temporary
database. Exit 1 means the diary holds more than 2 nights (bug present). Exit 0 means
it holds exactly 2 (fixed).
