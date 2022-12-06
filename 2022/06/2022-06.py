from __future__ import annotations

from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore


def main(input: str) -> (int | str | None):
    segments = input.rstrip("\n").split("\n\n")
    line = segments[0].split("\n")[0]
    for i in range(len(line)):
        print(line[i : i + 14])
        if len(set(line[i : i + 14])) == 14:
            return i + 14
    return None


EXPECTED = 19
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.input"
    INPUT_FILE = THIS_DIR / "input.input"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data, encoding="utf8")
    result = main(EXAMPLE_FILE.read_text(encoding="ansi"))
    if result != EXPECTED:
        raise SystemExit(f"Excepted {EXPECTED!r} but got {result!r} instead!")
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
