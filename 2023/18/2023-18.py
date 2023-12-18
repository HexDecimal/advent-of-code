from __future__ import annotations

import bisect
import itertools
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import numpy as np
import scipy.ndimage  # type: ignore[import-untyped]
from numpy.typing import NDArray
from parse import parse  # type: ignore[import-untyped]
from tqdm import tqdm

DIRS = {
    3: (-1, 0),
    1: (1, 0),
    2: (0, -1),
    0: (0, 1),
}


def fill_array2d(array: NDArray[np.bool_]) -> NDArray[np.bool_]:
    array = np.pad(array, [(1, 1), (1, 1)])
    labels, count = scipy.ndimage.label(~array)
    for i in range(1, count + 1):
        label = labels == i
        if label[0, :].any() or label[-1, :].any() or label[:, 0].any() or label[:, -1].any():
            continue
        array |= label
    return array[1:-1, 1:-1]


def iter_row(row: Iterable[tuple[int, int]]) -> Iterator[bool]:
    x = 0
    for start, length in row:
        for _ in range(x, start):
            yield False
        for _ in range(length):
            yield True
        x = start + length


class CompressedRows:
    def __init__(self) -> None:
        self.rows = DefaultDict[int, list[tuple[int, int]]](list)

    def add(self, key: tuple[int, int]) -> None:
        y, x = key
        for i, (start, length) in enumerate(self.rows[y]):
            if x == start - 1:
                self.rows[y][i] = (start - 1, length + 1)
                return
            if x == start + length:
                self.rows[y][i] = (start, length + 1)
                return
            assert not (start <= x < start + length)
        bisect.insort(self.rows[y], (x, 1))

    def compress(self) -> int:
        print("Compress...")
        min_y = min(self.rows)
        max_y = max(self.rows)
        row_weight: list[int] = []
        compressed_rows: list[tuple[tuple[int, int], ...]] = []
        for y in tqdm(range(min_y, max_y + 1), desc="compressing rows"):
            row = tuple(self.rows[y])
            if compressed_rows and row == compressed_rows[-1]:
                row_weight[-1] += 1
                continue
            compressed_rows.append(row)
            row_weight.append(1)
        print(f"{len(compressed_rows)} distinct rows")
        min_x = min(row[0][0] for row in compressed_rows)
        compressed_rows = [tuple((run[0] - min_x, run[1]) for run in row) for row in compressed_rows]
        max_x = max(row[-1][0] + row[-1][1] for row in compressed_rows)

        def iter_columns() -> Iterator[tuple[int, ...]]:
            yield from itertools.zip_longest(*(iter_row(row) for row in compressed_rows), fillvalue=False)

        column_weight: list[int] = []
        compressed_columns: list[tuple[int, ...]] = []

        for column in tqdm(iter_columns(), total=max_x, desc="compressing columns"):
            if compressed_columns and column == compressed_columns[-1]:
                column_weight[-1] += 1
                continue
            compressed_columns.append(column)
            column_weight.append(1)

        shape = len(compressed_rows), len(compressed_columns)
        print(f"{shape=}")
        dig_map = np.asarray(compressed_columns, dtype=np.bool_).T
        values = fill_array2d(dig_map).astype(np.int64)
        values[:] *= np.asarray(row_weight)[:, np.newaxis]
        values[:] *= np.asarray(column_weight)
        return values.sum()


def main(input: str) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    lines = segments[0].split("\n")
    current_pos = (0, 0)
    dig = CompressedRows()

    print("Digging...")
    for line in tqdm(lines):
        dist: int
        _, _, hex_string = parse("{} {:d} (#{})", line)
        dist = int(hex_string[:5], base=16)
        dx, dy = DIRS[int(hex_string[-1])]
        for _ in range(dist):
            current_pos = current_pos[0] + dx, current_pos[1] + dy
            dig.add(current_pos)

    return dig.compress()


EXPECTED = 952408144115
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.input"
    INPUT_FILE = THIS_DIR / "input.input"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data, encoding="utf8")
    result = main(EXAMPLE_FILE.read_text(encoding="ansi"))
    if result != EXPECTED:
        print(f"Expected {EXPECTED!r} but got {result!r} instead!")
        raise SystemExit()
    else:
        print("Example passed.")
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
