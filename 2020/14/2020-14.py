from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import Iterable, NamedTuple

import aocd  # type: ignore

ONES_TABLE = {
    ord("X"): ord("0"),
    ord("0"): ord("0"),
    ord("1"): ord("1"),
}
ZEROS_TABLE = {
    ord("X"): ord("0"),
    ord("0"): ord("1"),
    ord("1"): ord("0"),
}
WRITE_TABLE = {
    ord("X"): ord("1"),
    ord("0"): ord("0"),
    ord("1"): ord("0"),
}
MAX_36 = 0b111111111111111111111111111111111111


class Mask(NamedTuple):
    ones: int
    "Bitmask of ones bits."
    zeros: int
    "Bitmask of zeros bits."
    floating: int


def parse_mask(mask: str) -> Mask:
    ones = int(mask.translate(ONES_TABLE), base=2)
    zeros = int(mask.translate(ZEROS_TABLE), base=2)
    write = int(mask.translate(WRITE_TABLE), base=2)
    return Mask(ones, zeros, write)


def part1(input: str) -> (int | str | None):
    segments = input.strip().split("\n\n")
    lines = segments[0].split("\n")
    mask = Mask(0, 0, 0)
    memory = defaultdict[int, int](int)
    for line in lines:
        if match := re.match(r"mask = ([X01]+)$", line):
            mask = parse_mask(match[1])
        elif match := re.match(r"mem\[(\d+)\] = (\d+)$", line):
            index = int(match[1])
            value = int(match[2])
            value |= mask.ones
            value &= MAX_36 ^ mask.zeros
            memory[index] = value
        else:
            assert False

    return sum(memory.values())


def expand_floating_memory(floating: int) -> Iterable[int]:
    indexes = [0]
    for i in range(36):
        bit = 1 << i
        if floating & bit:
            indexes += [index | bit for index in indexes]
    return indexes


def main(input: str) -> (int | str | None):
    segments = input.strip().split("\n\n")
    lines = segments[0].split("\n")
    mask = Mask(0, 0, 0)
    memory = defaultdict[int, int](int)
    for line in lines:
        if match := re.match(r"mask = ([X01]+)$", line):
            mask = parse_mask(match[1])
        elif match := re.match(r"mem\[(\d+)\] = (\d+)$", line):
            index = int(match[1])
            value = int(match[2])
            index |= mask.ones
            index &= mask.floating ^ MAX_36
            for floating in expand_floating_memory(mask.floating):
                memory[index | floating] = value
        else:
            assert False
    return sum(memory.values())


EXPECTED = 208
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data + "\n", encoding="utf8")
    result = main(EXAMPLE_FILE.read_text(encoding="ansi"))
    assert result == EXPECTED, f"{result} != {EXPECTED}"
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
