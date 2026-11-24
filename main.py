#!/usr/bin/env python3
"""Write one one-line cat joke to /output/entry.txt.

The joke is a fixed string, so the program is fully deterministic: no
network, no clock, no randomness, no input. It writes the joke to the
path given as the first argument, or $OUTPUT_PATH, or /output/entry.txt,
prints exactly the joke to stdout, and refuses to write anything that
breaks the competition gate (a single line of 1 to 200 characters).
"""

import os
import sys
from pathlib import Path

JOKE = (
    "My cat knocked my phone off the table, then looked at me like I was "
    "the one who put it somewhere stupid."
)

OUTPUT_DEFAULT = "/output/entry.txt"


def pick_path(argv):
    if len(argv) > 1:
        return Path(argv[1])
    if os.environ.get("OUTPUT_PATH"):
        return Path(os.environ["OUTPUT_PATH"])
    return Path(OUTPUT_DEFAULT)


def check(joke):
    """Gate: one line, 1 to 200 characters, no em dash."""
    if not 1 <= len(joke) <= 200:
        raise ValueError(f"joke is {len(joke)} characters, outside 1-200")
    if "\n" in joke or "\r" in joke:
        raise ValueError("joke must be a single line")
    if "\u2014" in joke:
        raise ValueError("joke must not contain an em dash")
    if not joke.strip():
        raise ValueError("joke is only white space")


def write_entry(path, text):
    """Write the joke to path; return 0, or 1 with a clean error."""
    if path.is_dir():
        print(f"error: {path} is a directory, give a file path", file=sys.stderr)
        return 1
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    except OSError as exc:
        print(f"error: cannot write {path}: {exc}", file=sys.stderr)
        return 1
    return 0


def main(argv):
    check(JOKE)
    path = pick_path(argv)
    if write_entry(path, JOKE) != 0:
        return 1
    print(JOKE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
