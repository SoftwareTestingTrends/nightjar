# Also reproduced: duplicate import inflates night count and starts the nudge early

Same bug, seen from a second angle, with an impact not yet recorded here.

Steps: import a CSV containing 4 nights, then import the same file again.
Actual: the diary shows 8 nights (each stored twice).
Impact: the usual-bedtime calculation needs a minimum of 7 nights, so the nudge starts after only 4 real nights because the duplicates count toward the 7.
Expected: nights already in the diary are skipped on re-import, so the count stays 4 and no nudge appears.

Likely cause (from reading the code, not yet confirmed by a test): `Diary.add_nights` / `add_night` in `src/nightjar/diary.py` insert every row with no check for an existing night, and the `nights` table has no uniqueness constraint.
