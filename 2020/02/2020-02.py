from __future__ import annotations

import re
from pathlib import Path

import aocd  # type: ignore


def main(file: Path) -> (int | str | None):
    segments = file.read_text(encoding="ansi").strip().split("\n\n")
    count = 0
    for line in segments[0].split("\n"):
        match = re.match(r"(\d+)-(\d+) (\w): (\w+)", line)
        assert match
        low_, high_, ch, password = match.groups()
        low = int(low_) - 1
        high = int(high_) - 1
        if (password[low] == ch) + (password[high] == ch) == 1:
            count += 1
    return count


EXPECTED = 1
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data + "\n", encoding="utf8")
    if main(EXAMPLE_FILE) == EXPECTED:
        aocd.submit(main(INPUT_FILE))
