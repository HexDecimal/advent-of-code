from __future__ import annotations

import functools
import itertools
import re
from collections import Counter
from pathlib import Path

import aocd  # type: ignore
import numpy as np

RE_RULE = re.compile(r"(?P<container>.+) bags? contain (?P<contains>.+)")
RE_BAG = re.compile(r"(?P<number>\d+?) (?P<color>.+?) bags?")


def main(file: Path) -> (int | str | None):
    segments = file.read_text(encoding="ansi").strip().split("\n\n")
    # lines = np.asarray(segments[0], int)
    lines = segments[0].split("\n")
    rules: dict[str, Counter[str]] = {}
    for line in lines:
        match = RE_RULE.match(line)
        assert match
        rules[match["container"]] = Counter()
        for sub_match in RE_BAG.finditer(match["contains"]):
            rules[match["container"]][sub_match["color"]] += int(sub_match["number"])

    full_rules: dict[str, Counter[str]] = {}
    for bag, to_parse in rules.items():
        full_rules[bag] = Counter()
        to_parse = to_parse.copy()
        while to_parse:
            nested_color, nested_number = to_parse.popitem()
            full_rules[bag][nested_color] += nested_number
            to_parse += Counter({k: v * nested_number for k, v in rules[nested_color].items()})

    # return sum(bool(can_contain["shiny gold"]) for can_contain in full_rules.values())
    return sum(full_rules["shiny gold"].values())


EXPECTED = 32
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data + "\n", encoding="utf8")
    if main(EXAMPLE_FILE) == EXPECTED:
        aocd.submit(main(INPUT_FILE))
