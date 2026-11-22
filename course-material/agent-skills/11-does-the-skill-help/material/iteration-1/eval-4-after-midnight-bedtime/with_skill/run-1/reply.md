This isn't a bug, so I haven't written a repro script, a bug bundle or a ledger row.

**What happens:** I logged a night with bedtime 00:15 on Sun 15 Nov 2026 (America/Toronto) in a throwaway object, and the diary labels it **Sat 14 Nov**.

**Why it's intended:** the "Night of" column holds the evening the night began, not the calendar date of the bedtime.
- `src/nightjar/models.py:44` documents it: "a 00:15 bedtime on Sunday is Saturday night."
- `tests/test_diary.py:81` tests it.
- Story S-116 AC1 and test case TC-116-8 both expect a 00:15 bedtime on Sun 15 Nov to count as the night of Sat 14 Nov.
- Sleeping after midnight on Sunday is still Saturday night, as in "Saturday night's sleep".

**If the label is confusing:** the column header "Night of" is the only cue (`src/nightjar/templates/index.html:70`), and the row doesn't show the actual bedtime date. A clearer header, or a "bed 00:15 Sun" hint, would be a UX suggestion. It would change the behaviour the stories specify, so that's a product decision and not a defect.