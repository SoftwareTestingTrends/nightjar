# D-1: Bedtime 02:30 on 2026-03-08 (Toronto) is silently saved and shown as 03:30

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Open the diary with an empty database.
2. Log a night with bedtime `2026-03-08 02:30`, wake `2026-03-08 08:00`, time zone `America/Toronto` (`POST /nights`).
3. Look at the Bed column in the diary table.

## Expected
Not specified. S-114 only says the nudge must be "correct across daylight-saving transitions" and says nothing about logging a bedtime. Note that 02:30 does not exist in Toronto that night: clocks jump from 02:00 to 03:00, so the user could not have seen 02:30 on a clock.

Question for product: should a bedtime in the spring-forward gap be rejected with a message, snapped to a valid time with a notice, or accepted silently as today?

## Actual
The form is accepted (303 redirect, no error) and the diary shows `03:30`. `local_input_to_aware` (`src/nightjar/diary.py:151`) attaches the zone to the naive value without checking that it exists, so 02:30 is stored as 07:30 UTC (= 03:30 EDT). The user is never told that the time they typed was changed. Sleep duration is computed from the shifted time.

## Reproducibility
3 of 3 runs

## Repro
`uv run python bugs/D-1-dst-gap-bedtime-shifted/repro.py`: exits 1 while the diary silently shows a time other than 02:30; exits 0 once the input is rejected with an error (HTTP 400) or shown as entered. Any other fix needs the script updated to match product's answer.
