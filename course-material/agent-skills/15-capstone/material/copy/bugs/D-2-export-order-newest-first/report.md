# D-2: CSV export lists nights newest first instead of oldest first

Status: fixed
Tracker: NJ-16

## Steps to reproduce
1. Start with an empty diary.
2. Add three nights with bedtimes 2026-03-01, 2026-03-02, 2026-03-03 (notes first, second, third).
3. Download the export (`/export`, or `Diary.export_csv()`).

## Expected
S-117 AC4: nights in "night of" order, oldest first: first, second, third.

## Actual
Order is third, second, first.

Cause (from reading the code, not yet fixed): `export_csv` (`src/nightjar/diary.py:75`) iterates
`self.nights()`, which is `ORDER BY bedtime_utc DESC` (newest first, for the page). The export
needs its own ascending order; don't flip `nights()` as the diary page relies on it.

## Reproducibility
3 of 3 runs

## Repro
`uv run python bugs/D-2-export-order-newest-first/repro.py`: exits 1 while the export is newest first, 0 once it is oldest first.
