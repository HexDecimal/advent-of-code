from __future__ import annotations

from pathlib import Path

import aocd  # type: ignore[import-untyped]


def main(input: str) -> int | str | None:  # noqa: A002
    banks = [[int(c) for c in line] for line in input.splitlines()]
    total = 0
    for bank in banks:
        value = 0
        for i in range(11, -1, -1):
            best = max(bank[: -i if i else None])
            bank = bank[bank.index(best) + 1 :]  # noqa: PLW2901
            value = value * 10 + best
        print(value)
        total += value

    return total


EXPECTED = 3121910778619
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
