from __future__ import annotations

from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
from aoc import ints, reduce_multiply
from parse import parse


def fix_worry(v: int, factor: int) -> int:
    v -= v // factor * factor
    return v


class Monkey:
    def __init__(self, segment: str) -> None:
        lines = segment.strip().splitlines()
        self.id: int = parse("Monkey {:d}:", lines[0])[0]
        self.items = ints(parse("  Starting items: {}", lines[1])[0])
        self.operation: str = parse("  Operation: new = {}", lines[2])[0]
        if self.operation == "old * old":
            self.operation_lambda = lambda x: x * x
        else:
            rhs = ints(self.operation)[-1]
            if "*" in self.operation:
                self.operation_lambda = lambda x: x * rhs
            else:
                self.operation_lambda = lambda x: x + rhs

        self.div_test: int = parse("  Test: divisible by {:d}", lines[3])[0]
        self.send = ints(lines[5])[0], ints(lines[4])[0]
        self.inspects = 0

    def do_op(self, v: int) -> int:
        return self.operation_lambda(v)
        v = int(eval(self.operation.replace("old", str(v))))
        return v

    def send_to(self, v: int) -> int:
        return self.send[v % self.div_test == 0]


def main(input: str) -> (int | str | None):
    segments = input.rstrip("\n").split("\n\n")
    monkeys = [Monkey(s) for s in segments]
    factor: int = reduce_multiply(m.div_test for m in monkeys)  # type: ignore
    for round in range(1, 10001):
        for m in monkeys:
            m.items = [fix_worry(m.do_op(v), factor) for v in m.items]
            m.inspects += len(m.items)
            while m.items:
                next_m = m.send_to(m.items[0])
                monkeys[next_m].items.append(m.items.pop(0))
        if round in {1, 20, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000}:
            print(f"{round}: {[m.inspects for m in monkeys]}")

    monkeys.sort(key=lambda m: m.inspects)
    print(monkeys[-1].inspects, monkeys[-2].inspects)
    return monkeys[-1].inspects * monkeys[-2].inspects


EXPECTED = 2713310158
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
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
