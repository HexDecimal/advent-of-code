from __future__ import annotations

from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore


def main(input: str) -> (int | str | None):
    segments = input.strip().split("\n\n")

    # part 1
    bags = [(set(it[: len(it) // 2]), set(it[len(it) // 2 :])) for it in segments[0].split("\n")]
    total = 0
    for c1, c2 in bags:
        same = c1 & c2
        single = same.pop()
        total += " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".index(single)

    # part 2
    total = 0
    for group in zip(bags[::3], bags[1::3], bags[2::3]):

        same = (group[0][0] | group[0][1]) & (group[1][0] | group[1][1]) & (group[2][0] | group[2][1])
        total += " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".index(same.pop())

    return total


EXPECTED = 70
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data + "\n", encoding="utf8")
    result = main(EXAMPLE_FILE.read_text(encoding="ansi"))
    assert result == EXPECTED, f"{result} != {EXPECTED}"
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
