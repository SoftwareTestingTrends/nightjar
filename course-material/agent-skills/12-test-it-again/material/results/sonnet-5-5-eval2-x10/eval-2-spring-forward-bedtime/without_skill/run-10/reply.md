It isn't a bug, so I haven't written a repro script.

- **02:30 didn't exist that night.** On 8 March 2026 Toronto clocks jumped from 02:00 to 03:00. Nothing happened between 02:00 and 02:59.
- **03:30 is the correct way to resolve it.** The app takes your 02:30 using the pre-change offset (EST, UTC-5), which is 07:30 UTC. It stores that instant and shows it back in Toronto time, which is 03:30 EDT. I reproduced this by saving a 02:30 bedtime through `local_input_to_aware` and `Diary`, and the diary returned `03:30`.
- **The numbers stay consistent.** With a 09:00 wake-up, the duration is 5h30, which is the real elapsed time. The story's non-functional requirement (S-114) asks for correct behaviour across DST changes, and this meets it.
- **The same handling is documented.** `src/nightjar/nudge.py:46` describes it: "normalises wall times that DST skips (02:30 on spring-forward day becomes 03:30)".

**Possible UX gap, not a defect:** the form accepts the non-existent time without telling you it was shifted, so the diary shows a time you didn't type. If you want a warning or a validation error for skipped times, that would be a new requirement. Nothing in the docs asks for it today.

I couldn't check whether this was already filed, because the tracker at `127.0.0.1:8765` wasn't running.