from __future__ import annotations

import itertools
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import tcod.ecs
import tcod.ecs.callbacks
from aoc import ints
from tcod.ecs import Entity, World
from tqdm import tqdm

BlockShape: TypeAlias = frozenset[tuple[int, int, int]]
RestingOn: Final = "RestingOn"


@tcod.ecs.callbacks.register_component_changed(component=BlockShape)
def obj_shape_changed(entity: Entity, old: BlockShape | None, new: BlockShape | None) -> None:
    for pos in old or ():
        entity.tags.remove(pos)
    for pos in new or ():
        entity.tags.add(pos)


def main(input: str) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    world = World()
    for line in segments[0].split("\n"):
        ints_ = ints(line)
        assert ints_[0] <= ints_[3]
        assert ints_[1] <= ints_[4]
        assert ints_[2] <= ints_[5]
        block = world[object()]
        block.components[BlockShape] = frozenset(
            itertools.product(
                range(ints_[0], ints_[3] + 1), range(ints_[1], ints_[4] + 1), range(ints_[2], ints_[5] + 1)
            )
        )
    blocks = list(world.Q.all_of(components=[BlockShape]).get_entities())
    blocks.sort(key=lambda b: min(z for _, _, z in b.components[BlockShape]))
    for block in tqdm(blocks, desc="Falling blocks"):
        while True:
            next_shape = frozenset((x, y, z - 1) for x, y, z in block.components[BlockShape])
            enter_space = next_shape - block.components[BlockShape]
            if any(z == 0 for _, _, z in enter_space):
                block.tags.add("OnFloor")
                break  # Resting on floor
            touched_blocks = set[Entity]()
            for pos in enter_space:
                touched_blocks |= world.Q.all_of(tags=[pos]).get_entities()
            if touched_blocks:
                block.relation_tags_many[RestingOn] = touched_blocks
                break  # Resting on blocks
            block.components[BlockShape] = next_shape

    def can_destroy(block: Entity) -> bool:
        for upper_block in world.Q.all_of(relations=[(RestingOn, block)]):
            if upper_block.relation_tags_many[RestingOn] == {block}:
                return False
        return True

    return sum(can_destroy(block) for block in blocks)


EXPECTED = 5
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.input"
    INPUT_FILE = THIS_DIR / "input.input"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data, encoding="utf8")
    result = main(EXAMPLE_FILE.read_text(encoding="ansi"))
    if result != EXPECTED:
        print(f"Expected {EXPECTED!r} but got {result!r} instead!")
        raise SystemExit()
    else:
        print("Example passed.")
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
