# D-1: Importing the same CSV twice stores every night twice

Status: confirmed
Tracker: not filed

## Steps to reproduce

1. Start with an empty diary.
2. On the home page, import a CSV with 2 nights (`POST /import`). The page says "Imported 2 nights."
3. Import the same file again. The page says "Imported 2 nights." again.
4. Look at the diary (`Diary.nights()`, or the diary list on the page).

## Expected

Not specified. No requirement or story (BR-07, PR-21, S-114, S-116, S-117) says what
should happen when an import contains nights the diary already has. S-117 AC6 only
covers importing into an *empty* diary. Each night appearing once is the likely intent,
but product has to decide that.

**Question for product:** When an imported night matches one already in the diary
(same bedtime and wake time), should NightJar skip it, update it (for example its
notes), or reject the whole import? And should the "Imported N nights" message count
only the nights that were actually added?

## Actual

The diary holds 4 nights, two copies of each. `Diary.add_nights`
(`src/nightjar/diary.py`) inserts every parsed row without checking for duplicates, and
the `nights` table has no uniqueness constraint. Both imports report "Imported 2 nights."

Impact: duplicate nights feed into the usual-bedtime median (last 14 nights), so a
re-import changes which nights count and can shift the nudge time. The diary list
also shows each night twice.

## Reproducibility

3 of 3 runs (2026-11-21).

## Repro

`uv run python bugs/D-1-reimport-duplicates-nights/repro.py`

Imports a 2-night CSV twice through the real `/import` endpoint against a temporary
database. Exits 1 while the defect is present ("diary holds 4 nights"). Exits 0 once
the diary holds exactly 2 nights. If product picks "reject the import", the second
import would no longer return 200, so the script's status assert would need updating.
