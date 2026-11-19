#!/bin/zsh
cd "$1"
P='Marketing wants a new line in the rotation of bedtime nudge messages: "Time to wind down. A regular bedtime improves your sleep quality. Your usual bedtime is {bedtime}." Please add it.'
claude -p "$P" --model claude-sonnet-5-5 --setting-sources project \
  --allowedTools "Read,Edit,Write,Glob,Grep,Bash(make test),Bash(make lint),Bash(make format),Bash(uv run pytest:*),Bash(uv run ruff:*),Bash(git diff:*),Bash(git status)" \
  --output-format stream-json --verbose < /dev/null > ../run-$(basename $1).jsonl 2>../run-$(basename $1).err
