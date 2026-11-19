"""Merge-time gate checks for a NightJar working copy, against main.
   python3 gate_check.py <repo>
Each check prints PASS, BLOCK or NEEDS (a named owner must approve). Exit 1 on BLOCK."""
import re, subprocess, sys, glob, time
from pathlib import Path
R = Path(sys.argv[1])
def sh(cmd):
    t = time.time(); p = subprocess.run(cmd, cwd=R, shell=True, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr, time.time() - t
changed = set(sh("git diff --name-only main; git ls-files --others --exclude-standard")[1].split())
out = []
def report(status, gate, check, owner, detail="", secs=None):
    out.append(status); s = f" ({secs:.1f}s)" if secs is not None else ""
    print(f"{status:6} {gate:13} {check:42} owner: {owner}{s}" + (f"\n         {detail}" if detail else ""))
code, log, t = sh("make test"); report("PASS" if code == 0 else "BLOCK", "merge", "make test", "code owner", "" if code == 0 else log.strip().splitlines()[-1], t)
code, log, t = sh("make lint"); report("PASS" if code == 0 else "BLOCK", "merge", "make lint", "code owner", "" if code == 0 else log.strip().splitlines()[-1], t)
# Traceability: every T- test is listed; every AC row has a test; every eval id is inside the documented range.
trace = (R / "docs/traceability.md").read_text()
tests = re.findall(r"def (test_T_(\d+)_(\d+)_\w+)", "".join(Path(f).read_text() for f in glob.glob(f"{R}/tests/**/*.py", recursive=True)))
listed = set(re.findall(r"T-(\d+)-(\d+)", trace))
unlisted = sorted({f"T-{a}-{b}" for _, a, b in tests if (a, b) not in listed})
untested = sorted({f"T-{a}-{b}" for a, b in listed if not any((a, b) == (x, y) for _, x, y in tests)})
rng = re.search(r"E-01\.\.E-(\d+)", trace); top = int(rng.group(1)) if rng else 0
evals = sorted(re.findall(r"^id: E-(\d+)", "".join(Path(f).read_text() for f in glob.glob(f"{R}/evals/cases/*.yaml")), re.M))
undocumented = [f"E-{e}" for e in evals if int(e) > top]
problems = ([f"tests not in traceability.md: {unlisted}"] if unlisted else []) + ([f"ACs with no test: {untested}"] if untested else []) + ([f"eval cases outside E-01..E-{top:02d}: {undocumented}"] if undocumented else [])
report("BLOCK" if problems else "PASS", "merge", "traceability check", "code owner", "; ".join(problems))
# Claims: the register is Regulatory & Brand's; a machine can only notice the change.
if "claims/register.yaml" in changed:
    diff = sh("git diff main -- claims/register.yaml")[1]
    removed = [l[1:].strip() for l in diff.splitlines() if l.startswith("-") and not l.startswith("---")]
    report("NEEDS", "claims", "claims/register.yaml changed", "Regulatory & Brand", "removed lines: " + " | ".join(removed[:4]))
else:
    report("PASS", "claims", "claims/register.yaml unchanged", "Regulatory & Brand")
# Coach config: hand over to the real-model eval gate from the regression-testing lesson.
coach = sorted(f for f in changed if re.match(r"src/nightjar/coach/(prompts/|claude\.py)|evals/", f))
report("NEEDS" if coach else "PASS", "coach config", "real-model eval gate", "coach owner", ("touches " + ", ".join(coach)) if coach else "")
print("RESULT:", "BLOCKED" if "BLOCK" in out else ("WAITING FOR OWNERS" if "NEEDS" in out else "READY FOR REVIEW"))
sys.exit(1 if "BLOCK" in out else 0)
