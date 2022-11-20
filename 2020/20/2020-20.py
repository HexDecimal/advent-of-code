from __future__ import annotations

import functools
import operator
import re
from pathlib import Path
from typing import *  # noqa: F403

import aocd  # type: ignore
import numpy as np
import scipy.signal
from numpy.typing import NDArray

reduce_mulitply = functools.partial(functools.reduce, operator.mul)


def as_2d_bools(str_list: Iterable[str] | str, truthy: str = "#") -> NDArray[np.bool_]:
    if isinstance(str_list, str):
        str_list = str_list.splitlines()
    return np.array([[c == truthy for c in row] for row in str_list], dtype=np.bool_)


def pack_bits(array: NDArray[np.bool_]) -> int:
    return (array << np.arange(len(array))).sum()


class Tile:
    def __init__(self, string: str):
        lines = string.splitlines()
        match = re.match(r"Tile (?P<index>\d{4}):$", lines[0])
        assert match
        self.index = int(match["index"])
        self.array = as_2d_bools(lines[1:])
        self.edges = self.generate_edges()

    def generate_edges(self) -> tuple[int, int, int, int, int, int, int, int]:
        return (
            pack_bits(self.array[0, :]),  # N
            pack_bits(self.array[0, ::-1]),  # Flipped
            pack_bits(self.array[:, -1]),  # E
            pack_bits(self.array[::-1, -1]),
            pack_bits(self.array[-1, :]),  # S
            pack_bits(self.array[-1, ::-1]),
            pack_bits(self.array[:, 0]),  # W
            pack_bits(self.array[::-1, 0]),
        )


def part1(input: str) -> (int | str | None):
    segments = input.strip().split("\n\n")
    tiles = [Tile(segment) for segment in segments]

    all_edges = DefaultDict[int, set[Tile]](set)
    for tile in tiles:
        for edge in tile.edges:
            all_edges[edge].add(tile)

    total = 1
    for tile in tiles:
        surounding = set()
        for edge in tile.edges:
            surounding |= all_edges[edge]
        surounding.remove(tile)
        print(f"{tile.index=}, {len(surounding)}")
        if len(surounding) == 2:
            total *= tile.index

    return total


PATTERN_STR = """\
                  # \n\
#    ##    ##    ###
 #  #  #  #  #  #   """

PATTERN = as_2d_bools(PATTERN_STR).astype(np.int32)

IJ = tuple[int, int]

COMPASS_NESW = ((-1, 0), (0, 1), (1, 0), (0, -1))


