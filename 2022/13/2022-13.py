from __future__ import annotations

import functools
import itertools
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import ast


def cmp(lhs, rhs) -> int:
    if isinstance(lhs, list) and isinstance(rhs, list):
        for a, b in itertools.zip_longest(lhs, rhs):
            if a is None:
                return -1
            if b is None:
                return 1
            if (x := cmp(a, b)) != 0:
                return x
        return 0

    elif isinstance(lhs, int) and isinstance(rhs, int):
        return lhs - rhs
    else:
        lhs = [lhs] if isinstance(lhs, int) else lhs
        rhs = [rhs] if isinstance(rhs, int) else rhs
        return cmp(lhs, rhs)


def main(input: str) -> (int | str | None):
    segments = input.rstrip("\n").split("\n\n")
    lines = segments[0].split("\n")
    indexes = []
    all_items = []
    for i, s in enumerate(segments, start=1):
        lines = s.split("\n")
        lhs = ast.literal_eval(lines[0])
        rhs = ast.literal_eval(lines[1])
        all_items += [lhs, rhs]
        if cmp(lhs, rhs) <= 0:
            indexes.append(i)

    # return sum(indexes)  # part 1

    div1 = [[2]]
    div2 = [[6]]
    all_items += [div1, div2]
    all_items.sort(key=functools.cmp_to_key(lambda a, b: cmp(a, b)))

    return (all_items.index(div1) + 1) * (all_items.index(div2) + 1)


EXPECTED = 140
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
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
