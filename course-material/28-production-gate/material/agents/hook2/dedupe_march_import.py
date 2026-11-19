"""Remove duplicate nights created by the March import.

Duplicates share bedtime_utc, wake_time_utc and timezone. The lowest id is kept.
Groups whose notes differ are NOT touched; they are listed for a human to decide.

Usage: python scripts/dedupe_march_import.py DB_PATH [--apply]
Without --apply nothing is changed. With --apply a backup is written first.
"""

import shutil
import sqlite3
import sys

KEY = "bedtime_utc, wake_time_utc, timezone"


def main(path: str, apply: bool) -> None:
    con = sqlite3.connect(path)
    groups = con.execute(
        f"SELECT group_concat(id), count(DISTINCT notes) "
        f"FROM nights GROUP BY {KEY} HAVING count(*) > 1"
    ).fetchall()
    delete, conflicts = [], []
    for ids, distinct_notes in groups:
        ids = sorted(int(i) for i in ids.split(","))
        (conflicts if distinct_notes > 1 else delete).append(ids)
    to_delete = [i for ids in delete for i in ids[1:]]
    print(f"duplicate groups: {len(groups)}; rows to delete: {to_delete}")
    print(f"skipped (notes differ, needs a human): {conflicts}")
    if not apply:
        print("dry run; nothing changed")
        return
    backup = f"{path}.pre-dedupe.bak"
    shutil.copy(path, backup)
    with con:
        con.executemany("DELETE FROM nights WHERE id = ?", [(i,) for i in to_delete])
    print(f"deleted {len(to_delete)} rows; backup at {backup}")


if __name__ == "__main__":
    main(sys.argv[1], "--apply" in sys.argv)
