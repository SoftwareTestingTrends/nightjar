# D-1: Bedtime entered in the spring-forward gap is silently shifted an hour (02:30 shows as 03:30)

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Open the diary with a user in `America/Toronto`.
2. Log a night with bedtime `2026-03-08 02:30` and wake time `2026-03-08 09:00`, time zone `America/Toronto`.
3. Look at the night in the diary table.

Cause: `local_input_to_aware` (`src/nightjar/diary.py`) uses `datetime.fromisoformat(text).replace(tzinfo=zone(timezone))`.
On 2026-03-08 clocks in Toronto jump from 02:00 to 03:00, so 02:30 does not exist. `replace` accepts it
(fold=0, treated as EST, UTC-5), it is stored as 07:30 UTC, and that renders as 03:30 EDT.

## Expected
Not specified. No requirement or story says what to do with a local time that doesn't exist.
S-114 only requires the nudge to be correct across DST.

Question for product: when a user types a time that was skipped by the clock change, should NightJar
(a) reject it with a clear message, (b) accept it and tell the user it was moved to 03:30, or (c) something else?
Either (a) or (b) is better than silently showing a different time than the user typed.

## Actual
The form accepts it (HTTP 303) and the diary shows bedtime 03:30. The user is never told it changed.

## Reproducibility
3 of 3 runs.

## Repro
`uv run python bugs/D-1-spring-forward-bedtime-shifted/repro.py`

Exits 1 while the bug is present (the input is accepted and shown as 03:30). Exits 0 once the app either
rejects the nonexistent time (HTTP 400) or shows 02:30. If product picks option (b), update the repro's
pass condition to match.
