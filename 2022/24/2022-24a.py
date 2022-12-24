from __future__ import annotations

import functools
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import numpy as np
from aoc import as_bool_array
from numpy.typing import NDArray
import heapq


class State(NamedTuple):
    turn: int
    y: int
    x: int


def main(input: str) -> (int | str | None):
    segments = input.rstrip("\n").split("\n\n")
    walls = as_bool_array(segments[0], "#")
    blizzard_n = as_bool_array(segments[0], "^")
    blizzard_s = as_bool_array(segments[0], "v")
    blizzard_w = as_bool_array(segments[0], "<")
    blizzard_e = as_bool_array(segments[0], ">")

    @functools.cache
    def get_blizzard(turn: int) -> NDArray[np.bool_]:
        blocked = walls.copy()
        blocked[1:-1, 1:-1] |= np.roll(blizzard_n[1:-1, 1:-1], -turn, axis=0)
        blocked[1:-1, 1:-1] |= np.roll(blizzard_s[1:-1, 1:-1], turn, axis=0)
        blocked[1:-1, 1:-1] |= np.roll(blizzard_w[1:-1, 1:-1], -turn, axis=1)
        blocked[1:-1, 1:-1] |= np.roll(blizzard_e[1:-1, 1:-1], turn, axis=1)
        blocked.flags.writeable = False
        return blocked

    assert not walls[0, 1]
    target_yx = walls.shape[0] - 1, walls.shape[1] - 2
    assert not walls[target_yx]

    heap = [(0, State(turn=0, y=0, x=1))]
    touched = set()
    best_turns = float("inf")
    best_distance = float("inf")
    while heap:
        _, state = heapq.heappop(heap)
        next_turn = state.turn + 1
        if best_turns is not None and best_turns <= next_turn:
            continue
        blocked = get_blizzard(next_turn)
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)):
            next_y = state.y + dy
            if not (0 <= next_y < blocked.shape[0]):
                continue
            next_x = state.x + dx
            if blocked[next_y, next_x]:
                continue
            distance = abs(target_yx[0] - next_y) + abs(target_yx[1] - next_x)
            if distance < best_distance:
                best_distance = distance
                print(distance, next_turn, (next_x, next_y))
            if distance == 0:
                best_turns = min(next_turn, best_turns)
                print(best_turns)
                continue
            next_state = State(next_turn, next_y, next_x)
            if next_state in touched:
                continue
            touched.add(next_state)

            heapq.heappush(heap, (next_turn + distance, next_state))

    return int(best_turns)


EXPECTED = 18
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
