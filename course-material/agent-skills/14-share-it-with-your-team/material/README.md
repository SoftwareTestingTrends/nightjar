# Material: Share it with your team

How the recorded runs were set up (2026-11-22, Claude Code 2.1.330, Sonnet 5.5):

- **The team's remote**: a local bare copy of NightJar with `lesson/share-it` pushed as `main`, served
  on 127.0.0.1:8765 by `git_http.py` (smart HTTP through `git http-backend`; Python's plain file
  server can't serve the shallow clone Claude Code asks for). Nothing was pushed to GitHub.
- **The teammate**: a clone of that remote, with
  `claude plugin marketplace add http://127.0.0.1:8765/nightjar.git --scope local` and
  `claude plugin install nightjar-qa@nightjar-tools --scope local`, and
  `CLAUDE_CODE_PLUGIN_CACHE_DIR` pointed at a sandbox plugin store, so this machine's own plugins and
  settings were untouched (md5 of ~/.claude/settings.json, known_marketplaces.json and
  installed_plugins.json checked before and after).
- **run_team.sh**: copies the teammate's clone, installs the plugin in the copy (a project or local
  install is recorded per clone), and runs one `claude -p` session. runs/setup-v1 shows the copies
  without that install: the plugin didn't load.
- **other-plugin/**: a stand-in second plugin with its own `file-bug` skill, for the name test.
- **regression-1.1.0/**: the triage-bug eval kit (30 runs) on the packaged plugin.

Runs: v1-* against nightjar-qa 1.0.0 (skills moved unchanged), v2-* against 1.1.0.
