**It isn't a bug in the time maths, so I didn't write a repro or a bundle.**

On 8 March 2026 Toronto clocks jump from 02:00 straight to 03:00. A bedtime of 02:30 never happened that night. I reproduced this against a throwaway database. Saving `2026-03-08T02:30` in `America/Toronto` stores `07:30 UTC`, which displays as `03:30-04:00`. That is the standard way to resolve a time that falls in the gap, and it keeps the stored instant consistent. Any "fix" that made the diary show 02:30 would be wrong.

**Possible gap, a product decision:** the app accepts the nonexistent time and changes it without telling the user. `local_input_to_aware` in `src/nightjar/diary.py:159` just attaches the zone. The requirements and S-114 only say "correct across DST" (`docs/stories/S-114.md:22`). They don't say what to do when someone types a time that doesn't exist. Product could choose to:
- reject it with a message,
- warn and show the shifted time, or
- keep the current silent shift.

Until product picks one, a repro script has nothing to define as "fixed". If product wants a warning or a rejection, tell me and I'll triage it as a new defect with a repro for that behaviour.

The autumn case, 1 November 2026, is the reverse: 01:30 happens twice and the code silently picks the first one. It's the same kind of question, and I didn't test it.