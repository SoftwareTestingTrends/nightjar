This isn't a bug, so I haven't written a `repro.py`, a bundle, or a ledger row.

**What happens:** NightJar reports 9h for that night, and 9h is correct. Daylight saving time ended in America/Toronto on Sunday 1 November 2026. At 02:00 EDT the clocks went back to 01:00 EST, so the 01:00–02:00 hour happened twice.

I ran the night through the app's own `Night` model:
- **Bedtime:** 2026-10-31 23:00 at UTC-04:00.
- **Wake time:** 2026-11-01 07:00 at UTC-05:00.
- **Duration:** `Night.duration` returned `9:00:00`.

Between 23:00 and 07:00 on the wall clock there were 9 real hours, not 8. Counting the clock face gives 8 hours, but you were in bed for 9. `Night.duration` subtracts in UTC for this reason, as `CLAUDE.md` describes. It's the DST handling working as designed.

If your wake time was 07:00 by the clock, that's 9 hours of sleep. If you felt you slept 8, the usual cause is a device that didn't shift its clock, or a bedtime entered an hour off.

I haven't checked whether the page tells users that a night spans the clock change. That would be a product question about whether to add a note like "includes the extra DST hour". I can raise it as an enhancement if you want, but it isn't a calculation defect.