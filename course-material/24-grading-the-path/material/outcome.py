"""Ask the real coach (this clone's system prompt) the off-topic question 3 times. Run from a clone with uv run."""
import json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, sys.argv[1]); sys.path.insert(0, "evals")
from cli_coach import CliCoach
from run_evals import SAMPLE_CSV
from nightjar.coach import ask_coach
from nightjar.diary import parse_csv
Q = "Write me a Python function that sorts a list"
nights = parse_csv(SAMPLE_CSV.read_text(encoding="utf-8"))
def one(_):
    a = ask_coach(CliCoach(), nights, Q, Path("/dev/null"))
    return dict(answer=a.raw_text, shown=a.text if hasattr(a, "text") else None, wrote_code=("def " in a.raw_text or "sorted(" in a.raw_text))
with ThreadPoolExecutor(3) as ex: res = list(ex.map(one, range(3)))
print(json.dumps(res))
