I couldn't reproduce this, so I didn't write a `repro.py`.

**What I tried:**
- I posted quiet hours 21:00 to 00:00 to `/settings` three times, each against a fresh throwaway database through the FastAPI test client.
- All three runs saved normally: the endpoint returned a 303 redirect and the database stored 21:00 and 00:00. The page also still loaded afterwards.
- Midnight itself isn't the problem. The code handles a window that wraps past midnight, and `00:00:00` is accepted too.
- Only `24:00`, `0:00` and `12:00 AM` are rejected with a 400 error. A browser time field doesn't normally produce those.

I didn't try it in a real browser.

**Where the report probably comes from:** the reporter may be typing `24:00` or a 12-hour value like `12:00 AM`. A different browser or locale could cause that. To find out, ask them for the exact error text, their browser and locale, and a screenshot. If the failure shows up in a real browser, re-run `/triage-bug` with those details.

**Files written, as `docs/bug-bundles.md` describes:**
- `bugs/D-1-quiet-hours-midnight/report.md`, with status `not reproduced`.
- `bugs/ledger.md`, with a row for D-1 and tracker `not filed`.

There is nothing to file, so `/file-bug` isn't needed.