**It isn't a bug, so I didn't write a repro script.**

On 8 March 2026, America/Toronto switched to daylight saving time. At 02:00 the clocks jumped straight to 03:00, so 02:30 never happened on the wall clock that night. The app has to turn your entry into a real moment in time, and the only sensible reading of "02:30" that night is 30 minutes after 02:00 EST. That moment is 07:30 UTC, which the clock that night showed as **03:30 EDT**. The diary is showing the same moment you meant, written the way Toronto clocks actually read at the time.

I checked this directly. `local_input_to_aware` in `src/nightjar/diary.py:151` attaches the zone, and the value is stored in UTC:

| Entered (Toronto) | Stored (UTC) | Shown |
|---|---|---|
| 2026-03-07 02:30 | 07:30 | 02:30 −05:00 |
| **2026-03-08 02:30** | **07:30** | **03:30 −04:00** |
| 2026-03-09 02:30 | 06:30 | 02:30 −04:00 |

The nights either side show unchanged, so only the skipped hour is affected. Pushing a skipped time forward is also deliberate elsewhere in the code: `at_local_time` in `src/nightjar/nudge.py:46` describes exactly this case ("02:30 on spring-forward day becomes 03:30"), and test T-114-6 covers it.

Two side effects are worth knowing about:
- That night will look one hour shorter on the clock. The real sleep time is still correct, because `Night.duration` measures it in UTC.
- If you'd like the diary to warn people when they enter a time that didn't exist, instead of quietly moving it forward, that would be a feature request rather than a bug fix.