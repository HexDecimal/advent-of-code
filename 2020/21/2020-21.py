from __future__ import annotations

import functools
import itertools
import operator
import re
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import numpy as np
from numpy.typing import NDArray

reduce_multiply = functools.partial(functools.reduce, operator.mul)


def main(input: str) -> (int | str | None):
    segments = input.strip().split("\n\n")
    lines = segments[0].split("\n")
    listing: dict[frozenset, frozenset] = {}
    for line in lines:
        match = re.match(r"(?P<ingredients>[\w ]+) \(contains (?P<allergens>[\w, ]+)\)", line)
        assert match
        listing[frozenset(match["ingredients"].split())] = frozenset(match["allergens"].split(", "))

    all_ingredients = frozenset[str](itertools.chain.from_iterable(listing.keys()))
    all_allergens = frozenset[str](itertools.chain.from_iterable(listing.values()))

    allergens_for_ingredient = {i: set[str]() for i in all_ingredients}
    for k, v in listing.items():
        for i in k:
            allergens_for_ingredient[i] |= v

    potential_allergens = {i: set[str]() for i in all_allergens}
    for ingredients, allergens in allergens_for_ingredient.items():
        for i in allergens:
            potential_allergens[i].add(ingredients)

    allergens_sorted = list(sorted(all_allergens))

    def solve_allergens():
        pass

    ingredients_with_no_allergens = {k for k, v in allergens_for_ingredient.items() if not v}

    count = 0
    for k in listing.keys():
        count += len(k & ingredients_with_no_allergens)

    return count


EXPECTED = 5
if __name__ == "__main__":
    np.seterr("raise")
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data + "\n", encoding="utf8")
    result = main(EXAMPLE_FILE.read_text(encoding="ansi"))
    assert result == EXPECTED, f"{result} != {EXPECTED}"
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
