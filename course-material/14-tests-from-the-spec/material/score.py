"""Score agent-written test files the way the misguidance paper does.

misguided = passes on the buggy code, fails on the fixed code
bug-finding (effective) = fails on the buggy code, passes on the fixed code
"""
import shutil, subprocess, sys, xml.etree.ElementTree as ET
from pathlib import Path
S = Path(__file__).resolve().parent
BASE = S / "score-base"
if not BASE.exists():
    subprocess.run(["git", "clone", "-q", str(Path.home() / "ai-projects/nightjar"), str(BASE)], check=True)

def run(test_file: Path, nudge: Path) -> dict:
    shutil.copy(nudge, BASE / "src/nightjar/nudge.py")
    shutil.copy(test_file, BASE / "tests/test_nudge_dst_quiet.py")
    xml = S / "junit.xml"
    subprocess.run(["uv", "run", "pytest", "-q", "-p", "no:cacheprovider", "tests/test_nudge_dst_quiet.py", f"--junitxml={xml}"],
                   cwd=BASE, capture_output=True, text=True)
    res = {}
    for tc in ET.parse(xml).getroot().iter("testcase"):
        failed = any(c.tag in ("failure", "error") for c in tc)
        res[tc.get("name")] = not failed
    return res

for kind in sys.argv[1:]:
    f = S / f"nj-{kind}" / "tests" / "test_nudge_dst_quiet.py"
    if not f.exists():
        print(kind, "no test file"); continue
    bug, fix = run(f, S / "nudge_buggy.py"), run(f, S / "nudge_fixed.py")
    names = sorted(set(bug) | set(fix))
    mis = [n for n in names if bug.get(n) and not fix.get(n)]
    eff = [n for n in names if not bug.get(n) and fix.get(n)]
    both_fail = [n for n in names if not bug.get(n) and not fix.get(n)]
    print(f"{kind}: {len(names)} tests | misguided {len(mis)} | bug-finding {len(eff)} | fail on both {len(both_fail)}")
    for n in mis: print("   MISGUIDED", n)
    for n in eff: print("   FINDS BUG", n)
    for n in both_fail: print("   FAILS BOTH", n)
shutil.copy(S / "nudge_buggy.py", BASE / "src/nightjar/nudge.py")
