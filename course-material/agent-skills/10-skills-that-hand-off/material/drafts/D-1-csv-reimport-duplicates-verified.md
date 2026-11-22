Re-checked on 2026-11-21: no longer reproduces.

Repro `bugs/D-1-csv-reimport-duplicates/repro.py` exited 0 in 3 of 3 runs:
"OK: 2 nights after importing a 2-night file twice".

The fix for NJ-12 appears to have landed (uncommitted change in `src/nightjar/diary.py`
in the working tree at check time). Suggest closing once it is committed and reviewed.
