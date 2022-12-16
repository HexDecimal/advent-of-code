from __future__ import annotations

import functools
import itertools
import operator
import re
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import numpy as np
from aoc import as_array, as_bool_array, as_ord_array, ints, reduce_multiply, split_ints
from numpy.typing import NDArray
from parse import parse
import heapq


def main(input: str) -> (int | str | None):
    segments = input.rstrip("\n").split("\n\n")
    # array = as_array(segments[0]).astype(np.int32)
    # numbers = ints(segments[0].split(","))
    lines = segments[0].split("\n")
    graph = {}
    rates = {}
    for line in lines:
        this, rate_, others = re.match(
            r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)", line
        ).groups()  # type:ignore
        rates[this] = int(rate_)
        graph[this] = others.split(", ")

    for there, v in graph.items():
        for b in v:
            assert there in graph[b]

    distances = {}
    flow = {}
    for z in graph.keys():
        flow[z] = {z: z}
        distances[z] = {z: 0}
        q = [z]
        while q:
            to = q.pop(0)
            for from_ in graph[to]:
                if from_ in distances[z]:
                    continue

                flow[z][from_] = to
                distances[z][from_] = distances[z][to] + 1
                q.append(from_)

    unopened = {a for a in graph.keys() if rates[a]}
    best_pressure = 0
    heap = [(0, 26, 26, "AA", "AA", unopened)]
    best_states = {("AA", "AA", frozenset(unopened)): 0}
    while heap:

        pressure, you, ele, you_here, ele_here, unopened = heapq.heappop(heap)
        pressure = -pressure
        if best_pressure < pressure:
            best_pressure = pressure
            print(best_pressure, len(heap))

        for is_you in (False, True):
            ticks = (ele, you)[is_you]
            here = (ele_here, you_here)[is_you]
            for there in unopened:
                dist = distances[there][here]
                new_ticks = ticks - dist - 1
                if new_ticks <= 0:
                    continue
                new_pressure = pressure + new_ticks * rates[there]
                new_you = you
                new_ele = ele
                new_you_here = you_here
                new_ele_here = ele_here
                if is_you:
                    new_you = new_ticks
                    new_you_here = there
                else:
                    new_ele = new_ticks
                    new_ele_here = there
                new_unopened = unopened - {there}
                new_state = (new_you_here, new_ele_here, frozenset(new_unopened))
                if best_states.get(new_state, 0) >= new_pressure:
                    continue
                best_states[new_state] = new_pressure
                heapq.heappush(
                    heap,
                    (-new_pressure, new_you, new_ele, new_you_here, new_ele_here, unopened - {there}),
                )

    return best_pressure


EXPECTED = 1707
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
