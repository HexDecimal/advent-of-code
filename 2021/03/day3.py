from typing import Reversible, Tuple

import numpy as np
from numpy.typing import NDArray

report = """
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""

with open("day3.txt", "r", encoding="utf8") as f:
    report = f.read()

report_lines = report.strip().splitlines()
report_width = len(report_lines[0])
mask = (1 << report_width) - 1

counts = [0] * report_width

for line in report_lines:
    for i, bit in enumerate(line):
        counts[i] += int(bit)


gamma = 0
for i, count in enumerate(reversed(counts)):
    more = count > len(report_lines) // 2
    gamma |= more << i
epsilon = gamma ^ mask


# print(f"{gamma=},{gamma:b}")
# print(f"{epsilon=},{epsilon:b}")
# print(gamma * epsilon)

report_data = np.asarray([[int(c) for c in line] for line in report_lines], dtype=np.bool8)


most = report_data.copy()
least = report_data.copy()


def sort_bits(array_in: NDArray[np.bool8]) -> Tuple[int, int]:
    """Return (most bit, least bit) from a 1d bool array."""
    true_bits = array_in.sum()
    false_bits = array_in.size - true_bits
    if true_bits == false_bits:
        return True, False
    if true_bits > false_bits:
        return True, False
    return False, True


for i in range(report_width):
    if most.shape[0] > 1:
        which_most, _ = sort_bits(most[:, i])
        most = most[most[:, i] == which_most]
    if least.shape[0] > 1:
        _, which_least = sort_bits(least[:, i])
        least = least[least[:, i] == which_least]


def bits_to_int(array: NDArray[np.bool8]) -> int:
    return sum(bit << i for i, bit in enumerate(array[::-1].tolist()))


most_result = bits_to_int(most[0])
least_result = bits_to_int(least[0])

print(f"{most_result=},{most=}")
print(f"{least_result=},{least=}")

print(most_result * least_result)
