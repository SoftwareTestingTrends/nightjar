It reproduces, so I've logged it as a confirmed bug. But nothing in the requirements says what a bedtime that doesn't exist should become, so the "bug" part is a product decision.

**What happens:** Toronto's clocks jump from 02:00 to 03:00 on 8 March 2026, so 02:30 never occurs that night. Logging 02:30 through `POST /nights` stores 07:30 UTC, which the diary shows as 03:30 EDT, with no warning. I reproduced this 3 of 3 times through the real app path against a throwaway database.

**Why I didn't stop at "not a bug":** the triage procedure treats a reproducible defect with no spec as `confirmed`, with Expected set to "Not specified". The nudge code (`nudge.py`, `at_local_time`) moves skipped times forward to 03:30 on purpose, so the diary doing the same is consistent with the codebase. It's still undocumented, though, and the diary does it implicitly through `replace(tzinfo=...)`.

**Files written (all in gitignored `bugs/`, git status is clean):**
- `bugs/D-1-dst-gap-bedtime/repro.py`: exits 1 while 02:30 is shown as 03:30. Exits 0 if the entry is rejected or 02:30 is shown. It ran 3 times, exit 1 each time.
- `bugs/D-1-dst-gap-bedtime/report.md`: Expected is "Not specified", with a question for product.
- `bugs/ledger.md`: created, since it didn't exist yet. Row D-1, status `confirmed`, tracker `not filed`.

I didn't change any app code, so I didn't run `make test` or `make lint`.

**Question for product:** should a time that doesn't exist (02:30 on 8 March in Toronto) be kept as entered, shifted to 03:30 with a note, or rejected with a message? If it's rejected, the repro already treats that as fixed. If product picks 02:30 as entered, the repro's check should be tightened to require 02:30.

**Next step:** run `/file-bug bugs/D-1-dst-gap-bedtime` when you want it in the tracker. I left a scratch probe at `/tmp/nj-probe/`, outside the repo, because removing it needed approval.