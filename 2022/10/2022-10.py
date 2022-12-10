from __future__ import annotations

from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore


def main(input: str) -> (int | str | None):
    segments = input.rstrip("\n").split("\n\n")
    lines = segments[0].split("\n")
    cycle = 0
    signal = 1
    total = 0

    def add_cycle() -> None:
        nonlocal cycle, total
        cycle += 1
        if cycle in {20, 60, 100, 140, 180, 220}:
            # print(cycle, signal)
            total += cycle * signal

        print("#" if abs(cycle % 40 - signal - 1) <= 1 else ".", end="")
        if cycle % 40 == 0:
            print()

    for line in lines:
        match line.split():
            case ["noop"]:
                add_cycle()
            case ["addx", x]:
                add_cycle()
                add_cycle()
                signal += int(x)
    return total


EXPECTED = 13140
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.input"
    INPUT_FILE = THIS_DIR / "input.input"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data, encoding="utf8")
    # result = main(EXAMPLE_FILE.read_text(encoding="ansi"))
    # if result != EXPECTED:
    #    print(f"Expected {EXPECTED!r} but got {result!r} instead!")
    #    raise SystemExit()
    # aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
    main(INPUT_FILE.read_text(encoding="ansi"))
