# D-1: Bedtime 02:30 on 2026-03-08 (Toronto) is silently saved and shown as 03:30

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Open the diary with an empty database; user zone America/Toronto.
2. Add a night: bedtime `2026-03-08T02:30`, wake time `2026-03-08T09:30`, timezone `America/Toronto`.
3. Look at the diary row (`Night.local_bedtime`).

## Expected
Not specified. No requirement or story says what to do with a local time that falls in a
DST gap (S-114 only covers nudge scheduling across DST).

Context for product: on 2026-03-08 Toronto clocks jump from 02:00 to 03:00, so 02:30
never existed that night. The 03:30 the user sees is the same instant as "02:30 on the
pre-change offset" (07:30 UTC), so the report is not wrong arithmetic, but the user is
told nothing about it.

## Actual
The form returns 303 (accepted). The diary shows bedtime 03:30. `local_input_to_aware`
(`src/nightjar/diary.py`) does `datetime.fromisoformat(text).replace(tzinfo=zone(...))`,
which keeps the non-existent wall time with the pre-transition offset (-05:00); converting
to UTC and back lands on 03:30 EDT. No error or note is shown.

## Reproducibility
3 of 3 runs

## Repro
`uv run python bugs/D-1-nonexistent-local-time-shifted/repro.py`
Exit 1 = the input is accepted and shown as something other than what was typed (present).
Exit 0 = the input is rejected with HTTP 400, or shown as typed (fixed).
Prints one line, e.g. `typed 02:30, HTTP 303, diary shows 03:30`.

## Question for product
What should happen when a user logs a time that doesn't exist (DST gap)? Options: reject
with a message, shift forward with a visible note, or something else. Until decided,
the repro's "fixed" condition (rejected or shown as typed) is a proposal; adjust it if
product picks "shift forward with a note".
