from __future__ import annotations

from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore


def main(input: str) -> (int | str | None):
    original_ = [int(line) for line in input.strip().splitlines()]
    original = [(i, v * 811589153) for i, v in enumerate(original_)]
    mixed = original.copy()

    for _ in range(10):
        for i in original:
            index = mixed.index(i)
            mixed.pop(index)
            index += i[1]
            index %= len(mixed)
            mixed.insert(index, i)

    final = [v[1] for v in mixed]
    index = final.index(0)

    return sum(
        [
            final[(index + 1000) % len(final)],
            final[(index + 2000) % len(final)],
            final[(index + 3000) % len(final)],
        ]
    )


EXPECTED = 1623178306
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
