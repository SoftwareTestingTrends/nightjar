#!/bin/zsh
# usage: SNAGLY=<pinned snagly checkout> run_flow.sh <run-name> "<request, with APP_URL where the address goes>"
# A fresh NightJar copy (lesson/test-it-again) WITHOUT its CLAUDE.md and .claude/, so only
# Snagly's own instructions are in play. The app runs on a free port with a throwaway DB and
# the diary from the browser lesson (one note is a harmless instruction aimed at an AI).
# Snagly loads for this session only, from the pinned checkout, with --plugin-dir.
H=${0:A:h}; NAME=$1; REQ=$2; SNAGLY=${SNAGLY:?set SNAGLY}
R=$H/runs/$NAME; C=$(mktemp -d)/nightjar
rm -rf $R; mkdir -p $R $C
git -C ~/ai-projects/nightjar archive lesson/test-it-again | tar -x -C $C
cp $C/data/browser-check/diary-with-instruction.csv ${C:h}/diary.csv
rm -rf $C/CLAUDE.md $C/AGENTS.md $C/.claude $C/course-material $C/skill-tests $C/data/browser-check
cd $C && git init -q && git add -A && git -c user.email=eval@example.invalid -c user.name=eval commit -qm base && uv sync -q
echo "$REQ" > $R/request.txt
python3 $H/with_app.py --csv ${C:h}/diary.csv -- zsh -c "claude -p \"\$(sed \"s|APP_URL|\$1|g\" $R/request.txt)\" --plugin-dir $SNAGLY --model claude-sonnet-5-5 --setting-sources project --strict-mcp-config --allowedTools 'Read,Write,Edit,Glob,Grep,Skill,Bash(playwright-cli:*),Bash(npx @playwright/cli:*),Bash(npx --no-install @playwright/cli:*),Bash(curl:*),Bash(lsof:*),Bash(grep:*),Bash(git ls-files:*),Bash(ls:*),Bash(mkdir:*),Bash(cat:*)' --output-format stream-json --verbose < /dev/null > $R/transcript.jsonl 2> $R/stderr.txt" _ '{url}' > $R/with_app.log 2>&1
mkdir -p $R/outputs && cp -r $C/. $R/outputs/ 2>/dev/null; rm -rf $R/outputs/.venv $R/outputs/.git $R/outputs/src $R/outputs/tests
rm -rf ${C:h}
