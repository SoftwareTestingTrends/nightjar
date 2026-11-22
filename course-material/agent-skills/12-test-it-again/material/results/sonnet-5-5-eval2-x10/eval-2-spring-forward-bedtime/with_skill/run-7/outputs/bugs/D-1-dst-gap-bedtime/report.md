# D-1: Bedtime typed inside the spring-forward gap is silently shown an hour later

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. In the diary form, enter bedtime `2026-03-08 02:30`, wake time `2026-03-08 10:00`, zone `America/Toronto`.
2. Submit and look at the diary row ("Sat 07 Mar").

## Expected
Not specified. No requirement or story covers a local time that doesn't exist.
S-114 only requires the nudge to be correct across DST.

Context: on 8 Mar 2026 Toronto clocks jump from 02:00 to 03:00, so 02:30 never
happened. Showing 03:30 is the arithmetically consistent reading
(`local_input_to_aware` in `src/nightjar/diary.py` attaches the zone with fold=0, so
02:30 is read at the pre-transition offset, -05:00, which is 07:30 UTC, which is 03:30 EDT).
The defect is that the shift is silent: the user typed 02:30 and is never told.

Question for product: for a bedtime in the DST gap, should we reject it with a message,
accept and show a notice that it was moved to 03:30, or something else?

## Actual
Form accepted (303). Diary shows bedtime 03:30, no error or notice.

## Reproducibility
3 of 3 runs

## Repro
`uv run python bugs/D-1-dst-gap-bedtime/repro.py` exits 1 while the user gets no
rejection and no notice (page text containing "daylight", "does not exist",
"doesn't exist" or "skipped"), and 0 once the form is rejected or a notice is shown.
The pass condition is a stand-in until product decides the behaviour; adjust it then.
