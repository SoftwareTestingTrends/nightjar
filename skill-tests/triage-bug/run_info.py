"""Write run.json next to a run's grading.json: what was asked for and what actually ran.

usage: python3 run_info.py <run-dir> <requested-model> <claude-version> <app-commit> <skill-tree>
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

run_dir, model, claude_version, app_commit, skill_tree = sys.argv[1:6]
used = {}
for line in (Path(run_dir) / "transcript.jsonl").read_text().splitlines():
    event = json.loads(line)
    if event.get("type") == "result":
        used = event.get("modelUsage", {})
(Path(run_dir) / "run.json").write_text(json.dumps({
    "requested_model": model,
    "models_used": sorted(used),
    "claude_version": claude_version.split()[0],
    "app_commit": app_commit,
    "skill_tree": skill_tree,
    "finished": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
}, indent=2))
