# D-1: Settings reject quiet hours 21:00 to 00:00 as "invalid time"

Status: not reproduced
Tracker: not filed (tracker already has NJ-14 describing the same report, status Open)

## Steps to reproduce
1. Throwaway database, `create_app(...)` with the mock coach, TestClient.
2. `POST /settings` with `timezone=America/Toronto`, `quiet_start=21:00`, `quiet_end=00:00`.
3. Read the saved user back, and call `in_quiet_hours` for 20:00, 21:00, 23:00, 00:00, 01:00.

## Expected
00:00 is accepted as the end of quiet hours.

## Actual
Accepted: 303 redirect, no error, saved as 21:00 to 00:00. `in_quiet_hours` gives
False, True, True, False, False for the five times, which is correct for a window that wraps midnight.

## Reproducibility
0 of 3 runs showed the defect.

## Repro
None written: nothing to reproduce. Not tested in a real browser or on a deployed build.
