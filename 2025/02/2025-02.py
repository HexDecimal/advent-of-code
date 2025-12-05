from __future__ import annotations

from pathlib import Path

import aoc
import aocd  # type: ignore[import-untyped]


def main(input: str) -> int | str | None:  # noqa: A002
    ranges = aoc.split_ints(input.strip(), (",", "-"))
    total = 0
    for low, high in ranges:
        print(f"{low}-{high}")
        for i in range(low, high + 1):
            string = str(i)
            string_len = len(string)
            for pattern_size in range(1, (string_len // 2) + 1):
                string = str(i)
                if string_len % pattern_size != 0:
                    continue
                pattern, string = string[:pattern_size], string[pattern_size:]
                while string and string[:pattern_size] == pattern:
                    string = string[pattern_size:]
                if not string:
                    total += i
                    print(i)
                    break

    return total


EXPECTED = 4174379265
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
