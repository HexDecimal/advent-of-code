from __future__ import annotations

from pathlib import Path
from typing import Counter, Iterator, NamedTuple


class State(NamedTuple):
    w: int = 0
    x: int = 0
    y: int = 0
    z: int = 0
    p: int = 0

    def replace_arg(self, index: int, value: int) -> State:
        return self._replace(**{VAR_KEYWORDS[index]: value})


KEYWORDS = {
    "inp": 0,
    "add": 1,
    "mul": 2,
    "div": 3,
    "mod": 4,
    "eql": 5,
}

VAR_NAMES = {"w": 0, "x": 1, "y": 2, "z": 3}
VAR_KEYWORDS = "wxyz"


class Instruction:
    def __init__(self, input: str) -> None:
        self.keyword, *self.args = input.split()
        self.cmd = KEYWORDS[self.keyword]
        self.extra: int = 0
        self.arg0 = VAR_NAMES[self.args[0]]
        self.arg1 = 0
        self.arg1_var = False
        if len(self.args) > 1:
            if self.args[1] in VAR_NAMES:
                self.arg1_var = True
                self.arg1 = VAR_NAMES[self.args[1]]
            else:
                self.arg1 = int(self.args[1])

    def get_arg1(self, state: State) -> int:
        if self.arg1_var:
            return state[self.arg1]
        return self.arg1


def parse(lines: str) -> Iterator[Instruction]:
    yield from (Instruction(line) for line in lines.split("\n"))


def main(file: Path) -> (int | str | None):
    with open(file, "r", encoding="utf8") as f:
        instructions = list(parse(f.read().strip()))
    i = 14
    for instr in instructions:
        if instr.keyword == "inp":
            i -= 1
            instr.extra = 10 ** i
    assert i == 0
    heap = [(0, State())]
    best: dict[State, int] = {}
    hits = Counter[State]()
    iterations = 0
    while heap:
        iterations += 1
        if iterations == 10000000:
            iterations = 0
            for k in set(best) - set(hits):
                del best[k]
        model, state = heap.pop()
        try:
            intstr = instructions[state.p]
        except IndexError:
            if state.z != 0:
                print(f"\r{model}, unique={len(best)}, heap={len(heap)}, {state}", end="   ")
                continue
            print()
            print(state.z)
            return model

        state = state._replace(p=state.p + 1)
        if intstr.cmd == 0:
            for i in range(9, 0, -1):
                new_model = model + (intstr.extra * i)
                heap.append((new_model, state._replace(w=i)))
            continue
        elif intstr.cmd == 1:  # add
            state = state.replace_arg(intstr.arg0, state[intstr.arg0] + intstr.get_arg1(state))
        elif intstr.cmd == 2:  # mul
            state = state.replace_arg(intstr.arg0, state[intstr.arg0] * intstr.get_arg1(state))
        elif intstr.cmd == 3:  # div
            state = state.replace_arg(intstr.arg0, int(state[intstr.arg0] / intstr.get_arg1(state)))
        elif intstr.cmd == 4:  # mod
            if state[intstr.arg0] < 0 or intstr.get_arg1(state) <= 0:
                continue
            state = state.replace_arg(intstr.arg0, state[intstr.arg0] % intstr.get_arg1(state))
        elif intstr.cmd == 5:  # eql
            state = state.replace_arg(intstr.arg0, state[intstr.arg0] == intstr.get_arg1(state))
        else:
            assert False
        if state in best:
            hits[state] += 1
            continue
        best[state] = model
        heap.append((model, state))

    assert False


if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    INPUT_FILE = THIS_DIR / "input2.txt"
    main(INPUT_FILE)
