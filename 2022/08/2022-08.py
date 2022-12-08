from __future__ import annotations

from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
from aoc import as_array


def main(input: str) -> (int | str | None):
    segments = input.rstrip("\n").split("\n\n")
    array = as_array(segments[0])

    # part 1
    visible = 0
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            height = array[i, j]
            if (
                (array[:i, j] < height).all()
                or (array[i, :j] < height).all()
                or (array[i + 1 :, j] < height).all()
                or (array[i, j + 1 :] < height).all()
            ):
                visible += 1

    # return visible  # end part 1

    best = 0
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            height = array[i, j]
            this_best = 1
            for arr in [array[:i, j][::-1], array[i, :j][::-1], array[i + 1 :, j], array[i, j + 1 :]]:
                dir_score = 0
                for k in arr:
                    dir_score += 1
                    if k >= height:
                        break
                this_best *= dir_score
            best = max(best, this_best)

    return best


EXPECTED = 8
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
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
