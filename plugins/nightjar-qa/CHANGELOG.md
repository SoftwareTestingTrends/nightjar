# Changelog

## 1.1.0
- file-bug: the filing hook now runs from the plugin (`${CLAUDE_PLUGIN_ROOT}`). In 1.0.0 it pointed
  at `.claude/skills/…`, which no longer exists, so it failed silently and only the project's ask
  rule stopped a filing.
- triage-bug, test-nightjar, file-bug: handoffs name `/nightjar-qa:file-bug` in full. The short
  `/file-bug` works only while no other plugin has a skill with that name.
- The triage-bug eval kit loads the plugin with `--plugin-dir`.

## 1.0.0
- First release: the seven skills from `.claude/skills/`, moved into the plugin unchanged.
