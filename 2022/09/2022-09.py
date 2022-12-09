from __future__ import annotations

from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import math


def main(input: str) -> (int | str | None):
    segments = input.rstrip("\n").split("\n\n")
    knots = [(0, 0)] * 10
    lines = segments[0].split("\n")
    tails = {(0, 0)}
    for line in lines:
        d, dist_ = line.split()
        dx, dy = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}[d]
        for _ in range(int(dist_)):
            knots[0] = knots[0][0] + dx, knots[0][1] + dy
            for i in range(len(knots) - 1):
                while 1:
                    x_diff = knots[i][0] - knots[i + 1][0]
                    y_diff = knots[i][1] - knots[i + 1][1]
                    if abs(x_diff) <= 1 and abs(y_diff) <= 1:
                        break

                    mov_x = int(math.copysign(min(1, abs(x_diff)), x_diff))
                    mov_y = int(math.copysign(min(1, abs(y_diff)), y_diff))
                    knots[i + 1] = knots[i + 1][0] + mov_x, knots[i + 1][1] + mov_y
                    if i == 8:
                        tails.add(knots[i + 1])

    return len(tails)


EXPECTED = 36
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
