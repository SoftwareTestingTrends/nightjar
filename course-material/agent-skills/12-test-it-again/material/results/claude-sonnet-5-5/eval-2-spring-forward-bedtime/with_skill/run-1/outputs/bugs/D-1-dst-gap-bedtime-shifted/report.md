# D-1: Bedtime 02:30 on 2026-03-08 (Toronto) is silently stored and shown as 03:30

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Log a night with bedtime `2026-03-08T02:30` and zone `America/Toronto` (POST `/nights`).
2. Read the night back; its local bedtime is 03:30.

2026-03-08 is Toronto's spring-forward day: clocks jump from 02:00 to 03:00, so 02:30
never exists that night. `local_input_to_aware` (`src/nightjar/diary.py`) attaches the
zone with `replace(tzinfo=...)`, which resolves the nonexistent time to 07:30 UTC (03:30 EDT).
The user is never told their input was changed.

## Expected
Not specified. S-114 only says "correct across daylight-saving transitions". Question for
product: for a bedtime in the DST gap, should the app reject it with a clear message, shift
it (and tell the user), or something else?

## Actual
The entry is accepted with no warning and shown as 03:30. The user's 02:30 is not
what they typed, and the night is 1 hour shorter or longer than they may expect.

## Reproducibility
3 of 3 runs

## Repro
`uv run python bugs/D-1-dst-gap-bedtime-shifted/repro.py` prints what it saw. Exit 1 means
the bedtime was accepted but shown as something other than 02:30 (bug present). Exit 0
means it was shown as 02:30 or rejected with a 400 (fixed).
