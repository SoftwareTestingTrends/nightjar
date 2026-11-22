No, this isn't a bug, so I haven't written a repro script.

**Why:** in America/Toronto, clocks jumped from 02:00 straight to 03:00 on 8 March 2026, the day daylight saving started. 02:30 never appeared on a Toronto clock that night.

**What NightJar does:** it reads the 02:30 you typed using the offset in force just before the jump (UTC−5). That moment is 07:30 UTC, and 07:30 UTC on the Toronto clock after the jump is **03:30**. So 03:30 isn't a shifted or corrupted time; it's the same moment you entered, shown the way a Toronto clock would actually have read. I checked this through the same code path the diary uses for typed times (`local_input_to_aware` in `src/nightjar/diary.py:151`):

- **Stored as:** `2026-03-08T07:30:00+00:00`, which is 03:30 Toronto time.
- **Night it counts towards:** 7 March. That's right for a bedtime after midnight.
- **Length of the night:** I tested a wake time of 09:30, and the night came out as 6 h 00 min, which is the real time that passed. The diary didn't add a phantom extra hour.

The code chose this deliberately: `src/nightjar/nudge.py:46` describes the same handling ("02:30 on spring-forward day becomes 03:30"). The requirements (BR-07, PR-21, S-114/116/117) only ask for correct handling across daylight-saving changes, and this is correct.

**One possible improvement, not a defect:** the diary changes the time silently, which could look like a bug to the person who typed it. If you'd like, you could ask product for a small note when a typed time falls in the skipped hour, such as "02:30 didn't exist on 8 Mar (clocks went forward); saved as 03:30". That would be a new requirement for product to approve, not a fix.