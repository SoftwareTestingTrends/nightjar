Yes, it's a bug, though a small one. The repro is at `bugs/dst-gap-bedtime/repro.py`. It currently exits 1 and prints `bug: logged 02:30 (a time that doesn't exist), diary shows 03:30`, which is what you saw.

**What happens:** On 8 March 2026 Toronto clocks jump from 02:00 to 03:00, so 02:30 never occurs that night. `local_input_to_aware` (`src/nightjar/diary.py:151`) just attaches the zone to the typed time. Python picks the pre-jump offset (-05:00) for it, which is 07:30 UTC. That gets saved, and when the diary is read back it displays as 03:30 EDT.

**Why it's a bug:** The app accepts a time that doesn't exist and moves it by an hour without telling you. The stored night, its duration and the usual-bedtime median are all shifted. The form already returns a 400 with a message for invalid input (`web.py:81`), so rejecting this time would fit what it does today. Docs BR-07 and S-114 also require correct behavior across DST changes.

**The repro** saves the night through a real `Diary` on a throwaway database, then reads it back. It exits 0 if the time is rejected with a `ValueError`, or if the diary shows 02:30. I think rejection is the right fix, but you could instead accept the time and show a notice. The repro allows either.

I didn't write a `report.md` or a `bugs/ledger.md` row, which `docs/bug-bundles.md` asks for with a `D-<n>-` folder name. You asked only for the script, and the folder doesn't follow that naming. I can convert it to a full bundle if you want.