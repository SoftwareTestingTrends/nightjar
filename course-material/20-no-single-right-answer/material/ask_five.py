import json, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from cli_coach import CliCoach
from nightjar.coach import ask_coach
from nightjar.diary import parse_csv
nights = parse_csv(Path("data/sample_nights.csv").read_text())
q = "What's a good way to wind down tonight?"
out = []
for i in range(5):
    a = ask_coach(CliCoach(), nights, q, Path("/tmp/l19-trace.jsonl"))
    out.append({"run": i+1, "raw": a.raw_text, "shown": a.text, "violations": [v.rule for v in a.violations], "fallback": a.used_fallback})
    print(f"--- run {i+1} ({len(a.raw_text.split())} words, fallback={a.used_fallback})\n{a.raw_text}\n")
Path(sys.argv[2]).write_text(json.dumps(out, indent=1))
