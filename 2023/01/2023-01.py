from __future__ import annotations

import re
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore

N = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

FIRST = re.compile(rf".*?([0-9]|{"|".join(N.keys())})")
LAST = re.compile(rf".*([0-9]|{"|".join(N.keys())})")


def main(input: str) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    lines = segments[0].split("\n")
    total = 0
    for line in lines:
        first = FIRST.match(line)[1]  # type: ignore
        last = LAST.match(line)[1]  # type: ignore

        first = N.get(first, first)
        last = N.get(last, last)

        total += int(first + last)

    return total


EXPECTED = 281
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
    print(main(INPUT_FILE.read_text(encoding="ansi")))
    # aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
