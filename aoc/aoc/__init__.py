"""Personal Advent of Code helper library."""
from __future__ import annotations

__version__ = "0.0.0"

import functools
import operator
import re
from typing import *  # noqa: F403
from typing import overload

import numpy as np
from numpy.typing import NDArray

T = TypeVar("T")

RE_INTS = re.compile(r"(\d+)")


@overload
def parse_ints(string: str, delimiters: tuple[str]) -> list[int]:
    ...


@overload
def parse_ints(string: str, delimiters: tuple[str, str]) -> list[list[int]]:
    ...


@overload
def parse_ints(string: str, delimiters: tuple[str, str, str]) -> list[list[list[int]]]:
    ...


@overload
def parse_ints(string: str, delimiters: tuple[str, str, str, str]) -> list[list[list[list[int]]]]:
    ...


def parse_ints(string: str, delimiters: tuple[str, ...]) -> int | list[Any]:
    """Parse ints out of a string grouping them by delimiters."""
    if not delimiters:
        return int(string)
    return [parse_ints(split, delimiters[1:]) for split in string.split(delimiters[0])]  # type: ignore[arg-type]


def as_ints(lst: Iterable[Any]) -> list[int]:
    """Convert any iterable into a list of ints."""
    return [int(i) for i in lst]


def as_array(segment: str) -> NDArray[np.int8]:
    """Convert a segment of single digits into a 2D integer array."""
    return np.array([list(line) for line in segment.split("\n")], dtype=np.int8)


def as_bool_array(segment: str, truthy: str = "#") -> NDArray[np.bool8]:
    """Convert a segment into a 2D bool array."""
    return np.array([[ch in truthy for ch in line] for line in segment.split("\n")], dtype=np.bool8)


reduce_multiply = functools.partial(functools.reduce, operator.mul)


np.seterr("raise")  # Numpy should default to error checking to avoid missed overflows.
