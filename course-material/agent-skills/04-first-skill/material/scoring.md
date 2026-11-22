# Scoring the runs (2026-11-19)

All runs: Claude Code 2.1.328, claude-sonnet-5-5, `--setting-sources project`, a fresh copy of NightJar branch `lesson/first-skill` per run (`run.sh`). Scored by hand against `reference/S-116-reference.md` (R1–R12, Q1–Q4) and `reference/S-117-reference.md` (E1–E9, Q1–Q3), which were written before any run.

| Run | Request | Skill | Turns | Time | Output | Read src/ or tests/? | Conditions | Reference questions |
|---|---|---|---|---|---|---|---|---|
| 1 plain | "Write test cases for story S-116 (docs/stories/S-116.md)." | none | 30 | 146 s | 27 pytest tests against an invented `nightjar.summary` interface, all skipped (module doesn't exist), never run; edited `tests/test_api.py` and `docs/traceability.md` | yes (tests, models, nudge, web, templates) | 11.5 of 12 (no "updates after a night is added") | 2.5 of 4 (rounding tie, duplicates; zero-minute format partly; even-count median missed) |
| 2 guided | the six-point prompt in `prompt-guided.txt` | none | 11 | 250 s | `docs/test-cases/S-116.md`: 73 cases, 13 open questions | no | 12 of 12 | 4 of 4 |
| 3 hand skill on S-117 | "Write test cases for story S-117 (docs/stories/S-117.md)." | `write-test-cases` (by hand, 388 words) | 12 | 115 s | 67 cases, 14 open questions | no | 9 of 9 | 3 of 3 (spaces as a case; formula and encoding as questions) |
| 4 skill-creator drafts | "Use the skill-creator skill to create a project skill…" (draft only) | skill-creator (plugin) | 16 | 63 s | `story-test-cases`: SKILL.md 1,335 words + `references/template.md` 495 words | n/a | — | — |
| 5 skill-creator's skill on S-117 | same request as run 3 | `story-test-cases` | 10 | 117 s | 26 cases, 7 open questions each with a proposed answer | no | 9 of 9 | 3 of 3 |

Notes
- Run 4's first attempt (`run-skill-creator-blocked.jsonl`) asked to save into `.claude/skills/`; the write was blocked by permissions even though Write was allowed, and the agent stopped and asked. The recorded run saved to `skill-drafts/` and the draft was copied in by hand.
- Both skills triggered on the same short request that produced code in run 1.
- Run 3's TC-117-43 expects notes with leading and trailing spaces to come back unchanged. NightJar's existing CSV import trims notes (`diary.parse_csv` uses `.strip()`), so a round trip built on today's import would fail that case: a real conflict the test cases expose before any export code exists.
