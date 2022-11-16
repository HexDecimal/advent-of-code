from __future__ import annotations

from pathlib import Path

import aocd  # type: ignore


def part1(input: str) -> (int | str | None):
    segments = input.strip().split("\n\n")
    lines = segments[0].split("\n")
    depart = int(lines[0])
    buses = [int(i) if i != "x" else None for i in lines[1].split(",")]

    results = []
    for bus in buses:
        if bus is None:
            continue
        wait_time = bus - depart % bus
        results.append((wait_time, bus))

    print(results)
    wait_time, bus = min(results)
    return wait_time * bus


def main(input: str) -> (int | str | None):
    segments = input.strip().split("\n\n")
    lines = segments[0].split("\n")
    buses = [int(i) if i != "x" else None for i in lines[1].split(",")]
    assert buses[0] is not None

    best_cycle = buses[0]
    seen_runs: dict[tuple[int | None, ...], int] = {}
    start = 0
    while True:
        start += best_cycle
        print(f"{start=}, {best_cycle=}")
        for i, bus in enumerate(buses):
            if bus is None:
                continue
            if (start + i) % bus != 0:
                break
        else:  # nobreak
            return start
        run = tuple(buses[:i])
        if run in seen_runs:
            best_cycle = max(best_cycle, start - seen_runs[run])
        seen_runs[run] = start


EXPECTED = 1068781
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data + "\n", encoding="utf8")
    result = main(EXAMPLE_FILE.read_text(encoding="ansi"))
    assert result == EXPECTED, f"{result} != {EXPECTED}"
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
