Reproduced again, with a second consequence: the duplicates also trigger the nudge too early.

## Steps to reproduce

1. Start with an empty diary (default user, America/Toronto).
2. Import a CSV with 4 nights (test data, notes "test").
3. Import the same CSV a second time.

## Expected

The second import adds nothing, so the diary still has 4 nights and the nudge stays off. The nudge needs at least 7 nights (`MIN_NIGHTS = 7` in `sleep_window.py`).

## Actual

- After import 1: 4 nights stored, no nudge (correct).
- After import 2: 8 nights stored, and a nudge is scheduled ("Your usual bedtime is 23:00"), though only 4 real nights exist.

## Evidence

Script run against `Diary` and `next_nudge` with a fresh SQLite file:

```
import 1 -> stored total: 4 | nudge: None
import 2 -> stored total: 8 | nudge: Nudge(at=2026-03-06 22:15 America/Toronto, silent=False, text='A gentle reminder ... Your usual bedtime is 23:00.')
```

Cause: `Diary.add_night` / `add_nights` in `src/nightjar/diary.py` insert every row, and the `nights` table has no uniqueness constraint.

## Notes

Impact beyond NJ-12's description: duplicates can push the user over the 7-night threshold, so the nudge is based on a usual bedtime that isn't real. Reproduced 1 of 1 times.
