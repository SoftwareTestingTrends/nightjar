"""Summarise each run's path: reads, edits, checks (with results), in order."""
import sys, re
sys.path.insert(0, ".")
from steps import steps
def short(p): return re.sub(r".*/l24/[a-z0-9]+/", "", p)
def path(run):
    out = []
    for s in steps(f"run-{run}.jsonl"):
        t = s["tool"]
        if t == "REPORT": out.append(("report", "", s.get("secs"))); continue
        if t in ("Edit", "Write"): out.append(("edit" if not s["error"] else "edit-denied", short(s["arg"]), ""))
        elif t == "Read": out.append(("read", short(s["arg"]), ""))
        elif t == "Bash":
            cmd = s["arg"]
            checks = re.findall(r"make (test|lint|evals|format)", cmd)
            writes = bool(re.search(r"python3 - <<|cat > |sed -i", cmd))
            if s["error"]:
                out.append(("denied", ("writes files: " if writes else "") + ("+".join(checks) if checks else cmd.split("\n")[0][:50]), ""))
            elif checks:
                res = " / ".join(re.findall(r"(\d+ passed[^=]*?)(?: in [\d.]+s)?\s*=|All checks passed!|Found \d+ error|\d+/\d+ cases at or above|would reformat", s["result"]))
                out.append(("check", "+".join(checks), res))
            else:
                out.append(("look", cmd.split("\n")[0][:60], ""))
    return out
if __name__ == "__main__":
    for run in sys.argv[1:]:
        print("=====", run)
        for k, a, r in path(run): print(f"  {k:12} {a}  {r if r else ''}")
