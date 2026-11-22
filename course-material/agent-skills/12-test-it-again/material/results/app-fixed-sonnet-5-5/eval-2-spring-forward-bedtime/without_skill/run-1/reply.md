Yes, it's a bug. The repro is at `bugs/dst-gap-bedtime/repro.py`. It exits 1 now with `BUG: logged 02:30 on 2026-03-08 (skipped by DST), diary shows 03:30 with no warning`.

**Why it happens.** On 8 March 2026 Toronto clocks jump from 02:00 straight to 03:00, so 02:30 never happened that night. `local_input_to_aware` (`src/nightjar/diary.py:161`) attaches the zone to the typed time without checking that it exists. When the night is saved as UTC and read back, the instant becomes 07:30 UTC, which is 03:30 EDT.

**Why I call it a bug.** The app silently stores a time you didn't type, with no warning, and any choice for a skipped time is a guess. Rejecting the entry or asking for a corrected time would be honest. There's a second problem: before the save, `Night.local_bedtime` still reports 02:30, so what the app shows depends on whether the entry has been saved and reloaded.

The nudge code (`src/nightjar/nudge.py:46`) normalises skipped times to 03:30 on purpose, so the fix may need to follow that design. That works for scheduling a nudge, but it isn't a good reason to rewrite a user's logged bedtime.

**What counts as fixed.** The repro exits 0 if the diary rejects the entry with a `ValueError` or keeps it as typed (02:30). Either of those is a fix. Showing 03:30 is not.

**Not run.** I didn't run `make test` or `make lint`, since I only added a file under `bugs/`, which is gitignored. I also didn't create the `report.md` or ledger row that `docs/bug-bundles.md` describes, and I didn't file anything in the tracker. I used the short name you asked for rather than the `D-<n>-` folder name from that doc. I can write the full bundle if you want one.