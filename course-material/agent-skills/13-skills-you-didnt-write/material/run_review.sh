#!/bin/zsh
# usage: SNAGLY=<pinned snagly checkout> run_review.sh <with_skill|without_skill> <run-number>
# A fresh NightJar copy (lesson/skills-you-didnt-write) with a copy of the Snagly checkout beside
# it at ../snagly. Both configurations get the same request and the same deliverable sentence;
# without_skill has review-skill removed. Only reading tools, the inventory script and
# read-only git commands are allowed.
H=${0:A:h}; CFG=$1; N=$2; SNAGLY=${SNAGLY:?set SNAGLY}
R=$H/reviews/$CFG/run-$N; T=$(mktemp -d); T=${T:A}; C=$T/nightjar
rm -rf $R; mkdir -p $R $C
git -C ~/ai-projects/nightjar archive lesson/skills-you-didnt-write | tar -x -C $C
cp -R $SNAGLY $T/snagly
rm -rf $C/course-material
[[ $CFG == without_skill ]] && rm -rf $C/.claude/skills/review-skill
cd $C && git init -q && git add -A && git -c user.email=eval@example.invalid -c user.name=eval commit -qm base
PROMPT="We're thinking of installing the Snagly plugin for our testing. A copy is checked out at ../snagly. Can we use it? Write the review to docs/reviews/."
[[ $CFG == with_skill ]] && PROMPT="/review-skill $PROMPT"
echo "$PROMPT" > $R/prompt.txt
claude -p "$PROMPT" --model claude-sonnet-5-5 --setting-sources project --strict-mcp-config --add-dir $T/snagly \
  --allowedTools "Read,Write,Edit,Glob,Grep,Skill,Bash(python3 $C/.claude/skills/review-skill/scripts/inventory.py *),Bash(git -C * log *),Bash(git -C * rev-parse *),Bash(git -C * remote *),Bash(git -C * diff *),Bash(git -C * show *),Bash(git -C * tag *),Bash(ls:*),Bash(wc:*)" \
  --output-format stream-json --verbose < /dev/null > $R/transcript.jsonl 2> $R/stderr.txt
mkdir -p $R/outputs && [[ -d $C/docs/reviews ]] && cp -r $C/docs/reviews $R/outputs/
rm -rf $T
