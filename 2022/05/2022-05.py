from __future__ import annotations

import itertools
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
from parse import parse


def main(input: str) -> (int | str | None):
    segments = input.split("\n\n")
    lines = segments[0].split("\n")
    print(segments[0])
    print(lines)
    lines.pop()

    stacks: list[list[str]] = []

    for line in lines:
        stacks.append([])
        for x in line[1::4]:
            print(x)
            stacks[-1].append(x)
        print(stacks)
    print(stacks)
    stacks = list(list(reversed(zipped)) for zipped in itertools.zip_longest(*stacks, fillvalue=" "))
    for stack in stacks:
        while stack and stack[-1] == " ":
            stack.pop()

    print(stacks)
    for rule in segments[1].strip().split("\n"):
        repeats, from_, to_ = parse("move {:d} from {:d} to {:d}", rule)
        print(rule)
        from_ -= 1
        to_ -= 1
        print(stacks)
        stacks[to_].extend(stacks[from_][-repeats:])
        stacks[from_] = stacks[from_][:-repeats]

        # part 1
        # for _ in range(repeats)
        #     stacks[to_].append(stacks[from_].pop())

    print(stacks)
    return "".join(stack[-1] for stack in stacks)


EXPECTED = "MCD"
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data + "\n", encoding="utf8")
    result = main(EXAMPLE_FILE.read_text(encoding="ansi"))
    assert result == EXPECTED, f"{result} != {EXPECTED}"
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
