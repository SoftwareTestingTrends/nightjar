**It isn't a bug, so I haven't written a repro script.**

- **The time doesn't exist.** On 8 March 2026 Toronto's clocks jump from 02:00 EST straight to 03:00 EDT. No 02:30 happened that night.
- **The shift to 03:30 is standard.** I checked how the app handles it. `local_input_to_aware` (`src/nightjar/diary.py:151`) attaches `America/Toronto` to the 02:30 you typed. Python reads that as 02:30 at UTC-5, which is 07:30 UTC. The diary stores that instant and converts it back to local time for display. 07:30 UTC is 03:30 EDT, so the diary shows 03:30. This is the usual forward shift for a skipped time.
- **The repo documents the same rule.** The `at_local_time` docstring in `nudge.py:43` says "02:30 on spring-forward day becomes 03:30". The stored instant is a real moment, and durations stay correct because they are computed in UTC.

**Possible improvement.** The diary changes your time without telling you. If you want a different behaviour, such as a form warning ("02:30 doesn't exist on that date; saved as 03:30") or rejecting the input, that is a product decision. I'd file it as an enhancement rather than a defect.

I can write a repro if you think the requirement is different. For example, you might expect a skipped time to be rejected or to show a warning.