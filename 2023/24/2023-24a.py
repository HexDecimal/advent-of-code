from __future__ import annotations

import itertools
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
from aoc import ints
from sympy.geometry.line import Ray
from sympy.geometry.point import Point2D
from tqdm import tqdm


def main(input: str, low: int, high: int) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    lines = segments[0].split("\n")
    rays = []
    for line in lines:
        parsed = ints(line)
        point1 = Point2D(parsed[:2])
        point2 = Point2D(parsed[3:5])
        rays.append(Ray(point1, point1 + point2))
    total = 0
    for a, b in tqdm(list(itertools.combinations(rays, 2))):
        point: Point2D
        for point in a.intersection(b):
            assert isinstance(point, Point2D), point
            if low <= point.x <= high and low <= point.y <= high:
                total += 1
    return total


EXPECTED = 2
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.input"
    INPUT_FILE = THIS_DIR / "input.input"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data, encoding="utf8")
    result = main(EXAMPLE_FILE.read_text(encoding="ansi"), low=7, high=27)
    if result != EXPECTED:
        print(f"Expected {EXPECTED!r} but got {result!r} instead!")
        raise SystemExit()
    else:
        print("Example passed.")
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi"), low=200000000000000, high=400000000000000))
