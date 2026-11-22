No, this isn't a bug, so I haven't written a repro script.

8 March 2026 is the day Toronto's clocks spring forward. At 02:00 EST they jump straight to 03:00 EDT, so 02:30 never happens in America/Toronto that day.

The code handles that time in a standard way:
- `local_input_to_aware` (`src/nightjar/diary.py:153`) attaches the zone to the entered time. For a time that doesn't exist, Python uses the pre-jump offset (-05:00), so 02:30 is stored as 07:30 UTC.
- The diary then converts that instant back to local time with `Night.local_bedtime`. 07:30 UTC is 03:30 EDT, which is what you saw.

I checked this with a quick Python run. 02:30 on 8 March in America/Toronto converts to 07:30 UTC, which converts back to 03:30 EDT.

The stored instant is the real moment 02:30 would have been if the clock hadn't jumped. The duration maths stays correct because `Night.duration` subtracts in UTC.

One possible improvement is to reject or warn on non-existent local times at input, for example "02:30 doesn't exist on that date". That would be a new feature, since nothing in the requirements or `docs/traceability.md` asks for it. The silent shift is also what browsers and most calendar apps do. If you want that validation, I can write it up as a feature request.