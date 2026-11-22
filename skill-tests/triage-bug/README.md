# Does triage-bug help? An eval kit

Five reports (`evals.json`): two real bugs and three that aren't. Each runs with the
skill and without it, with the same deliverable sentence in the prompt, three times.
`grade.py` checks the result with code: does a repro exist, exit 1 today, exit 1 again
three times, exit 0 with the developer's fix (`fix-reimport.patch`), and leave the real
`nightjar.db` alone; for the reports that aren't bugs, does no repro claim a bug.

```bash
for e in 1 2 3 4 5; do for c in with_skill without_skill; do for n in 1 2 3; do
  zsh skill-tests/triage-bug/run.sh $e $c $n
done; done; done
```

The model is pinned: `run.sh` uses `claude-sonnet-5-5` unless you set `MODEL`
(`MODEL=claude-haiku-5-5 zsh skill-tests/triage-bug/run.sh …`). Each run writes `run.json`
with the model asked for, the models that actually answered, the Claude Code version,
the app commit and the skill's tree hash, so a result always says what produced it.

## Keep it as a regression suite

Rerun the whole set when the model, Claude Code or NightJar changes, or when you edit
the skill. Summarise the results and add them to the history:

```bash
python3 skill-tests/triage-bug/summary.py skill-tests/triage-bug/results \
  --append skill-tests/triage-bug/history.csv --note "why you reran it"
```

`history.csv` is committed: one row per configuration per rerun, with pass rate, runs
that passed every check, mean time, mean turns and each eval's result. Compare the new
rows with the last ones before you trust either.

You can also aggregate with skill-creator's script, from its skill folder:
`python -m scripts.aggregate_benchmark <path to skill-tests/triage-bug/results> --skill-name triage-bug`.
Results are gitignored. The run copies leave out `skill-tests/`, so the agent can't read
the expected answers.
