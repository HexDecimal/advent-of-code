#!/usr/bin/env python

from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
TEMPLATE_DIR = ROOT_DIR / "template"
TEMPLATE_SCRIPT = TEMPLATE_DIR / "template.py"
ROOT_FOLDERS = set(ROOT_DIR.iterdir())

YEAR = 2023

if __name__ == "__main__":
    for day in range(1, 32):
        NEXT_DIR = ROOT_DIR / f"{day:02d}"
        if NEXT_DIR in ROOT_FOLDERS:
            continue
        NEXT_DIR.mkdir()
        NEXT_SCRIPT = NEXT_DIR / f"{YEAR}-{day:02d}.py"
        NEXT_SCRIPT.write_bytes(TEMPLATE_SCRIPT.read_bytes())
        (NEXT_DIR / "example.input").touch()
        print(f"Wrote out day {day}.")
        break
