from __future__ import annotations

import functools
import itertools
import re
from pathlib import Path
from typing import Any, Iterable, Iterator, MutableSequence, NamedTuple, Optional, Sequence

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


def parse(lines: str) -> Iterator[tuple[bool, Rect]]:
    for line in lines.split("\n"):
        match = CODES.match(line)
        assert match
        bool_, *values_ = match.groups()
        on = bool_ == "on"
        min_x, max_x, min_y, max_y, min_z, max_z = [int(v) for v in values_]
        yield on, Rect((min_x, max_x + 1), (min_y, max_y + 1), (min_z, max_z + 1))


class Rect(NamedTuple):
    x: tuple[int, int]
    y: tuple[int, int]
    z: tuple[int, int]

    @property
    def volume(self) -> int:
        assert self.is_valid(), self
        return (self.x[1] - self.x[0]) * (self.y[1] - self.y[0]) * (self.z[1] - self.z[0])

    def is_valid(self) -> bool:
        return self.x[0] <= self.x[1] and self.y[0] <= self.y[1] and self.z[0] <= self.z[1]

    def __bool__(self) -> bool:
        """Return True if this Rect is non-empty."""
        assert self.is_valid(), self
        return self.x[0] != self.x[1] or self.y[0] != self.y[1] or self.z[0] != self.z[1]

    def split_on_axis(self, axis: int, pos: int) -> tuple[Rect, Rect]:
        assert self[axis][0] <= pos and pos < self[axis][1]
        left: Any = list(self)
        left[axis] = (self[axis][0], pos)
        right: Any = list(self)
        right[axis] = (pos, self[axis][1])
        assert Rect(*left)
        assert Rect(*right)
        assert Rect(*left).volume + Rect(*right).volume == self.volume
        return Rect(*left), Rect(*right)

    def divide_on_axis(self, axis: int, pos: int) -> tuple[Optional[Rect], Optional[Rect]]:
        if self[axis][1] <= pos:
            return self, None
        if self[axis][0] >= pos:
            return None, self
        return self.split_on_axis(axis, pos)

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
            self.x[1] <= other.x[1]
            and self.y[1] <= other.y[1]
            and self.z[1] <= other.z[1]
            and self.x[0] >= other.x[0]
            and self.y[0] >= other.y[0]
            and self.z[0] >= other.z[0]
        )

    def compute_intersection(self, other: Rect):
        assert self.intersects(other)
        for (x_bit, x_range), (y_bit, y_range), (z_bit, z_range) in itertools.product(
            *(axis_intersection(self[i], other[i]) for i in range(3))
        ):
            bits = x_bit & y_bit & z_bit
            if not bits:
                continue
            rect = Rect(x_range, y_range, z_range)
            if rect:
                yield bits, rect

    def union(self, other: Rect) -> Iterator[Rect]:
        assert self.intersects(other)
        if self.is_inside(other):
            yield other
            return
        elif other.is_inside(self):
            yield self
            return
        for _, rect in self.compute_intersection(other):
            yield rect

    def subtract(self, other: Rect) -> Iterator[Rect]:
        """Subtract other from self."""
        assert self.intersects(other)
        if self.is_inside(other):
            return
        for bits, rect in self.compute_intersection(other):
            if bits == 1:  # self rect only.
                yield rect


def axis_intersection(axis1: tuple[int, int], axis2: tuple[int, int]) -> Iterator[tuple[int, tuple[int, int]]]:
    """Yields (axis_bitfield, (start, stop))."""
    axis_index = (1, 2)  # (axis1_bit, axis2_bit)
    if axis1[0] > axis2[0]:
        axis1, axis2 = axis2, axis1
        axis_index = (2, 1)
    assert axis1[0] <= axis2[0]
    assert axis2[0] <= axis1[1]
    yield axis_index[0], (axis1[0], axis2[0])
    if axis1[1] <= axis2[1]:
        yield 3, (axis2[0], axis1[1])
        yield axis_index[1], (axis1[1], axis2[1])
    else:
        yield 3, (axis2[0], axis2[1])
        yield axis_index[0], (axis2[1], axis1[1])


class Tree:
    left: Tree
    right: Tree

    def __init__(
        self, axis: Optional[int] = None, index: Optional[int] = None, contents: Optional[list[Rect]] = None
    ) -> None:
        self.axis = axis
        self.index = index
        self.contents = contents if contents is not None else []

    def mark(self, rect: Rect) -> None:
        if self.axis is not None:
            assert self.index is not None
            left, right = rect.divide_on_axis(axis=self.axis, pos=self.index)
            if left is not None:
                self.left.mark(left)
            if right is not None:
                self.right.mark(right)
            return

        for r in list(self.contents):
            if not rect.intersects(r):
                continue
            self.contents.remove(r)
            for sub_rect in rect.union(r):
                self.mark(sub_rect)
            return  # rect was added as sub_rects.
        assert rect and rect.is_valid(), rect
        self.contents.append(rect)

        if len(self.contents) > 256:
            checked = []
            for axis in range(2):
                splits = set(itertools.chain.from_iterable(split_rect[axis] for split_rect in self.contents))
                for split in splits:
                    left_rects = []
                    right_rects = []
                    for rect in self.contents:
                        left, right = rect.divide_on_axis(axis, split)
                        if left is not None:
                            left_rects.append(left)
                        if right is not None:
                            right_rects.append(right)
                    checked.append((max(len(left_rects), len(right_rects)), axis, split, left_rects, right_rects))
            _, self.axis, self.index, left_rects, right_rects = min(checked)
            self.left = Tree(contents=left_rects)
            self.right = Tree(contents=right_rects)
            self.contents = []

    def unmark(self, rect: Rect) -> None:
        if self.axis is not None:
            assert self.index is not None
            left, right = rect.divide_on_axis(axis=self.axis, pos=self.index)
            if left is not None:
                self.left.unmark(left)
            if right is not None:
                self.right.unmark(right)
            return

        to_add: list[Iterable] = []
        for r in list(self.contents):
            if not rect.intersects(r):
                continue
            self.contents.remove(r)
            to_add.append(r.subtract(rect))

        for r in itertools.chain.from_iterable(to_add):
            self.mark(r)

    def sum(self) -> int:
        if self.axis is not None:
            assert not self.contents
            return self.left.sum() + self.right.sum()
        return sum(rect.volume for rect in self.contents)


def main(file: Path) -> (int | str):
    with open(file, "r", encoding="utf8") as f:
        (lines,) = f.read().strip().split("\n\n")

    tree = Tree()

    commands = list(parse(lines))
    for i, (on, rect) in enumerate(commands, 1):
        print(f"command {i}/{len(commands)}, sum={tree.sum()}")
        print(f"set={on}, {rect}")
        if on:
            tree.mark(rect)
        else:
            tree.unmark(rect)

    print(tree.sum())
    return tree.sum()


EXPECTED = 590784
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if main(EXAMPLE_FILE) == EXPECTED:
        main(INPUT_FILE)
