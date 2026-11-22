This isn't a bug, so I haven't written a repro script.

On 8 March 2026 Toronto clocks jump from 02:00 straight to 03:00, so 02:30 doesn't exist that night. I ran the app's own code to see what happens to it:

- The diary form (`local_input_to_aware`) reads `02:30` using the pre-jump offset, UTC-5.
- That is 07:30 UTC, and the diary stores it as UTC.
- When the entry is read back in `America/Toronto` it's 03:30 EDT (UTC-4), which is what the diary shows.
- 03:30 is the real instant that 02:30 resolves to. The other times around it behave normally: `01:30` is 06:30 UTC and `03:30` is 07:30 UTC.
- Durations come out right, because `Night.duration` subtracts in UTC.

The repo already treats this case the same way. `at_local_time` in `nudge.py` says a skipped wall time such as 02:30 on spring-forward day becomes 03:30. That is documented behaviour, and the story asks for correctness across DST.

The one weak spot is that the diary changes your entry silently. It doesn't tell you 02:30 was impossible that night. No requirement covers this, so "reject the entry" or "warn the user" would be a new feature, not a fix. I can't write a repro that exits 1 for it without making up the expected behaviour.

If you'd like a warning or a validation error for nonexistent local times, say which you want. I can write that up as an enhancement.