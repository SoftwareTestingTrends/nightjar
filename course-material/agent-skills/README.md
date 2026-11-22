# Course material: Teach the Agent to Test

The recorded runs, scripts and outputs behind the course
[**Teach the Agent to Test: Building Agent Skills for QA**](https://softwaretestingtrends.com/courses).
When a lesson says "this lesson's `material/` folder", it means
`course-material/agent-skills/<lesson>/material/` here. Folder numbers match the lesson
numbers on the site.

The skills themselves are on NightJar's lesson branches (`lesson/first-skill`,
`lesson/skill-descriptions` and so on), not here. This folder holds the evidence: what the
agent was asked, what it did, and what came out.

| Folder | Lesson |
|---|---|
| [`03-anatomy-of-a-skill`](03-anatomy-of-a-skill/material/) | Anatomy of a skill |
| [`04-first-skill`](04-first-skill/material/) | Your first skill: test cases from a story |
| [`05-the-description-decides`](05-the-description-decides/material/) | The description decides when it runs |
| [`06-instructions-an-agent-follows`](06-instructions-an-agent-follows/material/) | Writing instructions an agent follows |
| [`07-scripts-and-references`](07-scripts-and-references/material/) | Keep SKILL.md short: scripts and references |
| [`08-a-skill-that-drives-the-browser`](08-a-skill-that-drives-the-browser/material/) | A skill that drives the browser |
| [`09-a-skill-that-files-bugs`](09-a-skill-that-files-bugs/material/) | A skill that files bugs, safely |
| [`10-skills-that-hand-off`](10-skills-that-hand-off/material/) | Skills that hand off to each other |
| [`11-does-the-skill-help`](11-does-the-skill-help/material/) | Does the skill actually help? |
| [`12-test-it-again`](12-test-it-again/material/) | When the model changes, test the skill again |
| [`13-skills-you-didnt-write`](13-skills-you-didnt-write/material/) | Skills you didn't write |
| [`14-share-it-with-your-team`](14-share-it-with-your-team/material/) | Share it with your team: plugins |
| [`15-capstone`](15-capstone/material/) | Capstone: a testing toolkit for NightJar |

The introduction and "Stop pasting the same prompt" have no recorded runs.

## Reading a transcript

Most runs were recorded with `claude -p --output-format stream-json`, so a transcript is a
`.jsonl` file with one event per line: the session's settings first (`"subtype":"init"`), then
each assistant message, each tool call and its result, and a final `"type":"result"` line with
the turn count and duration. Search for `"name":"Skill"` to see when a skill loaded, and for
`"is_error":true` to see blocked or failed commands.

Folders named `copy` or `copy-*` are the throwaway copies of NightJar a run worked in, as they were when
the run ended, so you can see the files the agent wrote.

## What was changed before publishing

- Python environments (`.venv/`), the copies' own `.git/` folders and caches were left out.
- The local stand-in tracker's `tokens.json` files were removed. The tracker makes new
  tokens when it starts.
- The recording machine's home folder appears as `/Users/you`.
- Some early sessions listed the recording account's claude.ai connectors in their first
  line. That list was removed; none of them were used. Later runs used `--strict-mcp-config`.

Everything else is as it ran.
