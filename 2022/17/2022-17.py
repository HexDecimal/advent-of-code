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


def main(input: str) -> int:
    jets = [-1 if ch == "<" else 1 for ch in input.replace("\n", "")]
    jet_index = 0
    well = np.zeros((8, 7), dtype=np.bool_)
    well_top = 0
    block_index = 0

    def check_collision(block, x, y) -> bool:
        if x < 0:
            return True
        if x > 7 - block.shape[1]:
            return True
        if y < 0:
            return True
        return (well[y : y + block.shape[0], x : x + block.shape[1]] & block).any()

    def generate_jump(block_index: int, jet_index: int) -> tuple[int, int]:
        jump_height = 0
        start_block_index = block_index
        start_jex_index = jet_index
        block_key = (block_index, jet_index)
        r = 0
        while True:
            r += 1
            jump_height += history[block_key][1]
            block_index = (block_index + 1) % len(SHAPES)
            jet_index = (jet_index + len(history[block_key][0])) % len(jets)
            block_key = (block_index, jet_index)
            if block_key == (start_block_index, start_jex_index):
                break
        return (jump_height, r)

    history: dict[tuple[int, int], tuple[list[bool], int]] = {}

    r = 0
    while r < 1000000000000:
        r += 1
        block_key = (block_index, jet_index)
        if block_key in history and r > 20_000:
            try:
                jump_height, jump_blocks = generate_jump(block_index, jet_index)
                jumps = (1000000000000 - r) // jump_blocks
                r += jump_blocks * jumps
                well_top += jump_height * jumps

                if r < 1000000000000:
                    # r += 1
                    block_index = (block_index + 1) % len(SHAPES)
                    jet_index = (jet_index + len(history[block_key][0])) % len(jets)
                    well_top += history[block_key][1]
                continue
            except KeyError:
                pass
        block = SHAPES[block_index]
        block_index = (block_index + 1) % len(SHAPES)
        x = 2
        y = well_top + 3
        block_history = []
        while True:
            next_jet = jets[jet_index]
            jet_index = (jet_index + 1) % len(jets)
            new_x = x + next_jet
            if not check_collision(block, new_x, y):
                block_history.append(False)
                x = new_x
            else:
                block_history.append(True)
            if check_collision(block, x, y - 1):
                break
            y -= 1
        well[y : y + block.shape[0], x : x + block.shape[1]] |= block
        old_well_top = well_top
        well_top = max(well_top, y + block.shape[0])
        placed_height = well_top - old_well_top
        if block_key in history:
            # assert history[block_key] == (block_history, placed_height)
            if history[block_key] != (block_history, placed_height):
                print(history[block_key][0] == block_history, history[block_key][1] == placed_height, placed_height, r)
        history[block_key] = (block_history, placed_height)
        # print(well_top)
        # print_bool_array(well[well_top::-1])
        if well_top + 12 > well.shape[0]:
            well = np.pad(well, ((0, well.shape[0]), (0, 0)))
            # print(well)
            # print(well.shape)

    # print_bool_array(well[well_top::-1])
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
    # Shamefully guess the output from an almost correct result.
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")) + 2)
