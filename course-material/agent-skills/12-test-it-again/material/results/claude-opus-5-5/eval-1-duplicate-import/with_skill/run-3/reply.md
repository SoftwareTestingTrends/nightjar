This is a real bug: importing the same CSV twice stores every night twice. It happened on 3 of 3 runs.

**What happens:** I imported a 2-night CSV through the real `/import` endpoint against a temporary database, then imported it again. Both times the page said "Imported 2 nights.", and the diary ended up with 4 nights. The import code (`Diary.add_nights` in `src/nightjar/diary.py`) adds every row without checking whether that night is already stored, and the database doesn't block duplicates either. This matters beyond the diary list showing each night twice: the duplicates count toward the usual bedtime (median of the last 14 nights), so a re-import can move the nudge time.

**No requirement says what should happen instead.** The only story that mentions importing (S-117) covers importing into an empty diary. So under Expected the report says "Not specified" and asks product: when an imported night is already in the diary, should it be skipped, updated, or should the whole import be rejected? And should "Imported N nights" count only the new ones?

**What I wrote** (in `bugs/`, which git ignores):
- **`bugs/D-1-reimport-duplicates-nights/repro.py`**: it exits 1 while the bug is present and 0 once two imports leave exactly 2 nights. Run it with `uv run python bugs/D-1-reimport-duplicates-nights/repro.py`. You asked for `bugs/<short-name>/`, but I added a `D-1-` prefix because the team's bug-bundle format in `docs/bug-bundles.md` requires it.
- **`bugs/D-1-reimport-duplicates-nights/report.md`**: steps, expected (not specified), actual, and the question for product.
- **`bugs/ledger.md`**: a new row for D-1 with status `confirmed`, tracker `not filed`.

If product chooses "reject the import", the second import will fail and the script will still exit 1, so its check would need updating before it can confirm the fix.

I didn't change any app code, so I didn't run `make test` or `make lint`.

To file it in the tracker, run:

```
/file-bug bugs/D-1-reimport-duplicates-nights
```