# Course material

The recorded runs, scripts and outputs behind the course
[**Who Tests the Tests? Quality Engineering in the AI-Native SDLC**](https://softwaretestingtrends.com/courses/5d5b9470-037f-4eb4-9035-d60347980d2c).
When a lesson says
"this lesson's `material/` folder", it means `course-material/<lesson>/material/` here.
Folder numbers match the lesson numbers on the site.

The material for **Teach the Agent to Test: Building Agent Skills for QA** is in
[`agent-skills/`](agent-skills/).


| Folder | Lesson |
|---|---|
| [`05-the-agent-loop`](05-the-agent-loop/material/) | What a coding agent actually does |
| [`06-model-plus-harness`](06-model-plus-harness/material/) | Agent = model + harness |
| [`07-context-engineering`](07-context-engineering/material/) | Context is the spec the agent actually reads |
| [`08-advisory-vs-enforced`](08-advisory-vs-enforced/material/) | Asking vs enforcing: skills and hooks |
| [`10-the-traceable-chain`](10-the-traceable-chain/material/) | The traceable chain |
| [`11-reviewing-agent-written-specs`](11-reviewing-agent-written-specs/material/) | Reviewing a spec an agent wrote |
| [`13-test-design-with-agents`](13-test-design-with-agents/material/) | Test design with an agent at your side |
| [`14-tests-from-the-spec`](14-tests-from-the-spec/material/) | Tests from the spec, not from the code |
| [`15-reviewing-the-plan`](15-reviewing-the-plan/material/) | Reviewing the plan before the code |
| [`16-agent-checks-itself`](16-agent-checks-itself/material/) | Give the agent a way to check itself |
| [`17-failing-test-first`](17-failing-test-first/material/) | Failing test first, and lock it |
| [`18-judging-agent-tests`](18-judging-agent-tests/material/) | Judging tests an agent wrote |
| [`19-fresh-context-verifier`](19-fresh-context-verifier/material/) | A second pair of eyes with fresh context |
| [`20-no-single-right-answer`](20-no-single-right-answer/material/) | When there's no single right answer |
| [`21-first-eval-set`](21-first-eval-set/material/) | Building your first eval set |
| [`22-graders`](22-graders/material/) | Graders: code, model and human |
| [`23-run-it-ten-times`](23-run-it-ten-times/material/) | Run it once, run it ten times |
| [`24-grading-the-path`](24-grading-the-path/material/) | Grading the path, not just the answer |
| [`25-regression-testing-the-agent`](25-regression-testing-the-agent/material/) | Regression-testing the agent itself |
| [`26-quality-gates`](26-quality-gates/material/) | Quality gates a machine can run |
| [`27-reviewing-agent-code`](27-reviewing-agent-code/material/) | Reviewing code an agent wrote |
| [`28-production-gate`](28-production-gate/material/) | Up to the production gate, and no further |
| [`29-prompt-injection`](29-prompt-injection/material/) | Prompt injection: untrusted by default |
| [`30-security-gates`](30-security-gates/material/) | Security gates for generated code |
| [`31-multi-agent-failures`](31-multi-agent-failures/material/) | When multi-agent systems fail |
| [`32-traces-and-flywheel`](32-traces-and-flywheel/material/) | Traces, costs and the quality flywheel |
| [`33-measuring-what-matters`](33-measuring-what-matters/material/) | Measuring what matters |
| [`34-the-testers-new-job`](34-the-testers-new-job/material/) | The tester's new job |
| [`35-capstone-one-story-end-to-end`](35-capstone-one-story-end-to-end/material/) | Capstone: one story, end to end |

## What's in a folder

- **Agent transcripts** (`*.jsonl`): Claude Code runs recorded with `claude -p --output-format stream-json`.
  Each run's last `result` line has its cost, duration and turns.
- **Coach traces and eval results** (`*traces*.jsonl`, `results-*.jsonl`): what the coach was asked,
  what the model wrote and what the user was shown.
- **Scripts** (`*.py`, `*.sh`) and their **outputs** (`*.txt`, `*.json`).
- **Diffs** of the agents' changes, and the eval cases, rubrics and gate tables they were checked against.

## Reading a transcript

The agent transcripts (`run-*.jsonl` and similar) are the raw stream-JSON that
`claude -p --output-format stream-json` writes, the same format you'd get from an agent run in CI.
Each line is one event:

- `assistant` lines are the agent's turns. A `tool_use` block is a step it took (Read, Edit, Bash…),
  and a `text` block is what it said.
- `user` lines carry the tool results back to the agent.
- `system` lines include `permission_denied`, when a hook or permission rule blocked a step.
- The last line, `result`, has the agent's final report, its cost, time and number of turns.

To see the steps and the final report without the JSON, run:

```bash
python3 course-material/read_transcript.py course-material/24-grading-the-path/material/run-quick1.jsonl
```

The prompt each agent was given is in the lesson's `run.sh` or `agent-run.sh`, or in the lesson text.

One note on lesson 05: the agent's transcript calls the planted commit `d2ba38a`. On the
`lesson/agent-loop-demo` branch the same commit is `4e86073`, because the branch was re-created
before it was published.

## Running the scripts

Run them from the repository root and pass this folder:

```bash
python3 course-material/33-measuring-what-matters/material/output_volume.py course-material
python3 course-material/32-traces-and-flywheel/material/agent_costs.py course-material
```

Some scripts read other lessons' folders (the cost and monitoring scripts read every lesson's traces),
so keep the folder structure as it is. Scripts that call a model need the Claude Code CLI or an API key,
and cost real money; the saved outputs next to them are what the lessons quote.

## Notes

- The runs were recorded in October 2026 on clones of this repository, mostly with `claude-sonnet-5-5`.
  Costs are the list prices Claude Code reports.
- Personal names, email addresses and local paths in the transcripts have been replaced
  (for example `/tmp/work/...`), and each run's start-up event keeps only its working directory,
  model, permission mode and tools.
- The capstone's branch is `lesson/capstone-lead-time` in this repository.
- The company and team around NightJar are fictional.
