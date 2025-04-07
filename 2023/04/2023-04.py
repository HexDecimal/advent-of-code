from __future__ import annotations

from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
from parse import parse  # type: ignore[import-untyped]


def main(input: str) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    lines = segments[0].split("\n")
    last_card, _ = parse("{:d}{}", lines[-1].removeprefix("Card").strip())
    total = 0
    my_cards = Counter[int](dict.fromkeys(range(1, last_card + 1), 1))
    for line in lines:
        left: str
        right: str
        line = line.removeprefix("Card").strip()  # noqa: PLW2901
        print(line)
        card_n, left, right = parse("{:d}: {}|{}", line)
        left_n = {int(s) for s in left.strip().split(" ") if s}
        right_n = {int(s) for s in right.strip().split(" ") if s}
        matches = len(left_n & right_n)
        print(range(card_n + 1, card_n + 1 + matches))
        for i in range(card_n + 1, card_n + 1 + matches):
            my_cards[i] += my_cards[card_n]
        total += my_cards[card_n]
        print(f"CARD: {card_n} {my_cards[card_n]=} {matches=} {total=}")

    return total


EXPECTED = 30
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
