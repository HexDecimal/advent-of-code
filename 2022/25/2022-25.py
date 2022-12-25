from __future__ import annotations

import functools
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore


def decode_list(digits: list[int]) -> int:
    out = 0
    for p, d in enumerate(digits[::-1]):
        out += d * (5**p)
    return out


@functools.cache
def decode(code: str) -> int:
    digits = ["=-012".index(c) - 2 for c in code]
    out = decode_list(digits)
    assert encode(out) == code, f"{code} != {encode(out)}"
    return out


@functools.cache
def encode(n: int) -> str:
    digits = [2]
    while n - decode_list(digits) > 0:
        digits.append(2)
    for i in range(len(digits)):
        while n - decode_list(digits) < 0:
            digits[i] -= 1
        if n - decode_list(digits) > 0:
            digits[i] += 1

    return "".join("=-012"[d + 2] for d in digits)


def main(input: str) -> (int | str | None):
    segments = input.rstrip("\n").split("\n\n")
    lines = segments[0].split("\n")
    return encode(sum(decode(line) for line in lines))


EXPECTED = "2=-1=0"
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
