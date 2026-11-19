import sys
sys.path.insert(0, sys.argv[1])
from cli_coach import CliCoach
sys.path.insert(0, "evals")
import run_evals
run_evals.get_coach = lambda: CliCoach()
run_evals.TRACE_PATH = run_evals.ROOT / "traces" / "evals_v2_real.jsonl"
sys.argv = ["run_evals.py", "--cases", "evals/cases_v2", "--runs", "3"]
raise SystemExit(run_evals.main())
