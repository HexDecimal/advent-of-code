from __future__ import annotations

from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import numpy as np
from aoc import as_bool_array
import scipy.signal

N = np.array(
    [
        [1, 2, 4],
        [8, 0, 16],
        [32, 64, 128],
    ]
)[::-1, ::-1]


def main(input: str) -> (int | str | None):
    def debug_print() -> None:
        for row in elves:
            print("".join(".#"[e] for e in row))

    segments = input.rstrip("\n").split("\n\n")
    elves = as_bool_array(segments[0])

    MOVES = [
        ((-1, 0), 1 | 2 | 4),
        ((1, 0), 32 | 64 | 128),
        ((0, -1), 1 | 8 | 32),
        ((0, 1), 4 | 16 | 128),
    ]

    for _ in range(10):
        elves = np.pad(elves, 1)
        movement = DefaultDict(list)
        n = scipy.signal.convolve(elves, N, "same")
        for y, x in np.argwhere(elves):
            if n[y, x] == 0:
                pass
            else:
                for (dy, dx), check in MOVES:
                    if n[y, x] & check == 0:
                        movement[y + dy, x + dx].append((y, x))
                        break
        for dest, actors in movement.items():
            if len(actors) == 1:
                elves[actors[0]] = False
                elves[dest] = True

        debug_print()
        MOVES.append(MOVES.pop(0))
    debug_print()

    while not elves[0, :].any():
        elves = elves[1:, :]
    while not elves[:, 0].any():
        elves = elves[:, 1:]
    while not elves[-1, :].any():
        elves = elves[:-1, :]
    while not elves[:, -1].any():
        elves = elves[:, :-1]

    return (elves == 0).sum()


EXPECTED = 110
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
