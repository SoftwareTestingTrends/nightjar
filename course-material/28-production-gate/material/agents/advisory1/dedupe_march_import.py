"""Remove duplicate nights created by the March import.

Duplicates share bedtime_utc, wake_time_utc and timezone. The lowest id is kept;
a differing non-empty note on a removed row is appended to the kept row so no
journal text is lost. Dry run by default; pass --apply to write.

    uv run python scripts/dedupe_march_import.py nightjar-staging.db [--apply]
"""

import sqlite3
import sys


def main(path: str, apply: bool) -> None:
    con = sqlite3.connect(path)
    groups = con.execute(
        "SELECT group_concat(id) FROM nights "
        "GROUP BY bedtime_utc, wake_time_utc, timezone HAVING count(*) > 1"
    ).fetchall()
    removed = 0
    for (ids,) in groups:
        keep, *dupes = sorted(int(i) for i in ids.split(","))
        (notes,) = con.execute("SELECT notes FROM nights WHERE id=?", (keep,)).fetchone()
        for d in dupes:
            (dn,) = con.execute("SELECT notes FROM nights WHERE id=?", (d,)).fetchone()
            if dn.strip() and dn.strip() not in notes:
                notes = f"{notes}\n{dn}".strip()
                print(f"merge note of {d} into {keep}")
            print(f"delete {d} (keeping {keep})")
            con.execute("DELETE FROM nights WHERE id=?", (d,))
            removed += 1
        con.execute("UPDATE nights SET notes=? WHERE id=?", (notes, keep))
    if apply:
        con.commit()
    else:
        con.rollback()
    print(f"{'removed' if apply else 'would remove'} {removed} rows")


if __name__ == "__main__":
    main(sys.argv[1], "--apply" in sys.argv)
