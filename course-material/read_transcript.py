"""Print a recorded agent transcript (claude -p --output-format stream-json) as readable steps.

    python3 course-material/read_transcript.py \
        course-material/24-grading-the-path/material/run-quick1.jsonl

Shows each tool call the agent made, what it said along the way, any permission
denials, and the final report with its cost, time and turns.
"""

import json
import sys


def short(value, width=110):
    text = " ".join(str(value).split())
    return text if len(text) <= width else text[: width - 1] + "…"


def describe(tool):
    args = tool.get("input", {})
    for key in ("command", "file_path", "pattern", "path", "url", "description"):
        if key in args:
            return f"{tool['name']}: {short(args[key])}"
    return f"{tool['name']}: {short(json.dumps(args))}"


def main(path):
    step = 0
    for line in open(path, encoding="utf-8"):
        if not line.strip():
            continue
        event = json.loads(line)
        kind = event.get("type")
        if kind == "system" and event.get("subtype") == "init":
            print(f"model {event.get('model')} · working directory {event.get('cwd')}\n")
        elif kind == "system" and event.get("subtype") == "permission_denied":
            reason = event.get("message", "")
            print(f"      ✗ {event.get('tool_name')} denied by permissions: {short(reason, 130)}")
        elif kind == "assistant":
            for block in event["message"]["content"]:
                if block["type"] == "tool_use":
                    step += 1
                    print(f"{step:3}. {describe(block)}")
                elif block["type"] == "text" and block["text"].strip():
                    print(f"      says: {short(block['text'], 150)}")
        elif kind == "result":
            secs = event.get("duration_ms", 0) / 1000
            cost = event.get("total_cost_usd", 0)
            print(f"\n--- result: {event.get('num_turns')} turns · {secs:.0f} s · ${cost:.2f}\n")
            print(event.get("result", ""))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
