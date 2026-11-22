Yes, I think this is a bug. I reproduced it, and the repro is at `bugs/spring-forward-bedtime-shift/repro.py`.

**What happens:** Toronto clocks jump from 02:00 to 03:00 on 8 March 2026, so 02:30 doesn't exist that night. The form handler (`local_input_to_aware`, `src/nightjar/diary.py:153`) attaches the zone to the typed time without checking it exists. The result is stored as UTC, which comes back as 03:30. The app returns a 303 success and the diary shows 03:30. The user is never told, and the logged time is now one they didn't enter.

**Why I didn't call it intended:** the same shift is documented as deliberate in the nudge code (`at_local_time` in `src/nightjar/nudge.py:46`). That's reasonable there, because the app is computing a time itself. In the diary the user typed the time, so silently saving a different one is a data-integrity problem. The right fix is probably a 400 asking them to pick a real time, though that's a product call.

**Repro:** it posts 02:30 to `POST /nights` as `America/Toronto` against a temporary database. It exits 1 while the saved bedtime isn't 02:30, and 0 once the app rejects the input or no longer shifts it. Right now it prints `status = 303 | saved bedtime shown = 03:30` and then `BUG: entered 02:30 (does not exist in Toronto on 2026-03-08), saved as 03:30`. Ruff is clean on it.

- **Exit code:** I saw the BUG output but not the shell's exit code for that run, because my first attempt was blocked.
- **Tracker:** it wasn't running, so I didn't search for duplicates or file anything. I also didn't run `make test`, since I only added a script under `bugs/`.