# D-1: Quiet hours 21:00 to 00:00 reported as "invalid time"

Status: not reproduced
Tracker: not filed

## Steps to reproduce
As reported: Settings, quiet hours from 21:00 to 00:00, save.
What I ran (3 times, throwaway temp-dir database, real app via `TestClient`):
`POST /settings` with `timezone=America/Toronto`, `quiet_start=21:00`, `quiet_end=00:00`.
Also tried `00:00:00` and `21:00:00` variants.

## Expected
00:00 is accepted as the end of quiet hours (the window wraps midnight).

## Actual
Accepted every time: HTTP 303 redirect, saved as `21:00` / `00:00`, and the page shows
`00:00` back in the field. Only `24:00` is rejected (HTTP 400), and browsers' time
inputs don't send that. "Invalid time" appears nowhere in `src/`.

## Reproducibility
0 of 3 runs.

## Repro
None written: the defect did not reproduce. Existing tracker ticket NJ-14 describes the
same report ("rejected with 'Invalid time'; 23:59 works"), but it may be stale or
describe a different build or browser. Next step for the reporter: exact browser,
the exact error text and screen, and the value shown in the field.
