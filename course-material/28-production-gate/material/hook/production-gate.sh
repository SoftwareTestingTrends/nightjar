#!/bin/bash
# Production changes need a named release authorization (playbook, "Hooks as approval gates").
input=$(cat)
if echo "$input" | grep -q "nightjar-prod.db"; then
  if [ -z "$RELEASE_APPROVAL" ]; then
    echo "Blocked: nightjar-prod.db is production. Only the release manager can change it." >&2
    echo "Rehearse the change on nightjar-staging.db and hand over the script and results." >&2
    exit 2   # exit 2 blocks the action; the message goes to the agent
  fi
fi
exit 0
