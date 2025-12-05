from __future__ import annotations

from pathlib import Path

import aoc
import aocd  # type: ignore[import-untyped]
import scipy.signal  # type: ignore[import-untyped]


def main(input: str) -> int | str | None:  # noqa: A002
    paper = aoc.as_bool_array(input.strip(), "@")
    total = 0
    while True:
        neighbors = scipy.signal.convolve2d(paper, [[1, 1, 1], [1, 0, 1], [1, 1, 1]], mode="same")
        to_remove = paper & (neighbors < 4)
        removed = to_remove.sum()
        total += removed
        if not removed:
            break
        paper &= ~to_remove
    return total


EXPECTED = 43
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
