This isn't a bug, so I didn't write a repro script or a bundle.

**Why the 9h is correct:** Daylight saving time in Toronto ended on Sunday 1 November 2026 at 02:00. The clocks went back to 01:00, so that night had 9 real hours. I checked this against the app's own logic:

- Bed at 23:00 on 31 Oct is UTC-4.
- Wake at 07:00 on 1 Nov is UTC-5.
- The real elapsed time is **9:00:00**.

`Night.duration` (`src/nightjar/models.py:52`) subtracts in UTC for this reason, so it gets this case right. The 8 hours you counted is the difference between the two clock times. The clock repeated the 01:00 hour, so you were in bed for one extra real hour.

`docs/stories/S-116.md:30` says a night that spans a DST change is an hour shorter or longer on the clock. That matches what the app shows.

If the app showed 9h with no hint about the clock change, that would be a UX question for product. It isn't a calculation defect. I haven't added a ledger row, since there's no defect to track.