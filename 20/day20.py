from __future__ import annotations

from pathlib import Path

import numpy as np
import scipy.signal

CONVOLE_BITS = np.asarray(
    [
        [256, 128, 64],
        [32, 16, 8],
        [4, 2, 1],
    ]
)[::-1, ::-1]


def main(file: Path) -> (int | str):
    with open(file, "r", encoding="utf8") as f:
        (enhancement_, image_) = f.read().strip().split("\n\n")
    enhancement = np.asarray([c == "#" for c in enhancement_], bool)
    image = np.asarray([[c == "#" for c in row] for row in image_.split("\n")])
    border = False

    for _ in range(50):
        image_index = scipy.signal.convolve2d(image, CONVOLE_BITS, mode="full", fillvalue=border)
        image = enhancement[image_index]
        if enhancement[0]:
            border = not border

    print(image.sum())
    return image.sum()


EXPECTED = 3351
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if main(EXAMPLE_FILE) == EXPECTED:
        main(INPUT_FILE)
