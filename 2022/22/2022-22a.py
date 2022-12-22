from __future__ import annotations

import re
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
from aoc import as_bool_array

DIRS_XY = (
    (1, 0),  # E
    (0, 1),  # S
    (-1, 0),  # W
    (0, -1),  # N
)


def main(input: str) -> (int | str | None):
    map_, path_ = input.rstrip("\n").split("\n\n")
    valid = as_bool_array(map_, ".#")
    walls = as_bool_array(map_, "#")
    y = 0
    x = 0
    face = 0
    while not valid[y, x]:
        x += 1
    for inst in re.findall(r"\d+|L|R", path_):
        inst = str(inst)
        print(inst)
        if inst.isdigit():
            for _ in range(int(inst)):
                new_y, new_x = y, x
                while True:
                    dx, dy = DIRS_XY[face]
                    new_y, new_x = new_y + dy, new_x + dx
                    new_y %= valid.shape[0]
                    new_x %= valid.shape[1]
                    if valid[new_y, new_x]:
                        break
                if walls[new_y, new_x]:
                    break
                x, y = new_x, new_y
                print(x, y)

        elif inst == "R":
            face = (face + 1) % 4
        elif inst == "L":
            face = (face - 1) % 4
    print(y, x, face)
    return (y + 1) * 1000 + (x + 1) * 4 + face


EXPECTED = 6032
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
