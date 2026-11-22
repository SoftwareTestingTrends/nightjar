# D-1: Bedtime typed in the spring-forward gap (02:30, 8 Mar 2026, Toronto) is silently shown as 03:30

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Time zone America/Toronto. Log a night with bedtime `2026-03-08T02:30` (any later wake time, e.g. 09:30).
2. Look at the diary row.

(Same path as the web form: `local_input_to_aware` in `src/nightjar/diary.py:151`, then `Night.local_bedtime`.)

## Expected
Not specified. No requirement or story says what happens when the user enters a local time that doesn't exist.

Context: on 8 Mar 2026 Toronto clocks jump 02:00 -> 03:00, so 02:30 never happens that night. Showing 03:30 is the correct instant (`.replace(tzinfo=)` takes fold=0, i.e. 02:30 at the old -05:00 offset = 07:30 UTC = 03:30 EDT), so the stored data isn't corrupted. The problem is that the user typed one time and sees another, with no message.

Question for product: for a nonexistent local time, should we (a) reject it with a message, (b) accept and tell the user it was moved to 03:30, or (c) keep silently shifting? The repro treats "rejected" or "shows the typed time" as fixed. If product picks (b), the repro needs updating.

## Actual
Diary shows bedtime 03:30. No warning. Input was accepted.

## Reproducibility
3 of 3 runs.

## Repro
`uv run python bugs/D-1-dst-gap-bedtime-shifted/repro.py`
Exit 1 = defect present (prints `BUG: ...`). Exit 0 = fixed (the input is rejected with ValueError, or the diary shows 02:30).
