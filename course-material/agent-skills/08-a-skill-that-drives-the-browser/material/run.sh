#!/bin/zsh
# usage: run.sh <name> <with-skill: yes|no> <prompt>
H=${0:A:h}; C=$H/copy-$1; rm -rf $C; mkdir -p $C
git -C ~/ai-projects/nightjar archive lesson/browser-skill | tar -x -C $C
rm -rf $C/course-material
[[ "$2" == "no" ]] && rm -rf $C/.claude/skills/browser-check
cd $C && git init -q && git add -A && git -c user.email=ambysan@gmail.com -c user.name="Ambreen Khan" commit -qm base && uv sync -q
claude -p "$3" --model claude-sonnet-5-5 --setting-sources project \
  --allowedTools "Read,Write,Edit,Glob,Grep,Skill,Bash(python3:*),Bash(uv run:*),Bash(ls:*),Bash(mkdir:*),Bash(make:*),Bash(curl:*),Bash(git status)" \
  --output-format stream-json --verbose < /dev/null > $H/run-$1.jsonl 2>$H/run-$1.err
pkill -f "copy-$1.*uvicorn" 2>/dev/null; pkill -f "uvicorn nightjar.web:create_app.*--port 8000" 2>/dev/null; true
