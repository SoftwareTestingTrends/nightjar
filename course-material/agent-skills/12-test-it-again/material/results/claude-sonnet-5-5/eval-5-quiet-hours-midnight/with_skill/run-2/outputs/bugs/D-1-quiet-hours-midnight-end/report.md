# D-1: Quiet hours 21:00 to 00:00 reported as "invalid time"

Status: not reproduced
Tracker: not filed

## Steps to reproduce
POST /settings with timezone=America/Toronto, quiet_start=21:00, quiet_end=00:00 (throwaway DB, TestClient).

## Expected
Not specified in a requirement; accepting 00:00 as the end of quiet hours is reasonable.

## Actual
303 redirect to /, no error. The settings page shows 00:00 as the saved end. 23:59 behaves the same.

## Reproducibility
0 of 3 runs showed the error.

## Repro
None written: the report did not reproduce. A tracker seed ticket "[Settings] Quiet hours can't end at midnight" describes the same symptom and may be stale.
