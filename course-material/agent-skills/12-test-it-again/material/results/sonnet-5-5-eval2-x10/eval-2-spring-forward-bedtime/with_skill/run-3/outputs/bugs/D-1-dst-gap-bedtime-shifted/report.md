# D-1: Bedtime typed as 02:30 on 8 Mar 2026 (Toronto) is silently saved and shown as 03:30

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Set timezone America/Toronto. Add a night with bedtime `2026-03-08T02:30`, wake `2026-03-08T09:30`.
2. Read it back from the diary (`Diary.nights()[0].local_bedtime`).

Cause: 02:30 does not exist that day (spring forward, 02:00 -> 03:00). `local_input_to_aware`
(`src/nightjar/diary.py:151`) attaches the zone with `replace(tzinfo=...)`, which resolves the
gap to 07:30 UTC, i.e. 03:30 EDT. Nothing tells the user.

## Expected
Not specified. No requirement or story covers a local time inside the DST gap.
Question for product: reject with a message, accept and show a notice that it was moved to 03:30,
or something else?

## Actual
Accepted with no warning; diary shows 03:30 (-04:00).

## Reproducibility
3 of 3 runs.

## Repro
`uv run python bugs/D-1-dst-gap-bedtime-shifted/repro.py`
Exit 1 = still shifted silently. Exit 0 = fixed. Assumption: "fixed" means the nonexistent
time is rejected with `ValueError`; adjust the script if product picks another behaviour.
