# D-1: Bedtime in the spring-forward gap (02:30 on 2026-03-08, Toronto) is silently saved as 03:30

Status: confirmed
Tracker: not filed

## Steps to reproduce

1. Start NightJar with an empty diary.
2. In "Log a night", enter Bedtime `2026-03-08 02:30`, Wake time `2026-03-08 09:00`,
   Time zone `America/Toronto`, and click "Save night".
3. Look at the new row in the sleep diary.

Context: 2026-03-08 is spring-forward day in America/Toronto. Clocks jump from 02:00 EST
to 03:00 EDT, so 02:30 local time never happens that day.

## Expected

Not specified. No requirement or story (BR-07, PR-21, S-114, S-116, S-117) says what
should happen when someone enters a local time that doesn't exist. BR-07 only says
NightJar "works for users who … live through daylight-saving changes".

Question for product: when an entered bedtime or wake time falls in a DST gap, should
NightJar (a) reject it with a message, (b) save it as the shifted time (03:30) and tell
the user, or (c) keep doing what it does now and shift it silently?

## Actual

The form accepts the entry (303 redirect, no error). The night is stored as
`2026-03-08T07:30:00+00:00`, and the diary shows Bed **03:30** with Slept **5h 30m**.
The page doesn't say the time was changed.

Cause: `local_input_to_aware()` in `src/nightjar/diary.py` does
`datetime.fromisoformat(text).replace(tzinfo=zone)`. For a wall time in the gap,
`zoneinfo` (with fold=0) uses the pre-transition offset of -05:00. So 02:30 EST becomes
07:30 UTC, which shows as 03:30 EDT. The same shift is described as intentional in
`nudge.at_local_time()` for nudge scheduling, but nothing documents it for diary input.

## Reproducibility

3 of 3 runs (form route through the app against a throwaway SQLite database). The repro
script also printed DEFECT on 3 of 3 runs.

## Repro

`uv run python bugs/D-1-dst-gap-bedtime-shifted/repro.py`

Exit 1 means the defect is present: the night was saved, the diary shows 03:30 and no
error or notice appeared. Exit 0 means it's fixed: the time was rejected, or the page
shows a message (`role="alert"`). If product picks option (b) and the notice uses some
other element, update the check to match.
