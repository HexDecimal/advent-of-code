from __future__ import annotations

from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
from parse import parse  # type: ignore[import-untyped]

MAX = {"red": 12, "green": 13, "blue": 14}


def main(input: str) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    lines = segments[0].split("\n")
    total = 0
    for line in lines:
        game_n, rules = parse("Game {:d}: {}", line)
        win = True
        rule_sets = rules.split("; ")
        for rule_set in rule_sets:
            for cubes in rule_set.split(", "):
                n, color = parse("{:d} {}", cubes)
                if n > MAX[color]:
                    win = False

        total += game_n * win
    return total


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
    else:
        print("Example passed.")
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
