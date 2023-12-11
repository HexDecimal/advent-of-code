from __future__ import annotations

import itertools
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import numpy as np
from aoc import as_ord_array
from numpy.typing import NDArray


def expand(galaxies: NDArray[np.int32]) -> NDArray[np.int32]:
    repeats_i = []
    repeats_j = []
    for i in range(galaxies.shape[0]):
        repeats_i.append(1 if galaxies[i, :].any() else 2)
    for i in range(galaxies.shape[1]):
        repeats_j.append(1 if galaxies[:, i].any() else 2)
    galaxies = np.repeat(galaxies, repeats=repeats_i, axis=0)
    return np.repeat(galaxies, repeats=repeats_j, axis=1)


def total_pairs(galaxies: NDArray[np.int32]) -> int:
    total = 0
    for a, b in itertools.combinations(np.argwhere(galaxies).tolist(), 2):
        total += abs(a[0] - b[0]) + abs(a[1] - b[1])
    return total


def main(input: str) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    galaxies = as_ord_array(segments[0]) == ord("#")
    galaxies = expand(galaxies)
    return total_pairs(galaxies)


EXPECTED = 374
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
