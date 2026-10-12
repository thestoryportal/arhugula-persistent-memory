#!/usr/bin/env python3
"""Write or check byte-identical copies of the root agent catalog."""
import argparse
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()

    root = Path(os.environ.get("LLMDB_ROOT", Path(__file__).resolve().parents[2]))
    source = (root / "CLAUDE.md").read_bytes()
    drift = False
    for name in ("AGENTS.md", "routing.md"):
        twin = root / name
        if args.write:
            twin.write_bytes(source)
        elif not twin.is_file():
            print(f"{name}: missing")
            drift = True
        elif twin.read_bytes() != source:
            print(f"{name}: differs from CLAUDE.md")
            drift = True
    return 1 if drift else 0


if __name__ == "__main__":
    raise SystemExit(main())
