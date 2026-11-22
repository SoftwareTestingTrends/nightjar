# [Export] CSV export writes times with +00:00 instead of the night's own UTC offset

## Steps to reproduce

1. Start with an empty diary.
2. Add one night: bedtime `2026-03-01T00:25:00-05:00`, wake `2026-03-01T07:30:00-05:00`, zone `America/Toronto`.
3. Download the export (`/export`, or `Diary.export_csv()`).

## Expected

S-117 AC3: times are ISO 8601 with the UTC offset of that night's own zone, e.g.
`2026-03-01T00:25:00-05:00,2026-03-01T07:30:00-05:00,America/Toronto,`

## Actual

`2026-03-01T05:25:00+00:00,2026-03-01T12:30:00+00:00,America/Toronto,`

The instants are correct; only the offset and wall time are wrong. This also breaks AC6 (round-trip fidelity of local times).

## Evidence

`uv run python bugs/D-1-export-offset-utc/repro.py` exits 1 and prints the +00:00 row above.

## Environment

NightJar at commit 64f34e5 (S-117 first version), local run, test data only.

## Notes

Likely cause (from reading code, not fixed): `Diary.nights()` rebuilds datetimes from the UTC text in `bedtime_utc`, and `export_csv` (`src/nightjar/diary.py:75`) calls `.isoformat()` without converting to `zone(night.timezone)`.
Searches (export, UTC, CSV, offset, timezone, and phrase variants) found no duplicate. NJ-11 (Done) is related but different: duration across DST, not export format.

Reproduced 3 of 3 times. Related: NJ-11.
