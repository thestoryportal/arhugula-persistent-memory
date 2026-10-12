#!/usr/bin/env python3
"""Write or check byte-identical copies of the root and map agent catalogs."""
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
    drift = False
    for catalog in ("CLAUDE.md", "map/CLAUDE.md"):
        source_path = root / catalog
        if not source_path.is_file():
            print(f"{catalog}: missing")
            drift = True
            continue
        source = source_path.read_bytes()
        for name in ("AGENTS.md", "routing.md"):
            relative = Path(catalog).with_name(name)
            twin = root / relative
            if args.write:
                if not twin.is_file() or twin.read_bytes() != source:
                    twin.write_bytes(source)
            elif not twin.is_file():
                print(f"{relative}: missing")
                drift = True
            elif twin.read_bytes() != source:
                print(f"{relative}: differs from {catalog}")
                drift = True
    return 1 if drift else 0


if __name__ == "__main__":
    raise SystemExit(main())
