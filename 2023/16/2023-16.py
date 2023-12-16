from __future__ import annotations

import functools
import operator
import sys
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import numpy as np
from aoc import as_ord_array

sys.setrecursionlimit(2**30)


def main(input: str) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    contraption = as_ord_array(segments[0]).astype(np.int32)

    def test_beam(pos: tuple[int, int], dir: tuple[int, int]) -> int:
        beam = {
            (0, 1): np.zeros_like(contraption, np.bool_),
            (0, -1): np.zeros_like(contraption, np.bool_),
            (1, 0): np.zeros_like(contraption, np.bool_),
            (-1, 0): np.zeros_like(contraption, np.bool_),
        }

        def beam_travel(pos: tuple[int, int], dir: tuple[int, int]) -> None:
            if not (0 <= pos[0] < contraption.shape[0] and 0 <= pos[1] < contraption.shape[1]):
                return
            if beam[dir][pos]:
                return
            beam[dir][pos] = True
            here = contraption[pos]
            if here == ord("-") and dir[0]:
                beam_travel(pos, (0, 1))
                beam_travel(pos, (0, -1))
                return
            if here == ord("|") and dir[1]:
                beam_travel(pos, (1, 0))
                beam_travel(pos, (-1, 0))
                return
            if here == ord("/"):
                dir = {
                    (1, 0): (0, -1),
                    (-1, 0): (0, 1),
                    (0, 1): (-1, 0),
                    (0, -1): (1, 0),
                }[dir]
            if here == ord("\\"):
                dir = {
                    (1, 0): (0, 1),
                    (-1, 0): (0, -1),
                    (0, 1): (1, 0),
                    (0, -1): (-1, 0),
                }[dir]

            beam_travel((pos[0] + dir[0], pos[1] + dir[1]), dir)

        beam_travel(pos, dir)
        return functools.reduce(operator.or_, beam.values()).sum()

    def iter_starts() -> Iterator[tuple[tuple[int, int], tuple[int, int]]]:
        for i in range(contraption.shape[0]):
            yield (i, 0), (0, 1)
            yield (i, contraption.shape[0] - 1), (0, -1)
        for i in range(contraption.shape[1]):
            yield (0, i), (1, 0)
            yield (contraption.shape[1] - 1, 0), (-1, 0)

    return max(test_beam(*start) for start in iter_starts())


EXPECTED = 51
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
