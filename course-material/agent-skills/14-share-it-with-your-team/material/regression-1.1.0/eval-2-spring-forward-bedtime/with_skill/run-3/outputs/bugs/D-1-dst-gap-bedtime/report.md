# D-1: A bedtime of 02:30 on 8 Mar 2026 (Toronto) is silently shown as 03:30

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Set the zone to America/Toronto.
2. Log a night with bedtime `2026-03-08T02:30` and wake time `2026-03-08T09:30`.
3. Read the diary row's bedtime.

## Expected
Not specified. No requirement or story says what happens when a user enters a local time
that doesn't exist (BR-07 only asks for correctness across daylight-saving changes).

Background: on 8 Mar 2026 Toronto clocks jump from 02:00 to 03:00, so 02:30 never happens.
The app stores the instant in UTC. `local_input_to_aware` attaches the zone with the
pre-jump offset (-05:00), which is 07:30 UTC, which is 03:30 EDT. So 03:30 is the correct
conversion of that instant, but the user is never told their input was invalid or moved.

Question for product: for a time in the spring-forward gap, should the diary reject it
with a message, move it forward (as now) but say so, or something else?

## Actual
The diary shows 03:30. There is no warning or error.

## Reproducibility
3 of 3 runs.

## Repro
`uv run python bugs/D-1-dst-gap-bedtime/repro.py` exits 1 while the diary shows a time
different from the one entered with no warning. It exits 0 once the input is rejected
with an error or shown as entered. Product's answer may change what "fixed" means.
