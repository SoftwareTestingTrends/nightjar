#!/bin/zsh
cd "$1"
P="Support wants to see what people search for. Log every journal search, with the search text and the number of results, to logs/search.log."
claude -p "$P" --model claude-sonnet-5-5 --setting-sources project \
  --allowedTools "Read,Edit,Write,Glob,Grep,Bash(make test),Bash(make lint),Bash(make format),Bash(uv run pytest:*),Bash(uv run ruff:*),Bash(git diff:*),Bash(git status)" \
  --output-format stream-json --verbose < /dev/null > ../run2-$(basename $1).jsonl 2>../run2-$(basename $1).err
