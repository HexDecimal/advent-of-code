with open("day1.txt", "r", encoding="utf8") as f:
    depth_samples = [int(line) for line in f.read().strip().splitlines()]

# depth_samples = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]

depth_window = [sum(abc) for abc in zip(depth_samples[:], depth_samples[1:], depth_samples[2:])]


print(sum(first < second for first, second in zip(depth_window[:], depth_window[1:])))
