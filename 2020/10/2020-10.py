from __future__ import annotations

import functools
from pathlib import Path

import aocd  # type: ignore


@functools.cache
def count_possible_adaptors(current: int, adaptors: tuple[int]) -> int:
    if not adaptors:
        return 1
    total = 0
    for i, adaptor in enumerate(adaptors, start=1):
        if adaptor - current > 3:
            return total
        total += count_possible_adaptors(adaptor, adaptors[i:])
    return total


def main(file: Path) -> (int | str | None):
    segments = file.read_text(encoding="ansi").strip().split("\n\n")
    adaptors = tuple(sorted(int(i) for i in segments[0].split()))
    adaptors += (adaptors[-1] + 3,)
    print(count_possible_adaptors(0, adaptors))
    return count_possible_adaptors(0, adaptors)


EXPECTED = 19208
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data + "\n", encoding="utf8")
    if main(EXAMPLE_FILE) == EXPECTED:
        aocd.submit(main(INPUT_FILE))
