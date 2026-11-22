# Recorded runs

- setup-v1/: the URL never reached the agent ($0 in `zsh -c` was the shell name); no expected times in the request. All three stopped and asked.
- setup-v2/: the URL still never arrived (zsh read `{url} >` as a named file-descriptor redirect); expected times given. All three stopped and asked.
- flow-runner-N/: the recorded runs used in the lesson (URL fixed, CLAUDE.md, AGENTS.md and .claude/ removed from the copy).
