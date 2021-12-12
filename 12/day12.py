from pathlib import Path
from typing import DefaultDict, Iterator

THIS_DIR = Path(__file__).parent


def main(file: Path) -> (int | str):
    with open(file, "r", encoding="utf8") as f:
        lines = f.read().strip().splitlines()
    connections = DefaultDict[str, set[str]](set)

    for line in lines:
        a, b = line.split("-")
        connections[a].add(b)
        connections[b].add(a)

    def visit_all(visited: list[str] = ["start"], second_used=False) -> Iterator[list[str]]:
        if visited[-1] == "end":
            yield visited
            return
        for passage in connections[visited[-1]]:
            if passage == "start":
                continue
            if passage.islower() and passage in visited:
                if not second_used:
                    yield from visit_all(visited + [passage], second_used=True)
                continue
            yield from visit_all(visited + [passage], second_used)

    paths = list(visit_all())
    print(len(paths))

    return len(paths)


EXPECTED = 3509
if __name__ == "__main__":
    if main(THIS_DIR / "example.txt") == EXPECTED:
        main(THIS_DIR / "input.txt")
