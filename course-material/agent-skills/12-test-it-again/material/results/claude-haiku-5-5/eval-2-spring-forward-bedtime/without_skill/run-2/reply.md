This isn't a bug against any requirement I can find, so I didn't write a repro script.

**What happens:** 02:30 on 8 March 2026 never occurs in Toronto. At 02:00 the clock jumps to 03:00. The diary's input path (`local_input_to_aware` in `src/nightjar/diary.py`) attaches the zone to the typed time without checking that it exists. The result is the instant 07:30 UTC, which is 03:30 EDT. After a save and reload, the diary shows `03:30-04:00` and a 7h night. I confirmed this with a temporary database.

**Why it isn't a defect yet:**
- `at_local_time` in `src/nightjar/nudge.py` documents the same rule: a skipped wall time "becomes 03:30" on purpose. The test `test_T_114_6_nudge_time_skipped_by_dst_moves_forward_an_hour` checks it.
- None of the stories or requirements (S-114, S-116, S-117, PR-21, BR-07) says what to do with a typed time inside the gap. They only require that durations and nudges are correct across DST, and they are.
- The tracker has no ticket on this.

**What is a real gap:** the app changes what you typed without telling you. Your 02:30 is silently stored as 03:30, with no message. Whether that's acceptable is a product decision, not something the specs settle. The two reasonable options are:
1. Reject the input with a message such as "02:30 doesn't exist on 8 March in America/Toronto (clocks jump 02:00 → 03:00)", or
2. Keep the normalisation but show a note, such as "stored as 03:30 EDT".

If you choose one, I can write `bugs/<short-name>/repro.py` against that behaviour, with the matching test and traceability entry. I left the code unchanged.