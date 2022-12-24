from __future__ import annotations

from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
from aoc import ints, reduce_multiply
import attrs
import multiprocessing.pool
import heapq

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

    def solve(self) -> int:
        heap = [((0, 0, 0, 0), State())]
        best = 0
        touched = set()
        flow = {}
        best_flow = State()

        while heap:
            _, old_state = heapq.heappop(heap)
            for opt in old_state.get_options(self):
                new_state = old_state.advance(self, opt)
                if new_state in touched:
                    continue
                touched.add(new_state)
                flow[new_state] = (old_state, opt)
                new_potential = new_state.potential
                if new_potential < best:
                    continue
                if new_state.score > best:
                    best = new_state.score
                    print(f"Blueprint {self.index}, best geodes: {best}, heap: {len(heap)}")
                    continue
                if new_state.time_left:
                    heapq.heappush(
                        heap,
                        (
                            (
                                -new_state.resources.geode,
                                -new_state.resources.obsidian,
                                -new_state.resources.clay,
                                new_state.time_left,
                            ),
                            new_state,
                        ),
                    )
                elif new_state.resources.geode == best:
                    best_flow = new_state

        history = ""
        while best_flow in flow:
            best_flow, opt = flow[best_flow]
            history += "RCBG"[opt] if opt is not None else "-"
        print(f"Blueprint {self.index}: {best}: {history[::-1]}")
        return best


@attrs.define(frozen=True, order=True)
class State:
    resources: Resources = Resources()
    bots: Resources = Resources(ore=1)
    time_left: int = 32
    snubbed: frozenset[int] = frozenset()

    def get_options(self, bp: Blueprint) -> Sequence[None | int]:
        if self.time_left <= 1:
            return ()
        options: list[None | int] = [None]
        if self.resources.ore >= bp.ore_ore and self.bots.ore < bp.max_bots.ore:
            options.append(ORE)
        if self.resources.ore >= bp.clay_ore and self.bots.clay < bp.max_bots.clay:
            options.append(CLAY)
        if (
            self.resources.ore >= bp.obsidian_ore
            and self.resources.clay >= bp.obsidian_clay
            and self.bots.obsidian < bp.max_bots.obsidian
        ):
            options.append(OBSIDIAN)
        if self.resources.ore >= bp.geode_ore and self.resources.obsidian >= bp.geode_obsidian:
            options.append(GEODE)
        return options[::-1]  # - self.snubbed

    @property
    def potential(self) -> int:
        result = self.resources.geode
        bots = self.bots.geode
        for i in range(self.time_left):
            result += bots
            bots += 1
        return result

    @property
    def score(self) -> int:
        return self.resources.geode + self.time_left * self.bots.geode

    def advance(self, bp: Blueprint, build: None | int) -> State:
        assert self.time_left > 0
        snubbed = self.snubbed
        resources = Resources(*(a + b for a, b in zip(self.resources, self.bots)))
        bots = self.bots
        if build is None:
            pass  # snubbed |= self.get_options(bp)
        elif build == 0:
            resources = resources._replace(ore=resources.ore - bp.ore_ore)
            bots = bots._replace(ore=bots.ore + 1)
            snubbed = frozenset()
        elif build == 1:
            resources = resources._replace(ore=resources.ore - bp.clay_ore)
            bots = bots._replace(clay=bots.clay + 1)
            snubbed = frozenset()
        elif build == 2:
            resources = resources._replace(
                ore=resources.ore - bp.obsidian_ore,
                clay=resources.clay - bp.obsidian_clay,
            )
            bots = bots._replace(obsidian=bots.obsidian + 1)
            snubbed = frozenset()
        elif build == 3:
            resources = resources._replace(
                ore=resources.ore - bp.geode_ore,
                obsidian=resources.obsidian - bp.geode_obsidian,
            )
            bots = bots._replace(geode=bots.geode + 1)
            snubbed = frozenset()
        else:
            assert False
        return State(resources, bots, self.time_left - 1, snubbed)


def run(bp: Blueprint) -> int:
    return bp.solve()


def main(input: str) -> (int | str | None):
    segments = input.rstrip("\n").split("\n\n")
    blueprints = [Blueprint(line) for line in segments[0].split("\n")]

    # return sum(map(run, blueprints[:3]))
    return reduce_multiply(pool.map(run, blueprints[:3], 1))  # type: ignore[return-value]


if __name__ == "__main__":
    pool = multiprocessing.pool.Pool(3)
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.input"
    INPUT_FILE = THIS_DIR / "input.input"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data, encoding="utf8")
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
