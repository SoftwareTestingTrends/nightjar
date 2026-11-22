# Re-import also triggers the nudge early
Same defect seen again, with a user-visible consequence beyond the duplicate rows.

Steps: import a CSV containing 4 nights, then import the same file again.
Actual: 8 rows are stored. The usual-bedtime window needs at least 7 real nights, but the duplicates count toward that minimum, so the bedtime nudge (S-114) starts after only 4 real nights.
Expected: nights already in the diary are not added again, so the count stays at 4 and no nudge appears until there are 7 distinct nights.
