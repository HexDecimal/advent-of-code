from pathlib import Path

import numpy as np

THIS_DIR = Path(__file__).parent
FILE = THIS_DIR / "example.txt"
# FILE = THIS_DIR / "input.txt"


def main() -> None:
    with open(FILE, "r", encoding="utf8") as f:
        lines = f.read().strip().splitlines()
    for line in lines:
        pass


if __name__ == "__main__":
    main()
