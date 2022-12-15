from __future__ import annotations

import functools
import itertools
import operator
import re
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import numpy as np
from aoc import as_array, as_bool_array, as_ord_array, ints, reduce_multiply, split_ints
from numpy.typing import NDArray
from parse import parse


def main(input: str, check_y: int) -> (int | str | None):
    max_xy = check_y * 2
    segments = input.rstrip("\n").split("\n\n")
    lines = segments[0].split("\n")
    # Part 1
    # no_beacon = set()
    # beacons = set()
    # for line in lines:
    #    x, y, cx, cy = ints(line)
    #    beacons.add((cx, cy))
    #    range_ = abs(x - cx) + abs(y - cy)
    #    check_range = range_ - abs(y - check_y)
    #    print(range_, check_range)
    #    if check_range >= 0:
    #        for check_x in range(x - check_range, x + check_range + 1):
    #            no_beacon.add((check_x, check_y))

    # no_beacon -= beacons
    # return len(no_beacon)

    sensors = [ints(line) for line in lines]

    for search_y in range(max_xy):
        ranges = []
        for x, y, cx, cy in sensors:

            range_ = abs(x - cx) + abs(y - cy)
            check_range = range_ - abs(y - search_y)
            if check_range >= 0:
                ranges.append((x - check_range, x + check_range + 1))
        ranges.sort()
        if not ranges:
            continue
        search_x = ranges[0][0]
        while search_x < max_xy and ranges:
            if search_x < ranges[0][0]:
                print(search_x, search_y)
                return search_x * 4000000 + search_y
            search_x = max(search_x, ranges[0][1])
            ranges.pop(0)
        if search_y % 1000 == 0:
            print(search_y)


EXPECTED = 56000011
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.input"
    INPUT_FILE = THIS_DIR / "input.input"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data, encoding="utf8")
    result = main(EXAMPLE_FILE.read_text(encoding="ansi"), 10)
    if result != EXPECTED:
        print(f"Expected {EXPECTED!r} but got {result!r} instead!")
        raise SystemExit()
    else:
        print("Example passed.")
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi"), 2000000))
