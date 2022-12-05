from __future__ import annotations

import functools
import itertools
import operator
import re
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import numpy as np
from numpy.typing import NDArray
from parse import parse

from aoc import as_array, as_bool_array, as_ints, parse_ints, reduce_multiply


def main(input: str) -> (int | str | None):
    segments = input.strip().split("\n\n")
    # array = as_array(segments[0]).astype(np.int32)
    # lines = [int(i) for i in segments[0].split(",")]
    lines = segments[0].split("\n")
    for line in lines:
        pass
    return None


EXPECTED = 0
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data + "\n", encoding="utf8")
    result = main(EXAMPLE_FILE.read_text(encoding="ansi"))
    assert result == EXPECTED, f"{result} != {EXPECTED}"
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
