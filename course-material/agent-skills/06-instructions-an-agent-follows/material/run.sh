#!/bin/zsh
# usage: run.sh <name> <variant.md> <prompt>
H=${0:A:h}; C=$H/copy-$1; rm -rf $C; mkdir -p $C
git -C ~/ai-projects/nightjar archive lesson/skill-descriptions | tar -x -C $C
rm -rf $C/course-material
cp "$2" $C/.claude/skills/write-test-cases/SKILL.md
cd $C && git init -q && git add -A && git -c user.email=ambysan@gmail.com -c user.name="Ambreen Khan" commit -qm base && uv sync -q
claude -p "$3" --model claude-sonnet-5-5 --setting-sources project \
  --allowedTools "Read,Write,Edit,Glob,Grep,Skill,Bash(ls:*),Bash(mkdir:*),Bash(git status)" \
  --output-format stream-json --verbose < /dev/null > $H/run-$1.jsonl 2>$H/run-$1.err
