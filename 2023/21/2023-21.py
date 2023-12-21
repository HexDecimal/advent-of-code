from __future__ import annotations

from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import numpy as np
import tcod.path
from aoc import as_ord_array
from numpy.typing import NDArray


def main(input: str, max_steps: int) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    array = as_ord_array(segments[0]).astype(np.int32)
    assert array.shape[0] == array.shape[1]
    walkable: NDArray[np.bool_] = array != ord("#")
    start_ij: tuple[int, int] = tuple(np.argwhere(array == ord("S")).tolist()[0])  # type:ignore

    center_dist = tcod.path.maxarray(walkable.shape)
    center_dist[start_ij] = 0
    tcod.path.dijkstra2d(center_dist, out=center_dist, cost=walkable, cardinal=1)

    total = int(((center_dist <= max_steps) & (center_dist % 2 == max_steps % 2)).sum())

    def check_cardinal() -> int:
        next_dist = tcod.path.maxarray(walkable.shape)
        next_dist[0] = center_dist[-1] + 1
        tcod.path.dijkstra2d(next_dist, out=next_dist, cost=walkable, cardinal=1)
        mask = next_dist != np.iinfo(next_dist.dtype).max
        cardinal_steps = walkable.shape[0]

        this_total = 0

        while count := int(((next_dist <= max_steps) & (next_dist % 2 == max_steps % 2)).sum()):
            this_total += count
            next_dist[mask] += cardinal_steps

        return this_total

    def check_diagonal() -> int:
        next_dist = tcod.path.maxarray(walkable.shape)
        next_dist[0, 0] = center_dist[-1, -1] + 2
        tcod.path.dijkstra2d(next_dist, out=next_dist, cost=walkable, cardinal=1)
        mask = next_dist != np.iinfo(next_dist.dtype).max
        cardinal_steps = walkable.shape[0]
        chunks = 1

        this_total = 0

        while count := int(((next_dist <= max_steps) & (next_dist % 2 == max_steps % 2)).sum()):
            this_total += count * chunks
            next_dist[mask] += cardinal_steps
            chunks += 1

        return this_total

    for _ in range(4):
        total += check_cardinal()
        total += check_diagonal()
        walkable = np.rot90(walkable)
        center_dist = np.rot90(center_dist)

    return total


EXPECTED = 6536
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.input"
    INPUT_FILE = THIS_DIR / "input.input"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data, encoding="utf8")
    # result = main(EXAMPLE_FILE.read_text(encoding="ansi"), max_steps=100)
    # if result != EXPECTED:
    #    print(f"Expected {EXPECTED!r} but got {result!r} instead!")
    #    raise SystemExit()
    # else:
    #    print("Example passed.")
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi"), max_steps=26501365))
