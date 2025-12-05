from __future__ import annotations

from pathlib import Path

import aocd  # type: ignore[import-untyped]


def main(input: str) -> int | str | None:  # noqa: A002
    ranges_, ingredients = input.rstrip("\n").split("\n\n")
    ranges = []
    for line in ranges_.split("\n"):
        i_, j_ = line.split("-")
        ranges.append(range(int(i_), int(j_) + 1))

    total = 0
    for i in [int(s) for s in ingredients.split("\n")]:
        if any(i in r for r in ranges):
            total += 1

    return total


EXPECTED = 3
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
