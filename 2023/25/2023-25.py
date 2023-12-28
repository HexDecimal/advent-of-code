from __future__ import annotations

import collections
import copy
import itertools
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
from tqdm import tqdm


def main(input: str) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    connections = DefaultDict[str, set[str]](set)
    wires = set()
    lines = segments[0].split("\n")
    for line in lines:
        left, right = line.split(": ")
        for dest in right.split(" "):
            connections[left].add(dest)
            connections[dest].add(left)
            wires.add(tuple(sorted([left, dest])))

    def get_group(start: str, connections: dict[str, set[str]]) -> set[str]:
        group = {start}
        queue = collections.deque[str]([start])
        while queue:
            node = queue.popleft()
            for dest in connections[node] - group:
                queue.append(dest)
                group.add(dest)
        return group

    def get_path(start: str, end: str) -> list[tuple[str, str]]:
        visited = {start}
        queue = collections.deque([start])
        flow = {}
        while True:
            node = queue.popleft()
            for dest in connections[node] - visited:
                flow[dest] = node
                queue.append(dest)
                visited.add(dest)
                if dest == end:
                    node = end
                    wires = []
                    while node != start:
                        wires.append(tuple(sorted([node, flow[node]])))
                        node = flow[node]
                    return wires  # type: ignore[return-value]

    wire_heat = Counter[tuple[str, str]]()

    tested = set()
    i = 0
    for node_start, node_end in tqdm(list(itertools.combinations(connections, 2))):
        for wire in get_path(node_start, node_end):
            wire_heat[wire] += 1

        i += 1
        if i % 100 != 0:
            continue

        hottest_wires = [wire for wire, _ in wire_heat.most_common(3 + (i // 1000))]

        for to_cut in itertools.combinations(hottest_wires, 3):
            to_cut_set = frozenset(to_cut)
            if to_cut_set in tested:
                continue
            tested.add(to_cut_set)

            new_connections = copy.deepcopy(connections)
            for wire_a, wire_b in to_cut:
                new_connections[wire_a].remove(wire_b)
                new_connections[wire_b].remove(wire_a)
            group_a = get_group(next(iter(new_connections)), new_connections)
            if len(group_a) == len(new_connections):
                continue
            group_b = get_group(next(iter(new_connections.keys() - group_a)), new_connections)
            return len(group_a) * len(group_b)

    return None


EXPECTED = 54
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
