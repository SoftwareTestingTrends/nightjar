---
name: test-nightjar
description: Picks the right NightJar testing skill when a request is vague about what kind of check it wants ("test the import", "something's off with the diary", "what can you check?", "is NightJar OK?"). Not for requests that already name the job, such as writing test cases for a story, checking a flow in the browser, or rechecking a known bug: those skills start directly.
---

# Route a testing request

This skill doesn't test anything. It picks the skill that should, says which one and
why in one sentence, and starts it.

| They want to know | Skill |
|---|---|
| Whether a flow on the page works, step by step | browser-check |
| Whether something reported broken really is, and why | triage-bug |
| Whether a known defect is fixed now | verify-fix |
| What to test for a story | write-test-cases |
| How to get a bug into the tracker | tell them to run `/nightjar-qa:file-bug` (you can't start it) |

Ask a question only when the answer would change which skill runs. If the request
already says enough, start.
