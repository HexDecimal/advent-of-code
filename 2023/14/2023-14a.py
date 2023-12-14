from __future__ import annotations

from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import numpy as np
from aoc import as_ord_array
from numpy.typing import NDArray


def print_array(arrays: Sequence[NDArray[Any]], legend: str) -> None:
    out = []
    for i in range(arrays[0].shape[0]):
        for j in range(arrays[0].shape[1]):
            for k, array in enumerate(arrays):
                if array[i, j]:
                    out.append(legend[k])
                    break
            else:
                out.append(legend[-1])
        out.append("\n")
    print("".join(out[:-1]))


def tilt(walls: NDArray[np.bool_], rocks: NDArray[np.bool_]) -> NDArray[np.bool_]:
    walls = walls.T
    rocks = rocks.copy().T
    for i in range(rocks.shape[0]):
        for j in range(rocks.shape[1]):
            if rocks[i, j]:
                new_j = j
                while new_j > 0 and not walls[i, new_j - 1] and not rocks[i, new_j - 1]:
                    new_j -= 1
                rocks[i, j], rocks[i, new_j] = rocks[i, new_j], rocks[i, j]
    return rocks.T


def main(input: str) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    array = as_ord_array(segments[0]).astype(np.int32)
    walls = array == ord("#")
    rocks = array == ord("O")
    print_array([rocks, walls], "O#.")
    rocks = tilt(walls, rocks)
    print_array([rocks, walls], "O#.")
    total = 0
    for i in range(1, rocks.shape[0] + 1):
        total += rocks[-i, :].sum() * i

    return total


EXPECTED = 136
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
