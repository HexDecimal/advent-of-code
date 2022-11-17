from __future__ import annotations

from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import numpy as np
import scipy.signal

ADJ = np.ones((3, 3, 3), np.int8)
ADJ[1, 1, 1] = 0


def part1(input: str) -> (int | str | None):
    segments = input.strip().split("\n\n")
    cubes = np.array([[[c == "#" for c in line] for line in segments[0].splitlines()]], np.bool_)

    for i in range(6):
        neighbors = scipy.signal.convolve(cubes, ADJ, method="fft")
        new_active = (neighbors == 2) | (neighbors == 3)
        new_inactive = neighbors == 3
        cubes = np.pad(cubes, ((1, 1), (1, 1), (1, 1)))
        cubes = np.where(cubes, new_active, new_inactive)
        print(cubes.sum())

    return cubes.sum()


ADJ4 = np.ones((3, 3, 3, 3), np.int8)
ADJ4[1, 1, 1, 1] = 0


def main(input: str) -> (int | str | None):
    segments = input.strip().split("\n\n")
    cubes = np.array([[[[c == "#" for c in line] for line in segments[0].splitlines()]]], np.bool_)

    for i in range(6):
        neighbors = scipy.signal.convolve(cubes, ADJ4, method="fft")
        new_active = (neighbors == 2) | (neighbors == 3)
        new_inactive = neighbors == 3
        cubes = np.pad(cubes, ((1, 1), (1, 1), (1, 1), (1, 1)))
        cubes = np.where(cubes, new_active, new_inactive)
        print(cubes.sum())

    return cubes.sum()


EXPECTED = 848
if __name__ == "__main__":
    np.seterr("raise")
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data + "\n", encoding="utf8")
    result = main(EXAMPLE_FILE.read_text(encoding="ansi"))
    assert result == EXPECTED, f"{result} != {EXPECTED}"
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
