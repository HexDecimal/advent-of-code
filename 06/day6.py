import math
from pathlib import Path
from typing import Counter

import numpy as np

THIS_DIR = Path(__file__).parent

fish = Counter[int]()

with open(THIS_DIR / "input.txt", "r", encoding="utf8") as f:
    for intstr in f.read().strip().split(","):
        fish[int(intstr)] += 1


def step(current_fish: Counter[int]) -> Counter[int]:
    next_fish = Counter[int]()
    for i, n in sorted(current_fish.items()):
        if i == 0:
            next_fish[6] += n
            next_fish[8] += n
        else:
            next_fish[i - 1] += n
    return next_fish


for _ in range(256):
    fish = step(fish)

print(sum(fish.values()))
