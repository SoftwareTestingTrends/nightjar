# Bug bundles and the defect ledger

The testing skills hand work to each other through two kinds of file in `bugs/`
(gitignored, like `evidence/`). This page is the contract. A skill that writes them
follows it exactly; a skill that reads them relies on it.

## A bug bundle: `bugs/D-<n>-<short-name>/`

One folder per defect. `D-<n>` is the next free number in the ledger.

- `report.md`, with these lines and sections in this order:

  ```markdown
  # D-<n>: <one-line summary>

  Status: <a ledger status>
  Tracker: <NJ-n, "duplicate of NJ-n", or "not filed">

  ## Steps to reproduce
  ## Expected
  ## Actual
  ## Reproducibility        (e.g. "3 of 3 runs")
  ## Repro                  (the command below and what its exit code means)
  ```

- `repro.py`: a minimal script that reproduces the defect against an empty, throwaway
  database. Run it from the repository root with `uv run python bugs/D-<n>-<short-name>/repro.py`.
  It **exits 1 while the defect is present and 0 once it's fixed**, and prints one line
  saying what it saw. Anyone, or any skill, can rerun it later.

## The defect ledger: `bugs/ledger.md`

One table, one row per bundle, newest last:

```markdown
| ID | Summary | Status | Tracker | Last checked |
|---|---|---|---|---|
| D-1 | … | confirmed | not filed | 2026-11-21, repro exit 1 (3 of 3) |
```

Status is one of: `confirmed`, `not reproduced`, `filed`, `fixed`, `still broken`.
Update a row in place; never delete one.
