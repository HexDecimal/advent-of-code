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
    walkable: NDArray[np.bool_] = array != ord("#")
    start_ij: tuple[int, int] = tuple(np.argwhere(array == ord("S")).tolist()[0])  # type:ignore

    dist = tcod.path.maxarray(walkable.shape)
    dist[start_ij] = 0
    tcod.path.dijkstra2d(dist, out=dist, cost=walkable, cardinal=1)

    return ((dist <= max_steps) & ~(dist % 2)).sum()


EXPECTED = 16
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.input"
    INPUT_FILE = THIS_DIR / "input.input"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data, encoding="utf8")
    result = main(EXAMPLE_FILE.read_text(encoding="ansi"), max_steps=6)
    if result != EXPECTED:
        print(f"Expected {EXPECTED!r} but got {result!r} instead!")
        raise SystemExit()
    else:
        print("Example passed.")
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi"), max_steps=64))
