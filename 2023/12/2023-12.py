from __future__ import annotations

import functools
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
from aoc import ints


@functools.cache
def solve(row: str, arrangement: tuple[int, ...]) -> int:
    if not arrangement:
        return 1 if "#" not in row else 0
    if not row:
        return 0
    if row[0] == "." or row[-1] == ".":
        return solve(row.strip("."), arrangement)
    part_width = arrangement[0]
    right_bound = len(row) - sum(arrangement) - len(arrangement) + 2
    if right_bound <= 0:
        return 0
    total = 0
    for i in range(right_bound):
        try:
            if row[i + part_width] == "#":
                continue
        except IndexError:
            pass
        if "#" in row[:i]:
            break
        if "." in row[i : i + part_width]:
            continue
        assert "." not in row[i : i + part_width], (row, i)
        total += solve(row[i + part_width + 1 :], arrangement[1:])
    return total


def main(input: str) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    total = 0
    lines = segments[0].split("\n")
    for line in lines:
        row, arrangement_ = line.split(" ")
        arrangement = tuple(ints(arrangement_))
        print(f"{row:>32} {arrangement_} =", end="")
        row = "?".join([row] * 5)
        arrangement *= 5
        print(solve(row, arrangement))
        total += solve(row, arrangement)
    return total


EXPECTED = 525152
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
