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

The skills ship as the `nightjar-qa` plugin (`plugins/nightjar-qa/`). Both configurations load it
with `--plugin-dir`; `without_skill` removes `triage-bug` and the router from the copy first.

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

Reading a rerun that changed:

1. **What changed?** `run.json` says the model, the Claude Code version, the app commit and
   the skill version. Change one thing at a time when you can.
2. **Which eval moved?** Read the per-eval column, then the agent's reply for the runs that
   failed. If the agent is right and the label is wrong (a bug that's since been fixed,
   say), update `evals.json` in the same commit as the app change.
3. **Is it a break or a wobble?** 3/3 to 0/3 is a break. 3/3 to 2/3 can be chance: rerun
   that one eval ten times (`for n in $(seq 1 10); do zsh skill-tests/triage-bug/run.sh 2 with_skill $n results-eval2; done`)
   before you change the skill.

You can also aggregate with skill-creator's script, from its skill folder:
`python -m scripts.aggregate_benchmark <path to skill-tests/triage-bug/results> --skill-name triage-bug`.
Results are gitignored. The run copies leave out `skill-tests/`, so the agent can't read
the expected answers.
