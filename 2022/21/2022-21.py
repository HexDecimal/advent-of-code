from __future__ import annotations

import re
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore


def main(input: str, cond="<") -> (int | str | None):
    segments = input.rstrip("\n").replace("/", "//").split("\n\n")
    monkeys = {}
    lines = segments[0].split("\n")
    for line in lines:
        key, val = line.split(": ")
        monkeys[key] = val

    def recurse(key):
        value = monkeys[key]
        for sub in re.findall("[a-z]+", value):
            sub_val = recurse(sub)
            value = value.replace(sub, sub_val)

        if "~" not in value:
            value = str(eval(value))

        return f"({value})"

    # return eval(recurse("root"))  # part 1

    monkeys["root"] = monkeys["root"].replace("+", "==")

    monkeys["humn"] = "~"
    full = recurse("root")[1:-1]
    print(full)
    less_than = full.replace("==", cond)
    bits = 0
    bit = 0
    while True:
        i = bits + (1 << bit)

        lhsP, rhsP = full.replace("~", str(i)).split("==")
        print(f"{i}, {eval(lhsP)} == {eval(rhsP)}")

        if eval(full.replace("~", str(i))):
            return i
        if eval(less_than.replace("~", str(i))):
            bits = bits + (1 << (bit - 1))
            bit = 0
            continue
        bit += 1


EXPECTED = 301
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.input"
    INPUT_FILE = THIS_DIR / "input.input"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data, encoding="utf8")
    result = main(EXAMPLE_FILE.read_text(encoding="ansi"), ">")
    if result != EXPECTED:
        print(f"Expected {EXPECTED!r} but got {result!r} instead!")
        raise SystemExit()
    else:
        print("Example passed.")
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
