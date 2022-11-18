from __future__ import annotations

import re
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import numpy as np


class Ruleset:
    def __init__(self) -> None:
        self.rules: dict[int, str | tuple[tuple[int, ...], ...]] = {}
        self.full_rule: dict[int, str] = {}

    def add(self, rule: str) -> None:
        if match := re.match(r'(\d+): "(\w+)"', rule):
            self.rules[int(match[1])] = match[2]
            return

        match = re.match(r"(\d+): ([\d ]+)(?:\|([\d ]+))?$", rule)
        assert match

        combo1 = tuple(int(i) for i in match[2].strip().split())
        if match[3]:
            combo2 = tuple(int(i) for i in match[3].strip().split())
            self.rules[int(match[1])] = (combo1, combo2)
        else:
            self.rules[int(match[1])] = (combo1,)

    def get_rule(self, index: int, stack: int = 100) -> str:
        if stack == 0:
            return ""
        if index not in self.full_rule:
            rule = self.rules[index]
            match rule:
                case str():
                    self.full_rule[index] = rule
                case (combo1,):
                    self.full_rule[index] = "".join(self.get_rule(i, stack - 1) for i in combo1)
                case (combo1, combo2):
                    combo1_str = "".join(self.get_rule(i, stack - 1) for i in combo1)
                    combo2_str = "".join(self.get_rule(i, stack - 1) for i in combo2)
                    self.full_rule[index] = rf"(?:{combo1_str}|{combo2_str})"
                case _:
                    assert False, rule

        return self.full_rule[index]


def main(input: str) -> (int | str | None):
    segments = input.strip().split("\n\n")
    ruleset = Ruleset()
    for line in segments[0].split("\n"):
        ruleset.add(line)

    # part 2
    ruleset.add("8: 42 | 42 8")
    ruleset.add("11: 42 31 | 42 11 31")

    total = 0
    rule = re.compile(ruleset.get_rule(0) + "$")
    for line in segments[1].split("\n"):
        if rule.match(line):
            total += 1

    return total


EXPECTED = 12
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
