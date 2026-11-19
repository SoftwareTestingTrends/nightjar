"""Hand-made mutants of sleep_window.py, scored against two test sets."""
import shutil, subprocess, sys
from pathlib import Path
REPO = Path(sys.argv[1]); SRC = REPO/"src/nightjar/sleep_window.py"
orig = SRC.read_text()
MUTANTS = {
 "M1 window 14 -> 13 nights": ("WINDOW_NIGHTS = 14", "WINDOW_NIGHTS = 13"),
 "M2 cold start < -> <=": ("if len(recent) < MIN_NIGHTS:", "if len(recent) <= MIN_NIGHTS:"),
 "M3 newest -> oldest nights": ("reverse=True", "reverse=False"),
 "M4 median -> mean": ("statistics.median(minutes)", "statistics.mean(minutes)"),
 "M5 round -> floor": ("round(statistics.median(minutes))", "int(statistics.median(minutes))"),
 "M6 local -> UTC bedtime": ("night.local_bedtime.time()", "night.bedtime.time()"),
 "M7 count from 13:00, not noon": ("NOON = 12 * 60", "NOON = 13 * 60"),
 "M8 drop the % wrap": ("return (clock_time.hour * 60 + clock_time.minute - NOON) % MINUTES_PER_DAY", "return clock_time.hour * 60 + clock_time.minute - NOON"),
}
SETS = {"existing tests": ["tests/test_sleep_window.py","tests/test_nudge.py"], "agent's new tests": ["tests/test_sleep_window_extra.py"]}
def run(files):
    r = subprocess.run(["uv","run","pytest","-q","-p","no:cacheprovider","-x",*files], cwd=REPO, capture_output=True, text=True)
    return r.returncode != 0
res = {}
for name,(a,b) in MUTANTS.items():
    assert a in orig, name
    SRC.write_text(orig.replace(a,b,1))
    res[name] = {k: run(v) for k,v in SETS.items()}
SRC.write_text(orig)
for k in SETS:
    print(f"{k}: {sum(r[k] for r in res.values())}/{len(res)} mutants killed")
for name,r in res.items():
    print(f"  {name:32s} existing={'killed' if r['existing tests'] else 'SURVIVED'}  agent={'killed' if r[chr(97)+'gent'+chr(39)+'s new tests'] else 'SURVIVED'}")
