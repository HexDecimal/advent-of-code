from __future__ import annotations

import itertools
from pathlib import Path

import aocd  # type: ignore
import numpy as np


def find_contiguous_set(lines: list[int], target: int) -> None | int:
    total = lines[0]
    for i, it in enumerate(lines[1:], start=1):
        total += it
        if total == target:
            return min(lines[:i]) + max(lines[:i])
        if total > target:
            return None
    assert None


def main(file: Path, preamble: int) -> (int | str | None):
    segments = file.read_text(encoding="ansi").strip().split("\n\n")
    lines: list[int] = np.asarray(segments[0].split(), np.uint64).tolist()
    for i in range(preamble, len(lines)):
        target = lines[i]
        if not any(sum(test) == target for test in itertools.combinations(lines[i - preamble : i], 2)):
            for j in range(len(lines)):
                if found := find_contiguous_set(lines[j:], target):
                    return found

    return None


EXPECTED = 62
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data + "\n", encoding="utf8")
    if main(EXAMPLE_FILE, 5) == EXPECTED:
        aocd.submit(main(INPUT_FILE, 25))
