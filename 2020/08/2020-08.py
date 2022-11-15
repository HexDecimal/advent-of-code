from __future__ import annotations

import functools
import itertools
from collections import Counter
from pathlib import Path

import aocd  # type: ignore
import numpy as np


def test(instructions: list[tuple[str, int]]) -> None | int:
    acc = 0
    ptr = 0
    visited = Counter[int]()

    while ptr < len(instructions):
        if ptr in visited:
            return None
        visited[ptr] += 1
        match instructions[ptr]:
            case "acc", v:
                acc += v
                ptr += 1
            case "nop", _:
                ptr += 1
            case "jmp", v:
                ptr += v

    return acc


def main(file: Path) -> (int | str | None):
    segments = file.read_text(encoding="ansi").strip().split("\n\n")

    def parse(line: str) -> tuple[str, int]:
        cmd, value = line.split(" ")
        return cmd, int(value)

    instructions = [parse(line) for line in segments[0].split("\n")]
    for i, cmd in enumerate(instructions):
        modded = instructions.copy()
        result: int | None = None
        match cmd:
            case "nop", v:
                modded[i] = ("jmp", v)
                result = test(modded)
            case "jmp", v:
                modded[i] = ("nop", v)
                result = test(modded)
            case _:
                pass

        if result is not None:
            return result

    assert False


EXPECTED = 8
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data + "\n", encoding="utf8")
    if main(EXAMPLE_FILE) == EXPECTED:
        aocd.submit(main(INPUT_FILE))
