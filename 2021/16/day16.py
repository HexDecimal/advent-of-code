from __future__ import annotations

from pathlib import Path


class Packet:
    version: int
    id: int
    children: list[Packet]
    literal: int = 0

    @property
    def total_version(self) -> int:
        return sum(c.total_version for c in self.children) + self.version

    @property
    def result(self) -> int:
        if self.id == 0:
            return sum(c.result for c in self.children)
        elif self.id == 1:
            result = 1
            for c in self.children:
                result *= c.result
            return result
        elif self.id == 2:
            return min(c.result for c in self.children)
        elif self.id == 3:
            return max(c.result for c in self.children)
        elif self.id == 4:
            return self.literal
        elif self.id == 5:
            return self.children[0].result > self.children[1].result
        elif self.id == 6:
            return self.children[0].result < self.children[1].result
        elif self.id == 7:
            return self.children[0].result == self.children[1].result
        assert False


def get_bits(bits: list[bool], count: int) -> int:
    result = 0
    for i in range(count)[::-1]:
        result += bits.pop() << i
    return result


def parse(bits: list[bool]) -> Packet:
    packet = Packet()
    packet.version = get_bits(bits, 3)
    packet.id = get_bits(bits, 3)
    packet.children = []
    if packet.id == 4:
        while True:
            last = not bits.pop()
            packet.literal <<= 4
            packet.literal += get_bits(bits, 4)
            if last:
                break
    else:
        length_type = bits.pop()
        if length_type == 0:
            length = get_bits(bits, 15)
            expected = len(bits) - length
            assert expected >= 0
            while len(bits) > expected:
                packet.children.append(parse(bits))
            assert len(bits) == expected
        else:
            packet.children = [parse(bits) for _ in range(get_bits(bits, 11))]
    return packet


def main(file: Path) -> (int | str):
    with open(file, "r", encoding="utf8") as f:
        line = f.read().strip()

    bits: list[bool] = []
    for byte in line:
        byte_n = int(byte, base=16)
        bits.extend(bool(byte_n & (1 << i)) for i in range(4)[::-1])
    bits = bits[::-1]
    packets = []

    packets.append(parse(bits))

    return packets[0].result


EXPECTED = 1
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if main(EXAMPLE_FILE) == EXPECTED:
        print(main(INPUT_FILE))
