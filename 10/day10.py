from pathlib import Path
from typing import Tuple

import numpy as np

THIS_DIR = Path(__file__).parent
FILE = THIS_DIR / "example.txt"
FILE = THIS_DIR / "input.txt"


class Corrupted(Exception):
    def __init__(self, expected, got) -> None:
        self.expected = expected
        self.got = got
        super().__init__(f"{expected=}, {got=}")


STARTERS = "{[(<"
ENDS = {
    "{": "}",
    "[": "]",
    "(": ")",
    "<": ">",
}


def verify(line: str, missing: str = "") -> Tuple[str, str]:
    start, line = line[0], line[1:]
    end = ENDS[start]
    while line:
        if line[0] in ENDS.values():
            if line[0] != end:
                raise Corrupted(end, line[0])
            return line[1:], missing
        elif line[0] in STARTERS:
            line, missing = verify(line)
    missing += end
    return "", missing


def main() -> None:
    with open(FILE, "r", encoding="utf8") as f:
        lines = f.read().strip().splitlines()
    score = 0
    missing_scores = []
    for line in lines:
        print(line)
        try:
            while line:
                line, missing = verify(line)
        except Corrupted as exc:
            score += {
                ")": 3,
                "]": 57,
                "}": 1197,
                ">": 25137,
            }[exc.got]
            print(exc)
        else:
            missing_score = 0
            for c in missing:
                missing_score *= 5
                missing_score += {
                    ")": 1,
                    "]": 2,
                    "}": 3,
                    ">": 4,
                }[c]
            print(missing_score)
            missing_scores.append(missing_score)
    print(score)
    missing_scores.sort()
    print(missing_scores[len(missing_scores) // 2])


if __name__ == "__main__":
    main()
