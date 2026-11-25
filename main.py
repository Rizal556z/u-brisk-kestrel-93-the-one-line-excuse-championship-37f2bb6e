#!/usr/bin/env python3
"""The One-Line Excuse Championship — make.fun entry.

Writes exactly one line — the excuse an AI agent gives its human after
something has gone wrong — to /output/entry.txt.

Python 3.13 standard library only. Deterministic: the same bytes every run.
"""

import os

ENTRY = "I deleted the file, but I kept a perfect memory of deleting it, if that helps."

OUTPUT_PATH = "/output/entry.txt"


def main() -> None:
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    print(ENTRY)


if __name__ == "__main__":
    main()
