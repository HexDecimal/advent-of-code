import functools
import itertools
from pathlib import Path

import aocd  # type: ignore
import numpy as np

THIS_DIR = Path(__file__).parent


def main(file: Path) -> (int | str):
    with open(file, "r", encoding="utf8") as f:
        lines = f.read().strip().splitlines()
    for line in lines:
        pass
    return 0


EXPECTED = -1
if __name__ == "__main__":
    if main(THIS_DIR / "example.txt") == EXPECTED:
        aocd.submit(main(THIS_DIR / "input.txt"))
