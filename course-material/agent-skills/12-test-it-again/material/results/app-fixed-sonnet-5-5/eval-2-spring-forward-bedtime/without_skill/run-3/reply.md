This isn't a bug, so I haven't written a repro script.

**Why you see 03:30:** 8 March 2026 is the spring-forward day in America/Toronto. At 02:00 the clocks jump straight to 03:00, so 02:30 never happens that day. I ran the diary's own input conversion to check:

- `02:30` on 2026-03-08 is stored as `07:30 UTC`.
- `07:30 UTC` is 03:30 EDT in Toronto, which is what the diary shows when it reads the night back.
- `01:30` shows as 01:30 and `03:30` shows as 03:30, so the conversion is fine on either side of the gap.

The stored instant is a real moment, and it's the one a clock would reach if it ran 02:30 on the old offset. Showing it as 03:30 is the standard way to handle a time that doesn't exist.

The repo does this on purpose elsewhere. `at_local_time` in `src/nightjar/nudge.py` says "02:30 on spring-forward day becomes 03:30". Test `T_114_6` covers it, and S-114 requires correct behaviour across DST in Toronto.

**What's left is a usability gap, not a defect.** `local_input_to_aware` in `src/nightjar/diary.py` accepts 02:30 and shifts it without telling you. Nothing in the requirements asks it to reject or warn about such times. If you'd like the form to warn, or to reject nonexistent times, that would be a new requirement. I can draft it as a story or ticket if you want.