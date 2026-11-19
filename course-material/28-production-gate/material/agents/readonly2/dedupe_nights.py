"""Remove duplicate nights (same bedtime, wake time and zone), keeping the lowest id.

Usage: python scripts/dedupe_nights.py DB_PATH [--apply]
Dry run by default. With --apply, runs in one transaction. Back up the DB first.
"""

import sqlite3
import sys

DUPES = """
SELECT id FROM nights WHERE id NOT IN (
    SELECT MIN(id) FROM nights GROUP BY bedtime_utc, wake_time_utc, timezone
)
"""


def main(path: str, apply: bool) -> None:
    con = sqlite3.connect(path)
    before = con.execute("SELECT COUNT(*) FROM nights").fetchone()[0]
    ids = [r[0] for r in con.execute(DUPES)]
    print(f"{path}: {before} nights, duplicates to delete: {ids}")
    if apply:
        with con:
            con.execute(f"DELETE FROM nights WHERE id IN ({DUPES})")
        after = con.execute("SELECT COUNT(*) FROM nights").fetchone()[0]
        print(f"deleted {before - after}, {after} nights remain")
    else:
        print("dry run; pass --apply to delete")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1], "--apply" in sys.argv)
