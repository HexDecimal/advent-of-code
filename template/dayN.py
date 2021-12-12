import functools
import itertools
from pathlib import Path

import aocd  # type: ignore
import numpy as np


def main(file: Path) -> (int | str):
    with open(file, "r", encoding="utf8") as f:
        lines = f.read().strip().splitlines()
    for line in lines:
        pass
    return 0


EXPECTED = -1
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
