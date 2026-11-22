**No, this isn't a bug, so I haven't written a repro script.**

- **The time doesn't exist.** On 8 March 2026 Toronto clocks jump from 01:59 EST straight to 03:00 EDT. There is no 02:30 that night.
- **The diary resolves it to the next real instant.** `local_input_to_aware` (`src/nightjar/diary.py:151`) reads 02:30 as 02:30 EST, which is 07:30 UTC. The diary stores that and converts it back using the zone, so it displays 03:30 EDT. The instant is valid and consistent, and the displayed time is just the same moment on the post-jump clock.
- **It matches the project's own convention.** `at_local_time` (`src/nightjar/nudge.py:43`) documents "02:30 on spring-forward day becomes 03:30". `test_T_114_6_nudge_time_skipped_by_dst_moves_forward_an_hour` covers the same behaviour. It is also the standard shift-forward handling of a nonexistent local time.

If you actually went to bed at about that time, you probably meant a wall-clock time just after the jump. The shift to 03:30 is a reasonable reading.

**Possible improvement (a product decision):** the form accepts 02:30 silently and changes it without telling you. A validation message such as "02:30 doesn't exist on 8 March in Toronto; saved as 03:30" would be clearer. Nothing in the docs or acceptance criteria requires it. If you want it treated as a defect, I can file it as a UX gap with a repro that expects the form to reject or flag the time.