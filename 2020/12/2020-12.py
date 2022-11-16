from __future__ import annotations

from pathlib import Path

import aocd  # type: ignore

COMPASS = {
    "N": (0, 1),
    "S": (0, -1),
    "W": (-1, 0),
    "E": (1, 0),
}

DIRS = "ESWN"


def main(file: Path) -> (int | str | None):
    segments = file.read_text(encoding="ansi").strip().split("\n\n")
    ship_x = ship_y = 0
    way_x, way_y = 10, 1
    dir = 0
    lines = segments[0].split("\n")
    for line in lines:
        print(line, end=": ")
        cmd = line[0]
        value = int(line[1:])
        if cmd == "F":
            ship_x += way_x * value
            ship_y += way_y * value
        elif cmd in COMPASS:
            way_x += COMPASS[cmd][0] * value
            way_y += COMPASS[cmd][1] * value
        elif cmd in "LR":
            if cmd == "L":
                value *= -1
            rotate = (dir + 4 + value // 90) % 4
            while rotate:
                rotate -= 1
                way_x, way_y = way_y, -way_x

        print(f"{way_x=}, {way_y=}, {dir=}")

    return abs(ship_x) + abs(ship_y)


EXPECTED = 286
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data + "\n", encoding="utf8")
    if main(EXAMPLE_FILE) == EXPECTED:
        aocd.submit(main(INPUT_FILE))
