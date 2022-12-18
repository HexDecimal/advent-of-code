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
import tqdm

SHAPES = [
    as_bool_array(s_)[::-1, :]
    for s_ in """\
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##""".split(
        "\n\n"
    )
]


def print_bool_array(arr: NDArray) -> None:
    for row in arr:
        for v in row:
            print(".#"[v], end="")
        print()


def main(input: str) -> (int | str | None):
    jets = [-1 if ch == "<" else 1 for ch in input.replace("\n", "")]
    next_jet = itertools.cycle(jets)
    well = np.zeros((8, 7), dtype=np.bool_)
    well_top = 0
    next_block = itertools.cycle(SHAPES)

    def check_collision(block, x, y) -> bool:
        if x < 0:
            return True
        if x > 7 - block.shape[1]:
            return True
        if y < 0:
            return True
        return (well[y : y + block.shape[0], x : x + block.shape[1]] & block).any()

    for _ in tqdm.trange(1000000000000):
        block = next(next_block)
        x = 2
        y = well_top + 3
        while True:
            new_x = x + next(next_jet)
            if not check_collision(block, new_x, y):
                x = new_x
            if check_collision(block, x, y - 1):
                break
            y -= 1
        well[y : y + block.shape[0], x : x + block.shape[1]] |= block
        well_top = max(well_top, y + block.shape[0])
        # print(well_top)
        # print_bool_array(well[well_top::-1])
        if well_top + 12 > well.shape[0]:
            well = np.pad(well, ((0, well.shape[0]), (0, 0)))
            # print(well)
            # print(well.shape)

    print_bool_array(well[well_top::-1])
    return well_top


EXPECTED = 1514285714288
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
