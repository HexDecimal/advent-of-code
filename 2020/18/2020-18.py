from __future__ import annotations

import functools
import operator
import re
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import numpy as np

reduce_mulitply = functools.partial(functools.reduce, operator.mul)

OP_KEYS = {"*": operator.mul, "+": operator.add}


def combine(symbols: list[str | int]) -> int:
    result = 0
    while symbols:
        if symbols[0] == ")":
            symbols.pop(0)
            return result
        op = OP_KEYS[symbols.pop(0)]  # type: ignore[index]
        if symbols[0] == "(":
            symbols[0] = "+"  # Repalce ( with +
            result = op(result, combine(symbols))
        else:
            result = op(result, int(symbols.pop(0)))
    return result


def part1(input: str) -> (int | str | None):
    segments = input.strip().split("\n\n")
    lines = segments[0].split("\n")
    total = 0
    for line in lines:
        line = f"+ {line}"
        symbols = [int(s) if s.isdigit() else s for s in re.findall(r" *(\(|\)|\+|\*|\d)", line)]
        total += combine(symbols)

    return total


def combine2(symbols: list[str | int]) -> int:
    result = 0
    while symbols:
        if symbols[0] == ")":
            symbols.pop(0)
            return result
        op = OP_KEYS[symbols.pop(0)]  # type: ignore[index]
        if op == operator.mul:
            symbols.insert(0, "+")
            depth = 1
            for i, sym in enumerate(symbols):
                if sym == "(":
                    depth += 1
                elif sym == ")":
                    depth -= 1
                if depth == 0:
                    symbols.insert(i, ")")
                    break
            symbols.insert(0, combine2(symbols))
        if symbols[0] == "(":
            symbols[0] = "+"  # Repalce ( with +
            result = op(result, combine2(symbols))
        else:
            result = op(result, int(symbols.pop(0)))
    return result


def main(input: str) -> (int | str | None):
    segments = input.strip().split("\n\n")
    lines = segments[0].split("\n")
    totals = []
    for line in lines:
        line = f"+ {line}"
        symbols = [int(s) if s.isdigit() else s for s in re.findall(r" *(\(|\)|\+|\*|\d)", line)]
        totals.append(combine2(symbols))

    return sum(totals)


EXPECTED = 51 + 46 + 1445 + 669060 + 23340
if __name__ == "__main__":
    np.seterr("raise")
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data + "\n", encoding="utf8")
    result = main(EXAMPLE_FILE.read_text(encoding="ansi"))
    assert result == EXPECTED, f"{result} != {EXPECTED}"
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
