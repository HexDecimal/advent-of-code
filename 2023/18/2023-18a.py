from __future__ import annotations

from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import numpy as np
import scipy.ndimage  # type: ignore
from parse import parse  # type: ignore[import-untyped]

DIRS = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1),
}


def main(input: str) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    lines = segments[0].split("\n")
    current_pos = (0, 0)
    dig: dict[tuple[int, int], int] = {}
    for line in lines:
        dir_: str
        dist: int
        color_: int
        dir_, dist, color_ = parse("{} {:d} (#{:x})", line)
        dx, dy = DIRS[dir_]
        for _ in range(dist):
            current_pos = current_pos[0] + dx, current_pos[1] + dy
            dig[current_pos] = color_
    min_x = min(pos[0] for pos in dig)
    min_y = min(pos[1] for pos in dig)
    dig = {(pos[0] - min_x + 1, pos[1] - min_y + 1): value for pos, value in dig.items()}
    max_x = max(pos[0] for pos in dig)
    max_y = max(pos[1] for pos in dig)
    dig_map = np.zeros((max_x + 1, max_y + 1), dtype=np.bool_)
    for pos in dig:
        dig_map[pos] = True
    labels, count = scipy.ndimage.label(~dig_map)
    for i in range(1, count + 1):
        label = labels == i
        if label[0, :].any() or label[-1, :].any() or label[:, 0].any() or label[:, -1].any():
            continue
        dig_map |= label
    return dig_map.sum()


EXPECTED = 62
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
