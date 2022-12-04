from __future__ import annotations

import re
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore


def main(input: str) -> (int | str | None):
    segments = input.strip().split("\n\n")
    total = 0
    lines = segments[0].split("\n")
    for line in lines:
        a, b = [
            range(int(re.match(r"(\d+)", elf)[1]), int(re.match(r".+-(\d+)", elf)[1]) + 1) for elf in line.split(",")  # type: ignore[index]
        ]
        a_ = set(a)
        b_ = set(b)
        if a_ & b_:
            print(a_, b_)
            total += 1

    return total


EXPECTED = 4
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data + "\n", encoding="utf8")
    result = main(EXAMPLE_FILE.read_text(encoding="ansi"))
    assert result == EXPECTED, f"{result} != {EXPECTED}"
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
