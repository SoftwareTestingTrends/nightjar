# [Diary] Bedtime in the skipped spring-forward hour saved as 03:30 with no warning, Slept shows 5h 30m

## Steps to reproduce

1. Start NightJar with a fresh diary (or call `POST /nights`, which is what the Log a night form submits).
2. Log a night with time zone `America/Toronto`, bedtime `2026-03-08 02:30`, wake time `2026-03-08 09:00`, no notes. On that date the clocks jump from 02:00 to 03:00, so 02:30 never exists in Toronto.
3. Look at the new row in the sleep diary.

## Expected

Not specified. No requirement or story says what NightJar should do with a local time that does not exist (see Notes). BR-07 only says NightJar "works for users who travel or live through daylight-saving changes". The user should not get a silently different bedtime, so the app should at least reject the input or warn, rather than quietly changing it.

## Actual

- The request is accepted (HTTP 303 redirect, no error shown).
- The bedtime is saved and shown as 03:30 (-04:00), not the 02:30 that was entered. There is no warning.
- Slept shows 5h 30m. Wake 09:00 EDT minus the saved bedtime 03:30 EDT is 5h 30m. The user entered 6h 30m on the clock.

## Evidence

Run through the app's own endpoint with a temp database and the mock coach:

```
status: 303
local bedtime: 2026-03-08 03:30:00-04:00 | duration: 5:30:00
['Slept', '03:30', '5h 30m']
```

Cause, for whoever picks this up: `diary.local_input_to_aware` does `datetime.fromisoformat(text).replace(tzinfo=zone(timezone))`. For the nonexistent 02:30 this gives 02:30-05:00, which is 07:30 UTC. That is 03:30 EDT when shown in local time. Nothing checks that the local time exists.

## Environment

NightJar `main` at commit f21f9d9, Python 3.12, `uv run`, mock coach, zone `America/Toronto`. Test data only.

## Notes

- Question for product: what should happen when the user enters a local time that does not exist (spring-forward gap)? Options: reject with a message asking for another time, or accept and show the adjusted time with a notice. No story or requirement says.
- The matching autumn case (an hour that happens twice, 01:30 on 2026-11-01) is not checked here. Worth a look when this is fixed.
- Not a duplicate of NJ-11. NJ-11 (Done) was about Slept being an hour off across the autumn clock change, and was fixed in `Night.duration`. Here the duration maths is right for the saved times. The wrong value comes from the saved bedtime.

Reproduced 2 of 2 times (direct call and through `POST /nights`). Related: NJ-11.
