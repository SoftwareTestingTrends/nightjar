# D-1: A bedtime inside the spring-forward gap is silently stored and shown as a different time

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Open the diary form. Enter bedtime `2026-03-08 02:30`, wake time `2026-03-08 09:30`, time zone `America/Toronto`.
2. Submit, then read the Bed column of the new diary row.

Cause: `local_input_to_aware` (`src/nightjar/diary.py`) does `datetime.fromisoformat(text).replace(tzinfo=zone(...))`. At 02:00 on 2026-03-08 Toronto clocks jump to 03:00, so 02:30 never happened. `replace` accepts it anyway (treated as 02:30 EST, which is 07:30 UTC), and converting back for display gives 03:30 EDT. No error or notice is shown.

## Expected
Not specified. BR-07 and S-114 only say the app must work "across daylight-saving transitions"; nothing says what to do with a local time that doesn't exist.

Question for product: should the form reject a nonexistent local time with a clear message, shift it forward and tell the user, or something else? (The same gap applies to wake time.)

What is clear: the user sees a bedtime they didn't enter, with no explanation.

## Actual
The row shows Bed `03:30`. The stored instant is 07:30 UTC.

## Reproducibility
3 of 3 runs

## Repro
`uv run python bugs/D-1-dst-gap-bedtime-shifted/repro.py`

Exit 1 while an accepted bedtime is shown as a different time than the one entered. Exit 0 if the input is rejected or shown as entered. It deliberately doesn't pick between those fixes, since that's product's call.
