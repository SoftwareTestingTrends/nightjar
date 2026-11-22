# D-1: A 02:30 bedtime on 8 March 2026 (Toronto) is accepted and shown as 03:30

Status: confirmed
Tracker: not filed

## Steps to reproduce

1. Use an empty diary.
2. Add a night with bedtime `2026-03-08T02:30` and wake time `2026-03-08T09:00`, zone `America/Toronto`
   (the web form or `Diary.add_night` with `local_input_to_aware`).
3. Read the night back and look at its local bedtime.

## Expected

Not specified. No requirement or story says what happens to a bedtime inside the
spring-forward gap. The clocks went from 02:00 to 03:00 that day, so 02:30 never occurred.

## Actual

The entry is accepted without a message. The diary shows the bedtime as 03:30 EDT
(stored as 2026-03-08T07:30 UTC). The cause is `local_input_to_aware`, which uses
`datetime.replace(tzinfo=...)` with `fold=0`. For a time in the gap, that picks the
pre-transition offset (EST, -05:00).

This matches the convention in `nudge.at_local_time`, where a DST-skipped wall time
moves forward to the next real instant (02:30 becomes 03:30). The nudge behaviour is
tested in `tests/test_nudge.py::test_T_114_6_nudge_time_skipped_by_dst_moves_forward_an_hour`.
The diary follows that convention, but no spec says the diary should.

## Reproducibility

3 of 3 runs.

## Repro

Command, from the repository root:

    uv run python bugs/D-1-dst-gap-bedtime/repro.py

- Exit 1: the defect is present. The entry is accepted and shown as 03:30 EDT.
- Exit 0: fixed. The impossible 02:30 entry is refused with a `ValueError`.

The fixed behaviour is my assumption. The report does not say what the diary should do,
so the script treats refusal as the fix. If product wants a different outcome, such as
accepting and showing 03:30 with a note, update the script's exit-0 condition to match.

## Questions for product

1. Should the diary refuse a bedtime or wake time that doesn't exist in the user's zone
   (the 02:00-03:00 gap on 8 March), or accept it and show the next real time, as the
   nudge does?
2. If it is accepted, is 03:30 EDT the right display, or should the entry say the time was adjusted?
3. The reporter logged 02:30. Did they mean 01:30 EST, or 03:30 EDT? If it was a
   mistake, this may not need a fix at all.
