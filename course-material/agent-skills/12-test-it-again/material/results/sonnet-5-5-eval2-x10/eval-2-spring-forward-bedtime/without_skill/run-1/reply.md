Yes, it's a real bug. The repro is at `bugs/dst-gap-bedtime/repro.py`. I ran it on the current code and it prints `BUG: typed 2026-03-08T02:30 America/Toronto, diary shows 03:30 (accepted silently)` and exits 1.

**What happens**
- On 8 March 2026 Toronto clocks jump from 02:00 to 03:00, so 02:30 didn't exist that night.
- `local_input_to_aware` in `src/nightjar/diary.py:151` just attaches the zone to whatever you typed. It never checks that the time exists, so it builds `02:30-05:00`, which is the pre-jump offset.
- The diary stores that as UTC, `07:30Z`. When it's read back, `07:30Z` is 03:30 EDT, so that's what the diary shows.
- Nothing tells you the time was changed.

I think the right behaviour is to reject the time with a message such as "02:30 doesn't exist on that date in America/Toronto". The web form already shows a `ValueError` as a 400 error (`web.py:81`), so the fix is to raise one from `local_input_to_aware` when the time falls in a gap.

The script goes through a throwaway `Diary` in a temp directory, since the shift only appears after the save and reload. It exits 0 if the time is rejected, or if the diary shows it as typed. That way it doesn't depend on which fix you pick.

- **Same gap for other inputs:** every input that goes through `local_input_to_aware` gets the same shift. That covers the wake time too, and presumably the fall-back hour (01:00–02:00 on 1 Nov), which is ambiguous.
- **Tests:** I didn't run `make test` or `make lint`, since I only added a script under `bugs/`.
- **Tracker and bundle:** the tracker wasn't reachable (connection refused), so I didn't file anything. I put the script at the path you gave, not the `bugs/D-n-…/` layout in `docs/bug-bundles.md`, and I didn't add a `report.md` or a ledger row.