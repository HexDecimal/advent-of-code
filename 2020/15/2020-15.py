from __future__ import annotations

from pathlib import Path

import aocd  # type: ignore


def main(input: str) -> (int | str | None):
    segments = input.strip().split("\n\n")
    lines = [int(i) for i in segments[0].split(",")]
    last_seen = {}
    history = [lines.pop(0)]
    for next in lines:
        turn = len(history)
        last_seen[history[-1]] = turn
        history.append(next)
    while True:
        turn = len(history)
        last = history[-1]
        if turn == 30000000:
            return last
        if last in last_seen:
            next = turn - last_seen[last]
        else:
            next = 0
        last_seen[last] = turn
        history.append(next)


if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data + "\n", encoding="utf8")
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
