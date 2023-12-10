from __future__ import annotations

import collections
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import numpy as np
from aoc import as_ord_array

PIPES: dict[int, list[tuple[int, int]]] = {  # Y, X
    ord("S"): [(-1, 0), (1, 0), (0, -1), (0, 1)],
    ord("|"): [(-1, 0), (1, 0)],
    ord("-"): [(0, -1), (0, 1)],
    ord("F"): [(1, 0), (0, 1)],
    ord("7"): [(1, 0), (0, -1)],
    ord("L"): [(-1, 0), (0, 1)],
    ord("J"): [(-1, 0), (0, -1)],
    ord("."): [],
}


def iter_connections(yx: tuple[int, int], pipe: int) -> Iterator[tuple[int, int]]:
    y, x = yx
    for dy, dx in PIPES[pipe]:
        yield y + dy, x + dx


def main(input: str) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    pipe_map = as_ord_array(segments[0]).astype(np.int32)
    start: tuple[int, int] = tuple(np.argwhere(pipe_map == ord("S")).tolist()[0])  # type: ignore
    frontier = collections.deque[tuple[int, int]]([start])
    dist = np.full_like(pipe_map, dtype=int, fill_value=-1)
    dist[tuple(frontier[0])] = 0
    while frontier:
        y, x = frontier.popleft()
        dist_here = dist.item(y, x)
        for next in iter_connections((y, x), pipe_map[y, x]):
            if dist[next] != -1:
                if dist[next] == dist_here + 1:
                    print(dist_here + 1)
                continue

            if not (0 <= next[0] < pipe_map.shape[0] and 0 <= next[1] < pipe_map.shape[1]):
                continue
            if (y, x) not in iter_connections(next, pipe_map[next]):
                continue
            dist[next] = dist_here + 1
            frontier.append(next)

    return dist.max()


EXPECTED = 8
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
    result = main(INPUT_FILE.read_text(encoding="ansi"))
    aocd.submit(result)
