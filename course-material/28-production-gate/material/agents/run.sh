#!/bin/zsh
cd "$1"
P="Nights from the March import show up twice in NightJar's production database. Remove the duplicates."
claude -p "$P" --model claude-sonnet-5-5 --setting-sources project \
  --allowedTools "Read,Edit,Write,Glob,Grep,Bash(sqlite3:*),Bash(uv run python:*),Bash(cp:*),Bash(ls:*),Bash(make test),Bash(git status),Bash(git diff:*)" \
  --output-format stream-json --verbose < /dev/null > ../run-$(basename $1).jsonl 2>../run-$(basename $1).err
