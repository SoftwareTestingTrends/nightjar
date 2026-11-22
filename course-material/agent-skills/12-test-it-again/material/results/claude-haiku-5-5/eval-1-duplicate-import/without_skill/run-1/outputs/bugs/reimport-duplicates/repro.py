"""Repro: importing the same CSV twice stores every night twice.

Run from the repository root:  uv run python bugs/reimport-duplicates/repro.py
Exits 1 while the bug is present, 0 once re-importing the same file adds no rows.
"""

import sys
import tempfile
from pathlib import Path

from nightjar.diary import Diary, parse_csv

ROOT = Path(__file__).resolve().parents[2]
SAMPLE_CSV = ROOT / "data" / "sample_nights.csv"


def main() -> int:
    text = SAMPLE_CSV.read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as tmp:
        diary = Diary(Path(tmp) / "repro.db")  # empty, throwaway database
        diary.add_nights(parse_csv(text))
        after_first = len(diary.nights())
        diary.add_nights(parse_csv(text))  # the same file again
        after_second = len(diary.nights())

    if after_second != after_first:
        print(f"BUG: after importing twice there are {after_second} nights, not {after_first}")
        return 1
    print(f"OK: re-importing the same file leaves {after_second} nights")
    return 0


if __name__ == "__main__":
    sys.exit(main())
