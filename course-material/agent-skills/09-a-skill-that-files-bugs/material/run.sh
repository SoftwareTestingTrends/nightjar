#!/bin/zsh
# usage: run.sh <name> <setup: none|rule|guarded> <prompt> [resume-session-id]
#   none    = no file-bug skill, no ask rule
#   rule    = ask rule in .claude/settings.json, no skill
#   guarded = skill (with its hook) + ask rule
# The agent's environment holds the tracker's WRITE token in every run.
H=${0:A:h}; C=$H/copy-$1; T=$H/trackers/$1
if [[ -z "$4" ]]; then
  rm -rf $C $T; mkdir -p $C $T
  git -C ~/ai-projects/nightjar archive lesson/bug-filing | tar -x -C $C
  rm -rf $C/course-material
  [[ "$2" != "guarded" ]] && rm -rf $C/.claude/skills/file-bug
  [[ "$2" == "none" ]] && rm -f $C/.claude/settings.json
  cd $C && git init -q && git add -A && git -c user.email=ambysan@gmail.com -c user.name="Ambreen Khan" commit -qm base && uv sync -q
else
  cd $C
fi
export NJ_TRACKER_HOME=$T
lsof -ti tcp:8765 | xargs kill 2>/dev/null
SEED=--seed; [[ -n "$4" ]] && SEED=""
python3 tools/tracker/server.py $SEED > $T/server.log 2>&1 &
SP=$!; sleep 1
export NJ_TRACKER_TOKEN=$(python3 -c "import json;print(json.load(open('$T/tokens.json'))['write'])")
OUT=$H/runs/run-$1.jsonl; RES=(); [[ -n "$4" ]] && { RES=(--resume $4); OUT=$H/runs/run-$1-resume.jsonl; }
claude -p "$3" $RES --model claude-sonnet-5-5 --setting-sources project --strict-mcp-config \
  --allowedTools "Read,Write,Edit,Glob,Grep,Skill,Bash(python3:*),Bash(uv run:*),Bash(ls:*),Bash(mkdir:*),Bash(make:*),Bash(git status)" \
  --output-format stream-json --verbose < /dev/null > $OUT 2>${OUT%.jsonl}.err
kill $SP 2>/dev/null; true
