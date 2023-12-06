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
    races = zip(ints(lines[0].replace(" ", "")), ints(lines[1].replace(" ", "")), strict=True)  # time, distance
    for time, distance in races:
        low_miss = 0
        low_hit = time
        high_hit = 0
        high_miss = time
        while low_miss != low_hit - 1:
            hold_time = (low_miss + low_hit) // 2
            assert hold_time != low_miss, f"{hold_time=}, {low_miss=}, {low_hit=}"
            assert hold_time != low_hit, f"{hold_time=}, {low_miss=}, {low_hit=}"
            if test_race(time, distance, hold_time):
                low_hit = hold_time
                high_hit = max(high_hit, hold_time)
            else:
                low_miss = hold_time
        while high_hit != high_miss - 1:
            hold_time = (high_miss + high_hit) // 2
            assert hold_time != high_miss, f"{hold_time=}, {high_miss=}, {high_hit=}"
            assert hold_time != high_hit, f"{hold_time=}, {high_miss=}, {high_hit=}"
            if test_race(time, distance, hold_time):
                high_hit = hold_time
            else:
                high_miss = hold_time
        print(f"{low_hit=}, {high_hit=}")

    return high_hit - low_hit + 1


EXPECTED = 71503
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
