from __future__ import annotations

import itertools
import re
from pathlib import Path
from typing import Iterator, NamedTuple


class BBox(NamedTuple):
    left: int
    right: int
    bottom: int
    top: int


def in_bounds(xy: tuple[int, int], bounds: BBox) -> bool:
    return bounds[0] <= xy[0] <= bounds[1] and bounds.bottom <= xy[1] <= bounds.top


def simuate_x(bounds: BBox) -> Iterator[int]:
    for i in itertools.chain(range(bounds.left - 1, 0), range(0, bounds.right + 1)):
        x = 0
        x_speed = i
        while True:
            x += x_speed
            x_speed -= 1 if x_speed > 0 else -1
            if bounds.left <= x <= bounds.right:
                yield i
                break
            if x_speed == 0:
                break


def trace_xy(speed: tuple[int, int]) -> Iterator[tuple[int, int]]:
    x = 0
    y = 0
    x_speed, y_speed = speed
    while True:
        x += x_speed
        y += y_speed
        yield x, y
        if x_speed:
            x_speed -= 1 if x_speed > 0 else -1
        y_speed -= 1


def simulate_xy(bounds: BBox, x_speed: int) -> Iterator[bool]:
    for i in range(bounds.bottom, -bounds.bottom + 1)[::-1]:
        max_y = 0
        for x, y in trace_xy((x_speed, i)):
            max_y = max(max_y, y)
            if abs(x) > max(abs(bounds.left), abs(bounds.right)):
                break
            if y < bounds.bottom:
                break
            if in_bounds((x, y), bounds):
                yield True
                break
    return None


def main(file: Path) -> (int | str):
    with open(file, "r", encoding="utf8") as f:
        match = re.match("target area: x=([0-9-]+)..([0-9-]+), y=([0-9-]+)..([0-9-]+)", f.read().strip())
    assert match
    bounds = BBox(*(int(g) for g in match.groups()))
    print(bounds)

    print(list(simuate_x(bounds)))
    count = 0
    for x_speed in simuate_x(bounds):
        count += len(list(simulate_xy(bounds, x_speed)))
    print(count)
    return count


EXPECTED = 112
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if main(EXAMPLE_FILE) == EXPECTED:
        main(INPUT_FILE)
