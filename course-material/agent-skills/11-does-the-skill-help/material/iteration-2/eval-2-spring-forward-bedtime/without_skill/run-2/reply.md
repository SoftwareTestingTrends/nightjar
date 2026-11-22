Yes, it's a bug, though a narrow one.

**What happens:** 8 March 2026 is the spring-forward night in Toronto. Clocks jump from 02:00 straight to 03:00, so 02:30 never existed that night. `local_input_to_aware` (`src/nightjar/diary.py:151`) attaches the zone to the typed time without checking that it exists. Python resolves 02:30 using the old EST offset (-05:00) and stores it as 07:30 UTC. That instant is 03:30 EDT, which is what the diary displays. There's no error and no warning, so the logged bedtime is silently an hour off.

**Not the cause:** the diary's UTC conversion and display are fine. The problem is the unvalidated input.

**Repro:** I wrote `bugs/dst-gap-bedtime/repro.py`. It posts that bedtime through the real `/nights` endpoint against a throwaway database. It exits 1 while the diary shows 03:30 (it does now: `BUG: typed 02:30 (nonexistent, DST gap), diary shows 03:30, no warning`). It exits 0 if the input is rejected with a 400 or the diary shows anything other than 03:30.

**Fix choice:** I haven't picked one. The two reasonable options are to reject nonexistent local times with a clear message, or to snap to 03:00 and tell the user. The repro accepts either. If you'd rather it only accept one, I can tighten it.

I put it in `bugs/dst-gap-bedtime/` as you asked, not the `D-<n>-<name>` layout from `docs/bug-bundles.md`. I also didn't write a `report.md` or ledger entry.