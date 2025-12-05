from __future__ import annotations

from pathlib import Path

import aocd  # type: ignore[import-untyped]


def main(input: str) -> int | str | None:  # noqa: A002
    segments = input.rstrip("\n").split("\n\n")
    lines = segments[0].split("\n")
    position = 50
    hits = 0
    for line in lines:
        match (line[0], int(line[1:])):
            case ["L", amount]:
                sign = -1
            case ["R", amount]:
                sign = 1
        while amount:
            amount -= 1
            position += sign
            position %= 100
            if position == 0:
                hits += 1

    return hits


EXPECTED = 6
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.input"
    INPUT_FILE = THIS_DIR / "input.input"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data, encoding="utf8")
    result = main(EXAMPLE_FILE.read_text(encoding="ansi"))
    if result != EXPECTED:
        print(f"Expected {EXPECTED!r} but got {result!r} instead!")
        raise SystemExit
    else:
        print("Example passed.")
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
