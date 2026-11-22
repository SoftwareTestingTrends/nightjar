This isn't a bug, so I didn't write a repro script, bundle or ledger row.

On the night of Saturday 31 October 2026, clocks in America/Toronto go back an hour at 02:00 on Sunday 1 November. Daylight saving ends, and 02:00 EDT becomes 01:00 EST. That night has 9 real hours between 23:00 and 07:00, not 8.

I ran the calculation 3 times with a `Night` from 23:00 on 31 Oct to 07:00 on 1 Nov in America/Toronto. All 3 runs gave the same result:

- **UTC offsets:** The bedtime is at UTC-4 and the wake time is at UTC-5.
- **`duration`:** It came out as `9:00:00`, which is the elapsed time.
- **Night date:** `night_of` is 2026-10-31, as expected.

`Night.duration` in `src/nightjar/models.py` converts both times to UTC before subtracting, which is the right approach. If you want a night to read as 8 hours on wall-clock time, that would be a change in what the app shows. It wouldn't be a fix for a bug.

I haven't touched the ledger because `bugs/` doesn't exist yet and the ledger has one row per bundle. If you'd like this logged as `not reproduced`, I can add that row.