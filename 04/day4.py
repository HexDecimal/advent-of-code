import numpy as np


class Board:
    def __init__(self, input: str):
        self.placed = np.zeros((5, 5), dtype=np.bool8)
        self.board = np.zeros((5, 5), dtype=np.int32)
        self.positions = {}
        print(input)
        for y, row in enumerate(input.split("\n")):
            for x, n in enumerate(row.split()):
                self.positions[int(n)] = y, x
                self.board[y, x] = int(n)
                print(f"{int(n)=} {y=}, {x=}")

        print(self.positions)
        print("---")

    def place(self, n: int) -> None:
        if n in self.positions:
            self.placed[self.positions[n]] = True

    def is_won(self) -> bool:
        # if self.placed[[0, 1, 2, 3, 4], [0, 1, 2, 3, 4]].all():
        #    return True
        # if self.placed[[4, 3, 2, 1, 0], [0, 1, 2, 3, 4]].all():
        #    return True
        return self.placed.all(axis=0).any() or self.placed.all(axis=1).any()

    def get_score(self, winning_n: int) -> int:
        score = 0
        for n, index in self.positions.items():
            if not self.placed[index]:
                score += n
        print(score)
        return score * winning_n


with open("04/input.txt", "r", encoding="utf8") as f:
    numbers = np.asarray([int(str_n) for str_n in f.readline().split(",")])
    boards = [Board(in_board) for in_board in f.read().strip().split("\n\n")]
print(numbers)
print(boards)


def main() -> int:
    for n in numbers:
        print(n)
        for b in boards:
            b.place(n)
            if b.is_won():
                print(b.board)
                print(b.placed)
                return b.get_score(n)


def main2() -> int:
    boards_ = boards.copy()
    for n in numbers:
        for b in list(boards_):
            b.place(n)
            if b.is_won():
                if len(boards_) == 1:
                    return b.get_score(n)
                boards_.remove(b)


print(main2())
