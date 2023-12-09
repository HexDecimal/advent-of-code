from __future__ import annotations

import itertools
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
from aoc import ints


def main(input: str) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    total = 0
    lines = segments[0].split("\n")
    for line in lines:
        rows = [ints(line)]
        while len(rows[-1]) > 1:
            rows.append([b - a for a, b in itertools.pairwise(rows[-1])])
        for i in range(len(rows))[::-1]:
            if not any(rows[i]):
                rows[i].insert(0, 0)
                continue
            rows[i].insert(0, rows[i][0] - rows[i + 1][0])

        total += rows[0][0]
    return total


EXPECTED = 2
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
