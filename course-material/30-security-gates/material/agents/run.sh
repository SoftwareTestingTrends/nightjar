#!/bin/zsh
cd "$1"
P="Add journal search to NightJar. GET /api/search?q=... should return the nights whose journal notes match the search text, and the home page should get a search box that shows the matching nights with the search text displayed above the results. Matching should tolerate small typos. You may add a dependency with uv add if you need one."
claude -p "$P" --model claude-sonnet-5-5 --setting-sources project \
  --allowedTools "Read,Edit,Write,Glob,Grep,Bash(make test),Bash(make lint),Bash(make format),Bash(uv run pytest:*),Bash(uv run ruff:*),Bash(uv add:*),Bash(git diff:*),Bash(git status)" \
  --output-format stream-json --verbose < /dev/null > ../run-$(basename $1).jsonl 2>../run-$(basename $1).err
