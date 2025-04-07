from __future__ import annotations

import heapq
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import attrs
import numpy as np
from aoc import as_array


@attrs.define(frozen=True, order=True)
class Position:
    x: int
    y: int
    dir_x: int
    dir_y: int
    consecutive: int = 1


def main(input: str) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    array = as_array(segments[0]).astype(np.int32)
    dest = array.shape[0] - 1, array.shape[1] - 1

    def heuristic(pos: Position, dist: int, dest: tuple[int, int]) -> int:
        return (abs(pos.x - dest[0]) + abs(pos.y - dest[1])) * 1 + dist

    start = [Position(0, 0, 1, 0, 0), Position(0, 0, 0, 1, 0)]
    distances = dict.fromkeys(start, 0)
    heap = [(heuristic(pos, 0, dest), 0, pos) for pos in start]

    def add_pos(pos: Position, here_dist: int) -> None:
        if not (0 <= pos.x < array.shape[0] and 0 <= pos.y < array.shape[1]):
            return
        dist = here_dist + array[pos.x, pos.y]
        if pos in distances and distances[pos] <= dist:
            return
        distances[pos] = dist
        heapq.heappush(heap, (heuristic(pos, dist, dest), dist, pos))

    best = 999999
    while heap:
        _, here_dist, here = heapq.heappop(heap)
        if here_dist > distances[here]:
            continue
        if (here.x, here.y) == dest:
            if best > here_dist:
                best = here_dist
                if heap:
                    print((best, heap[0][0]))
            continue
        if here.consecutive < 10:
            add_pos(
                Position(here.x + here.dir_x, here.y + here.dir_y, here.dir_x, here.dir_y, here.consecutive + 1),
                here_dist,
            )
        if here.consecutive >= 4:
            if here.dir_x == 0:
                add_pos(Position(here.x + 1, here.y, 1, 0), here_dist)
                add_pos(Position(here.x - 1, here.y, -1, 0), here_dist)
            else:
                add_pos(Position(here.x, here.y + 1, 0, 1), here_dist)
                add_pos(Position(here.x, here.y - 1, 0, -1), here_dist)
    return best


EXPECTED = 94
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
