#!/bin/zsh
# usage: run.sh <name> <skill-dir> <prompt>
H=${0:A:h}; C=$H/copy-$1; rm -rf $C; mkdir -p $C
git -C ~/ai-projects/nightjar archive lesson/skill-instructions | tar -x -C $C
rm -rf $C/course-material $C/.claude/skills/write-test-cases
cp -R "$2" $C/.claude/skills/write-test-cases
cd $C && git init -q && git add -A && git -c user.email=ambysan@gmail.com -c user.name="Ambreen Khan" commit -qm base && uv sync -q
claude -p "$3" --model claude-sonnet-5-5 --setting-sources project \
  --allowedTools "Read,Write,Edit,Glob,Grep,Skill,Bash(ls:*),Bash(mkdir:*),Bash(git status),Bash(python3:*)" \
  --output-format stream-json --verbose < /dev/null > $H/run-$1.jsonl 2>$H/run-$1.err
