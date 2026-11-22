# NightJar defect ledger (from this course)

## Problems found in agent changes after their own tests passed (none merged)

| Changes | Problem | Found by |
|---|---|---|
| grading-the-path, 6 off-topic changes | Evidence couldn't fail: evals ran on the mock each agent had just taught | Model judge on the transcripts |
| grading-the-path, all 6 | Mock declines "My brain won't stop working on code at bedtime" | Probe (reviewing-agent-code lesson) |
| grading-the-path, quick1 | E-09 outside the documented traceability range | Merge gate (quality-gates lesson) |
| grading-the-path, plain2 | Formatter changed code after the last test run | Model judge |
| grading-the-path, plain3 | A test that only checks the prompt's text | Reading the diff |
| reviewing-agent-code, sum1–3 | Two readings of "the last 7 days" (sum1 and sum3 rolling 168 h, sum2 calendar days); disagree with the coach's average | Side-by-side run on the same diary |
| reviewing-agent-code, sum2 | Nights dated in the user's current zone | AI reviewer |
| reviewing-agent-code, sum1 | `average_sleep_minutes > 0` as the only check of the average | AI reviewer |

9 of 23 recorded agent changes; 0 escaped to main.

## Issues already in NightJar main (escaped before the course found them)

| Bug | Found by | Status |
|---|---|---|
| Quiet hours on the spring-forward night: a 03:00 nudge inside quiet hours is loud | An agent's test ideas (test-design lesson) | Fixed on `lesson/failing-test-first`; still on `main` |
| Shift workers: bedtimes either side of noon give a usual bedtime of 00:00 | A tester's idea (test-design lesson) | Open (product question) |
| The "last 14 nights" test can't tell a 13-night window apart | Mutation testing (judging-tests lesson) | Open (test gap) |
| Unit-test nights are built in local time, but the app loads them as UTC | Mutation testing (judging-tests lesson) | Open (test-data gap; API tests catch it) |
| The claims check replaces good refusals with the generic fallback | Real-model evals (no-single-right-answer lesson) | Open (product question) |
| The coach writes code when asked an off-topic question | The first eval set, on the real model | Open (product question) |
| "treat" flagged as a claim ("I treat journal entries as your data", "a treat") | The eval set and ten trials (run-it-ten-times lesson) | Open (same product question) |
| The coach overstates the diary ("helped", "usual" for a habit mentioned once) | A grounding judge (graders lesson) | Open (product question) |
| `make evals` runs the mock, so a prompt that doesn't work still passes | The model judge on the transcripts (grading-the-path lesson) | Addressed: CLAUDE.md rule and real-model evals in CI |
| About a third of answers break the "under 120 words" rule (29 of 90) | CI eval runs (regression-testing lesson) | Open (add a length grader) |
| The claims check flags about 1 in 5 good answers and catches 7 of 24 unsafe ones | Measured (quality-gates lesson) | Open (waiting on the coach owner and Regulatory & Brand) |
| A crisis answer with a flagged word would lose its crisis line to the fallback | The diagnose agent (traces lesson) | Open (safety decision for the product owner, Regulatory & Brand and a clinical advisor) |
| `CLAUDE.md` says a healthy run is "66 passed" | Agents in three lessons | Stale on `main` |
