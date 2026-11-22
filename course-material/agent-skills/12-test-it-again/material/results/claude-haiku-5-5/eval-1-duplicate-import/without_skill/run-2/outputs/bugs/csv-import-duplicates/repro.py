"""Repro: importing the same diary CSV twice stores every night twice.

Uses a throwaway SQLite database. Runs the same calls as POST /import
(parse_csv, then Diary.add_nights) twice with one CSV.

Exit 0: the second import leaves the diary with the same nights (fixed).
Exit 1: the second import added duplicate rows (bug present).
"""

import sys
import tempfile
from pathlib import Path

from nightjar.diary import Diary, parse_csv

CSV_TEXT = (
    "bedtime,wake_time,timezone,notes\n"
    "2026-03-01T23:00:00-05:00,2026-03-02T07:00:00-05:00,America/Toronto,\n"
    "2026-03-02T23:30:00-05:00,2026-03-03T07:15:00-05:00,America/Toronto,slept well\n"
)


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        diary = Diary(Path(tmp) / "repro.db")
        diary.add_nights(parse_csv(CSV_TEXT))
        first = len(diary.nights())
        diary.add_nights(parse_csv(CSV_TEXT))
        second = len(diary.nights())

    if second == first:
        print(f"OK: importing twice left {second} nights (no duplicates)")
        return 0
    print(f"BUG: first import stored {first} nights, second import brought the total to {second}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
