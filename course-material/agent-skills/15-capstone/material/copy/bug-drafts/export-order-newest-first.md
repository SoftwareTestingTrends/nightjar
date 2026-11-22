# [Export] CSV export lists nights newest first when the diary has several nights

## Steps to reproduce

1. Start with an empty diary.
2. Add three nights with bedtimes 2026-03-01, 2026-03-02, 2026-03-03 (notes: first, second, third).
3. Download the export (`/export`, or `Diary.export_csv()`).

## Expected

S-117 AC4: nights in "night of" order, oldest first: first, second, third.

## Actual

Rows come out in the order third, second, first (newest first).

## Evidence

`uv run python bugs/D-2-export-order-newest-first/repro.py` prints
`export order: ['third', 'second', 'first']` and exits 1 (exits 0 once fixed).

## Environment

NightJar main at 64f34e5, local app, test data only.

## Notes

Likely cause (from reading the code, not verified by a fix): `export_csv` (`src/nightjar/diary.py:75`) iterates `self.nights()`, which is `ORDER BY bedtime_utc DESC` for the diary page. The export needs its own ascending order; `nights()` itself should stay as is because the page relies on it.

Reproduced 3 of 3 times. Related: none.
