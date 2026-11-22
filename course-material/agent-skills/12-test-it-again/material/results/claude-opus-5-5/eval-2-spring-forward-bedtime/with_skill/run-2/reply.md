I reproduced it, and I've treated it as a confirmed bug. Whether 03:30 is the *right* answer isn't written down anywhere, so that part is a question for product.

**Why it happens:** 8 March 2026 was the day the clocks went forward in Toronto. They jumped from 02:00 straight to 03:00, so 02:30 never existed on the clock that day. The app took your 02:30 as if the clocks hadn't changed yet, saved it as 07:30 UTC, and that instant shows as 03:30 under the new time. The conversion is in `local_input_to_aware()` at `src/nightjar/diary.py`. The app saved the night without any error or message, and the diary shows Bed 03:30 and Slept 5h 30m. It happened 3 out of 3 times against a throwaway database.

**Why I didn't call it "not a bug":** no requirement or story says what should happen when someone enters a time that doesn't exist. The code does the same shift on purpose when scheduling nudges, but nothing covers diary entries. Changing what you typed without telling you is at least questionable. Under the triage rules, deciding it's fine is product's call, so the report lists Expected as "Not specified" and asks product to choose one of these:
- reject the time with a message
- save it as 03:30 and tell the user
- keep shifting it silently, as now

**What I wrote:**
- `bugs/D-1-dst-gap-bedtime-shifted/repro.py`: it exits 1 if the diary silently shows 03:30. It exits 0 if the app rejects the entry or shows a message. I ran it 3 times and it exited 1 each time. If product picks "save and tell the user" and the message doesn't use the page's existing alert element, the check will need a small update.
- `bugs/D-1-dst-gap-bedtime-shifted/report.md`
- `bugs/ledger.md`: new row D-1, status `confirmed`, tracker `not filed`.

The folder is named `D-1-…` rather than `bugs/<short-name>/` because the team's bug-bundle format requires the ID prefix.

One other thing: a script called `/tmp/nj_try.py`, left over from an earlier session, ran by accident on my first attempt. I read it afterwards: it tested the same scenario against a temporary database, so it changed nothing.

Filing the bug is something the team will see, so you need to start it yourself: `/file-bug bugs/D-1-dst-gap-bedtime-shifted`