def main(input: str) -> (int | str | None):
    segments = input.strip().split("\n\n")
    unplaced_tiles = [Tile(segment) for segment in segments]

    all_edges = DefaultDict[int, set[Tile]](set)
    for tile in unplaced_tiles:
        for edge in tile.edges:
            all_edges[edge].add(tile)

    def surrounding_unplaced(tile: Tile) -> set[Tile]:
        surounding = set()
        for edge in tile.edges:
            surounding |= all_edges[edge]
        surounding.discard(tile)
        return surounding

    def count_surrounding_unplaced(tile: Tile) -> int:
        surounding = set()
        for edge in tile.edges:
            surounding |= all_edges[edge]
        surounding.discard(tile)
        return len(surounding)

    placed_tiles_by_pos: dict[IJ, Tile] = {}
    placed_tiles: dict[Tile, IJ] = {}
    unresolved_tiles: list[Tile] = []

    def place_tile(tile: Tile, pos: tuple[int, int]) -> None:
        placed_tiles_by_pos[pos] = tile
        placed_tiles[tile] = pos
        unplaced_tiles.remove(tile)
        for edge in tile.edges:
            all_edges[edge].remove(tile)
            if not all_edges[edge]:
                del all_edges[edge]
        unresolved_tiles.append(tile)

    place_tile(min(unplaced_tiles, key=count_surrounding_unplaced), (0, 0))

    while unresolved_tiles:
        next_tile = min(unresolved_tiles, key=count_surrounding_unplaced)
        unresolved_tiles.remove(next_tile)
        tile_y, tile_x = placed_tiles[next_tile]
        while adj_tiles := surrounding_unplaced(next_tile):
            adj_tile = adj_tiles.pop()
            matching_edges = set(next_tile.edges[::2]) & set(adj_tile.edges)
            assert len(matching_edges) == 1
            for match_edge in matching_edges:
                tile_edge_index = next_tile.edges[::2].index(match_edge)
                dy, dx = COMPASS_NESW[tile_edge_index]
                new_y, new_x = tile_y + dy, tile_x + dx
                if (new_y, new_x) in placed_tiles_by_pos:
                    continue
                expected_edge_index = (tile_edge_index + 2) * 2 % 8

                # Rotate
                adj_edge_index = adj_tile.edges.index(match_edge)
                adj_tile.array = np.rot90(adj_tile.array, k=(adj_edge_index - expected_edge_index) // 2)
                adj_tile.edges = adj_tile.generate_edges()

                # Flip
                adj_edge_index = adj_tile.edges.index(match_edge)
                if adj_edge_index != expected_edge_index:
                    if adj_edge_index == 1 or adj_edge_index == 5:
                        adj_tile.array = np.flip(adj_tile.array, axis=1)
                    if adj_edge_index == 3 or adj_edge_index == 7:
                        adj_tile.array = np.flip(adj_tile.array, axis=0)
                adj_tile.edges = adj_tile.generate_edges()

                adj_edge_index = adj_tile.edges.index(match_edge)
                assert adj_edge_index == expected_edge_index

                assert next_tile.edges[tile_edge_index * 2] == adj_tile.edges[(tile_edge_index * 2 + 4) % 8]
                assert adj_tile.edges[(tile_edge_index * 2 + 4) % 8] == match_edge
                print("TILE CONNTECTED")
                place_tile(adj_tile, (new_y, new_x))
                break

            else:  # nobreak
                assert False

    flip_i = False
    flip_j = False
    max_i = 0
    max_j = 0
    for pos in placed_tiles_by_pos:
        flip_i |= pos[0] < 0
        flip_j |= pos[1] < 0

    for tile, (i, j) in list(placed_tiles.items()):
        if flip_i:
            tile.array = np.flip(tile.array, axis=0)
        if flip_j:
            tile.array = np.flip(tile.array, axis=1)
        del placed_tiles_by_pos[i, j]
        i = abs(i)
        j = abs(j)
        placed_tiles_by_pos[i, j] = tile
        max_i = max(max_i, i)
        max_j = max(max_j, j)

    for (i, j), tile in placed_tiles_by_pos.items():
        if i:
            assert (placed_tiles_by_pos[i - 1, j].array[-1, :] == tile.array[0, :]).all()
        if j:
            assert (placed_tiles_by_pos[i, j - 1].array[:, -1] == tile.array[:, 0]).all()

    for (i, j), tile in placed_tiles_by_pos.items():
        tile.array = tile.array[1:-1, 1:-1]  # Remove padding

    final_image = np.vstack(
        [np.hstack([placed_tiles_by_pos[i, j].array for j in range(max_j + 1)]) for i in range(max_i + 1)]
    )
    sea_monsters = 0
    for _ in range(2):
        final_image = final_image[::-1]
        for _ in range(4):
            final_image = np.rot90(final_image, 1)
            found = (scipy.signal.convolve(final_image, PATTERN) == PATTERN.sum()).sum()
            sea_monsters = max(sea_monsters, found)
            if sea_monsters:
                break
        if sea_monsters:
            break

    print(" ---")
    for row in final_image:
        print("".join(".#"[i] for i in row.tolist()))

    print(f"{sea_monsters=}")
    return final_image.sum() - sea_monsters * PATTERN.sum()


EXPECTED = 273
if __name__ == "__main__":
    np.seterr("raise")
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data + "\n", encoding="utf8")
    result = main(EXAMPLE_FILE.read_text(encoding="ansi"))
    assert result == EXPECTED, f"{result} != {EXPECTED}"
    print("Example result is correct.")
    aocd.submit(main(INPUT_FILE.read_text(encoding="ansi")))
