# D-1: A bedtime typed inside the spring-forward gap is silently stored an hour later

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Log a night with timezone `America/Toronto`, bedtime `2026-03-08T02:30`, wake time `2026-03-08T09:30` (POST `/nights`, or the form).
2. Look at the diary. The bedtime shows 03:30.

Cause: `local_input_to_aware` (`src/nightjar/diary.py`) does `.replace(tzinfo=zone(...))`. 02:30 does not exist on that date (clocks jump 02:00 to 03:00), so it resolves with the pre-transition offset (-05:00) to 07:30 UTC, which is 03:30 EDT. Nothing tells the user.

## Expected
Not specified. No requirement or story says what to do with a local time that doesn't exist. See the question for product.

## Actual
The night is accepted (HTTP 303) and the diary shows 03:30. Duration is an hour shorter than the user would expect (6 h instead of 7 h for 02:30 to 09:30), and the usual-bedtime median can be affected.

## Questions for product
- Should a nonexistent local time be rejected with a message ("02:30 doesn't exist on 8 March in Toronto"), or accepted and shifted forward with a visible notice? Either would make the repro exit 0. The repro treats "no silent change" as fixed.
- Same question for CSV import and for the ambiguous hour in autumn (01:30 occurs twice).

## Reproducibility
3 of 3 runs

## Repro
`uv run python bugs/D-1-dst-gap-bedtime-shifted/repro.py` prints one line. Exit 1 means the bedtime was silently changed (bug present). Exit 0 means it was rejected or kept as entered (fixed).
