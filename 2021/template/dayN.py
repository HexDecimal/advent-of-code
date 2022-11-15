from __future__ import annotations

import functools
import itertools
from pathlib import Path

import aocd  # type: ignore
import numpy as np


def main(file: Path) -> (int | str | None):
    with open(file, "r", encoding="utf8") as f:
        (lines,) = f.read().strip().split("\n\n")
    for line in lines.split("\n"):
        pass
    return None


EXPECTED = 0
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if not INPUT_FILE.exists():
        data = aocd.get_data() + "\n"
        with open(INPUT_FILE, "w", encoding="utf8") as f:
            f.write(data)
    if main(EXAMPLE_FILE) == EXPECTED:
        aocd.submit(main(INPUT_FILE))
