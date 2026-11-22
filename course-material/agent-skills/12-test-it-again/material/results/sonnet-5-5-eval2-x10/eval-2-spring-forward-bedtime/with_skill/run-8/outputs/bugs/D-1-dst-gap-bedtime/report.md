# D-1: A bedtime in the spring-forward gap (02:30, 8 Mar 2026, Toronto) is silently saved and shown as 03:30

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Fresh empty database. Open the diary form (or `POST /nights`).
2. Bedtime `2026-03-08T02:30`, wake time `2026-03-08T09:00`, timezone `America/Toronto`.
3. Submit, then look at the night's bedtime in the diary.

Cause: `local_input_to_aware` (`src/nightjar/diary.py:151`) does `.replace(tzinfo=ZoneInfo)`. On 8 Mar 2026
clocks in Toronto jump 02:00 -> 03:00, so 02:30 never happened. Python resolves it with the
pre-transition offset (-05:00), which is 07:30 UTC, which is 03:30 EDT. The app accepts it (303) with no warning.

## Expected
Not specified. No requirement or story says what to do with a local time that doesn't exist.
The user's input and the diary disagree, and they are never told.

Question for product: should a nonexistent local time be rejected with a message (e.g. "02:30 doesn't exist on
8 March in Toronto; clocks went forward"), or moved forward deliberately and the user told? The repro assumes
"rejected with a 400" or "stored as typed" counts as fixed; adjust it if product decides otherwise.

## Actual
The form is accepted (HTTP 303). The diary shows bedtime 03:30. Not the "02:30" the user typed, and no message.
The 03:30 is a consequence of Python's gap handling, not a decision. The same applies to the wake time field.

## Reproducibility
3 of 3 runs.

## Repro
`uv run python bugs/D-1-dst-gap-bedtime/repro.py`
Exit 1 = the nonexistent time was accepted and shown as 03:30. Exit 0 = it was rejected with a 400 (or stored as typed).
