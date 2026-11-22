# Skill trigger tests

Does a skill load for the requests it should, and stay out of the ones it shouldn't?

    python3 skill-tests/trigger_eval.py . write-test-cases skill-tests/write-test-cases/train.json 3 /tmp/out.json

Each query runs 3 times in a fresh `claude -p` session. The script watches the agent's
first tool call: loading the skill counts as a trigger, anything else as a miss, and the
session is stopped there (nothing is changed). A query passes if it triggers in at least
half its runs (should-trigger) or in fewer than half (should-not).

- `train.json`: the set you tune the description against.
- `holdout-1.json`, `holdout-2.json`: sets you don't tune against. Once you've looked at a
  held-out set's failures and changed the description because of them, it stops being
  held out: write a fresh one.

Method from skill-creator's `scripts/run_eval.py` (anthropics/claude-plugins-official).
