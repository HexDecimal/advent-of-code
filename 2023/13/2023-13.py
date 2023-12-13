from __future__ import annotations

from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import numpy as np
from aoc import as_bool_array
from numpy.typing import NDArray


def get_score(mirrors: NDArray[np.bool8], ignore: tuple[int, int] | None = None) -> tuple[int, int] | None:
    for i in range(1, mirrors.shape[0]):
        width = min(mirrors.shape[0] - i, i)
        if (mirrors[i : i + width, :] == mirrors[i - width : i, :][::-1, :]).all():
            if ignore == (0, i * 100):
                continue
            return (0, i * 100)
    for i in range(1, mirrors.shape[1]):
        width = min(mirrors.shape[1] - i, i)
        if (mirrors[:, i : i + width] == mirrors[:, i - width : i][:, ::-1]).all():
            if ignore == (i, 0):
                continue
            return (i, 0)
    return None


def smudge(mirrors: NDArray[np.bool8]) -> int:
    original_score = get_score(mirrors)
    for i in range(mirrors.shape[0]):
        for j in range(mirrors.shape[1]):
            clone = mirrors.copy()
            clone[i, j] = not clone[i, j]
            smudged_score = get_score(clone, ignore=original_score)
            if smudged_score:
                print((smudged_score, i, j))
                return sum(smudged_score)
    raise AssertionError()


def main(input: str) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    total = 0
    for segment in segments:
        mirrors = as_bool_array(segment)
        total += smudge(mirrors)

    return total


EXPECTED = 400
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
