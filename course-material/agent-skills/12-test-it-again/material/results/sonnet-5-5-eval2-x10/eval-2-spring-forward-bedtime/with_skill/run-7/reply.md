**Verdict: it's a real bug, but a narrow one.** I've logged it as D-1, status `confirmed`.

**Why you saw 03:30.** On 8 March 2026, Toronto clocks jump from 02:00 to 03:00, so 02:30 never happened that night. NightJar read your 02:30 at the old UTC offset, which is 03:30 on the new clock.

**What's wrong.** The app accepted 02:30 and showed 03:30 without telling you. No error and no notice. No requirement or story says what should happen with a time that doesn't exist, so under Expected I wrote "Not specified". I also added a question for product: should the form reject it, or accept it with a notice that it was moved to 03:30?

**Reproduction.** I ran `uv run python bugs/D-1-dst-gap-bedtime/repro.py` three times against a throwaway database. It exited 1 each time, printing: `BUG: typed 02:30 (nonexistent; clocks jump 02:00->03:00), diary shows 03:30, no notice`.

**The pass condition is my stand-in.** The script exits 0 if the form is rejected, or if the page shows a notice containing "daylight", "does not exist", "doesn't exist" or "skipped". Product hasn't picked a behaviour, so adjust it once they do.

I didn't run the test suite or lint, because I only added files under `bugs/`. I also didn't fix the bug, which is outside this skill.

**Files** (all in `bugs/`, which is gitignored):
- `D-1-dst-gap-bedtime/report.md`
- `D-1-dst-gap-bedtime/repro.py`
- `ledger.md`

**Next step.** Filing is visible to the team, so I haven't done it. To file it, run:

`/file-bug bugs/D-1-dst-gap-bedtime`