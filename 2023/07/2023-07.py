from __future__ import annotations

import functools
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore

CARD_VALUE = {
    **{str(i): i for i in range(2, 10)},
    "T": 10,
    "J": 1,
    "Q": 12,
    "K": 13,
    "A": 14,
}
CARD_VALUE_INV = {v: k for k, v in CARD_VALUE.items()}


@functools.total_ordering
class Hand:
    def __init__(self, line: str) -> None:
        hand_, bid_ = line.split(" ")
        self.hand = tuple(CARD_VALUE[c] for c in hand_)
        self.bid = int(bid_)
        assert len(self.rank) == 7

    @property
    def rank(self) -> tuple[int, ...]:
        counts = Counter[int](self.hand)
        jokers = counts[1]
        counts[1] = 0
        counts[counts.most_common(1)[0][0]] += jokers
        counts[0] = 1
        assert len(counts) >= 2, counts
        return (*(count for card, count in counts.most_common(2)), *self.hand)

    def __lt__(self, other: Hand) -> bool:
        return self.rank < other.rank

    def __repr__(self) -> str:
        hand = "".join(CARD_VALUE_INV[c] for c in self.hand)
        return f"{hand} {self.rank}"


def main(input: str) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    lines = segments[0].split("\n")
    hands = [Hand(line) for line in lines]

    for h in sorted(hands):
        print(h)
    print("---")

    return sum(i * hand.bid for i, hand in enumerate(sorted(hands), start=1))


EXPECTED = 5905
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
