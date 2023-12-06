from __future__ import annotations

from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
from aoc import ints


def test_race(time: int, distance: int, hold_time: int) -> bool:
    """True if win."""
    return (time - hold_time) * hold_time > distance


def main(input: str) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    lines = segments[0].split("\n")
    races = zip(ints(lines[0]), ints(lines[1]), strict=True)  # time, distance
    total = 1
    for time, distance in races:
        count = 0
        print(f"\n{time=} {distance=}:")
        for i in range(1, distance):
            if test_race(time, distance, i):
                print(i, end=" ")
                count += 1
        total *= count

    return total


EXPECTED = 288
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
