from __future__ import annotations

import functools
import itertools
import re
from pathlib import Path
from typing import Any, Iterator, MutableSequence, Optional, Sequence

import aocd  # type: ignore
import numpy as np
import scipy.sparse

CODES = re.compile(R"(\w+) x=([0-9-]+)..([0-9-]+),y=([0-9-]+)..([0-9-]+),z=([0-9-]+)..([0-9-]+)")


def part1(file: Path) -> (int | str):
    with open(file, "r", encoding="utf8") as f:
        (lines,) = f.read().strip().split("\n\n")
    cubes = np.zeros((101, 101, 101), bool)
    for line in lines.split("\n"):
        match = CODES.match(line)
        assert match
        bool_, *values_ = match.groups()
        on = bool_ == "on"
        min_x, max_x, min_y, max_y, min_z, max_z = [int(v) for v in values_]
        min_x = max(0, min_x + 50)
        min_y = max(0, min_y + 50)
        min_z = max(0, min_z + 50)
        max_x = max_x + 51
        max_y = max_y + 51
        max_z = max_z + 51
        cubes[min_x:max_x, min_y:max_y, min_z:max_z] = on

    print(cubes.sum())
    return cubes.sum()


class QuadTree:
    def __init__(self, size):
        pass


def parse(lines: str) -> Iterator[tuple[bool, Rect]]:
    for line in lines.split("\n"):
        match = CODES.match(line)
        assert match
        bool_, *values_ = match.groups()
        on = bool_ == "on"
        min_x, max_x, min_y, max_y, min_z, max_z = [int(v) for v in values_]
        yield on, Rect((min_x, max_x + 1), (min_y, max_y + 1), (min_z, max_z + 1))


def _handle_slice(s: slice, dir: int) -> slice:
    if dir == -1:
        s = slice(-s.stop, -s.start)
    return slice(max(s.start, 0), max(0, s.stop))


def iter_slices(slices: tuple[slice, slice, slice]) -> Iterator[tuple[slice, slice, slice]]:
    for dir in itertools.product((-1, 1), (-1, 1), (-1, 1)):
        yield tuple(_handle_slice(s, i) for i, s in zip(dir, slices))  # type: ignore


MIN_SIZE = 8


class OctTree:
    def __init__(self, size=0x100000, default: bool = False):
        self.oct: list[bool | OctTree | Any] = [default] * 2 * 2 * 2  # type: ignore
        self.size = size
        self.half_size = size >> 1

    def __setitem__(self, slices: tuple[slice, slice, slice], value: bool) -> None:
        xx, yy, zz = slices
        assert xx.start >= -self.size
        assert yy.start >= -self.size
        assert zz.start >= -self.size
        assert xx.stop <= self.size
        assert yy.stop <= self.size
        assert zz.stop <= self.size
        for i, xyz in enumerate(iter_slices(slices)):
            if any(s == slice(0, 0) for s in xyz):
                continue
            elif all(s == slice(0, self.size) for s in xyz):
                self.oct[i] = value
            else:
                if isinstance(self.oct[i], bool):
                    if self.size == MIN_SIZE:
                        self.oct[i] = np.full((self.size, self.size, self.size), fill_value=self.oct[i], dtype=bool)
                    else:
                        self.oct[i] = OctTree(size=self.half_size, default=self.oct[i])  # type: ignore

                if self.size == MIN_SIZE:
                    self.oct[i][xyz] = value  # type: ignore
                else:
                    self.oct[i][  # type: ignore
                        slice(xyz[0].start - self.half_size, xyz[0].stop - self.half_size),
                        slice(xyz[1].start - self.half_size, xyz[1].stop - self.half_size),
                        slice(xyz[2].start - self.half_size, xyz[2].stop - self.half_size),
                    ] = value

    def sum(self) -> int:
        result = 0
        for o in self.oct:
            if o is True:
                result += self.size * self.size * self.size
            elif not isinstance(o, bool):
                result += o.sum()
        return result


class Rect:
    def __init__(self, x: tuple[int, int], y: tuple[int, int], z: tuple[int, int]) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f"Rect({self.x}, {self.y}, {self.z})"

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __eq__(self, __o: object) -> bool:
        assert isinstance(__o, Rect)
        return self.x == __o.x and self.y == __o.y and self.z == __o.z

    @property
    def volume(self) -> int:
        return self.x[1] - self.x[0] * self.y[1] - self.y[0] * self.z[1] - self.z[0]

    def intersects(self, other: Rect) -> bool:
        return (
            self.x[0] < other.x[1]
            and self.y[0] < other.y[1]
            and self.z[0] < other.z[1]
            and self.x[1] > other.x[0]
            and self.y[1] > other.y[0]
            and self.z[1] > other.z[0]
        )

    def is_inside(self, other: Rect) -> bool:
        return (
            self.x[1] < other.x[1]
            and self.y[1] < other.y[1]
            and self.z[1] < other.z[1]
            and self.x[0] > other.x[0]
            and self.y[0] > other.y[0]
            and self.z[0] > other.z[0]
        )

    def combine(self, other: Rect) -> Iterator[Rect]:
        if self.is_inside(other):
            yield self
        elif other.is_inside(self):
            yield other
        else:
            pass


class Tree:
    left: Tree
    right: Tree

    def __init__(self, axis: Optional[int] = None, index: Optional[int] = None) -> None:
        self.axis = axis
        self.index = index
        self.contents: set[Rect] = set()

    def mark(self, rect: Rect) -> None:
        for r in self.contents:
            assert not rect.intersects(r), r
        self.contents.add(rect)

    def unmark(self, rect: Rect) -> None:
        for r in self.contents:
            assert not rect.intersects(r), r


def main(file: Path) -> (int | str):
    with open(file, "r", encoding="utf8") as f:
        (lines,) = f.read().strip().split("\n\n")

    tree = Tree()

    for on, rect in parse(lines):
        print(f"set={on}, {rect}")
        if on:
            tree.mark(rect)
        else:
            tree.unmark(rect)
        # print(cubes.sum())
        # cubes[xx, yy, zz] = on

    print(cubes.sum())
    return cubes.sum()


EXPECTED = 2758514936282235
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if main(EXAMPLE_FILE) == EXPECTED:
        aocd.submit(main(INPUT_FILE))
