from pathlib import Path

import numpy as np
import tcod


def part1(file: Path) -> (int | str):
    with open(file, "r", encoding="utf8") as f:
        (lines,) = f.read().strip().split("\n\n")
    cost = np.asarray([[int(ch) for ch in row] for row in lines.split("\n")], int)
    dist = tcod.path.maxarray(cost.shape)
    dist[0, 0] = 0
    dist = tcod.path.dijkstra2d(dist, cost, 1)
    return int(dist[-1, -1])


def part2(file: Path) -> (int | str):
    with open(file, "r", encoding="utf8") as f:
        (lines,) = f.read().strip().split("\n\n")
    cost = np.asarray([[int(ch) for ch in row] for row in lines.split("\n")], int)
    cost -= 1
    cost = np.concatenate([cost + i for i in range(5)], axis=0)
    cost = np.concatenate([cost + i for i in range(5)], axis=1)
    cost %= 9
    cost += 1
    dist = tcod.path.maxarray(cost.shape)
    dist[0, 0] = 0
    dist = tcod.path.dijkstra2d(dist, cost, 1)
    return int(dist[-1, -1])


if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    print(part1(EXAMPLE_FILE))  # 40
    print(part2(EXAMPLE_FILE))  # 315
