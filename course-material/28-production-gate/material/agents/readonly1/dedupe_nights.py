"""Remove duplicate nights (same bedtime_utc, wake_time_utc, timezone) from a NightJar DB.

Keeps the lowest id of each group. If duplicates carry different non-empty notes, the
distinct notes are merged into the kept row (joined by a blank line) so no journal text
is lost.

Usage: python dedupe_nights.py DB_PATH [--apply]
Without --apply it only reports (dry run). With --apply it runs in one transaction.
Back up the database first when targeting production.
"""

import sqlite3
import sys


def main(path: str, apply: bool) -> None:
    con = sqlite3.connect(path)
    groups = con.execute(
        "SELECT bedtime_utc, wake_time_utc, timezone FROM nights "
        "GROUP BY 1, 2, 3 HAVING COUNT(*) > 1"
    ).fetchall()
    before = con.execute("SELECT COUNT(*) FROM nights").fetchone()[0]
    removed = 0
    for b, w, tz in groups:
        rows = con.execute(
            "SELECT id, notes FROM nights WHERE bedtime_utc=? AND wake_time_utc=? "
            "AND timezone=? ORDER BY id",
            (b, w, tz),
        ).fetchall()
        keep = rows[0][0]
        notes = list(dict.fromkeys(n for _, n in rows if n.strip()))
        merged = "\n\n".join(notes)
        suffix = " (notes merged)" if len(notes) > 1 else ""
        print(f"{b} {tz}: keep {keep}, drop {[r[0] for r in rows[1:]]}{suffix}")
        con.execute("UPDATE nights SET notes=? WHERE id=?", (merged, keep))
        con.execute(
            "DELETE FROM nights WHERE bedtime_utc=? AND wake_time_utc=? "
            "AND timezone=? AND id<>?",
            (b, w, tz, keep),
        )
        removed += len(rows) - 1
    after = con.execute("SELECT COUNT(*) FROM nights").fetchone()[0]
    print(f"rows {before} -> {after} ({removed} removed)")
    if apply:
        con.commit()
    else:
        con.rollback()
        print("dry run: nothing changed (use --apply)")


if __name__ == "__main__":
    main(sys.argv[1], "--apply" in sys.argv)
