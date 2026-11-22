This is not a bug, so I haven't written a repro script or a ledger row.

**Why 9 hours is correct:** Daylight saving time ended in Toronto at 02:00 on Sunday 1 November 2026, when clocks went back to 01:00. Your night from 23:00 on Saturday 31 October to 07:00 on Sunday 1 November therefore had an extra hour. The clock showed 8 hours, but 9 hours really passed.

**What I checked:**
- **Time zone offsets:** At 23:00 on 31 October Toronto is at UTC−4. At 07:00 on 1 November it is at UTC−5. Converted to UTC, the two times are exactly 9:00:00 apart.
- **The code:** `Night.duration` in `src/nightjar/models.py:52` subtracts the two times in UTC. That is the approach `CLAUDE.md` calls for, and it gives the right answer here.

If you want the diary to show 8 hours for that night, that would be a product decision. It would mean counting wall-clock time, which would be wrong for the real hours slept. I'd treat the 9h as accurate.