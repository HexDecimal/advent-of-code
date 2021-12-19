from __future__ import annotations

import itertools
from pathlib import Path
from typing import Any, Iterator, Optional

import numpy as np

XYZ = tuple[int, int, int]


def get_matrix() -> Iterator[Any]:
    for xd, yd, zd in itertools.product([-1, 1], [-1, 1], [-1, 1]):
        for xa, ya, za in itertools.permutations((0, 1, 2)):
            matrix = np.zeros((3, 3), int)
            matrix[0, xa] = xd
            matrix[1, ya] = yd
            matrix[2, za] = zd
            print(matrix)
            yield matrix


ROTATIONS = list(get_matrix())


class Scanner:
    def __init__(self, index: int, beacons: set[XYZ], pos: Optional[XYZ] = None, parent: Optional[Scanner] = None):
        self.index = index
        self.beacons = beacons
        self.parent = parent
        self.pos = pos
        self.others: dict[Scanner, XYZ] = {}

    def get_all_beacons(self, pos: XYZ = (0, 0, 0), ignore: Optional[set[Scanner]] = None):
        if ignore is None:
            ignore = set()
        elif self in ignore:
            return
        ignore.add(self)
        sx, sy, sz = pos
        yield from ((x + sx, y + sy, z + sz) for (x, y, z) in self.beacons)
        for other, (ox, oy, oz) in self.others.items():
            yield from other.get_all_beacons((sx + ox, sy + oy, sz + oz), ignore)

    def rotations(self) -> Iterator[Scanner]:
        assert not self.others
        beacons = self.beacons
        for matrix in ROTATIONS:
            self.beacons = {tuple((matrix @ xyz).tolist()) for xyz in beacons}  # type: ignore
            yield self

    def __repr__(self) -> str:
        return f"Scanner{self.index}"


def main(file: Path) -> (int | str):
    with open(file, "r", encoding="utf8") as f:
        scanner_in = f.read().strip().split("\n\n")

    scanners: list[Scanner] = []

    for i, section in enumerate(scanner_in):
        lines = section.split("\n")[1:]
        beacons = {tuple(int(x_) for x_ in line.split(",")) for line in lines}
        scanners.append(
            Scanner(
                i,
                beacons,  # type: ignore
            )
        )

    scanners[0].pos = (0, 0, 0)
    root = scanners[0]

    while set(root.others) != set(scanners[1:]):
        for scanner2 in scanners[1:]:
            if scanner2 in root.others:
                continue
            print(f"{root.index} -> {scanner2.index}")
            for scanner2 in scanner2.rotations():
                for beacon1 in root.beacons:
                    for beacon2 in scanner2.beacons:
                        dx, dy, dz = beacon2[0] - beacon1[0], beacon2[1] - beacon1[1], beacon2[2] - beacon1[2]
                        relative = {(x - dx, y - dy, z - dz) for x, y, z in scanner2.beacons}
                        matches = len(root.beacons.intersection(relative))
                        if matches >= 12:
                            print(matches)
                            print(f"found {(dx, dy, dz)}")
                            root.others[scanner2] = (-dx, -dy, -dz)
                            root.beacons |= relative
                            # scanner2.others[root] = (-dx, -dy, -dz)
                            break
                    if scanner2 in root.others:
                        break
                if scanner2 in root.others:
                    break
            print(root.others)
    result = len(root.beacons)
    print(result)
    return result


EXPECTED = 79
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if main(EXAMPLE_FILE) == EXPECTED:
        main(INPUT_FILE)
