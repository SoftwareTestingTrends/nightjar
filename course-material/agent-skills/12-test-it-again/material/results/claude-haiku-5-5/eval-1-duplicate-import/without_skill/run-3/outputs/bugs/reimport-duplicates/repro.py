"""NJ-12: importing the same CSV twice stores every night twice.

Run from the repository root:  uv run python bugs/reimport-duplicates/repro.py
Exits 1 while the bug is present, 0 once re-importing leaves the diary unchanged.
"""

import sys
import tempfile
from pathlib import Path

from nightjar.diary import Diary, parse_csv

SAMPLE = Path("data/sample_nights.csv")


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        diary = Diary(Path(tmp) / "repro.db")
        nights = parse_csv(SAMPLE.read_text(encoding="utf-8-sig"))

        diary.add_nights(nights)
        first = len(diary.nights())
        diary.add_nights(nights)
        second = len(diary.nights())

    if second != first:
        print(f"BUG: first import gave {first} nights, re-import left {second}")
        return 1
    print(f"OK: re-import left the diary at {second} nights")
    return 0


if __name__ == "__main__":
    sys.exit(main())
