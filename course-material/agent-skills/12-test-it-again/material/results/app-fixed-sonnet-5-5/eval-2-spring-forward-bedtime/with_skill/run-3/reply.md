**Partly.** The shift to 03:30 is expected, but NightJar changes your entry without telling you, and I've logged that as a bug.

On 8 March 2026 Toronto clocks jump from 02:00 to 03:00, so 02:30 doesn't exist that night. 03:30 is the nearest real time, and `nudge.py` already maps skipped times the same way. The problem is that the app accepts 02:30, redirects as if nothing happened, and shows 03:30. No requirement or story covers this case, so I marked the expected behaviour "Not specified" and left a question for product. They need to choose between accepting with a notice, accepting silently (as now), or rejecting with an error.

I reproduced it through the real form (`POST /nights`) against a throwaway database, and the repro exited 1 in 3 of 3 runs.

The repro exits 0 once the entry is rejected or the page tells the user about the change. That definition of "fixed" is my assumption until product answers, so it may need adjusting.

Files are in `bugs/`:
- `D-1-dst-gap-bedtime-shifted/repro.py`
- `D-1-dst-gap-bedtime-shifted/report.md`
- `ledger.md`, with D-1 as `confirmed`, tracker `not filed`

I didn't run `make test` or `make lint`, since I changed no source or tests.

To file it in the tracker, run `/file-bug bugs/D-1-dst-gap-bedtime-shifted`.