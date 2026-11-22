# D-1: A bedtime typed inside the spring-forward gap is accepted and shown an hour later

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Start with an empty diary.
2. Log a night with bedtime `2026-03-08 02:30`, wake time `2026-03-08 09:30`, zone `America/Toronto`.
3. Look at the bedtime in the diary.

(On 8 March 2026 Toronto clocks jump from 02:00 to 03:00, so 02:30 never happens that night.)

## Expected
Not specified. No requirement or story covers nonexistent local times. Open question for product, below.

## Actual
The form accepts the night (HTTP 303) with no error or notice. The diary then shows bedtime 03:30, not the 02:30 that was typed.

Cause: `local_input_to_aware` (`src/nightjar/diary.py`) attaches the zone to the typed wall time without checking that it exists. 02:30 gets the pre-jump offset (-05:00), is stored as 07:30 UTC, and reads back as 03:30 EDT.

The 03:30 is the right instant for that stored value. The defect is the silent change.

## Reproducibility
3 of 3 runs

## Repro
`uv run python bugs/D-1-dst-gap-bedtime-shifts/repro.py`

Exit 1 while a gap time is accepted and shown as something other than what was typed. Exit 0 once it is rejected (HTTP 400) or shown as typed.

## Questions for product
- For a bedtime in the spring-forward gap, should NightJar reject it with a message, shift it and tell the user, or something else?
- The repro treats "rejected" or "shown as typed" as fixed. If product picks "shift and tell the user", the repro needs updating.
