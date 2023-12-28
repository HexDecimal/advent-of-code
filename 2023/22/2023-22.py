from __future__ import annotations

import copy
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
    if old == new:
        return
    for pos in old or ():
        entity.tags.remove(pos)
    for pos in new or ():
        entity.tags.add(pos)


def main(input: str) -> int | str | None:
    segments = input.rstrip("\n").split("\n\n")
    world = World()
    world[None].components[("count", int)] = 0
    for i, line in enumerate(segments[0].split("\n")):
        ints_ = ints(line)
        assert ints_[0] <= ints_[3]
        assert ints_[1] <= ints_[4]
        assert ints_[2] <= ints_[5]
        block = world[i]
        block.components[BlockShape] = frozenset(
            itertools.product(
                range(ints_[0], ints_[3] + 1), range(ints_[1], ints_[4] + 1), range(ints_[2], ints_[5] + 1)
            )
        )
        world[None].components[("count", int)] += 1

    def lowest_block_key(block: Entity) -> int:
        return min(z for _, _, z in block.components[BlockShape])

    def solve_falling_blocks(world: World, bar: bool = False) -> int:
        blocks = list(world.Q.all_of(components=[BlockShape]).get_entities())
        blocks.sort(key=lowest_block_key)
        has_fallen = set()
        for block in tqdm(blocks, desc="falling blocks", disable=not bar):
            current_shape = block.components[BlockShape]
            while True:
                next_shape = frozenset((x, y, z - 1) for x, y, z in current_shape)
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
                has_fallen.add(block)
                current_shape = next_shape
            block.components[BlockShape] = current_shape
        return len(has_fallen)

    def count_chain(uid: int) -> int:
        del world[uid].components[BlockShape]
        result = solve_falling_blocks(world)
        for block in world.Q.all_of(components=[("original", BlockShape)]):
            block.components[BlockShape] = block.components[("original", BlockShape)]
        return result

    solve_falling_blocks(world, bar=True)
    for block in world.Q.all_of(components=[BlockShape]):
        block.components[("original", BlockShape)] = block.components[BlockShape]
    return sum(count_chain(uid) for uid in tqdm(range(world[None].components[("count", int)]), desc="checking blocks"))


EXPECTED = 7
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
