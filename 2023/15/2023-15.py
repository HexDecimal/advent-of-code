from __future__ import annotations

import re
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore


def str_hash(string: str) -> int:
    result = 0
    for c in string:
        result = ((result + ord(c)) * 17) % 256
    return result


def main(input: str) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    (line,) = segments[0].split("\n")
    boxes = DefaultDict[int, list[tuple[str, int]]](list)
    for command in line.split(","):
        match = re.match(r"(\w+)([-=])(\d*)", command)
        assert match
        label, operation, focal_ = match.groups()
        index = str_hash(label)
        if operation == "-":
            boxes[index] = [lens for lens in boxes[index] if lens[0] != label]
            continue
        if operation == "=":
            focal = int(focal_)
            for i, lens in enumerate(boxes[index]):
                if lens[0] == label:
                    boxes[index][i] = (label, focal)
                    break
            else:
                boxes[index].insert(0, (label, focal))
            continue
        raise AssertionError(command)

    total = 0
    for box_i, slots in boxes.items():
        for lens_i, (_, focal) in enumerate(slots[::-1]):
            total += (box_i + 1) * (lens_i + 1) * focal

    return total


EXPECTED = 145
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
