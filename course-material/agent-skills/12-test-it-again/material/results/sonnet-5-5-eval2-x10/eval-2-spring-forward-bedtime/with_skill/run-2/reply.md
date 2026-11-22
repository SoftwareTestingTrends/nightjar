**Short answer: this isn't a bug, so I haven't written a repro or a bundle.**

02:30 on 8 March 2026 doesn't exist in America/Toronto. Clocks jump from 01:59 EST to 03:00 EDT that night. I submitted your entry through the real `/nights` form against a throwaway database and got:

- **Stored:** `2026-03-08 07:30 UTC`. The app read 02:30 with the pre-jump offset (EST, −5), and that instant is 03:30 EDT.
- **Shown:** 03:30. That is the correct local time for the stored instant, and no other display would be right.
- **Duration:** 02:30 to 09:30 shows as 6:00, not 7:00. That is the real elapsed time across the spring-forward, and it matches the DST requirement in S-114 and BR-07.

**The real gap is that the app accepts 02:30 without telling you.** `local_input_to_aware` in `src/nightjar/diary.py` takes the input as given, and the form returns a 303 redirect with no warning that the time was shifted. No requirement or story says what should happen with a nonexistent local time, so I can't call that a defect. A repro script would also have to define what "fixed" means, for example a 400 error, a warning, or snapping to 03:00. That is a product decision.

**Question for product:** when a user enters a local time that falls in the spring-forward gap, should the app reject it with an error, accept it and show a notice, or keep shifting it silently as it does now? If product wants a change, say so and I'll triage it as `confirmed` with that expected behaviour and write the repro.

**Cleanup:** I left a scratch probe at `bugs/scratch_probe.py` because my `rm` needed approval. It's safe to delete, and `bugs/` is gitignored.