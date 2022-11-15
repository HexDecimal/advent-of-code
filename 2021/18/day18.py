from __future__ import annotations

import copy
import itertools
from pathlib import Path
from typing import Any, Literal, Optional


class Pair:
    def __init__(self, left: Pair | int | list[Any], right: Pair | int | list[Any], *, parent: Optional[Pair]):
        if isinstance(left, list):
            left = Pair(*left, parent=self)
        if isinstance(right, list):
            right = Pair(*right, parent=self)
        self.left = left
        self.right = right
        self.parent = parent
        if isinstance(left, Pair):
            left.parent = self
        if isinstance(right, Pair):
            right.parent = self

    def __repr__(self) -> str:
        return f"[{self.left}, {self.right}]"

    def __int__(self) -> int:
        return int(self.left) * 3 + int(self.right) * 2

    def new_split(self, n: int) -> Pair:
        return Pair(n // 2, n - (n // 2), parent=self)

    def replace_with(self, new: Pair | int) -> None:
        assert self.parent
        if self.parent.left is self:
            self.parent.left = new
        if self.parent.right is self:
            self.parent.right = new

    def bubble(self, n: int, dir: Literal["left", "right"]) -> None:
        if self.parent is None:
            return
        if getattr(self.parent, dir) is self:
            return self.parent.bubble(n, dir)
        if isinstance(getattr(self.parent, dir), int):
            self.parent.__dict__[dir] += n
            return
        else:
            self = getattr(self.parent, dir)
            dir = "right" if dir != "right" else "left"
            while isinstance(getattr(self, dir), Pair):
                self = getattr(self, dir)
            self.__dict__[dir] += n
            return

    def try_explode(self, depth: int = 0) -> bool:
        if depth >= 4 and isinstance(self.left, int) and isinstance(self.right, int):
            self.bubble(self.left, "left")
            self.bubble(self.right, "right")
            self.replace_with(0)
            return True
        return (
            isinstance(self.left, Pair)
            and self.left.try_explode(depth=depth + 1)
            or isinstance(self.right, Pair)
            and self.right.try_explode(depth=depth + 1)
        )

    def try_split(self) -> bool:
        if isinstance(self.left, int):
            if self.left >= 10:
                self.left = self.new_split(self.left)
                return True
        else:
            if self.left.try_split():
                return True
        if isinstance(self.right, int):
            if self.right >= 10:
                self.right = self.new_split(self.right)
                return True
        else:
            return self.right.try_split()
        return False


def part1(file: Path) -> (int | str):
    with open(file, "r", encoding="utf8") as f:
        (lines,) = f.read().strip().split("\n\n")
    pairs = None
    for line in lines.split("\n"):
        new_pairs = Pair(*eval(line), parent=None)
        if pairs is None:
            pairs = new_pairs
        else:
            pairs = Pair(pairs, new_pairs, parent=None)
        while True:
            print(pairs)
            if pairs.try_explode():
                continue
            if pairs.try_split():
                continue
            break

    assert pairs
    print(int(pairs))
    return int(pairs)


def main(file: Path) -> (int | str):
    with open(file, "r", encoding="utf8") as f:
        (lines,) = f.read().strip().split("\n\n")
    all_pairs = [Pair(*eval(line), parent=None) for line in lines.split("\n")]
    best = 0
    for a, b in itertools.permutations(all_pairs, 2):
        pairs = Pair(copy.deepcopy(a), copy.deepcopy(b), parent=None)
        while True:
            if pairs.try_explode():
                continue
            if pairs.try_split():
                continue
            break
        best = max(best, int(pairs))

    print(best)
    return best


EXPECTED = 3993
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if main(EXAMPLE_FILE) == EXPECTED:
        main(INPUT_FILE)
