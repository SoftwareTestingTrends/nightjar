#!/bin/zsh
cd "$1"
P="Add a weekly summary to NightJar's JSON API. GET /api/summary should return the number of nights logged in the last 7 days, the average sleep over those nights, and the user's usual bedtime, all in the user's local time. It should work for a new user with no nights yet. You may add a dependency with uv add if you need one."
claude -p "$P" --model claude-sonnet-5-5 --setting-sources project \
  --allowedTools "Read,Edit,Write,Glob,Grep,Bash(make test),Bash(make lint),Bash(make format),Bash(uv run pytest:*),Bash(uv run ruff:*),Bash(uv add:*),Bash(git diff:*),Bash(git status)" \
  --output-format stream-json --verbose < /dev/null > ../run-$(basename $1).jsonl 2>../run-$(basename $1).err
