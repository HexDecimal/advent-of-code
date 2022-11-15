from __future__ import annotations

import functools
import itertools
from collections import Counter
from pathlib import Path

import aocd  # type: ignore
import numpy as np


def main(file: Path) -> (int | str | None):
    segments = file.read_text(encoding="ansi").strip().split("\n\n")
    # lines = np.asarray(segments[0].split(), np.int64)
    # lines = [int(i) for i in segments[0].split()]
    lines = segments[0].split("\n")
    for line in lines:
        pass
    return None


EXPECTED = 0
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data + "\n", encoding="utf8")
    if main(EXAMPLE_FILE) == EXPECTED:
        aocd.submit(main(INPUT_FILE))
