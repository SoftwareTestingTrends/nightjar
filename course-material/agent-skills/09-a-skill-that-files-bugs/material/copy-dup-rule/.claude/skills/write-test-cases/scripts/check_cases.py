#!/usr/bin/env python3
"""Check a test-case document against its story.

    python3 check_cases.py docs/stories/S-117.md docs/test-cases/S-117.md

Prints one line per check and exits 1 if any check FAILs, so you can fix the
document and run it again. Checks:
  - every criterion in the story (AC1.., Edge, Non-functional) has its own section with cases
  - no criterion has more than 5 cases, unless its section has a line "More than 5: <reason>"
  - case IDs are TC-<story number>-1, -2, ... with no repeats or gaps
  - every case row has a non-empty expected result
  - the "Open questions" table has Proposed answer and Who decides columns, filled in every row
  - the document holds no test code (python code blocks, def test_, import pytest, assert)
"""
import re
import sys

LIMIT = 5


def criteria(story_text):
    found = re.findall(r"^\s*-\s*\*\*(AC\d+|Edge|Non-functional)\*\*", story_text, re.M)
    return list(dict.fromkeys(found))


def key(heading):
    m = re.search(r"\b(AC\s?\d+|Edge|Non-functional)\b", heading, re.I)
    if not m:
        return None
    k = m.group(1).replace(" ", "")
    return k.upper() if k.upper().startswith("AC") else k.capitalize()


def main(story_path, doc_path):
    story, doc = open(story_path, encoding="utf-8").read(), open(doc_path, encoding="utf-8").read()
    number = re.search(r"S-(\d+)", story_path).group(1)
    results = []

    def report(ok, msg):
        results.append(ok)
        print(("PASS  " if ok else "FAIL  ") + msg)

    sections, current, reasons, ids, empty = {}, None, set(), [], []
    in_questions = False
    for line in doc.splitlines():
        h = re.match(r"#{2,4}\s+(.*)", line)
        if h:
            in_questions = "open question" in h.group(1).lower()
            current = None if in_questions else key(h.group(1))
            continue
        if current and line.strip().lower().startswith("more than 5:"):
            reasons.add(current)
        row = re.match(rf"\|\s*(TC-{number}-(\d+))\s*\|", line)
        if row and not in_questions:
            ids.append(int(row.group(2)))
            if current:
                sections.setdefault(current, []).append(row.group(1))
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not cells[-1]:
                empty.append(row.group(1))

    for c in criteria(story):
        k = c.upper() if c.upper().startswith("AC") else c.capitalize()
        n = len(sections.get(k, []))
        report(n > 0, f"{c}: {n} case(s)" + ("" if n else " (no section with cases)"))
        if n > LIMIT:
            report(k in reasons, f"{c}: more than {LIMIT} cases" + (" with a stated reason" if k in reasons else ' (merge cases, or add a line "More than 5: <reason>")'))
    expected = list(range(1, len(ids) + 1))
    report(ids == expected, f"case IDs TC-{number}-1 to -{len(ids)} in order" + ("" if ids == expected else f" (found {ids[:12]}{'...' if len(ids) > 12 else ''})"))
    report(not empty, "every case has an expected result" + (f" (empty: {', '.join(empty)})" if empty else ""))

    q = re.search(r"#+\s*Open questions(.*)", doc, re.I | re.S)
    if q:
        lines = [l for l in q.group(1).splitlines() if l.strip().startswith("|")]
        header = [c.strip().lower() for c in lines[0].strip().strip("|").split("|")] if lines else []
        has_cols = any("proposed" in c for c in header) and any("who" in c for c in header)
        report(has_cols, "open questions table has 'Proposed answer' and 'Who decides' columns")
        if has_cols:
            p, w = next(i for i, c in enumerate(header) if "proposed" in c), next(i for i, c in enumerate(header) if "who" in c)
            rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in lines[2:]]
            bad = [r[0] for r in rows if len(r) <= max(p, w) or not r[p] or not r[w]]
            report(not bad, f"all {len(rows)} open questions have a proposed answer and an owner" + (f" (missing in: {', '.join(bad)})" if bad else ""))
    else:
        report(True, "no open questions section (none needed)")
    code = re.search(r"```(python|py)\b|^\s*def test_|^\s*import pytest|^\s*assert ", doc, re.M)
    report(not code, "no test code in the document")

    fails = results.count(False)
    print(f"\n{len(results) - fails} passed, {fails} failed")
    return 1 if fails else 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2]))
