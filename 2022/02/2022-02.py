from __future__ import annotations

from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore


def main(input: str) -> (int | str | None):
    segments = input.strip().split("\n\n")
    lines = segments[0].split("\n")
    guide = []
    for line in lines:
        guide.append((ord(line[0]) - ord("A") + 1, ord(line[-1]) - ord("X") + 1))
    score = 0
    for x, y in guide:
        y = [[2, 0, 1], [0, 1, 2], [1, 2, 0]][x - 1][y - 1] + 1
        a = (y - x) % 3
        score += y
        score += [3, 6, 0][a]

    return score


EXPECTED = 12
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data + "\n", encoding="utf8")
    result = main(EXAMPLE_FILE.read_text(encoding="ansi"))
    assert result == EXPECTED, f"{result} != {EXPECTED}"
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
