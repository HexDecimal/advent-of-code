from __future__ import annotations

import functools
import itertools
from pathlib import Path

import aocd  # type: ignore
import numpy as np


def main(file: Path) -> (int | str | None):
    segments = file.read_text(encoding="ansi").strip().split("\n\n")
    map = np.asarray([[c == "#" for c in row] for row in segments[0].splitlines()], bool)
    map_height, map_width = map.shape
    total = 1
    for x_speed, y_speed in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)):
        y_pos = np.arange(0, map_height, y_speed)
        x_pos = np.arange(len(y_pos)) * x_speed % map_width
        total *= int(map[y_pos, x_pos].sum())
        print(total)
    return total


EXPECTED = 336
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data + "\n", encoding="utf8")
    if main(EXAMPLE_FILE) == EXPECTED:
        aocd.submit(main(INPUT_FILE))
