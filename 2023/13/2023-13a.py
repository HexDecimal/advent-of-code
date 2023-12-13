from __future__ import annotations

from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import numpy as np
from aoc import as_bool_array
from numpy.typing import NDArray


def get_score(mirrors: NDArray[np.bool8]) -> int:
    for i in range(1, mirrors.shape[0]):
        width = min(mirrors.shape[0] - i, i)
        if (mirrors[i : i + width, :] == mirrors[i - width : i, :][::-1, :]).all():
            return i * 100
    for i in range(1, mirrors.shape[1]):
        width = min(mirrors.shape[1] - i, i)
        if (mirrors[:, i : i + width] == mirrors[:, i - width : i][:, ::-1]).all():
            return i
    raise AssertionError()


def main(input: str) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    total = 0
    for segment in segments:
        mirrors = as_bool_array(segment)
        total += get_score(mirrors)

    return total


EXPECTED = 405
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
