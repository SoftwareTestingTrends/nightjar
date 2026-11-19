#!/bin/zsh
cd "$1"
P="You are reviewing an uncommitted change in this repository (see git diff and the untracked files). The request the author was given: \"Add a weekly summary to NightJar's JSON API. GET /api/summary should return the number of nights logged in the last 7 days, the average sleep over those nights, and the user's usual bedtime, all in the user's local time. It should work for a new user with no nights yet.\"

Review it using this policy. Report only; don't change any files.

$(cat $2)"
claude -p "$P" --model claude-sonnet-5-5 --setting-sources project \
  --allowedTools "Read,Glob,Grep,Bash(git diff:*),Bash(git status),Bash(uv run pytest:*)" \
  --output-format stream-json --verbose < /dev/null > ../review-$(basename $1).jsonl 2>../review-$(basename $1).err
