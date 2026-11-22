# Does an ask rule beat a skill's allowed-tools?

`.claude/skills/write-thing` pre-approves `Bash(python3:*)` and runs
`python3 -c "…" --apply`. Run `claude -p "/write-thing" --setting-sources project` twice:

- with `settings.with-ask.json` as `.claude/settings.json`: the command is stopped
  ("permission hasn't been granted"), permission_denials lists it.
- with `{}`: it runs without asking: `wrote ['--apply']`.

Recorded 2026-11-22, Claude Code 2.1.330, Sonnet 5.5.
