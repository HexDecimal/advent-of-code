from __future__ import annotations

from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
from aoc import ints
from parse import parse  # type: ignore[import-untyped]


def main(input: str) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    seeds = ints(segments.pop(0))
    mapping: dict[str, list[Any]] = {}
    for segment in segments:
        lines = segment.split("\n")
        lhs, rhs = parse("{}-to-{} map:", lines.pop(0))
        mapping.setdefault(lhs, [])

        for line in lines:
            dest_start, source_start, length = ints(line)
            source_range = range(source_start, source_start + length)
            diff = dest_start - source_start
            mapping[lhs].append((source_range, diff))
    for maps in mapping.values():

        def update(seed: int, maps: Any) -> int:
            for range_, diff in maps:
                if seed in range_:
                    return seed + diff
            return seed

        seeds = [update(seed, maps) for seed in seeds]
    return min(seeds)


EXPECTED = 35
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
