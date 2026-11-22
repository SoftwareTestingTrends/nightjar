# D-1: Bedtime 02:30 on 2026-03-08 (Toronto) is silently saved as 03:30

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Open the diary with an empty database; time zone America/Toronto.
2. Log a night with bedtime `2026-03-08T02:30` and wake time `2026-03-08T09:30`.
3. Look at the bedtime the diary shows.

(On 2026-03-08 clocks in Toronto jump from 02:00 straight to 03:00, so 02:30 never happens that night.)

## Expected
Not specified. No requirement or story says what to do with a local time that doesn't exist
(DST spring-forward gap). The input is not valid, so showing exactly "02:30" isn't possible either.

Question for product: should the form reject it with a clear message, accept it and tell the
user it was adjusted to 03:30, or something else? (Sleep for a user who really went to bed
"around 02:30" by their clock is also affected, see Cause.)

## Actual
The entry is accepted (HTTP 303, no warning) and the diary shows 03:30. The user's input is
changed without any notice.

Cause: `local_input_to_aware` in `src/nightjar/diary.py` does
`datetime.fromisoformat(text).replace(tzinfo=zone(timezone))`. For a time in the gap,
zoneinfo (fold=0) uses the pre-transition offset (EST, UTC-5), so 02:30 EST = 07:30 UTC,
which is 03:30 EDT. The ambiguous autumn case (01:30 occurs twice) is silently resolved to
the first occurrence in the same way. Not a rendering bug: the stored instant is the shifted one.

## Reproducibility
3 of 3 runs.

## Repro
`uv run python bugs/D-1-dst-gap-bedtime-shifted/repro.py`

Exits 1 while the diary silently shows 03:30 for the 02:30 entry; exits 0 once the entry is
rejected or the diary shows 02:30 as entered. If product picks "accept and show the adjusted
time with a notice", update the repro to check for that notice.
