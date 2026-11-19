"""Merge-time gate checks for a NightJar working copy, against a base branch.
   python3 gate_check.py <repo> [base]   (base defaults to main)
v2 (capstone): the claims gate now covers user-facing copy as gates.md says, not only
the register. Text added to templates or the nudge copy is run through check_text
(a violation blocks), and any copy change waits for Regulatory & Brand.
Each check prints PASS, BLOCK or NEEDS (a named owner must approve). Exit 1 on BLOCK."""
import re, subprocess, sys, glob, time
from pathlib import Path
R = Path(sys.argv[1]); BASE = sys.argv[2] if len(sys.argv) > 2 else "main"
def sh(cmd):
    t = time.time(); p = subprocess.run(cmd, cwd=R, shell=True, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr, time.time() - t
changed = set(sh(f"git diff --name-only {BASE}; git ls-files --others --exclude-standard")[1].split())
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
# Claims: the register and all user-facing copy are Regulatory & Brand's. A machine can
# run new text through check_text and notice the change; only the owner can approve it.
copy_files = sorted(f for f in changed if f == "claims/register.yaml" or f.startswith("src/nightjar/templates/"))
if copy_files:
    diff = sh(f"git diff {BASE} -- " + " ".join(copy_files))[1]
    added = [l[1:] for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++")]
    text = [re.sub(r"\s+", " ", re.sub(r"\{[{%#].*?[}%#]\}|<[^>]*>", " ", l)).strip() for l in added]
    text = [t for t in text if re.search(r"[A-Za-z]{3}", t) and not t.startswith(("#", "- id:", "pattern:", "reason:"))]
    code, out_text, _ = sh("uv run python -c \"import sys, json; from nightjar.claims import check_text; "
                           "print(json.dumps([[v.rule for v in check_text(t)] for t in json.load(sys.stdin)]))\" <<'JSON'\n"
                           + __import__("json").dumps(text) + "\nJSON")
    hits = [f"{t!r}: {v}" for t, v in zip(text, __import__("json").loads(out_text.strip().splitlines()[-1])) if v] if code == 0 else [out_text.strip()[-200:]]
    report("BLOCK" if hits else "PASS", "claims", "new copy passes check_text", "Regulatory & Brand", "; ".join(hits))
    report("NEEDS", "claims", "user-facing copy changed", "Regulatory & Brand",
           f"{', '.join(copy_files)}; new text: " + " | ".join(text[:6]))
else:
    report("PASS", "claims", "no user-facing copy changed", "Regulatory & Brand")
# Coach config: hand over to the real-model eval gate from the regression-testing lesson.
coach = sorted(f for f in changed if re.match(r"src/nightjar/coach/(prompts/|claude\.py)|evals/", f))
report("NEEDS" if coach else "PASS", "coach config", "real-model eval gate", "coach owner", ("touches " + ", ".join(coach)) if coach else "")
print("RESULT:", "BLOCKED" if "BLOCK" in out else ("WAITING FOR OWNERS" if "NEEDS" in out else "READY FOR REVIEW"))
sys.exit(1 if "BLOCK" in out else 0)
