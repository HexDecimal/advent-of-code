from __future__ import annotations

import itertools
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
from parse import parse  # type: ignore[import-untyped]


def main(input: str) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    print(segments[0])
    directions = itertools.cycle([0 if c == "L" else 1 for c in segments[0]])
    lines = segments[1].split("\n")
    graph: dict[str, tuple[str, str]] = {}
    for line in lines:
        here, left, right = parse("{} = ({}, {})", line)
        graph[here] = (left, right)
    pos = "AAA"
    steps = 0
    for d in directions:
        steps += 1
        pos = graph[pos][d]
        if pos == "ZZZ":
            break

    return steps


EXPECTED = 6
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
