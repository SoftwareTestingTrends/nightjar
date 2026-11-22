Yes, it's a defect, but a narrow one. I've logged it as D-1 with status `confirmed`.

**Why it happens:** 8 March 2026 is the spring-forward day in Toronto. Clocks jump from 02:00 to 03:00, so 02:30 doesn't exist that night. `local_input_to_aware` (`src/nightjar/diary.py:151`) attaches the zone without checking for that gap. The time silently resolves to 07:30 UTC, which is 03:30 EDT. The diary accepts it with no warning, so you never learn your input was changed.

**Expected behaviour is not specified.** No requirement or story covers a local time inside the DST gap, so I wrote "Not specified" under Expected. There is an open question for product: reject it, accept it with a notice that it was moved to 03:30, or something else?

**Repro:** `uv run python bugs/D-1-dst-gap-bedtime-shifted/repro.py` exited 1 on all 3 runs and printed `typed 02:30, diary shows 03:30, accepted without warning`. It exits 0 once the input is rejected with a `ValueError`. That definition of "fixed" is my assumption. If product picks a different behaviour, the script needs adjusting.

You asked for `bugs/<short-name>/repro.py`. I used `bugs/D-1-dst-gap-bedtime-shifted/` because `docs/bug-bundles.md` requires that naming. The bundle also has `report.md`, and `bugs/ledger.md` has the new row.

I haven't filed it in the tracker. To do that, run `/file-bug bugs/D-1-dst-gap-bedtime-shifted`.