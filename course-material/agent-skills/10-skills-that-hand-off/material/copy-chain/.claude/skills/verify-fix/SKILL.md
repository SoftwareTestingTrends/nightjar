---
name: verify-fix
description: Checks whether known NightJar defects are fixed by rerunning each bug bundle's repro script, and updates the defect ledger. Use when someone asks "is D-1 fixed?", "did the fix land?", "recheck the open bugs" or "update the ledger". Not for investigating a new problem (that's triage-bug).
---

# Verify a fix

The ledger in `bugs/ledger.md` and the bundles it points to are the record. The
formats are in `docs/bug-bundles.md`.

## Steps

1. Read the ledger. Check the IDs you were given, or every row whose status isn't
   `fixed`.
2. For each one, run its repro 3 times: `uv run python bugs/<bundle>/repro.py`. Don't
   edit the script to make it pass; if it no longer runs at all, report that.
3. Exit 0 all 3 times: `fixed`. Exit 1 all 3 times: `still broken`. Mixed: report it
   as flaky and leave the status alone.
4. Update the row's Status and Last checked (date, exit code, n of 3), and the
   `Status:` line in the bundle's `report.md`.
5. If the bundle has a tracker key, write a short comment for that ticket to
   `bug-drafts/<bundle>-verified.md` and tell the person. Posting it is a change the
   team sees, so leave that to them.
6. Report a table: ID, result, how many runs, tracker key.
