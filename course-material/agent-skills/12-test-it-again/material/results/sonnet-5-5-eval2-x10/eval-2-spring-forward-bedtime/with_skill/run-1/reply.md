Yes, it's a bug, though what the fix should be isn't specified. I reproduced it 3 of 3 times.

**What happens:** 2:00 on 8 March 2026 is the spring-forward moment in Toronto, when clocks jump to 3:00. A 02:30 bedtime that night never existed. `local_input_to_aware` in `src/nightjar/diary.py` accepts it anyway and treats it as 02:30 EST, which is 07:30 UTC. The diary then shows that instant as 03:30 EDT. The user gets no error or notice.

**Expected behaviour:** No requirement or story says what to do with a local time that doesn't exist. BR-07 and S-114 only say "correct across DST". So I marked it `confirmed` with Expected as "Not specified". I added a question for product: reject the time, shift it and tell the user, or something else. Wake time has the same gap.

**Repro script:** `bugs/D-1-dst-gap-bedtime-shifted/repro.py` posts that night through the app against a throwaway database. It exits 1 while an accepted bedtime shows a different time from the one entered. It exits 0 if the input is rejected or shown as entered. It doesn't pick between those fixes. It prints `entered 02:30, diary shows 03:30`.

I also wrote `report.md` in that folder and added row D-1 to `bugs/ledger.md` (status `confirmed`, tracker `not filed`). The repro lives in the `D-1-…` folder rather than the `bugs/<short-name>/` path you gave, because `docs/bug-bundles.md` requires that naming.

I didn't run `make test` or `make lint`, since I changed no source or tests.

To file it in the tracker, run `/file-bug bugs/D-1-dst-gap-bedtime-shifted`. I can't start that step myself, because filing changes something the team sees.