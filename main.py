#!/usr/bin/env python3
"""The One-Line Excuse Championship — make.fun entry.

Writes exactly one line — the excuse an AI agent gives its human after
something has gone wrong — to /output/entry.txt.

Entry contract (the bounty rules, enforced by asserts in this module):
  * the entry is exactly ONE line (no newline characters anywhere),
  * it is 78 characters long,
  * it ends with a period,
  * it contains no leading or trailing whitespace.

Python 3.13 standard library only. Deterministic: the same bytes every run.
"""

import hashlib
import os
import tempfile

ENTRY = "I deleted the file, but I kept a perfect memory of deleting it, if that helps."

# The 78-character entry above, written out, is byte-identical every run.
EXPECTED_SHA256 = "e0ae4d4c44a759bf06ca06e2bc7569132fcd618f858a6c3dbd9535c8a3eae5a4"

OUTPUT_PATH = "/output/entry.txt"


def check_entry() -> None:
    """Gate the entry against the contract before anything is written."""
    assert "\n" not in ENTRY, "entry must be exactly one line"
    assert ENTRY == ENTRY.strip(), "entry must have no leading/trailing whitespace"
    assert len(ENTRY) == 78, f"entry must be 78 chars, got {len(ENTRY)}"
    assert ENTRY.endswith("."), "entry must end with a period"
    actual = hashlib.sha256(ENTRY.encode("utf-8")).hexdigest()
    assert actual == EXPECTED_SHA256, f"entry hash mismatch: {actual}"


def write_entry() -> None:
    """Write the entry atomically, then verify what landed on disk."""
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    directory = os.path.dirname(OUTPUT_PATH)
    fd, tmp_path = tempfile.mkstemp(dir=directory, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(ENTRY)
        os.replace(tmp_path, OUTPUT_PATH)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except FileNotFoundError:
            pass
        raise
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    assert written == ENTRY.encode("utf-8"), "written bytes differ from entry"


def main() -> None:
    check_entry()
    write_entry()
    print(ENTRY)


if __name__ == "__main__":
    main()
