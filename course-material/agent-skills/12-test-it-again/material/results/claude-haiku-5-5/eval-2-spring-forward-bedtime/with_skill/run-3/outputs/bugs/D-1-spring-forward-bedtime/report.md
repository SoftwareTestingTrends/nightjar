# D-1: A bedtime entered inside the spring-forward gap is silently shown an hour later

Status: confirmed
Tracker: not filed

## Steps to reproduce

1. In the diary form, set time zone America/Toronto and enter bedtime `2026-03-08 02:30`
   (Sunday 8 March 2026 is the spring-forward day: clocks jump 02:00 -> 03:00).
2. Enter any wake time after it, e.g. `2026-03-08 08:00`, and save.
3. Look at the diary entry.

Underlying path: `web.py` calls `local_input_to_aware()` (`diary.py`), which does
`datetime.replace(tzinfo=ZoneInfo)` with `fold=0`. For a time that doesn't exist, that picks
the pre-jump offset (UTC-5), so 02:30 EST is stored as 07:30 UTC. The diary then displays
07:30 UTC in Toronto as 03:30 EDT.

## Expected

Not specified. No requirement or story says what a wall-clock time that does not exist
should do (reject it, or store it and show it as entered). The 02:30 -> 03:30 mapping
matches the convention in `nudge.py` `at_local_time()`, which documents that DST-skipped
times normalise to 03:30. That convention is for computed nudge times, not user input.

## Actual

The save succeeds with no warning. The diary shows 03:30 EDT for a bedtime the user
entered as 02:30.

## Reproducibility

3 of 3 runs (`repro.py` exit 1 each time).

## Repro

Command, from the repository root:

    uv run python bugs/D-1-spring-forward-bedtime/repro.py

- Exit 1: the defect is present. The script prints `BUG: entered 2026-03-08T02:30 (no error), diary shows 03:30`.
- Exit 0: fixed. Either the input is rejected with an error, or the diary shows 02:30.
  The script accepts either outcome, so it does not decide which one product wants.

## Question for product

For a bedtime that falls in the spring-forward gap, should the diary:

a. reject it with a message asking the user to pick a time that exists, or
b. accept it and show the normalised time (03:30 today), with or without a note?

Until product decides, the repro accepts either (a) or showing 02:30 as fixed.
