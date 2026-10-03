"""PreToolUse hook: while NIGHTJAR_LOCK_TESTS=1, agents may not edit files under tests/.

Claude Code runs this before every Edit or Write. Exit code 2 blocks the edit, and
whatever we print to stderr is sent back to the agent as the reason.
"""

import json
import os
import sys

if os.environ.get("NIGHTJAR_LOCK_TESTS") != "1":
    sys.exit(0)  # tests are unlocked: normal work, including writing new tests

call = json.load(sys.stdin)
path = call.get("tool_input", {}).get("file_path", "")
relative = os.path.relpath(path, call.get("cwd", os.getcwd()))

if relative == "tests" or relative.startswith("tests" + os.sep):
    print(
        f"Blocked: {relative} is locked while tests are locked (NIGHTJAR_LOCK_TESTS=1). "
        "Fix the code, not the test. If the requirement really changed, a person updates the test.",
        file=sys.stderr,
    )
    sys.exit(2)
