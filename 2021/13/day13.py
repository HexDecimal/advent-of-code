import re
from pathlib import Path

import numpy as np


def main(file: Path) -> (int | str):
    with open(file, "r", encoding="utf8") as f:
        marks_, cmds = f.read().strip().split("\n\n")
    dots: set[tuple[int, int]] = set()
    for line in marks_.split("\n"):
        x_, y_ = line.split(",")
        dots.add((int(x_), int(y_)))

    for cmd in cmds.split("\n"):
        print(cmd)
        match = re.match("fold along (\w)=(\d+)", cmd)
        assert match
        axis_, at_ = match.groups()
        axis = {"x": 0, "y": 1}[axis_]
        at = int(at_)
        for xy in list(dots):
            if xy[axis] > at:
                dots.remove(xy)
                if axis == 0:
                    new_xy = at - (xy[0] - at), xy[1]
                else:
                    new_xy = xy[0], at - (xy[1] - at)
                print(f"{xy} -> {new_xy}")
                dots.add(new_xy)

    print(len(dots))
    xx, yy = zip(*dots)
    a = np.zeros((max(xx) + 1, max(yy) + 1), bool)
    for x, y in dots:
        a[x, y] = True
    for row in a.T:
        print("".join(" #"[x] for x in row))
    return len(dots)


EXPECTED = 17
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    main(INPUT_FILE)
