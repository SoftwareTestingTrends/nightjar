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

Then aggregate with skill-creator's script, from its skill folder:
`python -m scripts.aggregate_benchmark <path to skill-tests/triage-bug/results> --skill-name triage-bug`.
Results are gitignored. The run copies leave out `skill-tests/`, so the agent can't read
the expected answers.
