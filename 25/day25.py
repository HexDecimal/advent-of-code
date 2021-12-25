from __future__ import annotations

from pathlib import Path

import numpy as np
import scipy.signal


def show(east, south):
    for y in range(east.shape[0]):
        print("".join(".>v"[e + s * 2] for e, s in zip(east[y], south[y])))


def main(file: Path) -> (int | str | None):
    with open(file, "r", encoding="utf8") as f:
        (lines,) = f.read().strip().split("\n\n")
    start = np.asarray([[{".": 0, ">": 1, "v": 2}[c] for c in row] for row in lines.split("\n")], int)
    east = start == 1
    south = start == 2
    steps = 0
    while True:
        # show(east, south)
        steps += 1
        last = (east.copy(), south.copy())
        east = np.pad(east, ((1, 1), (1, 1)), mode="wrap")
        south = np.pad(south, ((1, 1), (1, 1)), mode="wrap")
        blocked = scipy.signal.convolve2d(east, [[1, 0, 0]], mode="same")
        blocked |= scipy.signal.convolve2d(south, [[1, 1, 0]], mode="same")
        can_move = east & ~blocked
        move = scipy.signal.convolve2d(can_move, [[0, -1, 1]], mode="same")
        east &= ~move == -1
        east |= move == 1

        blocked = scipy.signal.convolve2d(south, np.transpose([[1, 0, 0]]), mode="same")
        blocked |= scipy.signal.convolve2d(east, np.transpose([[1, 1, 0]]), mode="same")
        can_move = south & ~blocked
        move = scipy.signal.convolve2d(can_move, np.transpose([[0, -1, 1]]), mode="same")
        south &= ~move == -1
        south |= move == 1

        east = east[1:-1, 1:-1]
        south = south[1:-1, 1:-1]

        if np.array_equal(last[0], east) and np.array_equal(last[1], south):
            print(steps)
            return steps


EXPECTED = 58
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if main(EXAMPLE_FILE) == EXPECTED:
        main(INPUT_FILE)
