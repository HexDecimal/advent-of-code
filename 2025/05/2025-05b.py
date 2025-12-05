from __future__ import annotations

from pathlib import Path

import aocd  # type: ignore[import-untyped]


def main(input: str) -> int | str | None:  # noqa: A002
    ranges_, _ = input.rstrip("\n").split("\n\n")
    ranges: list[range] = []
    for line in ranges_.split("\n"):
        i_, j_ = line.split("-")
        ranges.append(range(int(i_), int(j_) + 1))

    ranges.sort(key=lambda r: r.start)

    total = 0
    while ranges:
        lowest_range = ranges.pop(0)
        if lowest_range.start >= lowest_range.stop:
            continue
        total += len(lowest_range)
        ranges = [range(max(r.start, lowest_range.stop), r.stop) for r in ranges]

    return total


EXPECTED = 14
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
