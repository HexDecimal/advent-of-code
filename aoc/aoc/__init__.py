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
def split_ints(string: str, delimiters: tuple[str]) -> list[int]:
    ...


@overload
def split_ints(string: str, delimiters: tuple[str, str]) -> list[list[int]]:
    ...


@overload
def split_ints(string: str, delimiters: tuple[str, str, str]) -> list[list[list[int]]]:
    ...


@overload
def split_ints(string: str, delimiters: tuple[str, str, str, str]) -> list[list[list[list[int]]]]:
    ...


def split_ints(string: str, delimiters: tuple[str, ...]) -> int | list[Any]:
    """Parse ints out of a string grouping them by a sequence of delimiters."""
    if not delimiters:
        return int(string)
    return [split_ints(split, delimiters[1:]) for split in string.split(delimiters[0])]  # type: ignore[arg-type]


def ints(value: Iterable[Any] | re.Match | str | None) -> list[int]:
    """Converts various iterables into a list of integers."""
    match value:
        case None:
            raise TypeError("Can not convert None to integers.")
        case str():
            return ints(RE_INTS.findall(value))
        case re.Match():
            return [int(i) for i in value.groups()]
        case _:
            return [int(i) for i in value]


def as_array(segment: str) -> NDArray[np.int8]:
    """Convert a segment of single digits into a 2D integer array."""
    return np.array([list(line) for line in segment.split("\n")], dtype=np.int8)


def as_str_array(segment: str) -> NDArray[np.string_]:
    """Convert a segment into a 2D array of strings."""
    return np.array([[ch for ch in line] for line in segment.split("\n")], dtype=np.string_)


def as_ord_array(segment: str) -> NDArray[np.int32]:
    """Convert a segment into a 2D array of strings."""
    return np.array([[ord(ch) for ch in line] for line in segment.split("\n")], dtype=np.int32)


def as_bool_array(segment: str, truthy: str = "#") -> NDArray[np.bool8]:
    """Convert a segment into a 2D bool array.  `truthy` one be one or more characters to count as True."""
    return np.array([[ch in truthy for ch in line] for line in segment.split("\n")], dtype=np.bool8)


reduce_multiply = functools.partial(functools.reduce, operator.mul)


np.seterr("raise")  # Numpy should default to error checking to avoid missed overflows.
