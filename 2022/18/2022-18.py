from __future__ import annotations

from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import numpy as np
from aoc import ints
import scipy.signal
import tcod


def main(input: str) -> (int | str | None):
    segments = input.rstrip("\n").split("\n\n")
    lines = segments[0].split("\n")
    cubes_list = np.array([ints(line) for line in lines])

    cubes = np.zeros(cubes_list.max(axis=0) + 1, dtype=int)
    cubes[tuple(cubes_list.T)] = 1
    print(cubes)

    N = [
        [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0],
        ],
        [
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0],
        ],
        [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0],
        ],
    ]

    cubes = np.pad(cubes, 1)
    graph = tcod.path.CustomGraph(cubes.shape)
    graph.add_edges(edge_map=N, cost=cubes == 0)
    pf = tcod.path.Pathfinder(graph)
    pf.add_root((0, 0, 0))
    pf.resolve()
    cubes[pf.distance == np.iinfo(pf.distance.dtype).max] = 1

    neighbors = scipy.signal.convolve(cubes, N, "same")

    result = cubes * 6
    result -= neighbors
    result[result < 0] = 0
    return int(result.sum())


EXPECTED = 58
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
