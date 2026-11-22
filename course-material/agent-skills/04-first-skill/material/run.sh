#!/bin/zsh
# usage: run.sh <name> <prompt> [skill-dir-to-install]
# Fresh copy of NightJar branch lesson/first-skill for every run; transcript in ../run-<name>.jsonl
H=${0:A:h}; C=$H/copy-$1; rm -rf $C; mkdir -p $C
git -C ~/ai-projects/nightjar archive lesson/first-skill | tar -x -C $C
rm -rf $C/course-material
if [[ -n "$3" ]]; then mkdir -p $C/.claude/skills; cp -R "$3" $C/.claude/skills/; fi
cd $C && git init -q && git add -A && git -c user.email=ambysan@gmail.com -c user.name="Ambreen Khan" commit -qm base && uv sync -q
claude -p "$2" --model claude-sonnet-5-5 --setting-sources project \
  --allowedTools "Read,Write,Edit,Glob,Grep,Skill,Bash(make:*),Bash(uv run:*),Bash(ls:*),Bash(mkdir:*),Bash(git status),Bash(git diff:*)" \
  --output-format stream-json --verbose < /dev/null > $H/run-$1.jsonl 2>$H/run-$1.err
