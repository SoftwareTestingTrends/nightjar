---
name: triage-bug
description: Confirms whether something reported broken in NightJar really is, and writes a bug bundle with a minimal repro script and a row in the defect ledger. Use when someone reports or suspects a NightJar bug ("X seems broken", "is this a bug?", "reproduce this"), or when a browser-check step fails. Not for filing tickets (that's /file-bug) and not for checking whether a known bug is fixed (that's verify-fix).
---

# Triage a bug

A report is someone's reading of what happened. Find out what actually happens, then
leave a bundle the next skill, or the next person, can pick up without asking you
anything. The bundle and ledger formats are in `docs/bug-bundles.md`: read it first
and follow it exactly.

## Steps

1. Reproduce the report as given, against a throwaway database (never `nightjar.db`).
2. If it doesn't reproduce in 3 tries, say what you tried, add a ledger row with
   status `not reproduced`, and stop.
3. If it does, write `repro.py`: the fewest steps that show the defect, exiting 1 while
   it's present and 0 once it's fixed. Run it 3 times.
4. Write `report.md` and add the ledger row (status `confirmed`, tracker `not filed`).
   Check the ledger first: if a row already describes this defect, update that row
   instead of adding a new one.
5. Hand off. Filing changes something the team sees, so you can't start it: tell the
   person the exact command to run, `/file-bug bugs/D-<n>-<short-name>`.
