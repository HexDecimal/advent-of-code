from __future__ import annotations

import re
from pathlib import Path

import aocd  # type: ignore

REQUIRED = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}


def valid_byr(string: str) -> bool:
    match = re.match(r"\d{4}$", string)
    return match is not None and 1920 <= int(match.group()) <= 2002


def valid_iyr(string: str) -> bool:
    match = re.match(r"\d{4}$", string)
    return match is not None and 2010 <= int(match.group()) <= 2020


def valid_eyr(string: str) -> bool:
    match = re.match(r"\d{4}$", string)
    return match is not None and 2020 <= int(match.group()) <= 2030


def valid_hgt(string: str) -> bool:
    match = re.match(r"(\d+)(in|cm)$", string)
    if not match:
        return False
    match match.groups():
        case (h, "cm"):
            return 150 <= int(h) <= 193
        case (h, "in"):
            return 59 <= int(h) <= 76
        case _:
            return False


def valid_hcl(string: str) -> bool:
    match = re.match(r"#[0-9a-f]{6}$", string)
    return bool(match)


def valid_ecl(string: str) -> bool:
    return string in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}


def valid_pid(string: str) -> bool:
    match = re.match(r"\d{9}$", string)
    return bool(match)


def valid_cid(string: str) -> bool:
    return True


FIELDS = re.compile(r"(\S+):(\S+)")


def check(segment: str) -> bool:
    fields = {k: v for k, v in FIELDS.findall(segment)}
    if not REQUIRED.issubset(fields.keys()):
        return False
    if not all(globals()[f"valid_{key}"](value) for key, value in fields.items()):
        return False
    return True


def main(file: Path) -> (int | str | None):
    segments = file.read_text(encoding="ansi").strip().split("\n\n")
    valid = 0
    for segment in segments:
        valid += check(segment)

    return valid


assert not check("eyr:1972 cid:100 hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926")
assert not check("iyr:2019 hcl:#602927 eyr:1967 hgt:170cm ecl:grn pid:012533040 byr:1946")
assert not check("hcl:dab227 iyr:2012 ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277")
assert not check("hgt:59cm ecl:zzz eyr:2038 hcl:74454a iyr:2023 pid:3556412378 byr:2007")

assert check(
    """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f"""
)
assert check(
    """eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm"""
)
assert check(
    """hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022"""
)
assert check("""iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719""")


EXPECTED = 2
if __name__ == "__main__":
    THIS_DIR = Path(__file__).parent
    EXAMPLE_FILE = THIS_DIR / "example.txt"
    INPUT_FILE = THIS_DIR / "input.txt"
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(aocd.data + "\n", encoding="utf8")
    if main(EXAMPLE_FILE) == EXPECTED:
        aocd.submit(main(INPUT_FILE))
