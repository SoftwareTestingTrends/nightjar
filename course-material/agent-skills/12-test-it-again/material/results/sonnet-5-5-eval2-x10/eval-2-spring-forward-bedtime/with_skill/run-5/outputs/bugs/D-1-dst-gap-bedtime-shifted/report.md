# D-1: Bedtime 02:30 on the spring-forward night is silently saved as 03:30

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Open the diary with time zone America/Toronto.
2. Log a night with bedtime `2026-03-08 02:30` and wake time `2026-03-08 09:30`.
3. The night is saved with no error, and the diary shows a bedtime of 03:30.

## Expected
Not specified. No requirement or story says what to do with a local time that doesn't
exist. On 8 March 2026 clocks in Toronto jump from 02:00 to 03:00, so 02:30 never
happened. The app can't show 02:30, but it also shouldn't change what the user typed
without telling them.

Question for product: should the form (a) reject a nonexistent time with a clear message,
(b) accept it and say it was adjusted to 03:30, or (c) something else? The same question
applies to CSV import.

## Actual
`local_input_to_aware` (`src/nightjar/diary.py:151`) attaches the zone with
`.replace(tzinfo=...)`. For a time in the gap, Python uses the pre-transition offset
(EST, -05:00), which is 07:30 UTC. That is 03:30 EDT on the wall clock. The night is saved
and shown as 03:30 with no warning. The user's bedtime looks wrong by an hour, and
anything built on it (usual bedtime, nudge, coach) inherits the shift.

So the "bug" is not the 03:30 itself. It is that the app silently accepts a time that
doesn't exist and rewrites it.

## Reproducibility
3 of 3 runs

## Repro
`uv run python bugs/D-1-dst-gap-bedtime-shifted/repro.py` exits 1 while a nonexistent
bedtime is saved without error and shown at a different time. It exits 0 once the request
is rejected, or the bedtime is kept as entered.
