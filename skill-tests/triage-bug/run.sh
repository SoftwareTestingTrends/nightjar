#!/bin/zsh
# One eval run, from the repository root:
#   [MODEL=claude-sonnet-5-5] zsh skill-tests/triage-bug/run.sh <eval-id> <with_skill|without_skill> <run-number> [out-dir]
# Runs Claude Code on a fresh copy of the committed code (git archive HEAD), without
# skill-tests/ so the agent can't read the expected answers, then grades it with grade.py.
# The model is pinned (MODEL, default below), so a change of default model can't
# change the results without anyone noticing. run.json records what actually ran.
# Results go to <out-dir>/eval-<id>-<name>/<config>/run-<n>/ (default out-dir: skill-tests/triage-bug/results).
K=${0:A:h}; ROOT=$(git -C $K rev-parse --show-toplevel); E=$1; CFG=$2; N=$3; OUT=${4:-$K/results}
MODEL=${MODEL:-claude-sonnet-5-5}
NAME=$(python3 -c "import json;print([x for x in json.load(open('$K/evals.json'))['evals'] if x['id']==$E][0]['name'])")
R=$OUT/eval-$E-$NAME/$CFG/run-$N; C=$(mktemp -d)/nightjar
mkdir -p $R $C && git -C $ROOT archive HEAD | tar -x -C $C
rm -rf $C/skill-tests $C/course-material
[[ $CFG == without_skill ]] && rm -rf $C/.claude/skills/triage-bug $C/.claude/skills/test-nightjar
cd $C && git init -q && git add -A && git -c user.email=eval@example.invalid -c user.name=eval commit -qm base && uv sync -q
PROMPT=$(python3 -c "
import json;d=json.load(open('$K/evals.json'));e=[x for x in d['evals'] if x['id']==$E][0]
p=e['prompt']+' '+d['deliverable']
print(('/triage-bug '+p) if '$CFG'=='with_skill' else p)")
echo "$PROMPT" > $R/prompt.txt
claude -p "$PROMPT" --model $MODEL --setting-sources project --strict-mcp-config \
  --allowedTools "Read,Write,Edit,Glob,Grep,Skill,Bash(python3:*),Bash(uv run:*),Bash(ls:*),Bash(mkdir:*),Bash(make:*),Bash(git status)" \
  --output-format stream-json --verbose < /dev/null > $R/transcript.jsonl 2>$R/stderr.txt
python3 $K/grade.py $K/evals.json $E $C $R
python3 $K/run_info.py $R "$MODEL" "$(claude --version)" "$(git -C $ROOT rev-parse --short HEAD)" \
  "$(git -C $ROOT rev-parse --short HEAD:.claude/skills/triage-bug)"
mkdir -p $R/outputs && [[ -d $C/bugs ]] && cp -r $C/bugs $R/outputs/
rm -rf ${C:h}
