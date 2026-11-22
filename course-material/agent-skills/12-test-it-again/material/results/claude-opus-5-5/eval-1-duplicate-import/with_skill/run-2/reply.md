Yes, it's a real bug. If you import the same CSV twice, every night ends up in the diary twice.

**What I found:** I imported a 2-night CSV twice through the real `/import` endpoint, using a temporary database. Both imports succeeded with "imported 2", and the diary ended up holding 4 nights. This happened 3 times out of 3. The cause is that the import adds every row from the file without checking for nights already stored, and the database doesn't block duplicates either.

**Why it matters beyond the import:** the usual-bedtime calculation counts each copy as a separate night.
- The app is supposed to send no reminder until there are 7 nights. Importing 4 real nights twice gives 8 rows, so the reminder turns on too early.
- The bedtime is meant to come from the last 14 nights. With duplicates, it really comes from only 7 different nights.

**What should happen isn't written down anywhere.** No requirement or story says what re-importing an existing night should do: skip it, replace it, or reject the file. So I marked Expected as "Not specified" and added a question for product, including what the "imported N nights" message should say in that case.

**Files written** (`bugs/` is gitignored, so nothing is committed):
- `bugs/D-1-double-import/repro.py`: exits 1 while the bug is present and 0 once it's fixed. I put it in a `D-1-` folder rather than plain `bugs/double-import/` because the project's bug format in `docs/bug-bundles.md` requires the number.
- `bugs/D-1-double-import/report.md`
- `bugs/ledger.md`: new row for D-1, status `confirmed`, not filed.

To rerun it: `uv run python bugs/D-1-double-import/repro.py`

**Next step:** filing it puts it in front of the team, so that's for you to start. Run `/file-bug bugs/D-1-double-import`.