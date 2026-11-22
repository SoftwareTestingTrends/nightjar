#!/bin/zsh
# Self-test for the file-bug hook. From the repository root:
#   zsh plugins/nightjar-qa/skills/file-bug/scripts/test_check_filing.sh
# Prints each case and the hook's exit code (2 = blocked, 0 = allowed).
HOOK=${1:-plugins/nightjar-qa/skills/file-bug/scripts/check_filing.py}; HOOK=${HOOK:A}
T=$(mktemp -d); cd $T; mkdir -p bug-drafts .tracker
cat > bug-drafts/good.md <<'D'
# [Diary] Bedtime in the skipped spring hour is saved an hour later

## Steps to reproduce
1. Log bed 2026-03-08 02:30
## Expected
Not specified
## Actual
Shown as 03:30
## Evidence
x
## Environment
local
## Notes
Reproduced 2 of 2 times.
D
sed 's/## Expected/## Expectation/' bug-drafts/good.md > bug-drafts/nosection.md
sed 's/^local$/local, reported by sam@example.com/' bug-drafts/good.md > bug-drafts/email.md
run(){ printf '{"cwd":"%s","tool_input":{"command":"%s"}}' "$T" "$2" | python3 $HOOK 2>&1 | sed 's/^/    /'; echo "  exit ${pipestatus[2]}  $1"; }
run "no searches yet: should block"            "python3 tools/tracker/tracker.py create --draft bug-drafts/good.md"
for q in "daylight saving" "bedtime spring"; do echo "{\"time\": $(date +%s), \"query\": \"$q\", \"hits\": 0}" >> .tracker/searches.jsonl; done
run "two searches, good draft: should pass"    "python3 tools/tracker/tracker.py create --draft bug-drafts/good.md"
run "missing Expected section: should block"   "python3 tools/tracker/tracker.py create --draft bug-drafts/nosection.md"
run "email address in draft: should block"     "python3 tools/tracker/tracker.py create --draft bug-drafts/email.md"
run "draft file missing: should block"         "python3 tools/tracker/tracker.py create --draft bug-drafts/missing.md"
run "a search: should pass untouched"          "python3 tools/tracker/tracker.py search import csv"
run "another command: should pass untouched"   "make test"
rm -rf $T
