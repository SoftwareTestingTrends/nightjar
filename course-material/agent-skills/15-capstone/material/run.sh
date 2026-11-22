#!/bin/zsh
# The capstone: one change, story to verified fix, in separate sessions joined only by files.
#   run.sh init                  fresh copy of lesson/capstone at the developer's first version
#   run.sh run <name> <prompt>   one session in that copy (files persist between sessions)
#   run.sh dev <commit>          the developer applies a commit from lesson/capstone to the copy
# Skills come from the nightjar-qa plugin in the copy (--plugin-dir); the project's ask rule
# applies; the agent's environment holds the stand-in tracker's WRITE token; MCP servers are off.
H=${0:A:h}; C=$H/copy; T=$H/tracker
FIRST=${FIRST:-8b269e5}
case $1 in
init)
  rm -rf $C $T; mkdir -p $C $T
  git -C ~/ai-projects/nightjar archive $FIRST | tar -x -C $C
  rm -rf $C/course-material
  cd $C && git init -q && git add -A && git -c user.email=ambysan@gmail.com -c user.name="Ambreen Khan" commit -qm "S-117 first version" && uv sync -q
  ;;
dev)
  cd $C && git -C ~/ai-projects/nightjar diff $2~1 $2 | git apply && git add -A && git -c user.email=ambysan@gmail.com -c user.name="Ambreen Khan" commit -qm "developer: $2" && git log --oneline -1
  ;;
run)
  cd $C
  export NJ_TRACKER_HOME=$T
  lsof -ti tcp:8765 | xargs kill 2>/dev/null
  SEED=""; [[ -f $T/issues.json ]] || SEED=--seed
  python3 tools/tracker/server.py $SEED > $T/server.log 2>&1 &
  SP=$!; sleep 1
  export NJ_TRACKER_TOKEN=$(python3 -c "import json;print(json.load(open('$T/tokens.json'))['write'])")
  echo "$3" > $H/runs/$2.prompt.txt
  claude -p "$3" --model claude-sonnet-5-5 --setting-sources project --strict-mcp-config \
    --plugin-dir $C/plugins/nightjar-qa \
    --allowedTools "Read,Write,Edit,Glob,Grep,Skill,Bash(python3:*),Bash(uv run:*),Bash(ls:*),Bash(mkdir:*),Bash(make:*),Bash(git status),Bash(git diff:*),Bash(git log:*)" \
    --output-format stream-json --verbose < /dev/null > $H/runs/$2.jsonl 2>$H/runs/$2.err
  kill $SP 2>/dev/null; true
  ;;
esac
