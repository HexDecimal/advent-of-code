from typing import Counter, Iterator, Tuple


def iter_points(file: str = "05/input.txt") -> Iterator[Tuple[Tuple[int, int], Tuple[int, int]]]:
    with open(file, "r", encoding="utf8") as f:
        for line in f.read().strip().splitlines():
            begin, end = line.split(" -> ")
            x1, y1 = begin.split(",")
            x2, y2 = end.split(",")
            yield (int(x1), int(y1)), (int(x2), int(y2))


overlap = Counter[Tuple[int, int]]()

points = list(iter_points())


for begin, end in points:
    if begin[0] == end[0]:
        x = begin[0]
        for y in range(min(begin[1], end[1]), max(begin[1], end[1]) + 1):
            overlap[x, y] += 1
    elif begin[1] == end[1]:
        y = begin[1]
        for x in range(min(begin[0], end[0]), max(begin[0], end[0]) + 1):
            overlap[x, y] += 1
    else:
        xx = range(min(begin[0], end[0]), max(begin[0], end[0]) + 1)
        if begin[0] > end[0]:
            xx = xx[::-1]
        yy = range(min(begin[1], end[1]), max(begin[1], end[1]) + 1)
        if begin[1] > end[1]:
            yy = yy[::-1]
        for x, y in zip(xx, yy):
            overlap[x, y] += 1

print(sum(count >= 2 for count in overlap.values()))
