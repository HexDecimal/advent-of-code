from __future__ import annotations

from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
from parse import parse  # type: ignore[import-untyped]


def main(input: str) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    lines = segments[0].split("\n")
    total = 0
    for line in lines:
        left: str
        right: str
        line = line.removeprefix("Card").strip()  # noqa: PLW2901
        print(line)
        card_n, left, right = parse("{:d}: {}|{}", line)
        left_n = {int(s) for s in left.strip().split(" ") if s}
        right_n = {int(s) for s in right.strip().split(" ") if s}
        matches = len(left_n & right_n)
        score = 2 ** (matches - 1) if matches else 0
        total += score
        print(f"CARD: {card_n} {left_n & right_n} {score=}")

    return total


EXPECTED = 13
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
