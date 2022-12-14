from __future__ import annotations

import itertools
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import numpy as np
from aoc import split_ints
import tcod


def main(input: str) -> (int | str | None):
    segments = input.rstrip("\n").split("\n\n")
    walls = np.zeros((1000, 1000), dtype=np.bool_)
    sand = 0
    lines = segments[0].split("\n")
    for line in lines:
        for start, end in itertools.pairwise(split_ints(line, (" -> ", ","))):
            sx, sy = start
            ex, ey = end
            for x, y in tcod.los.bresenham((sx, sy), (ex, ey)):
                walls[y, x] = True

    inflow_ij = (0, 500)
    for y in range(1000)[::-1]:
        if walls[y].any():
            walls = walls[: y + 3]
            walls[-1] = True
            break

    def drop(y, x) -> bool:
        assert not walls[y, x]
        if y + 1 >= walls.shape[0]:
            return False
        left, down, right = walls[y + 1, x - 1 : x + 2]
        if not down:
            return drop(y + 1, x)
        if not left:
            return drop(y + 1, x - 1)
        if not right:
            return drop(y + 1, x + 1)
        walls[y, x] = True
        return True

    while not walls[inflow_ij]:
        assert drop(*inflow_ij)
        sand += 1

    return sand


EXPECTED = 93
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
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
