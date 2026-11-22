# D-1: Bedtime 02:30 on the spring-forward night is silently saved and shown as 03:30

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Set the time zone to America/Toronto.
2. Log a night with bedtime `2026-03-08T02:30` (any later wake time, e.g. 09:00).
3. Look at the diary entry.

Cause: `local_input_to_aware` (`src/nightjar/diary.py:153`) does `.replace(tzinfo=zone)`.
On 2026-03-08 clocks jump 02:00 to 03:00 in Toronto, so 02:30 doesn't exist. Python
treats it as 02:30 EST (UTC-5), which is 07:30 UTC. Once stored as UTC and read back, that is 03:30 EDT.

## Expected
Not specified. No requirement or story says what happens when a user enters a local time
that doesn't exist. S-114 only requires DST correctness for the nudge.
Question for product: should the app reject the input with a message, move it to the
nearest valid time and tell the user, or something else?

## Actual
The entry is accepted with no warning and the diary shows 03:30, not 02:30. Nothing tells
the user their input was changed. The same applies to the wake time.

## Reproducibility
3 of 3 runs

## Repro
`uv run python bugs/D-1-dst-gap-bedtime/repro.py`

Exit 1 while a gap-time bedtime is silently shown as a different time. Exit 0 once it is
rejected with an error or shown as entered.
