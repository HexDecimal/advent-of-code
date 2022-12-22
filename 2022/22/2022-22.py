from __future__ import annotations

import re
from pathlib import Path
from typing import *  # noqa: F403
from pprint import pprint

import aocd  # type: ignore
import numpy as np
from aoc import as_bool_array
from numpy.typing import NDArray

DIRS_XY = (
    (1, 0),  # E
    (0, 1),  # S
    (-1, 0),  # W
    (0, -1),  # N
)
DIRS_XY_INVERSE = {k: i for i, k in enumerate(DIRS_XY)}

E = (1, 0)
S = (0, 1)
W = (-1, 0)
N = (0, -1)

R_TRANSFORM = np.array([[0, -1], [1, 0]])
L_TRANSFORM = R_TRANSFORM @ R_TRANSFORM @ R_TRANSFORM


def main(input: str, chunk_size: int) -> (int | str | None):
    def debug_print() -> None:
        display = np.zeros_like(valid, int)
        display[:] = 0x20
        display[valid] = ord(".")
        display[walls] = ord("#")
        display[y, x] = ord(">v<^"[face])
        for row in display:
            print("".join(chr(ch) for ch in row))

    map_, path_ = input.rstrip("\n").split("\n\n")
    valid = as_bool_array(map_, ".#")
    walls = as_bool_array(map_, "#")
    y = 0
    x = 0
    face = 0
    while not valid[y, x]:
        x += 1

    cube_map: dict[tuple[int, int], dict[tuple[int, int], tuple[tuple[int, int], NDArray[np.int32]]]] = {}

    valid_small = valid[::chunk_size, ::chunk_size]

    def recurse_fold_first(x: int, y: int) -> None:
        assert valid_small[y, x]
        if (x, y) in cube_map:
            return
        cube_map[(x, y)] = {}

        if x > 0 and valid_small[y, x - 1]:
            recurse_fold_first(x - 1, y)
            cube_map[(x, y)][W] = (x - 1, y), np.identity(2, int)
            cube_map[(x - 1, y)][E] = (x, y), np.identity(2, int)
        if x + 1 < valid_small.shape[1] and valid_small[y, x + 1]:
            recurse_fold_first(x + 1, y)
            cube_map[(x, y)][E] = (x + 1, y), np.identity(2, int)
            cube_map[(x + 1, y)][W] = (x, y), np.identity(2, int)
        if y + 1 < valid_small.shape[0] and valid_small[y + 1, x]:
            recurse_fold_first(x, y + 1)
            cube_map[(x, y)][S] = (x, y + 1), np.identity(2, int)
            cube_map[(x, y + 1)][N] = (x, y), np.identity(2, int)

    recurse_fold_first(x // chunk_size, 0)

    def search_fold(x: int, y: int) -> bool:
        def test_fold(d_fwd: int, d_dir: int, rotate: NDArray[np.integer]) -> bool:
            d_right = (d_fwd + d_dir) % 4
            d_left = (d_right - d_dir) % 4
            try:
                right1 = cube_map[(x, y)][DIRS_XY[d_right]]
                d_transform: Any = tuple((right1[1] @ DIRS_XY[d_left]).tolist())
                right2 = cube_map[right1[0]][d_transform]
            except KeyError:
                return False
            else:
                assert right2[0] != (x, y)
                print(f"Found {right2[0]} via {x, y} - {right1[0]} - {right2[0]}")
                cube_map[(x, y)][DIRS_XY[d_fwd]] = (right2[0], right1[1] @ right2[1] @ rotate)
                # pprint(cube_map)
            return True

        all_found = True
        for d in range(4):
            if DIRS_XY[d] not in cube_map[(x, y)]:
                all_found &= test_fold(d, 1, R_TRANSFORM) or test_fold(d, -1, L_TRANSFORM)
        return all_found

    while not all([search_fold(x, y) for x, y in cube_map.keys()]):
        pass  # pprint(cube_map)

    for inst in re.findall(r"\d+|L|R", path_):
        inst = str(inst)
        print(inst)
        if inst.isdigit():
            for _ in range(int(inst)):
                new_y, new_x = y, x
                print(f"Moving to: {new_x}, {new_y}")
                dx, dy = DIRS_XY[face]
                new_face = face
                new_y, new_x = new_y + dy, new_x + dx
                if not (0 <= new_y < valid.shape[0] and 0 <= new_x < valid.shape[1] and valid[new_y, new_x]):
                    print("Off side")
                    new_y = new_y % chunk_size
                    new_x = new_x % chunk_size
                    print(f"Normal position {new_x, new_y}")
                    new_side, transform = cube_map[x // chunk_size, y // chunk_size][dx, dy]
                    print(f"Transform {transform}")
                    new_x, new_y = (transform @ (new_x, new_y)).tolist()
                    print(f"Now normal position {new_x, new_y}")
                    if new_x < 0:
                        new_x -= 1
                    if new_y < 0:
                        new_y -= 1
                    new_y %= chunk_size
                    new_x %= chunk_size
                    print(f"Now normal position {new_x, new_y}")
                    dx, dy = (transform @ (dx, dy)).tolist()
                    new_face = DIRS_XY_INVERSE[dx, dy]
                    print(f"From side {x // chunk_size, y // chunk_size} to {new_side}, facing {face} -> {new_face}")
                    if new_face == 0:
                        new_x = 0
                    elif new_face == 1:
                        new_y = 0
                    if new_face == 2:
                        new_x = -1
                    elif new_face == 3:
                        new_y = -1
                    new_y %= chunk_size
                    new_x %= chunk_size

                    print(f"Now normal position {new_x, new_y}")

                    new_x += new_side[0] * chunk_size
                    new_y += new_side[1] * chunk_size
                    print(f"New position at {new_x, new_y}")
                    assert valid[new_y, new_x]

                if walls[new_y, new_x]:
                    print("blocked")
                    break
                x, y = new_x, new_y
                face = new_face
                # debug_print()
                # print(x, y)

        elif inst == "R":
            face = (face + 1) % 4
        elif inst == "L":
            face = (face - 1) % 4
    print(y, x, face)
    return (y + 1) * 1000 + (x + 1) * 4 + face


EXPECTED = 5031
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.input"
    INPUT_FILE = THIS_DIR / "input.input"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data, encoding="utf8")
    result = main(EXAMPLE_FILE.read_text(encoding="ansi"), 4)
    if result != EXPECTED:
        print(f"Expected {EXPECTED!r} but got {result!r} instead!")
        raise SystemExit()
    else:
        print("Example passed.")
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi"), 50))
