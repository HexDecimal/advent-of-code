from pathlib import Path

import numpy as np
import scipy.ndimage

THIS_DIR = Path(__file__).parent
FILE = THIS_DIR / "example.txt"
FILE = THIS_DIR / "input.txt"


with open(FILE, "r", encoding="utf8") as f:
    heightmap = np.asarray([[i for i in line] for line in f.read().strip().splitlines()], dtype=int)

low_points = []
risk = 0

for y in range(heightmap.shape[0]):
    for x in range(heightmap.shape[1]):
        here = heightmap[y, x]
        adj = []
        for dx, dy in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
            adj_x = x + dx
            adj_y = y + dy
            if 0 <= adj_x < heightmap.shape[1] and 0 <= adj_y < heightmap.shape[0]:
                adj.append(heightmap[adj_y, adj_x])
        if all(a > here for a in adj):
            # print(f"{here=}, {adj=}")
            low_points.append((y, x))
            risk += 1 + here


labels, label_count = scipy.ndimage.label(heightmap != 9, [[0, 1, 0], [1, 1, 1], [0, 1, 0]])
basin = []
for i in range(1, label_count + 1):
    basin.append((labels == i).sum())

basin.sort()
print(basin[-3:])
print(basin[-1] * basin[-2] * basin[-3])
