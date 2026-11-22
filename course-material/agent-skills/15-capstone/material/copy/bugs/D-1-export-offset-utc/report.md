# D-1: CSV export writes every time in UTC (+00:00) instead of the night's own offset

Status: fixed
Tracker: NJ-15

## Steps to reproduce
1. Start with an empty diary.
2. Add one night: bedtime `2026-03-01T00:25:00-05:00`, wake `2026-03-01T07:30:00-05:00`, zone `America/Toronto`.
3. Download the export (`/export`, or `Diary.export_csv()`).

## Expected
S-117 AC3: times are ISO 8601 with the UTC offset of that night's own zone, e.g.
`2026-03-01T00:25:00-05:00,2026-03-01T07:30:00-05:00,America/Toronto,`.

## Actual
`2026-03-01T05:25:00+00:00,2026-03-01T12:30:00+00:00,America/Toronto,`

Cause (from reading the code, not yet fixed): `Diary.nights()` rebuilds datetimes from the UTC
text in `bedtime_utc`, so they carry a UTC tzinfo, and `export_csv` (`src/nightjar/diary.py:75`)
calls `.isoformat()` on them without converting to `zone(night.timezone)`. The instants are
right; the offset is wrong. It also breaks AC6 round-trip fidelity of local times.

## Reproducibility
3 of 3 runs

## Repro
`uv run python bugs/D-1-export-offset-utc/repro.py`: exits 1 while the export shows +00:00, 0 once it shows the night's own offset.
