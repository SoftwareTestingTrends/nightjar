#!/bin/zsh
# usage:
#   run.sh init <copy>                 fresh copy of lesson/handoffs + fresh tracker
#   run.sh run  <copy> <name> <prompt> [max-turns]   one session in that copy (files persist)
#   run.sh fix  <copy>                 apply the developer's fix (fix-reimport.patch) to the copy
# The agent's environment holds the tracker's WRITE token; MCP servers are off.
H=${0:A:h}; C=$H/copy-$2; T=$H/trackers/$2
case $1 in
init)
  rm -rf $C $T; mkdir -p $C $T
  git -C ~/ai-projects/nightjar archive lesson/handoffs | tar -x -C $C
  rm -rf $C/course-material
  cd $C && git init -q && git add -A && git -c user.email=ambysan@gmail.com -c user.name="Ambreen Khan" commit -qm base && uv sync -q
  ;;
fix)
  cd $C && git apply $H/fix-reimport.patch && git diff --stat
  ;;
run)
  cd $C
  export NJ_TRACKER_HOME=$T
  lsof -ti tcp:8765 | xargs kill 2>/dev/null
  SEED=""; [[ -f $T/issues.json ]] || SEED=--seed
  python3 tools/tracker/server.py $SEED > $T/server.log 2>&1 &
  SP=$!; sleep 1
  export NJ_TRACKER_TOKEN=$(python3 -c "import json;print(json.load(open('$T/tokens.json'))['write'])")
  MT=(); [[ -n "$5" ]] && MT=(--max-turns $5)
  claude -p "$4" $MT --model claude-sonnet-5-5 --setting-sources project --strict-mcp-config \
    --allowedTools "Read,Write,Edit,Glob,Grep,Skill,Bash(python3:*),Bash(uv run:*),Bash(ls:*),Bash(mkdir:*),Bash(make:*),Bash(git status)" \
    --output-format stream-json --verbose < /dev/null > $H/runs/run-$3.jsonl 2>$H/runs/run-$3.err
  kill $SP 2>/dev/null; true
  ;;
esac
