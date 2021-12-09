from pathlib import Path

import numpy as np

THIS_DIR = Path(__file__).parent
FILE = THIS_DIR / "example.txt"
# FILE = THIS_DIR / "input.txt"

with open(FILE, "r", encoding="utf8") as f:
    f.read().strip().splitlines()
