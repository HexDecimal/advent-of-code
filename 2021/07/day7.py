from functools import lru_cache
from pathlib import Path
from typing import Counter

import numpy as np

THIS_DIR = Path(__file__).parent

with open(THIS_DIR / "input.txt", "r", encoding="utf8") as f:
    crabs = [int(s) for s in f.read().strip().split(",")]


costs = [0]


def get_cost(dist: int):
    while len(costs) <= dist:
        costs.append(costs[-1] + len(costs))
    return costs[dist]


tests = Counter[int]()

for i in range(min(crabs), max(crabs) + 1):
    for crab in crabs:
        tests[i] += get_cost(abs(crab - i))

print(min((fuel, pos) for pos, fuel in tests.items()))
