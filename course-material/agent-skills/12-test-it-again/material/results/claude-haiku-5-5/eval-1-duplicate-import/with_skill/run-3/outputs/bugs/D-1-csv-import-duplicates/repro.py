"""D-1: importing the same CSV twice stores every night twice.

Run from the repository root:  uv run python bugs/D-1-csv-import-duplicates/repro.py
Exit 1: defect present (the second import doubled the diary).
Exit 0: defect fixed (the diary still holds the 21 nights from the sample file).
Uses a throwaway database in a temporary directory; nightjar.db is never touched.
"""

import sys
import tempfile
from pathlib import Path

from nightjar.diary import Diary, parse_csv

SAMPLE = Path(__file__).resolve().parents[2] / "data" / "sample_nights.csv"
EXPECTED_NIGHTS = 21


def main() -> int:
    nights = parse_csv(SAMPLE.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as tmp:
        diary = Diary(Path(tmp) / "repro.db")
        diary.add_nights(nights)
        diary.add_nights(nights)  # the same file, imported a second time
        count = len(diary.nights())

    if count == EXPECTED_NIGHTS:
        print(f"OK: {count} nights after importing the same file twice")
        return 0
    print(f"BUG: {count} nights after importing the same {EXPECTED_NIGHTS}-night file twice")
    return 1


if __name__ == "__main__":
    sys.exit(main())
