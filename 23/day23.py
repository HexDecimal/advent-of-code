from __future__ import annotations

import functools
import heapq
import itertools
from pathlib import Path
from typing import Any, Counter, Iterable, Iterator, NamedTuple

import aocd  # type: ignore
import numpy as np

XY = tuple[int, int]

MOVE_COST = (0, 1, 10, 100, 1000)


@functools.cache
def get_distance(start: XY, stop: XY) -> int:
    if start[0]:
        assert stop[0] == 0
        return get_distance(stop, start)
    assert start[0] == 0  # start == hall
    assert stop[0] != 0  # stop == room
    steps = 1 + stop[1]
    start_x = start[1] + max(0, min(start[1] - 1, 4))
    stop_x = 2 * stop[0]
    steps += abs(stop_x - start_x)
    return steps


assert get_distance((0, 5), (4, 1)) == 3
assert get_distance((0, 6), (4, 1)) == 4
assert get_distance((0, 0), (1, 1)) == 4
assert get_distance((0, 1), (1, 1)) == 3
assert get_distance((0, 2), (1, 1)) == 3
assert get_distance((0, 3), (1, 1)) == 5
assert get_distance((0, 6), (2, 1)) == 8


class State(NamedTuple):
    hall: tuple[int, int, int, int, int, int, int] = (0, 0, 0, 0, 0, 0, 0)
    roomA: tuple[int, int] = (1, 1)
    roomB: tuple[int, int] = (2, 2)
    roomC: tuple[int, int] = (3, 3)
    roomD: tuple[int, int] = (4, 4)

    @classmethod
    def from_coords(cls, coords: Iterable[tuple[int, int]]) -> State:
        state = [[0, 0, 0, 0, 0, 0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        for i, j in coords:
            state[i][j] = 1
        return cls(tuple(state[0]), tuple(state[1]), tuple(state[2]), tuple(state[3]), tuple(state[4]))  # type: ignore

    def valid_moves(self, start: XY, token: int) -> Iterator[XY]:
        assert self[start[0]][start[1]] == token
        if not start[0]:  # In hall
            if self[token][1] and self[token][1] != token:
                return  # Would block another token from exiting.
            if self[token][0]:
                return  # Can't enter room.
            if start[1] < token + 2:
                if any(self.hall[start[1] + 1 : token + 1]):
                    return  # Blocked along hallway.
            elif token + 1 < start[1]:
                if any(self.hall[token + 1 : start[1]]):
                    return
            yield token, (1 if not self[token][1] else 0)
        else:  # In room
            if start[0] == token:
                if self[token][1] == token:
                    return  # This token is correct.
            if start[1] == 1 and self[start[0]][0]:
                return  # Path to hall blocked.
            for i in range(start[0], -1, -1):
                if self.hall[i] != 0:
                    break
                yield 0, i
            for i in range(start[0] + 1, 7):
                if self.hall[i] != 0:
                    break
                yield 0, i

    def iter_tokens(self) -> Iterator[tuple[XY, int]]:
        for i, row in enumerate(self):
            for j, t in enumerate(row):
                if t:
                    yield (i, j), t

    @functools.cache
    def move(self, start: XY, stop: XY) -> State:
        self_list: Any = list(self)
        self_list[start[0]] = list(self_list[start[0]])
        self_list[stop[0]] = list(self_list[stop[0]])
        self_list[stop[0]][stop[1]] = self_list[start[0]][start[1]]
        self_list[start[0]][start[1]] = 0
        self_list[start[0]] = tuple(self_list[start[0]])
        self_list[stop[0]] = tuple(self_list[stop[0]])
        return State(*self_list)


HeapItem = tuple[int, State]


def parse(lines: str) -> State:
    starting: list[list[int]] = [[], [], [], []]
    for line in lines.split("\n")[2:4]:
        for i, c in enumerate(line.strip().replace("#", "")):
            starting[i].append({"A": 1, "B": 2, "C": 3, "D": 4}[c])
    return State(
        (0, 0, 0, 0, 0, 0, 0),
        tuple(starting[0]),  # type: ignore
        tuple(starting[1]),  # type: ignore
        tuple(starting[2]),  # type: ignore
        tuple(starting[3]),  # type: ignore
    )


TARGET = State()


def _test_move(state: State, token: int, start: XY, stop: XY, dist: int) -> State:
    assert (start, token) in list(state.iter_tokens())
    assert stop in list(state.valid_moves(start, token))
    assert get_distance(start, stop) == dist
    return state.move(start, stop)


def tests() -> None:
    assert list(State((0, 0, 0, 0, 0, 0, 0), (0, 2), (0, 0), (0, 0), (0, 0)).valid_moves((1, 1), 2)) == [
        (0, 1),
        (0, 0),
        (0, 2),
        (0, 3),
        (0, 4),
        (0, 5),
        (0, 6),
    ]
    state = State.from_coords(State((1, 0, 0, 0, 0, 0, 0), (0, 0), (0, 0), (0, 0), (0, 0)).valid_moves((0, 0), 1))
    assert state == State((0, 0, 0, 0, 0, 0, 0), (0, 1), (0, 0), (0, 0), (0, 0))
    assert not list(State((1, 1, 0, 0, 0, 0, 0), (0, 0), (0, 0), (0, 0), (0, 0)).valid_moves((0, 0), 1))
    assert list(State((1, 1, 0, 0, 0, 0, 0), (0, 0), (0, 0), (0, 0), (0, 0)).valid_moves((0, 1), 1))
    assert list(State((1, 1, 1, 1, 0, 0, 0), (0, 0), (0, 0), (0, 0), (0, 0)).valid_moves((0, 1), 1))
    assert list(State((1, 1, 1, 1, 0, 0, 0), (0, 0), (0, 0), (0, 0), (0, 0)).valid_moves((0, 2), 1))
    assert not list(State((1, 1, 1, 1, 0, 0, 0), (0, 0), (0, 0), (0, 0), (0, 0)).valid_moves((0, 3), 1))
    state = State.from_coords(State((0, 0, 0, 0, 0, 0, 0), (0, 2), (0, 0), (0, 0), (0, 0)).valid_moves((1, 1), 2))
    assert state == State((1, 1, 1, 1, 1, 1, 1), (0, 0), (0, 0), (0, 0), (0, 0))
    state = State.from_coords(State((0, 1, 0, 0, 0, 0, 0), (0, 2), (0, 0), (0, 0), (0, 0)).valid_moves((1, 1), 2))
    assert state == State((0, 0, 1, 1, 1, 1, 1), (0, 0), (0, 0), (0, 0), (0, 0))
    assert not list(State((0, 1, 1, 0, 0, 0, 0), (0, 2), (0, 0), (0, 0), (0, 0)).valid_moves((1, 1), 2))
    assert not list(State((0, 0, 1, 1, 0, 0, 0), (0, 0), (0, 1), (0, 0), (0, 0)).valid_moves((2, 1), 1))
    assert not list(State((0, 0, 0, 1, 1, 0, 0), (0, 0), (0, 0), (1, 1), (0, 0)).valid_moves((3, 0), 1))
    assert not list(State((2, 0, 1, 1, 0, 0, 0), (0, 0), (0, 0), (0, 0), (0, 0)).valid_moves((0, 0), 2))
    assert not list(State((0, 0, 1, 1, 0, 0, 2), (0, 0), (0, 0), (0, 0), (0, 0)).valid_moves((0, 6), 2))
    assert list(State((0, 1, 2, 1, 1, 0, 0), (0, 0), (0, 0), (0, 0), (0, 0)).valid_moves((0, 2), 2))
    assert list(State((0, 1, 1, 2, 1, 0, 0), (0, 0), (0, 0), (0, 0), (0, 0)).valid_moves((0, 3), 2))


def main(file: Path, test_example: bool = False) -> (int | str):
    heap = list[HeapItem]()
    with open(file, "r", encoding="utf8") as f:
        state_ = parse(f.read().strip())

    best = {state_: 0}
    best_path: dict[State, State] = {}
    heap.append((0, state_))
    last_cost = -1

    if test_example:
        state_ = _test_move(state_, 2, (3, 0), (0, 2), 4)

        state_ = _test_move(state_, 3, (2, 0), (0, 3), 2)
        state_ = _test_move(state_, 3, (0, 3), (3, 0), 2)

        state_ = _test_move(state_, 4, (2, 1), (0, 3), 3)
        state_ = _test_move(state_, 2, (0, 2), (2, 1), 3)

        state_ = _test_move(state_, 2, (1, 0), (0, 2), 2)
        state_ = _test_move(state_, 2, (0, 2), (2, 0), 2)

        state_ = _test_move(state_, 4, (4, 0), (0, 4), 2)
        state_ = _test_move(state_, 1, (4, 1), (0, 5), 3)

        state_ = _test_move(state_, 4, (0, 4), (4, 1), 3)
        state_ = _test_move(state_, 4, (0, 3), (4, 0), 4)

        state_ = _test_move(state_, 1, (0, 5), (1, 0), 8)
        assert state_ == TARGET

    while heap:
        cost, state = heapq.heappop(heap)
        if best[state] != cost:
            continue
        if cost != last_cost:
            last_cost = cost
            print(f"\r{cost=}, heap={len(heap)}, unique={len(best)} ", end="")
        if state == TARGET:
            print("")
            path = [state]
            while state in best_path:
                state = best_path[state]
                path.append(state)
            for state in path[::-1]:
                print(f"{state} {best[state]}")
            print(cost)
            return cost

        for xy, t in state.iter_tokens():
            for dest in state.valid_moves(xy, t):
                new_state = state.move(xy, dest)
                new_cost = cost + get_distance(xy, dest) * MOVE_COST[t]
                try:
                    if best[new_state] <= new_cost:
                        continue
                except KeyError:
                    pass
                best_path[new_state] = state
                best[new_state] = new_cost
                heapq.heappush(heap, (new_cost, new_state))
    assert False


EXPECTED = 12521
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    tests()
    if main(EXAMPLE_FILE, test_example=True) == EXPECTED:
        aocd.submit(main(INPUT_FILE))
