#!/bin/zsh
# usage: [BRANCH=lesson/handoffs] [ITER=iteration-1] run_eval.sh <eval-id> <with_skill|without_skill> <run-number>
# One run: a fresh copy of NightJar lesson/handoffs, the eval prompt plus the same
# deliverable sentence for both configurations ("/triage-bug " in front for with_skill),
# then the code grader. The copy's .venv is deleted afterwards to save space.
H=${0:A:h}; E=$1; CFG=$2; N=$3
NAME=$(python3 -c "import json;e=[x for x in json.load(open('$H/evals/evals.json'))['evals'] if x['id']==$E][0];print(e['name'])")
BRANCH=${BRANCH:-lesson/handoffs}; ITER=${ITER:-iteration-1}
R=$H/$ITER/eval-$E-$NAME/$CFG/run-$N; C=$H/copies/$ITER-eval-$E-$CFG-$N
rm -rf $R $C; mkdir -p $R $C
git -C ~/ai-projects/nightjar archive $BRANCH | tar -x -C $C
rm -rf $C/course-material $C/skill-tests/triage-bug
[[ $CFG == without_skill ]] && rm -rf $C/.claude/skills/triage-bug $C/.claude/skills/test-nightjar
cd $C && git init -q && git add -A && git -c user.email=ambysan@gmail.com -c user.name="Ambreen Khan" commit -qm base && uv sync -q
PROMPT=$(python3 -c "
import json;d=json.load(open('$H/evals/evals.json'));e=[x for x in d['evals'] if x['id']==$E][0]
p=e['prompt']+' '+d['deliverable']
print(('/triage-bug '+p) if '$CFG'=='with_skill' else p)")
echo "$PROMPT" > $R/prompt.txt
claude -p "$PROMPT" --model claude-sonnet-5-5 --setting-sources project --strict-mcp-config \
  --allowedTools "Read,Write,Edit,Glob,Grep,Skill,Bash(python3:*),Bash(uv run:*),Bash(ls:*),Bash(mkdir:*),Bash(make:*),Bash(git status)" \
  --output-format stream-json --verbose < /dev/null > $R/transcript.jsonl 2>$R/stderr.txt
python3 $H/grade.py $H/evals/evals.json $E $C $R
mkdir -p $R/outputs && [[ -d $C/bugs ]] && cp -r $C/bugs $R/outputs/
rm -rf $C/.venv
