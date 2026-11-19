"""Remove duplicate nights (same bedtime_utc, wake_time_utc, timezone), keeping the lowest id.

Usage: dedupe_nights.py DB [--apply]
Dry run by default. With --apply it first writes a backup next to the DB.
Pairs whose notes differ are NOT deleted; they are listed for a human to resolve.
"""

import sqlite3
import sys

GROUPS_SQL = (
    "SELECT group_concat(id) FROM nights "
    "GROUP BY bedtime_utc, wake_time_utc, timezone HAVING count(*) > 1"
)


def main(path: str, apply: bool) -> None:
    db = sqlite3.connect(path)
    to_delete, conflicts = [], []
    groups = db.execute(GROUPS_SQL).fetchall()
    for (ids,) in groups:
        ids = sorted(int(i) for i in ids.split(","))
        notes = set()
        for i in ids:
            notes.add(db.execute("SELECT notes FROM nights WHERE id=?", (i,)).fetchone()[0])
        if len(notes - {""}) > 1:
            conflicts.append(ids)
        else:
            to_delete += ids[1:]
    print(f"{path}: {len(groups)} duplicate groups, {len(to_delete)} rows to delete")
    for ids in conflicts:
        print(f"  SKIPPED (notes differ, needs a human): ids {ids}")
    if not apply:
        print("dry run; pass --apply to delete")
        return
    backup = sqlite3.connect(path + ".bak-before-dedupe")
    db.backup(backup)
    backup.close()
    db.executemany("DELETE FROM nights WHERE id=?", [(i,) for i in to_delete])
    db.commit()
    print("remaining rows:", db.execute("SELECT count(*) FROM nights").fetchone()[0])


if __name__ == "__main__":
    main(sys.argv[1], "--apply" in sys.argv)
