from __future__ import annotations

from collections import Counter
from pathlib import Path

import aocd  # type: ignore


def main(file: Path) -> (int | str | None):
    segments = file.read_text(encoding="ansi").strip().split("\n\n")

    groups: list[Counter[str]] = [
        sum((Counter(line + "!") for line in segment.splitlines()), Counter()) for segment in segments
    ]
    total = 0
    for group in groups:
        for k, v in group.items():
            if k == "!":
                continue
            if v == group["!"]:
                total += 1

    return total


EXPECTED = 11
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data + "\n", encoding="utf8")
    aocd.submit(main(INPUT_FILE))
