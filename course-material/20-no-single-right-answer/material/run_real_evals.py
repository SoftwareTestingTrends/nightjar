import sys
sys.path.insert(0, sys.argv[1])
from cli_coach import CliCoach
import nightjar.coach as nc
sys.path.insert(0, "evals")
import run_evals
run_evals.get_coach = lambda: CliCoach()
sys.argv = ["run_evals.py", "--runs", "3"]
raise SystemExit(run_evals.main())
