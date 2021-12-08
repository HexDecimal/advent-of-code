import itertools
from pathlib import Path

import numpy as np

THIS_DIR = Path(__file__).parent

count = 0

DIGITS = {
    0: frozenset("abcefg"),
    1: frozenset("cf"),
    2: frozenset("acdeg"),
    3: frozenset("acdfg"),
    4: frozenset("bdcf"),
    5: frozenset("abdfg"),
    6: frozenset("abdefg"),
    7: frozenset("acf"),
    8: frozenset("abcdefg"),
    9: frozenset("abcdfg"),
}
DIGITS_INV = {v: k for k, v in DIGITS.items()}

ALL_DIGITS: dict[frozenset[frozenset[str]], dict[frozenset[str], int]] = {}

for mutation in itertools.permutations("abcdefg"):
    translate = {a: b for a, b in zip("abcdefg", mutation)}

    circuts = {frozenset(translate[i] for i in c): d for c, d in DIGITS_INV.items()}
    ALL_DIGITS[frozenset(circuts.keys())] = circuts


with open(THIS_DIR / "input.txt", "r", encoding="utf8") as f:
    for line in f.read().strip().splitlines():
        sample_s, display_s = line.split(" | ")
        display = [frozenset(string) for string in display_s.split()]
        samples = set([frozenset(string) for string in sample_s.split()] + display)
        known: dict[int, frozenset[str]] = {}
        known_inv: dict[frozenset[str], int] = {}
        for check, mapping in ALL_DIGITS.items():
            if not samples.issubset(check):
                continue
            display_count = 0
            for s in display:
                display_count *= 10
                display_count += mapping[s]
            count += display_count
            break

print(count)
