import itertools
from pathlib import Path

import numpy as np

THIS_DIR = Path(__file__).parent
FILE = THIS_DIR / "example.txt"
FILE = THIS_DIR / "input.txt"


def main() -> None:
    with open(FILE, "r", encoding="utf8") as f:
        lines = f.read().strip().splitlines()
    octopus = np.asarray([[int(c) for c in line] for line in lines], dtype=int)
    flashes = 0
    for step in itertools.count(1):
        octopus += 1
        flashed = np.zeros_like(octopus, dtype=bool)
        while True:
            flashing = (octopus > 9) & ~flashed
            if not flashing.any():
                break
            flashed |= flashing
            if flashed.all():
                print(step)
                return
            for i, j in np.argwhere(flashing):
                flashes += 1
                octopus[max(0, i - 1) : i + 2, max(0, j - 1) : j + 2] += 1
        octopus[flashed] = 0
    print(flashes)


if __name__ == "__main__":
    main()
