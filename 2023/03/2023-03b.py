from __future__ import annotations

import itertools
import re
from pathlib import Path
from typing import *  # noqa: F403

import aoc
import aocd  # type: ignore


def main(input: str) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    lines = segments[0].split("\n")
    numbers = {}
    numbers_coords = {}
    FIND_NUM = re.compile(r"\d+")
    for y, line in enumerate(lines):
        while match := FIND_NUM.search(line):
            number = int(match.group())
            number_xy = match.span()[1] - 1, y
            numbers[number_xy] = number
            line = line[: match.span()[0]] + "." * (match.span()[1] - match.span()[0]) + line[match.span()[1] :]  # noqa: PLW2901
            for x in range(*match.span()):
                numbers_coords[x, y] = number_xy

    total = 0
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == ".":
                continue
            gear_coords = set(itertools.product(range(x - 1, x + 2), range(y - 1, y + 2)))
            numbers_coords_ = {numbers_coords[coord] for coord in numbers_coords.keys() & gear_coords}
            if len(numbers_coords_) <= 1:
                continue

            total += aoc.reduce_multiply(numbers[coord] for coord in numbers_coords_)

    return total


EXPECTED = 467835
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.input"
    INPUT_FILE = THIS_DIR / "input.input"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data, encoding="utf8")
    result = main(EXAMPLE_FILE.read_text(encoding="ansi"))
    if result != EXPECTED:
        print(f"Expected {EXPECTED!r} but got {result!r} instead!")
        raise SystemExit()
    else:
        print("Example passed.")
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
