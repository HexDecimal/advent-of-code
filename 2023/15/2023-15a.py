from __future__ import annotations

from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore


def str_hash(string: str) -> int:
    result = 0
    for c in string:
        result = ((result + ord(c)) * 17) % 256
    return result


def main(input: str) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    (line,) = segments[0].split("\n")

    return sum(str_hash(command) for command in line.split(","))


EXPECTED = 1320
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
