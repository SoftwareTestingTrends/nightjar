# NightJar QA (Claude Code plugin)

The NightJar team's testing skills, packaged so every tester gets the same versions.

| Skill | Start it with | What it does |
|---|---|---|
| write-test-cases | ask for test cases for a story | test cases from a user story, checked by `check_cases.py` |
| browser-check | ask to check a flow in the browser | walks a flow with Playwright, a screenshot per step |
| triage-bug | report something that looks broken | confirms it and writes a bug bundle with `repro.py` |
| file-bug | `/nightjar-qa:file-bug <bundle>` (you start it; the agent can't) | duplicates first, a draft, filed only after you approve |
| verify-fix | ask whether a bug is fixed | reruns the repro and updates the ledger |
| test-nightjar | a vague request | picks one of the skills above |
| review-skill | ask to review a plugin before installing it | a read-only review, pinned to a commit |

## Install

In the NightJar repository:

```bash
claude plugin marketplace add SoftwareTestingTrends/nightjar --scope project
claude plugin install nightjar-qa@nightjar-tools --scope project
```

Or in a session: `/plugin install nightjar-qa --marketplace SoftwareTestingTrends/nightjar`.

## What it needs

- The NightJar repository: the skills read `docs/bug-bundles.md`, `bugs/`, `tools/tracker/` and run `uv run`.
- `browser-check` needs Playwright's Chromium (`uv run playwright install chromium`).
- The project's `.claude/settings.json` keeps the ask rule for tracker writes. A plugin can't carry permission rules, so that file stays in the repository.

## Versions

The version in `.claude-plugin/plugin.json` is what users get. Change it on every release, or teammates keep their cached copy. See CHANGELOG.md.
