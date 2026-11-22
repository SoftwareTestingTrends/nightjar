#!/bin/zsh
# usage: run.sh <name> <prompt>   (runs in ./nj, writes ../run-<name>.jsonl)
cd "${0:A:h}/nj"
claude -p "$2" --model claude-sonnet-5-5 --setting-sources project \
  --allowedTools "Read,Write,Edit,Glob,Grep,Skill,Bash(make:*),Bash(uv run:*),Bash(python:*),Bash(python3:*),Bash(ls:*),Bash(mkdir:*)" \
  --output-format stream-json --verbose < /dev/null > ../run-$1.jsonl 2>../run-$1.err
