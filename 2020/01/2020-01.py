from __future__ import annotations

import itertools
from pathlib import Path

import aocd  # type: ignore
import numpy as np


def main(file: Path) -> (int | str | None):
    segments = file.read_text(encoding="ansi").strip().split("\n\n")
    lines = np.asarray(segments[0].split(), int)
    for a, b, c in itertools.combinations(lines, 3):
        if a + b + c == 2020:
            return a * b * c
    return None


EXPECTED = 241861950
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data + "\n", encoding="ansi")
    if main(EXAMPLE_FILE) == EXPECTED:
        aocd.submit(main(INPUT_FILE))
