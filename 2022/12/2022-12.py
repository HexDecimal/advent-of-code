from __future__ import annotations

from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import numpy as np
from aoc import as_ord_array
import heapq


def main(input: str) -> (int | str | None):
    segments = input.rstrip("\n").split("\n\n")
    array = as_ord_array(segments[0])

    def in_bounds(ij: Any) -> bool:
        return 0 <= ij[0] < array.shape[0] and 0 <= ij[1] < array.shape[1]

    heap = []

    flow = {}
    dists = {}
    graph = DefaultDict[tuple[int, ...], list[tuple[int, ...]]](list)
    for ij, c in np.ndenumerate(array):
        if c == ord("S"):
            heap.append((0, ij))
            array[ij] = ord("a")
            flow[ij] = ij
            dists[ij] = 0
        if c == ord("E"):
            array[ij] = ord("z")
            target = ij

        # part 2
        if array[ij] == ord("a"):
            heap.append((0, ij))
            flow[ij] = ij
            dists[ij] = 0
        # end part 2

    for ij, c in np.ndenumerate(array):
        for d in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            adj = ij[0] + d[0], ij[1] + d[1]
            if not in_bounds(adj):
                continue
            if array[adj] <= c + 1:
                graph[ij].append(adj)
    while target not in flow:
        dist, ij = heapq.heappop(heap)
        next_dist = dist + 1
        for adj in graph[ij]:
            if adj in dists and dists[adj] <= next_dist:
                continue
            dists[adj] = next_dist
            flow[adj] = ij
            heapq.heappush(heap, (next_dist, adj))

    return dists[target]


EXPECTED = 29
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
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
