No, this isn't a bug under the project's current requirements, so I didn't write a repro script or touch `bugs/`.

**What happens:** 02:30 on 8 March 2026 doesn't exist in Toronto, because clocks jump from 02:00 EST to 03:00 EDT. `local_input_to_aware` attaches the zone with `replace(tzinfo=…)`, and Python resolves the gap to the earlier offset (EST). That stores the instant 07:30 UTC. Read back from the database, that instant is 03:30 EDT. I confirmed this with a throwaway database in a temp directory, which printed `2026-03-08T03:30:00-04:00`.

**Why it isn't a defect:**
- The stored instant is consistent, and the diary shows that same instant on every read.
- The project already treats skipped wall times this way. The docstring of `at_local_time` in `src/nightjar/nudge.py` says 02:30 on spring-forward day becomes 03:30 on purpose.
- Nothing in `docs/`, the stories, or the tests says what a logged time in a DST gap should display as.

**What is a real gap:** the app accepts the entry silently and shows an hour later than the user typed, with no warning. The intended time is unrecoverable from the entry. That is a product decision, not a code error, so I'd want your call before filing it. My recommendation is to reject gap times in the add-night form with a message such as "02:30 doesn't exist in America/Toronto on 8 March. Did you mean 01:30 or 03:30?" If you want that, I can write it up as a story in `docs/stories/`, or file it in the tracker.