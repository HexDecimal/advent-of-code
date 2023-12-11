from __future__ import annotations

import itertools
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import numpy as np
from aoc import as_ord_array
from numpy.typing import NDArray


def total_pairs(galaxies: NDArray[np.int32], void_size: int) -> int:
    dist_i = []
    dist_j = []
    for i in range(galaxies.shape[0]):
        dist_i.append(1 if galaxies[i, :].any() else void_size)
    for i in range(galaxies.shape[1]):
        dist_j.append(1 if galaxies[:, i].any() else void_size)
    total = 0
    for a, b in itertools.combinations(np.argwhere(galaxies).tolist(), 2):
        i_range = slice(*sorted([a[0], b[0]]))
        j_range = slice(*sorted([a[1], b[1]]))
        total += sum(dist_i[i_range]) + sum(dist_j[j_range])
    return total


def main(input: str, void_size: int = 1000000) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    galaxies = as_ord_array(segments[0]) == ord("#")
    return total_pairs(galaxies, void_size)


EXPECTED = 8410
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.input"
    INPUT_FILE = THIS_DIR / "input.input"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data, encoding="utf8")
    result = main(EXAMPLE_FILE.read_text(encoding="ansi"), void_size=100)
    if result != EXPECTED:
        print(f"Expected {EXPECTED!r} but got {result!r} instead!")
        raise SystemExit()
    else:
        print("Example passed.")
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
