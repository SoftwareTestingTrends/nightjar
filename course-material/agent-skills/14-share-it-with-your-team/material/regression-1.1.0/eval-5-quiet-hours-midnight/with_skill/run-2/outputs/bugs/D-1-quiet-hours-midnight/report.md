# D-1: Quiet hours 21:00 to 00:00 reported as "invalid time"

Status: not reproduced
Tracker: not filed

## Steps to reproduce
As reported: Settings, quiet hours 21:00 to 00:00, save.
Tried against a throwaway database through `POST /settings` (the same call the form makes), 3 times.

## Expected
Not specified in the requirements, but the wrap-around window code (`in_quiet_hours`) treats 21:00 to 00:00 as valid.

## Actual
Not reproduced. `POST /settings` with `quiet_start=21:00`, `quiet_end=00:00` returns 303 (saved) every time. The Settings page then shows `00:00` as the saved end time. `00:00:00` is also accepted. Only `24:00` is rejected (HTTP 400), which is correct.

Not tried in a real browser. The page has no client-side validation script. A browser-only cause would need a browser check, for example `/nightjar-qa:browser-check`.
Open tracker ticket NJ-14 describes the same report ("Invalid time", and "23:59 works"). It may be stale, or the reporter may have typed a different value, such as `24:00`.

## Reproducibility
0 of 3 runs showed the defect.

## Repro
None written, because the bug did not reproduce.
