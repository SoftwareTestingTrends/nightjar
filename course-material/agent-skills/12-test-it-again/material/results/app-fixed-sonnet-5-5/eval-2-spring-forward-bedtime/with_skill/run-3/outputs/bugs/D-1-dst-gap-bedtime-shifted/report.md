# D-1: Bedtime 02:30 on spring-forward day (Toronto) is silently shown as 03:30

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Add a night with timezone America/Toronto, bedtime `2026-03-08T02:30`, wake time `2026-03-08T08:00` (via the form, `POST /nights`).
2. Look at the night in the diary.

## Expected
Not specified. No requirement or story says what to do with a wall time that DST skips.
Note that 02:30 on 2026-03-08 does not exist in Toronto (clocks jump 02:00 -> 03:00), so
"shows 02:30" is not possible. The app's own nudge code deliberately maps such times
forward (02:30 becomes 03:30, see `nudge.py`), so the shift itself may be fine. What is
unclear is whether the user should be told, or the entry rejected.

Question for product: for a bedtime that falls in the DST gap, should NightJar (a) accept
and shift it, with a visible notice, (b) accept silently as today, or (c) reject with an error?

## Actual
The entry is accepted (303 redirect, no message) and the diary shows 03:30. The user entered
02:30 and is never told it was changed. Cause: `local_input_to_aware` attaches the zone to a
nonexistent wall time (`diary.py:159`); the instant is stored as 07:30 UTC, which renders as 03:30 EDT.

## Reproducibility
3 of 3 runs

## Repro
`uv run python bugs/D-1-dst-gap-bedtime-shifted/repro.py` exits 1 while the entry is accepted
and shown as 03:30 with no notice, 0 once it's rejected or the page tells the user. That
definition of "fixed" is my assumption until product answers the question above.
