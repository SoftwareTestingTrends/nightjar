# D-1: Bedtime typed inside the spring-forward gap is silently saved as a different time

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Start with an empty diary (user zone America/Toronto).
2. Log a night with bedtime `2026-03-08T02:30` and zone `America/Toronto` (POST `/nights`).
3. Look at the saved night's local bedtime.

On 8 March 2026 Toronto clocks jump from 02:00 straight to 03:00, so 02:30 never happens that day.

## Expected
Not specified. No requirement or story says what to do with a local time that doesn't exist (BR-07 and S-114 only say DST must be handled correctly). The repro assumes the app must not silently change what the user typed: either reject it with an error, or show it as typed. Product decides which.

Question for product: for a bedtime in the DST gap, should we reject it with a message, or accept it and move it to 03:30 (and tell the user)?

## Actual
The form is accepted with no error and the diary shows 03:30. Cause: `local_input_to_aware` in `src/nightjar/diary.py` uses `.replace(tzinfo=zone(...))`. Python treats the missing 02:30 as 02:30 EST (07:30 UTC), which displays as 03:30 EDT. The user is never told.

So the 03:30 is a side effect of the missing hour, not a random error. It is still a defect, because the change is silent. It also makes the night an hour shorter than the user thinks.

## Reproducibility
3 of 3 runs

## Repro
`uv run python bugs/D-1-dst-gap-bedtime-shifted/repro.py`

Exit 1 means the diary silently saved a different time than typed. Exit 0 means 02:30 was rejected, or is shown as typed.
