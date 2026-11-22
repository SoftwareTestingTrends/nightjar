**It isn't a bug, so I haven't written a repro script.**

- **02:30 never happened on 8 March 2026 in Toronto.** At 02:00 EST the clocks jumped straight to 03:00 EDT, so local times from 02:00 to 02:59 don't exist that night.
- **The input is read the standard way.** `local_input_to_aware` (`src/nightjar/diary.py:151`) attaches `America/Toronto` to `02:30`, and Python's `zoneinfo` resolves the missing time using the pre-transition offset, UTC-5. I ran it and got `02:30-05:00`, which is 07:30 UTC.
- **The display is correct for that instant.** Stored in UTC, 07:30 UTC is 03:30 EDT, which is what `Night.local_bedtime` renders. Nothing is lost or off by an hour. The code converts to UTC and back as `CLAUDE.md` asks.
- **It matches the project's existing rule.** `test_T_114_6_nudge_time_skipped_by_dst_moves_forward_an_hour` already says a nonexistent local time moves forward an hour.

If you'd like the form to tell the user their time was adjusted, or to reject nonexistent times, that would be a feature request. It isn't a defect, because no requirement says otherwise. I can add the message or the rejection if you want.