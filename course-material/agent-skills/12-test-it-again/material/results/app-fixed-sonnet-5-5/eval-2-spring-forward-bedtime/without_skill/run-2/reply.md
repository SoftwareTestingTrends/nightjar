Yes, this is a real bug, and I've written a repro for it.

**Why it happens:** On 8 March 2026, Toronto clocks jump from 02:00 to 03:00, so 02:30 never happens that night. `local_input_to_aware` in `src/nightjar/diary.py:159` just attaches the zone to the typed time. It never checks that the time exists. Python reads the nonexistent 02:30 with the old offset, which makes it 07:30 UTC. That converts back to 03:30 in Toronto. The `POST /nights` route accepts it with a 303 redirect, so the user's entry is changed and nothing tells them.

**Where it sits:** The non-functional requirement in `docs/stories/S-114.md` says the app must be correct across spring-forward in Toronto. A shifted bedtime also feeds the usual-bedtime median that the nudge uses.

**Expected fix:** Reject a nonexistent local time with a clear 400 message, as the other validation errors do. Quietly shifting it is the wrong behaviour. The fix would probably go in `local_input_to_aware` or `add_night`.

**Repro:** `bugs/dst-gap-bedtime/repro.py` posts that bedtime to the real `/nights` route using a throwaway database.
- It currently exits 1 and prints `BUG: entered 02:30 (doesn't exist), HTTP 303 diary shows 03:30`.
- It exits 0 once the bedtime is no longer stored as 03:30.
- Run it from the repo root with `uv run python bugs/dst-gap-bedtime/repro.py`.

I used the folder name you asked for. `docs/bug-bundles.md` expects `bugs/D-<n>-<name>/` with a `report.md` and a ledger row. I haven't added those, and I haven't filed anything in the tracker. I can do either if you want.

I didn't run `make test` or `make lint`, since I changed no source or tests.