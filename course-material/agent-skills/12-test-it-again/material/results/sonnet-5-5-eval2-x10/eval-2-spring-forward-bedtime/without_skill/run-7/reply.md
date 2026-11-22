Yes, I think this is a bug. The repro script is at `bugs/dst-gap-bedtime/repro.py`. I ran it and it printed `BUG: logged 02:30 on 2026-03-08 (America/Toronto), diary shows 03:30, no error` and exited 1.

**Why it happens:**
- On 8 March 2026 Toronto clocks jump from 02:00 to 03:00, so 02:30 never happens that night.
- `local_input_to_aware` (`src/nightjar/diary.py:151`) just stamps the zone onto the typed time. That gives 02:30 at the old winter offset (−05:00), which is 07:30 UTC.
- The diary stores UTC and converts back to local time for display, so 07:30 UTC shows as 03:30 (−04:00).

**Why I call it a bug:** the app changes the time you entered by an hour without telling you. Neither the form nor `Night` checks for a time that doesn't exist. The off-by-an-hour bedtime also flows into duration and the usual-bedtime calculation.

**What counts as fixed:** the repro exits 0 if the app either rejects 02:30 with a clear error or shows 02:30 as you logged it. I left the choice of fix open. Rejecting it with a message in the form is probably simplest.

I didn't change any app code. I also didn't add a `bugs/ledger.md` row or a `report.md`, since you only asked for the repro script.