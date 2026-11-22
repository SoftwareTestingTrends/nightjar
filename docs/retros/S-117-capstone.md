# S-117 retro: one change, story to verified fix

Seven sessions, joined only by files, all with the `nightjar-qa` plugin (Claude Code 2.1.330,
Sonnet 5.5). Transcripts are in the course's capstone material.

| Session | Skill | What happened |
|---|---|---|
| 1. "Write the test cases" | write-test-cases | 25 cases in `docs/test-cases/S-117.md`, checker 13 passed, 0 failed |
| 2. Browser check | browser-check | Ran 7 of 25 cases. AC1, AC2 pass; AC3 (all times `+00:00`) and AC4 (newest first) fail |
| 3. "Can you triage these?" | triage-bug | D-1 and D-2 confirmed, repro 3 of 3 each, bundles and ledger rows |
| 4. `/nightjar-qa:file-bug` ×2 | file-bug | Duplicate searches, two drafts, stopped for approval; a person filed NJ-15 and NJ-16 |
| 5. "Record the keys" | none | Keys written to the bundles and the ledger (from the contract) |
| 6. "Are D-1 and D-2 fixed?" | verify-fix | Both fixed, 3 of 3; draft tracker comments, not posted |
| 7. Browser recheck | browser-check | Ran 7 of 25 cases (AC1 to AC4); all pass |

## Which skill needs work next: browser-check

Each browser check ran 7 of the 25 test cases, all from AC1 to AC4. Most of the rest were never exercised:

- **No clock.** The helper (`with_app.py`) can't set "now", so the date cases (TC-117-2 to 4)
  can't run. NightJar's `create_app(clock=…)` already accepts one.
- **No test data sets.** It loads one CSV. The cases name data sets from
  `write-test-cases/references/test-data.md` (D-dst, D-notes, D-1000, Ana's zone change) that
  the helper can't build, so AC3's clock-change cases, AC5 and the 1,000-night timing never ran.
- **AC4 barely tested.** The sample is already in order, and the code sorts by bedtime instant,
  not "night of" date (TC-117-15 is the risk).
- **AC6 (round trip) not run.**

Next change: give `with_app.py` a `--now` option and a `--data <set>` option that builds the
reference data sets, and add a step that lists which cases this run can and can't execute.

## Also worth fixing

- **Exit codes.** 11 of 17 permission denials were the agent capturing a repro's exit code
  with `echo $?` (triage-bug, file-bug, verify-fix). verify-fix then wrote "exit 0 (3 of 3)"
  as an inference. A shared `run_repro.py` that runs a repro N times and prints each exit
  code would be one allowed command.
- **Scope.** triage-bug offered "I can also fix both". Fixing is the developer's job.
- **Recording keys** after a person files has no skill; the agent followed the contract.

## Still open for product

- Line endings: LF now; the test cases propose CRLF (RFC 4180).
- "Night of" order vs bedtime order for nights in different zones (TC-117-15).
