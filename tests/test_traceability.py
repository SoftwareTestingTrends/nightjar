"""Every trace id used in a test name must be listed in docs/traceability.md.

CLAUDE.md asks agents to update the table when they add a T_ test. Asking isn't
enough, so this test checks it.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRACE_ID = re.compile(r"def test_(T_\d+_\d+)")


def test_every_trace_id_in_a_test_name_is_in_the_traceability_table():
    used = set()
    for test_file in (ROOT / "tests").rglob("test_*.py"):
        used |= {m.replace("_", "-") for m in TRACE_ID.findall(test_file.read_text())}
    table = (ROOT / "docs" / "traceability.md").read_text()
    missing = sorted(trace_id for trace_id in used if trace_id not in table)
    assert not missing, f"Add these trace ids to docs/traceability.md: {missing}"
