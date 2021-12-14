import itertools
from pathlib import Path
from typing import Counter


def main(file: Path) -> (int | str):
    with open(file, "r", encoding="utf8") as f:
        element_, lines = f.read().strip().split("\n\n")
    element = list(element_)
    endpoints = element[0], element[-1]
    rules: dict[str, dict[str, str]] = {}
    for line in lines.split("\n"):
        lhs, add = line.split(" -> ")
        (first, last) = lhs[0], lhs[1]
        if first not in rules:
            rules[first] = {}
        rules[first][last] = add

    element_pairs = Counter[tuple[str, str]](itertools.pairwise(element))

    for _ in range(40):
        for pair, count in list(element_pairs.items()):
            try:
                lastdict = rules[pair[0]]
                add = lastdict[pair[1]]
            except KeyError:
                pass
            except IndexError:
                pass
            else:
                element_pairs[pair[0], add] += count
                element_pairs[add, pair[1]] += count
                element_pairs[pair] -= count
        # print(f"step {_}")

    counter = Counter[str](endpoints[-1])
    for pair, count in list(element_pairs.items()):
        counter[pair[0]] += count
    print(counter)

    print(min(counter.values()))
    print(max(counter.values()))
    print(max(counter.values()) - min(counter.values()))
    return max(counter.values()) - min(counter.values())


EXPECTED = 2188189693529
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if main(EXAMPLE_FILE) == EXPECTED:
        main(INPUT_FILE)
