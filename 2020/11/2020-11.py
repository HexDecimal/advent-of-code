from __future__ import annotations

import functools
import itertools
from collections import Counter
from pathlib import Path

import aocd  # type: ignore
import numpy as np
from numpy.typing import NDArray
from scipy.signal import convolve2d


def parse_bool_array(segment: str) -> NDArray[np.bool_]:
    return np.asarray([[ch == "L" for ch in row] for row in segment.splitlines()], np.bool_)


ADJACENT = [
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1],
]


def part1(file: Path) -> (int | str | None):
    segments = file.read_text(encoding="ansi").strip().split("\n\n")
    seats = parse_bool_array(segments[0])
    occupied = np.zeros_like(seats, np.bool_)

    while True:
        neighbors = convolve2d(occupied, ADJACENT, "same")
        new_occupied = occupied | ((neighbors == 0) & seats)
        new_occupied &= ~(neighbors >= 4)
        print(new_occupied.sum())
        if (new_occupied == occupied).all():
            return new_occupied.sum()
        occupied = new_occupied


def find_seat(seats: NDArray[np.bool_], ij: tuple[int, int], dir: tuple[int, int], default: int) -> int:
    i, j = ij
    dir_i, dir_j = dir
    while True:
        i += dir_i
        j += dir_j
        if not (0 <= i < seats.shape[0] and 0 <= j < seats.shape[1]):
            return default
        if not seats[i, j]:
            continue
        return i * seats.shape[1] + j


def main(file: Path) -> (int | str | None):
    segments = file.read_text(encoding="ansi").strip().split("\n\n")
    seats = parse_bool_array(segments[0])
    for i, seat in enumerate(seats.ravel()):
        if not seat:
            null_seat = i  # Find a non-seat to use as a null seat index.
            break

    seat_visibility = np.full(seats.shape + (8,), null_seat)
    for seat_i, seat_j in np.argwhere(seats):
        for i, dir in enumerate(((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))):
            seat_visibility[seat_i, seat_j, i] = find_seat(seats, (seat_i, seat_j), dir, null_seat)

    occupied = np.zeros_like(seats, np.bool_)

    while True:
        neighbors = occupied.ravel()[seat_visibility].sum(axis=2)
        new_occupied = occupied | ((neighbors == 0) & seats)
        new_occupied &= ~(neighbors >= 5)
        print(new_occupied.sum())
        if (new_occupied == occupied).all():
            return new_occupied.sum()
        occupied = new_occupied


EXPECTED = 26
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data + "\n", encoding="utf8")
    if main(EXAMPLE_FILE) == EXPECTED:
        aocd.submit(main(INPUT_FILE))
