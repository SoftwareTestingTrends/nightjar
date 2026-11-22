# D-1: Bedtime in the spring-forward gap is silently saved and shown an hour later

Status: confirmed
Tracker: not filed

## Steps to reproduce

1. Start with an empty diary.
2. In "Log a night", enter bedtime `2026-03-08 02:30`, wake time `2026-03-08 09:00`,
   time zone `America/Toronto`, and save.
3. Look at the new row in the sleep diary.

## Expected

Not specified. No requirement or story (BR-07, PR-21, S-114, S-116, S-117) says what
should happen when someone enters a local time that doesn't exist. BR-07 only says
NightJar "works for users who … live through daylight-saving changes".

Question for product: on spring-forward night 02:00–02:59 doesn't exist in
America/Toronto. When someone enters a time in that gap, should the form
(a) refuse it and ask for a real time, (b) save it as 03:30 and tell the user it was
moved, or (c) save it as 03:30 silently (what happens now)? Also: should the CSV import
behave the same way? (Import requires a UTC offset, so it can't hit this gap.)

## Actual

The form accepts it with no message (HTTP 303). It's stored as `2026-03-08T07:30:00Z`,
and the diary shows Bed `03:30` (EDT). "Slept" shows 5h 30m, measured from 03:30.

Cause: `local_input_to_aware()` in `src/nightjar/diary.py` does
`datetime.fromisoformat(text).replace(tzinfo=zone(timezone))`. For a time in the gap,
`zoneinfo` (fold=0) applies the pre-transition offset (-05:00). So 02:30 EST becomes
07:30Z, which reads back as 03:30 EDT. Nothing checks whether the wall time exists.
`nudge.py` does the same 02:30 → 03:30 shift on purpose for scheduling (see its
docstring), but nothing says that's right for user input.

## Reproducibility

3 of 3 runs (2026-11-21).

## Repro

`uv run python bugs/D-1-dst-gap-bedtime-shifted/repro.py`

Uses a throwaway temp database and the app's real form endpoint. Exits 1 while the form
saves the gap time silently and the diary shows a different bedtime. Exits 0 if the form
refuses it (non-303, nothing saved) or the diary shows `02:30`. That check assumes fix
(a). If product picks (b), extend the check to look for the notice.
