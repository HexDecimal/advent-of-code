from __future__ import annotations

import re
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import attrs
from aoc import reduce_multiply

Part = dict[str, int]


@attrs.define(frozen=True)
class Parts:
    x: range = range(1, 4000)
    m: range = range(1, 4000)
    a: range = range(1, 4000)
    s: range = range(1, 4000)

    def __getitem__(self, category: str) -> range:
        return getattr(self, category)

    def asdict(self) -> dict[str, range]:
        return attrs.asdict(self)

    def replace(self, category: str, value: range) -> Parts:
        vars = self.asdict()
        assert category in vars
        vars[category] = value
        return Parts(**vars)

    def sum(self) -> int:
        return reduce_multiply(v.stop - v.start + 1 for v in self.asdict().values())

    def split(self, category: str, value: int, operator: str) -> tuple[Parts | None, Parts | None]:
        values = self[category]
        left: range | None = None
        right: range | None = None
        if operator == "<":
            if values.start < value:
                left = range(values.start, min(values.stop, value - 1))
            if values.stop >= value:
                right = range(max(values.start, value), values.stop)
        else:
            if values.start <= value:
                right = range(values.start, min(values.stop, value))
            if values.stop > value:
                left = range(max(values.start, value + 1), values.stop)

        return (
            self.replace(category, left) if left is not None else None,
            self.replace(category, right) if right is not None else None,
        )


class Rule:
    def __init__(self, line: str) -> None:
        self.category = ""
        self.operator = ""
        self.value = 0
        self.dest = line
        if match := re.match(r"(\w+)([<>])(\d+):(\w+)", line):
            self.category = match[1]
            self.operator = match[2]
            self.value = int(match[3])
            self.dest = match[4]

    def test(self, parts: Parts) -> tuple[Parts | None, Parts | None]:
        if not self.operator:
            return parts, None
        return parts.split(self.category, self.value, self.operator)


Workflow = list[Rule]


def main(input: str) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    workflows: dict[str, Workflow] = {}
    lines = segments[0].split("\n")
    for line in lines:
        line = line.strip("}")  # noqa: PLW2901
        workflow_name, workflow_rules = line.split("{")
        workflows[workflow_name] = [Rule(rule_str) for rule_str in workflow_rules.split(",")]

    def test_parts(parts: Parts | None, workflow: str) -> int:
        if workflow == "A":
            assert parts
            return parts.sum()
        if workflow == "R":
            return 0

        total = 0
        for rule in workflows[workflow]:
            if not parts:
                break
            accept, parts = rule.test(parts)
            if accept:
                total += test_parts(accept, rule.dest)
        return total

    return test_parts(Parts(), "in")


EXPECTED = 167409079868000
if __name__ == "__main__":
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
