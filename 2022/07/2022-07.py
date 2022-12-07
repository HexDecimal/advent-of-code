from __future__ import annotations

from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore


class Dir:
    def __init__(self, parent: Dir | None = None) -> None:
        self.files = dict[str, int]()
        self.dirs = DefaultDict[str, Dir](lambda: Dir(self))
        self._parent = parent

    @property
    def parent(self) -> Dir:
        assert self._parent
        return self._parent

    def walk(self) -> Iterable[Dir]:
        yield self
        for d in self.dirs.values():
            yield from d.walk()

    @property
    def total_size(self) -> int:
        total = 0
        for d in self.walk():
            total += sum(d.files.values())
        return total


def main(input: str) -> (int | str | None):
    segments = input.rstrip("\n").split("\n\n")
    lines = segments[0].split("\n")
    top_dir = Dir()
    cur_dir = top_dir
    while lines:
        cmd = lines.pop(0)
        match cmd.split():
            case ["$", "cd", "/"]:
                cur_dir = top_dir
            case ["$", "cd", ".."]:
                cur_dir = cur_dir.parent
            case ["$", "cd", x]:
                cur_dir = cur_dir.dirs[x]
            case ["$", "ls"]:
                while lines and lines[0][0] != "$":
                    match lines.pop(0).split():
                        case "dir", new_dir:
                            cur_dir.dirs[new_dir]
                        case size, name:
                            cur_dir.files[name] = int(size)
            case _:
                assert False

    total = 0
    for d in top_dir.walk():
        if d.total_size <= 100000:
            total += d.total_size

    # return total  # part 1

    free_space = 70000000 - top_dir.total_size
    to_free = 30000000 - free_space
    for d in sorted(top_dir.walk(), key=lambda d: d.total_size):
        if d.total_size > to_free:
            return d.total_size

    assert False


EXPECTED = 24933642
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.input"
    INPUT_FILE = THIS_DIR / "input.input"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data, encoding="utf8")
    result = main(EXAMPLE_FILE.read_text(encoding="ansi"))
    if result != EXPECTED:
        raise SystemExit(f"Excepted {EXPECTED!r} but got {result!r} instead!")
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
