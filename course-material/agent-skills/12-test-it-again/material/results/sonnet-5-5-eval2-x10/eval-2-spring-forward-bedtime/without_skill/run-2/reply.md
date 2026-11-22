**It isn't a bug, so I haven't written a repro script.**

On 8 March 2026 Toronto clocks jump from 02:00 to 03:00 (EST to EDT). A local time of 02:30 never happened that night. I ran the check in Python:

- `datetime(2026,3,8,2,30, tzinfo=ZoneInfo("America/Toronto"))` resolves to `02:30-05:00`, which is 07:30 UTC.
- 07:30 UTC is 03:30 EDT on a Toronto wall clock, which is what the diary shows.

The path is the web form's `local_input_to_aware` in `src/nightjar/diary.py:151`. It attaches the zone with `.replace(tzinfo=...)`, so Python's standard rule for nonexistent times picks the pre-transition offset. The stored instant is right, the diary renders it correctly in the night's own zone, and durations are computed in UTC. Nothing in the requirements or S-114 says what to do with an entry like this.

The one weak spot is that the app accepts 02:30 without telling you it doesn't exist and then shows a different time. That's a possible UX improvement: reject the entry with a message like "that time doesn't exist on this date", or show a note when it's shifted. It doesn't break any stated requirement. If you want it tracked, I can write it up as an enhancement, or add a repro with a decision on the intended behaviour (reject or shift).