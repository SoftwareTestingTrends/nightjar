# D-1: Quiet hours 21:00 to 00:00 reported as "invalid time"

Status: not reproduced
Tracker: not filed (tracker already has NJ-14 with the same claim, still Open)

## Steps to reproduce
1. Fresh throwaway database (temp dir, not nightjar.db).
2. POST /settings with timezone=America/Toronto, quiet_start=21:00, quiet_end=00:00
   (what the page's time inputs send).
3. GET / and read the saved values.

## Expected
00:00 is accepted as the end of quiet hours.

## Actual
303 redirect, no error. The page shows quiet_start=21:00 and quiet_end=00:00.
Only "24:00" and "0:00" return 400 (a time input cannot produce either).
"23:59" and "00:00:00" are also accepted.

## Reproducibility
Not reproduced: 0 of 3 runs showed the error.

## Repro
None written, because the defect did not reproduce. If the reporter can give the exact
input, browser or error message, try again with that.
