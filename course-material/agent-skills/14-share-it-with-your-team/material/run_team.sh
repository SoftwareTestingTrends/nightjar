#!/bin/zsh
# usage: TEAM=<team sandbox> [EXTRA="more claude flags"] run_team.sh <run-name> "<prompt>" "<allowed tools>"
# Runs one session as the teammate: a copy of their NightJar clone, with nightjar-qa installed from
# the team marketplace at local scope, and Claude Code's plugin store moved to the sandbox
# (CLAUDE_CODE_PLUGIN_CACHE_DIR), so nothing touches this machine's own plugins.
H=${0:A:h}; NAME=$1; PROMPT=$2; TOOLS=$3; TEAM=${TEAM:?set TEAM}
R=$H/runs/$NAME; C=$(mktemp -d); C=${C:A}/nightjar
rm -rf $R; mkdir -p $R
cp -R $TEAM/teammate/nightjar $C
echo "$PROMPT" > $R/prompt.txt
# A project or local install is recorded per clone, so install once in this copy, as a teammate would.
(cd $C && CLAUDE_CODE_PLUGIN_CACHE_DIR=$TEAM/plugin-store claude plugin install nightjar-qa@nightjar-tools --scope local > $R/install.txt 2>&1)
cd $C && CLAUDE_CODE_PLUGIN_CACHE_DIR=$TEAM/plugin-store claude -p "$PROMPT" --model claude-sonnet-5-5 \
  --setting-sources project,local --strict-mcp-config ${=EXTRA} --allowedTools "$TOOLS" \
  --output-format stream-json --verbose < /dev/null > $R/transcript.jsonl 2> $R/stderr.txt
mkdir -p $R/outputs; for d in bugs bug-drafts; do [[ -d $C/$d ]] && cp -r $C/$d $R/outputs/; done
rm -rf ${C:h}
