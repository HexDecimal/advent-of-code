from __future__ import annotations

import collections
import itertools
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore


def main(input: str) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    modules: dict[str, tuple[str, ...]] = {}
    lines = segments[0].split("\n")
    for line in lines:
        module_key, dest_list = line.split(" -> ")
        modules[module_key] = tuple(dest_list.split(", "))

    for key in list(modules):
        key_to_replace = key.strip("&%")
        modules = {
            key_: tuple((key if old_dest == key_to_replace else old_dest) for old_dest in modules[key_])
            for key_ in modules
        }

    conjunction_inputs = DefaultDict[str, frozenset[str]](frozenset)
    for key, destinations in modules.items():
        for dest in destinations:
            if dest[0] == "&":
                conjunction_inputs[dest] |= {key}

    def step(
        queue_: tuple[tuple[str, str, bool], ...], state: set[str], memory: dict[str, set[str]]
    ) -> tuple[set[str], dict[str, set[str]], bool]:
        done = False
        queue = collections.deque(queue_)
        while queue:
            prev, current, high_pulse = queue.popleft()
            if current not in modules:
                if current == "rx" and not high_pulse:
                    done = True
                continue

            if current[0] == "%":
                if high_pulse:
                    continue
                if current in state:
                    state.remove(current)
                    queue.extend((current, dest, False) for dest in modules[current])
                    continue
                else:  # noqa: RET507
                    state.add(current)
                    queue.extend((current, dest, True) for dest in modules[current])
                    continue

            if high_pulse:
                memory[current].add(prev)
            else:
                memory[current].discard(prev)

            send_high = conjunction_inputs[current] != memory[current]
            queue.extend((current, dest, send_high) for dest in modules[current])
            continue

        return state, memory, done

    state = set[str]()
    memory = dict[str, set[str]]({m: set() for m in modules if m[0] == "&"})
    broadcast = tuple(("", dest, False) for dest in modules["broadcaster"])
    for i in itertools.count(1):
        if i % 1000 == 0:
            print(f"\r{i}", end="")
        state, memory, done = step(broadcast, state, memory)
        if done:
            return i

    raise AssertionError()


if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    INPUT_FILE = THIS_DIR / "input.input"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data, encoding="utf8")
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
