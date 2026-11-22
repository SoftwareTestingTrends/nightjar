#!/usr/bin/env python3
"""PreToolUse hook for the file-bug skill.

Runs before every Bash command while the skill is active. For a tracker.py
create or comment command it checks the draft and blocks (exit 2) when:
- fewer than two different duplicate searches were run in the last two hours,
- a new ticket is missing its summary format or a required section,
- the draft contains an email address, a token-like string or the tracker token.
Every other command passes through untouched (exit 0).
"""

import json
import os
import re
import shlex
import sys
import time
from pathlib import Path

SECTIONS = ["Steps to reproduce", "Expected", "Actual", "Evidence", "Environment"]


def main() -> int:
    event = json.load(sys.stdin)
    command = event.get("tool_input", {}).get("command", "")
    action = re.search(r"tracker\.py\s+(create|comment)\b", command)
    if not action:
        return 0
    cwd = Path(event.get("cwd", "."))
    problems = []

    words = shlex.split(command, posix=True) if command.count("'") % 2 == 0 else command.split()
    draft = words[words.index("--draft") + 1] if "--draft" in words[:-1] else None
    text = ""
    if draft is None or not (cwd / draft).is_file():
        problems.append(f"draft file not found: {draft}")
    else:
        text = (cwd / draft).read_text()

    log = cwd / ".tracker" / "searches.jsonl"
    recent = set()
    if log.is_file():
        for line in log.read_text().splitlines():
            entry = json.loads(line)
            if time.time() - entry["time"] < 2 * 3600:
                recent.add(entry["query"].lower())
    if len(recent) < 2:
        problems.append(
            f"search for duplicates first: {len(recent)} different search(es)"
            " in the last two hours, need 2"
        )

    if text and action.group(1) == "create":
        first = text.splitlines()[0] if text.strip() else ""
        if not re.match(r"^# \[[A-Z][\w ]*\] .{10,}", first):
            problems.append("summary line must look like '# [Area] symptom when condition'")
        for section in SECTIONS:
            if not re.search(rf"^## {section}\s*$", text, re.M):
                problems.append(f"missing section: ## {section}")

    if text:
        if re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", text):
            problems.append("contains an email address")
        if re.search(r"\b[A-Za-z0-9_\-]{32,}\b", text):
            problems.append("contains a token-like string (32+ letters and digits)")
        token = os.environ.get("NJ_TRACKER_TOKEN")
        if token and token in text:
            problems.append("contains the tracker token")

    if problems:
        print("Blocked by the file-bug hook:\n- " + "\n- ".join(problems), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
