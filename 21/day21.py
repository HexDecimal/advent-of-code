from __future__ import annotations

import functools
import itertools
from pathlib import Path
from typing import Callable, Counter, Mapping, NamedTuple

import aocd  # type: ignore
import numpy as np


class Dice:
    def __init__(self) -> None:
        self.i = 0
        self.rolls = 0

    def __call__(self) -> int:
        self.rolls += 1
        self.i = (self.i + 1) % 100
        print(self.i)
        return self.i

    def roll3(self) -> int:
        return self() + self() + self()


def part1(file: Path) -> (int | str):
    with open(file, "r", encoding="utf8") as f:
        (lines,) = f.read().strip().split("\n\n")
    d = Dice()
    player_pos = []
    player_score = [0, 0]
    for line in lines.split("\n"):
        player_pos.append(int(line.split(" ")[-1]))

    winner = None
    while winner is None:
        for i in range(len(player_pos)):

            player_pos[i] = ((player_pos[i] + d.roll3() - 1) % 10) + 1
            player_score[i] += player_pos[i]
            if player_score[i] >= 1000:
                winner = i
                break
            print(f"Player {i+1}, pos {player_pos[i]}, score {player_score[i]}")
            if winner is not None:
                break

    loser = 1 if winner == 0 else 1

    print(f"{player_score[loser]=} {d.rolls=}")
    r = player_score[loser] * d.rolls
    print(r)
    return r


class State(NamedTuple):
    player_pos: tuple[int, int]
    player_score: tuple[int, int]


def main(file: Path) -> (int | str):
    with open(file, "r", encoding="utf8") as f:
        (lines,) = f.read().strip().split("\n\n")
    state = Counter[State](
        [
            State(
                tuple(int(line.split(" ")[-1]) for line in lines.split("\n")),  # type: ignore
                (0, 0),
            )
        ]
    )

    def roll(state: Counter[State], player: int) -> None:
        items = list(state.items())
        state.clear()
        for k, v in items:
            pos = list(k.player_pos)
            for _ in range(3):
                pos[player] = (pos[player] % 10) + 1
                k = k._replace(player_pos=tuple(pos))  # type: ignore
                state[k] += v

    def add_score(state: Counter[State], player: int) -> None:
        items = list(state.items())
        state.clear()
        for k, v in items:
            score = list(k.player_score)
            score[player] += k.player_pos[player]
            k = k._replace(player_score=tuple(score))  # type: ignore
            state[k] += v

    tally = [0, 0]
    while state:
        print(len(state))
        for player in range(2):
            roll(state, player)
            roll(state, player)
            roll(state, player)
            add_score(state, player)
            for k, v in list(state.items()):
                if k.player_score[player] >= 21:
                    tally[player] += v
                    del state[k]

    print(tally)
    return max(tally)


EXPECTED = 444356092776315
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if main(EXAMPLE_FILE) == EXPECTED:
        print(main(INPUT_FILE))
