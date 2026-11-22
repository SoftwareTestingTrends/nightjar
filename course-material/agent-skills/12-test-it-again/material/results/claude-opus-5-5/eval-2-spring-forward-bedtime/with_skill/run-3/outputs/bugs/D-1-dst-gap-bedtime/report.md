# D-1: Bedtime in the spring-forward gap (02:30, 8 Mar 2026, Toronto) is silently saved and shown as 03:30

Status: confirmed
Tracker: not filed

## Steps to reproduce

1. Start with an empty diary.
2. Log a night with the form: bedtime `2026-03-08T02:30`, wake time `2026-03-08T09:30`,
   time zone `America/Toronto`.
3. Look at the sleep diary.

## Expected

Not specified. No requirement or story (BR-07, PR-21, S-114, S-116, S-117) says what
the app should do when someone enters a local time that doesn't exist. 02:30 on
2026-03-08 is inside the DST gap in America/Toronto, where clocks jump from 02:00 to 03:00.

Question for product: when a user enters a time that DST skipped, should NightJar
(a) reject it and ask for a real time, (b) save the shifted time (03:30) and tell the
user, or (c) keep saving it silently as it does now?

## Actual

The form accepts the entry with HTTP 200 and shows no message. The diary row shows bedtime
**03:30**, wake 09:30, duration 6h 00m, night of Sat 07 Mar.

Cause: `local_input_to_aware` (`src/nightjar/diary.py:151`) attaches the zone with
`.replace(tzinfo=...)`. For a nonexistent wall time, `zoneinfo` (fold=0) uses the
pre-transition offset, so the value becomes 02:30-05:00 = 07:30 UTC = 03:30-04:00. The stored
instant and the duration agree with each other. The only problem is that the user isn't told.
`nudge.at_local_time` does the same normalisation on purpose (see its docstring), but
that is for computed nudge times, not for user input.

CSV import isn't affected, because it requires explicit UTC offsets.

## Reproducibility

3 of 3 runs (2026-11-21).

## Repro

`uv run python bugs/D-1-dst-gap-bedtime/repro.py`

Exits 1 while the gap time is saved silently and the page shows 03:30 without mentioning
02:30. Exits 0 if the entry is rejected (nothing saved), or if the page mentions 02:30
(for example, a notice that it was saved as 03:30). That pass condition covers options
(a) and (b) above. If product picks (c), close this bug as working as intended rather
than changing the script.
