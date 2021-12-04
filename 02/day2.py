commands = """\
forward 5
down 5
forward 8
up 3
down 8
forward 2
"""

with open("day2.txt", "r", encoding="utf8") as f:
    commands = f.read()

aim = 0
horizontal = 0
depth = 0

for line in commands.strip().splitlines():
    args = line.split()
    print(line)

    match args:
        case ["forward", n]:
            horizontal += int(n)
            depth += int(n) * aim
        case ["down", n]:
            aim += int(n)
        case ["up", n]:
            aim -= int(n)
        case x:
            assert False, x
    print(f"{horizontal=}, {depth=}, {aim=}")

print(horizontal * depth)
