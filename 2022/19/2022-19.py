from __future__ import annotations

import functools
import itertools
import operator
import re
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import numpy as np
from aoc import as_array, as_bool_array, as_ord_array, ints, reduce_multiply, split_ints
from numpy.typing import NDArray
from parse import parse
import attrs
import multiprocessing.pool

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3


class Resources(NamedTuple):
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0


class Blueprint:
    def __init__(self, line: str) -> None:
        (
            self.index,
            self.ore_ore,
            self.clay_ore,
            self.obsidian_ore,
            self.obsidian_clay,
            self.geode_ore,
            self.geode_obsidian,
        ) = ints(line)
        self.max_bots = Resources(
            max(self.ore_ore, self.clay_ore, self.geode_ore), self.obsidian_clay, self.geode_obsidian
        )


@attrs.define
class State:
    resources: Resources = Resources()
    bots: Resources = Resources(ore=1)
    time_left: int = 24
    snubbed: frozenset[int] = frozenset()
    history: str = ""

    def get_options(self, bp: Blueprint) -> set[int]:
        options: set[int] = set()
        if self.resources.ore >= bp.ore_ore and self.bots.ore < bp.max_bots.ore:
            options.add(ORE)
        if self.resources.ore >= bp.clay_ore and self.bots.clay < bp.max_bots.clay:
            options.add(CLAY)
        if (
            self.resources.ore >= bp.obsidian_ore
            and self.resources.clay >= bp.obsidian_clay
            and self.bots.obsidian < bp.max_bots.obsidian
        ):
            options.add(OBSIDIAN)
        if self.resources.ore >= bp.geode_ore and self.resources.obsidian >= bp.geode_obsidian:
            options.add(GEODE)
        return options - self.snubbed

    def advance(self, bp: Blueprint, build: None | int) -> State:
        snubbed = self.snubbed
        resources = Resources(*(a + b for a, b in zip(self.resources, self.bots)))
        bots = self.bots
        if build is None:
            snubbed |= self.get_options(bp)
            history = self.history + "-"
        elif build == 0:
            resources = resources._replace(ore=resources.ore - bp.ore_ore)
            bots = bots._replace(ore=bots.ore + 1)
            snubbed = frozenset()
            history = self.history + "R"
        elif build == 1:
            resources = resources._replace(ore=resources.ore - bp.clay_ore)
            bots = bots._replace(clay=bots.clay + 1)
            snubbed = frozenset()
            history = self.history + "C"
        elif build == 2:
            resources = resources._replace(ore=resources.ore - bp.obsidian_ore, clay=resources.clay - bp.obsidian_clay)
            bots = bots._replace(obsidian=bots.obsidian + 1)
            snubbed = frozenset()
            history = self.history + "B"
        elif build == 3:
            resources = resources._replace(
                clay=resources.clay - bp.obsidian_clay, obsidian=resources.obsidian - bp.geode_obsidian
            )
            bots = bots._replace(geode=bots.geode + 1)
            snubbed = frozenset()
            history = self.history + "G"
        return State(resources, bots, self.time_left - 1, snubbed, history)

    def solve(self, bp: Blueprint) -> State:
        if self.time_left == 1:
            return self.advance(bp, None)
        options = self.get_options(bp)
        states = [self.advance(bp, opt).solve(bp) for opt in (*options, None)]
        return max(states, key=lambda s: s.resources.geode)


def run(line: str) -> int:
    bp = Blueprint(line)
    solved = State().solve(bp)
    print(f"Blueprint{bp.index:3d}:{solved.resources.geode:3d}, {solved.history}")
    return solved.resources.geode * bp.index


def main(input: str) -> (int | str | None):
    segments = input.rstrip("\n").split("\n\n")

    return sum(pool.map(run, segments[0].split("\n"), 1))


EXPECTED = 33
if __name__ == "__main__":
    pool = multiprocessing.pool.Pool()
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.input"
    INPUT_FILE = THIS_DIR / "input.input"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data, encoding="utf8")
    result = main(EXAMPLE_FILE.read_text(encoding="ansi"))
    if result != EXPECTED:
        print(f"Expected {EXPECTED!r} but got {result!r} instead!")
        raise SystemExit()
    else:
        print("Example passed.")
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
