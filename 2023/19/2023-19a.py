from __future__ import annotations

import re
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore

Part = dict[str, int]


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

    def test(self, part: Part) -> bool:
        match self.operator:
            case "<":
                return part[self.category] < self.value
            case ">":
                return part[self.category] > self.value
            case _:
                return True


Workflow = list[Rule]


def main(input: str) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    workflows = {}
    lines = segments[0].split("\n")
    for line in lines:
        line = line.strip("}")  # noqa: PLW2901
        workflow_name, workflow_rules = line.split("{")
        workflows[workflow_name] = [Rule(rule_str) for rule_str in workflow_rules.split(",")]
    total = 0
    for line in segments[1].split("\n"):
        part = {s[0]: int(s[2:]) for s in line.strip("{}").split(",")}
        current_workflow = "in"
        while current_workflow not in ("A", "R"):
            for rule in workflows[current_workflow]:
                if rule.test(part):
                    current_workflow = rule.dest
                    break
        if current_workflow == "A":
            total += sum(part.values())

    return total


EXPECTED = 19114
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
