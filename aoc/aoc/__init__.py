"""Personal Advent of Code helper library."""

from __future__ import annotations

import functools
import itertools
import operator
import re
from collections.abc import Iterable, Iterator
from typing import Any, TypeVar, overload

import numpy as np
from numpy.typing import NDArray

__version__ = "0.0.0"

T = TypeVar("T")

RE_INTS = re.compile(r"(-?\d+)")


@overload
def split_ints(string: str, delimiters: tuple[str]) -> list[int]: ...


@overload
def split_ints(string: str, delimiters: tuple[str, str]) -> list[list[int]]: ...


@overload
def split_ints(string: str, delimiters: tuple[str, str, str]) -> list[list[list[int]]]: ...


@overload
def split_ints(string: str, delimiters: tuple[str, str, str, str]) -> list[list[list[list[int]]]]: ...


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


def as_str_array(segment: str) -> NDArray[np.bytes_]:
    """Convert a segment into a 2D array of strings."""
    return np.array([list(line) for line in segment.split("\n")], dtype=np.bytes_)


def as_ord_array(segment: str) -> NDArray[np.int32]:
    """Convert a segment into a 2D array of strings."""
    return np.array([[ord(ch) for ch in line] for line in segment.split("\n")], dtype=np.int32)


def as_bool_array(segment: str, truthy: str = "#") -> NDArray[np.bool_]:
    """Convert a segment into a 2D bool array.  `truthy` one be one or more characters to count as True."""
    lines = segment.split("\n")
    max_width = max(len(line) for line in lines)
    return np.array(
        [[ch in truthy for ch in line] + [False] * (max_width - len(line)) for line in lines],
        dtype=bool,
    )


def reduce_multiply[T](values: Iterable[T], /) -> T:
    """Reduce an iterator to a single number by multiplying its values together."""
    return functools.reduce(operator.mul, values)


known_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541]  # fmt: skip


def iter_primes() -> Iterator[int]:
    """Iterate over primes and cache results, not thread safe."""
    yield from known_primes
    for n in itertools.count(known_primes[-1] + 2, 2):
        if any(n % known == 0 for known in known_primes):
            continue
        known_primes.append(n)
        yield n
    raise AssertionError


def factors(n: int, /) -> list[int]:
    """Return the prime factors of a number.

    >>> list(factors(20))
    [2, 2, 5]
    """
    assert n > 0, n
    result = []
    primes = list(itertools.takewhile(lambda d: d <= n, iter_primes()))
    for d in primes[::-1]:
        while n % d == 0:
            result.append(d)
            n //= d
            if n == 1:
                return result[::-1]
    raise AssertionError


np.seterr("raise")  # Numpy should default to error checking to avoid missed overflows.
