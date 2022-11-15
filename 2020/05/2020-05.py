from __future__ import annotations

from pathlib import Path

import aocd  # type: ignore


def get_seat(seat: str) -> tuple[int, int, int]:
    """Return (row, column, id)"""
    row = 0
    column = 0
    for i, ch in enumerate(reversed(seat[:7])):
        if ch == "B":
            row += 1 << i
    for i, ch in enumerate(reversed(seat[7:])):
        if ch == "R":
            column += 1 << i
    return row, column, row * 8 + column


def main(file: Path) -> (int | str | None):
    segments = file.read_text(encoding="ansi").strip().split("\n\n")
    # lines = np.asarray(segments[0], int)
    lines = segments[0].split("\n")
    seats = {get_seat(line)[2] for line in lines}
    for i in seats:
        if i + 1 not in seats and i + 2 in seats:
            return i + 1
    return None


assert get_seat("BFFFBBFRRR") == (70, 7, 567), get_seat("BFFFBBFRRR")
assert get_seat("FFFBBBFRRR") == (14, 7, 119), get_seat("FFFBBBFRRR")
assert get_seat("BBFFBBFRLL") == (102, 4, 820), get_seat("BBFFBBFRLL")


if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data + "\n", encoding="utf8")
    aocd.submit(main(INPUT_FILE))
