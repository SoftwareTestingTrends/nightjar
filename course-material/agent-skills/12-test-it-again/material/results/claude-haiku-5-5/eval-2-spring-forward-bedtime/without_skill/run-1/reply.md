No, this isn't a bug, so I didn't write a `repro.py`. Nothing in the repo changed.

Toronto springs forward at 02:00 on 8 March 2026, so 02:30 local never existed that night. The clock went from 01:59 EST straight to 03:00 EDT.

- Your input goes through `local_input_to_aware` in `src/nightjar/diary.py`, which attaches the zone with `replace(tzinfo=...)` and leaves `fold=0`. For a skipped time, that reads 02:30 as standard time (UTC−5), which is 07:30 UTC.
- The diary reads the night back from SQLite as UTC and converts it, so it shows 07:30 UTC as 03:30 EDT. I confirmed this with a round trip through a temporary database.
- `nudge.py` documents the same mapping on purpose: "02:30 on spring-forward day becomes 03:30."

So 03:30 is the correct instant for "02:30 EST", and the stored value is right. The spec (S-114) only requires correct DST handling in `zoneinfo`, not how to treat impossible wall-clock times, so there is no requirement this breaks.

The one thing I'd call a gap is UX: the form accepts a time that doesn't exist and silently shifts it an hour, without telling you. If you want that, the change would be to reject nonexistent local times in `local_input_to_aware` (or show a warning), and to add an acceptance criterion for it. That's a feature decision, so I haven't made it. Ambiguous fall-back times (01:30 on 1 November) have the same `fold=0` behaviour and could be covered at the same time.