from __future__ import annotations

import functools
import operator
import re
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import numpy as np
from numpy.typing import NDArray


class Rule:
    def __init__(self, input: str):
        match = re.match(r"(.*)?: (\d+)-(\d+) or (\d+)-(\d+)", input)
        assert match
        self.name = match[1]
        self.min1 = int(match[2])
        self.max1 = int(match[3])
        self.min2 = int(match[4])
        self.max2 = int(match[5])

    def check(self, tickets: NDArray[np.integer]) -> NDArray[np.bool_]:
        return (tickets >= self.min1) & (tickets <= self.max1) | (tickets >= self.min2) & (tickets <= self.max2)

    def where(self, tickets: NDArray[np.integer]) -> list[int]:
        """Return a list of valid column indexes."""
        valid = self.check(tickets)
        valid = valid.all(axis=0)
        where = np.argwhere(valid).ravel()
        return where.tolist()

    def __repr__(self) -> str:
        return f"{self.name}: {self.min1}-{self.max1} or {self.min2}-{self.max2}"


def part1(input: str) -> (int | str | None):
    segments = input.strip().split("\n\n")
    rules = [Rule(line) for line in segments[0].splitlines()]
    nearby_tickets = np.array([line.split(",") for line in segments[2].splitlines()[1:]], dtype=np.int32)
    any_valid = np.zeros_like(nearby_tickets, np.bool_)
    for rule in rules:
        any_valid |= (nearby_tickets >= rule.min1) & (nearby_tickets <= rule.max1)
        any_valid |= (nearby_tickets >= rule.min2) & (nearby_tickets <= rule.max2)
    return nearby_tickets[~any_valid].sum()


def sort_rules(rules: list[Rule], tickets: NDArray[np.integer]) -> list[Rule]:
    if not rules:
        return []

    valid = np.zeros_like(tickets, np.bool_)
    for rule in rules:
        valid |= (tickets >= rule.min1) & (tickets <= rule.max1)
        valid |= (tickets >= rule.min2) & (tickets <= rule.max2)
    if not valid.all():
        raise RuntimeError()

    for i in range(len(rules)):
        if rules[i].check(tickets[:, 0]).all():
            this_rule = rules[i]
            sub_rules = rules.copy()
            del sub_rules[i]
            try:
                return [this_rule] + sort_rules(sub_rules, tickets[:, 1:])
            except RuntimeError:
                pass
    else:
        raise RuntimeError()


def main(input: str) -> (int | str | None):
    segments = input.strip().split("\n\n")
    rules = [Rule(line) for line in segments[0].splitlines()]
    nearby_tickets = np.array([line.split(",") for line in segments[2].splitlines()[1:]], dtype=np.int32)
    any_valid = np.zeros_like(nearby_tickets, np.bool_)
    for rule in rules:
        any_valid |= (nearby_tickets >= rule.min1) & (nearby_tickets <= rule.max1)
        any_valid |= (nearby_tickets >= rule.min2) & (nearby_tickets <= rule.max2)

    nearby_tickets = nearby_tickets[any_valid.all(axis=1)]

    rules.sort(key=lambda x: len(x.where(nearby_tickets)))

    for r in rules:
        print(r.where(nearby_tickets))

    rules = sort_rules(rules, nearby_tickets)

    my_ticket = np.array(segments[1].splitlines()[1].split(","), dtype=np.int32)

    return functools.reduce(operator.mul, my_ticket[[r.name.startswith("departure") for r in rules]].tolist())


EXPECTED = 71
if __name__ == "__main__":
    np.seterr("raise")
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data + "\n", encoding="utf8")
    result = part1(EXAMPLE_FILE.read_text(encoding="ansi"))
    assert result == EXPECTED, f"{result} != {EXPECTED}"
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
