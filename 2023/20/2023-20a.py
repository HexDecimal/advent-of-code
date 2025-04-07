from __future__ import annotations

import collections
import functools
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import cattrs
from frozendict import frozendict


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

    @functools.cache
    def step(
        queue_: tuple[tuple[str, str, bool], ...], state_: frozenset[str], memory_: frozendict[str, frozenset[str]]
    ) -> tuple[frozenset[str], frozendict[str, frozenset[str]], int, int]:
        if not queue_:
            return state_, memory_, 0, 0
        state = set(state_)
        memory = cattrs.structure(memory_, dict[str, set[str]])
        total_low = total_high = 0
        queue = collections.deque(queue_)
        while queue:
            prev, current, high_pulse = queue.popleft()
            print(f"""{[" low", "high"][high_pulse]} -> {current}""")
            if high_pulse:
                total_high += 1
            else:
                total_low += 1
            if current not in modules:
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
        print("""---""")

        memory_ = frozendict(cattrs.structure(memory, frozendict[str, frozenset[str]]))
        return frozenset(state), memory_, total_low, total_high

    state = frozenset[str]()
    memory = frozendict[str, frozenset[str]]({m: frozenset() for m in modules if m[0] == "&"})
    broadcast = tuple(("", dest, False) for dest in modules["broadcaster"])
    total_low = total_high = 0
    for _ in range(1000):
        state, memory, low, high = step(broadcast, state, memory)
        total_low += low + 1
        total_high += high

    return total_low * total_high


EXPECTED = 11687500
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
