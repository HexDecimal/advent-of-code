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
        _, rules = parse("Game {:d}: {}", line)
        rule_sets = rules.split("; ")
        needed = {"red": 0, "green": 0, "blue": 0}
        for rule_set in rule_sets:
            for cubes in rule_set.split(", "):
                n, color = parse("{:d} {}", cubes)
                needed[color] = max(n, needed[color])

        total += needed["red"] * needed["green"] * needed["blue"]
    return total


EXPECTED = 2286
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
