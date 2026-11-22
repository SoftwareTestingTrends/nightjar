"""Summarise one results folder and, optionally, add it to the history.

usage: python3 summary.py <results-dir> [--append history.csv] [--note "why this run"]

Prints, per configuration: mean pass rate, runs that passed every check, mean time and
mean turns, then each eval's runs that passed everything. With --append, adds one row
per configuration to the history file, so every rerun can be compared with the last.
"""
import argparse
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("results", type=Path)
ap.add_argument("--append", type=Path)
ap.add_argument("--note", default="")
args = ap.parse_args()

runs = defaultdict(list)  # config -> [(eval, grading, timing, info)]
for grading_file in sorted(args.results.glob("eval-*/*/run-*/grading.json")):
    run = grading_file.parent
    runs[run.parent.name].append((
        run.parent.parent.name,
        json.loads(grading_file.read_text()),
        json.loads((run / "timing.json").read_text()),
        json.loads((run / "run.json").read_text()) if (run / "run.json").exists() else {},
    ))

rows = []
for config in ("with_skill", "without_skill"):
    if config not in runs:
        continue
    items = runs[config]
    rates = [g["summary"]["pass_rate"] for _, g, _, _ in items]
    perfect = sum(r == 1.0 for r in rates)
    seconds = statistics.mean(t["total_duration_seconds"] for _, _, t, _ in items)
    turns = statistics.mean(t["num_turns"] for _, _, t, _ in items)
    infos = [i for _, _, _, i in items if i]
    first = infos[0] if infos else {}
    per_eval = defaultdict(lambda: [0, 0])
    for name, g, _, _ in items:
        per_eval[name][0] += g["summary"]["pass_rate"] == 1.0
        per_eval[name][1] += 1
    print(f"{config}: pass rate {statistics.mean(rates):.0%}, {perfect}/{len(items)} runs passed everything, "
          f"{seconds:.1f} s, {turns:.1f} turns  [{first.get('requested_model', '?')}, "
          f"Claude Code {first.get('claude_version', '?')}]")
    for name, (ok, total) in sorted(per_eval.items()):
        print(f"    {name}: {ok}/{total}")
    rows.append({
        "date": max((i.get("finished", "") for i in infos), default="")[:10],
        "claude_version": first.get("claude_version", ""),
        "model": first.get("requested_model", ""),
        "skill_tree": first.get("skill_tree", ""),
        "config": config,
        "pass_rate": f"{statistics.mean(rates):.2f}",
        "perfect_runs": f"{perfect}/{len(items)}",
        "mean_seconds": f"{seconds:.1f}",
        "mean_turns": f"{turns:.1f}",
        "per_eval": " ".join(f"{n.split('-')[1]}:{ok}/{total}" for n, (ok, total) in sorted(per_eval.items())),
        "note": args.note,
    })

if args.append and rows:
    new = not args.append.exists()
    with args.append.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        if new:
            writer.writeheader()
        writer.writerows(rows)
    print(f"added {len(rows)} rows to {args.append}")
