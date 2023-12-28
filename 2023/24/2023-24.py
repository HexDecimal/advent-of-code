from __future__ import annotations

import functools
import itertools
import operator
import re
from math import lcm
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import numpy as np
from aoc import as_array, as_bool_array, as_ord_array, ints, reduce_multiply, split_ints
from numpy.typing import NDArray
from parse import parse  # type: ignore[import-untyped]
from sympy.geometry.line import Line3D, Ray3D
from sympy.geometry.point import Point3D
from sympy.geometry.polygon import Polygon
from tqdm import tqdm


def main(input: str, low: int, high: int) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    lines = segments[0].split("\n")
    rays: list[Ray3D] = []
    for line_ in lines:
        parsed = ints(line_)
        point1 = Point3D(parsed[:3])
        point2 = Point3D(parsed[3:])
        rays.append(Ray3D(point1, point1 + point2))

    for step_distance in itertools.count(1):
        for a, b in tqdm(list(itertools.permutations(rays, 2)), desc=f"{step_distance=}"):
            first = a.source + a.direction * (1 + step_distance)
            second = b.source + b.direction * (2 + step_distance)
            velocity = second - first
            line = Line3D(first, second)
            if any(not line.intersection(ray) for ray in rays):
                continue
            for j in itertools.count():
                new_ray = Ray3D(first - velocity * (j + 1), first - velocity * j)
                if any(not new_ray.intersection(ray) or new_ray.source == ray.p2 for ray in rays):
                    continue
                break
            test_set = set(rays)
            new_ray_score = new_ray.source.x + new_ray.source.y + new_ray.source.z
            while True:
                if any(not new_ray.intersection(ray) for ray in test_set):
                    break
                new_ray = Ray3D(new_ray.source + new_ray.direction, new_ray.source + new_ray.direction * 2)
                test_set = {
                    Ray3D(ray.source + ray.direction, ray.source + ray.direction * 2)
                    for ray in test_set
                    if ray.source + ray.direction != new_ray.source
                }
                if not test_set:
                    return new_ray_score

    return None


EXPECTED = 47
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
