#!/usr/bin/env python3
"""H-SLICE item 5 staging check: the staged index must equal a ticket's admitted move list.

Read only. It runs one Git command, `git -C REPO diff --cached --name-status -M -z`,
and never stages, commits or moves anything.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

# A row is (status, path) or ("R100", src, dst). Staged renames keep their score (e.g. "R087"),
# so a rename below R100 can never equal an admitted R100 row.
ADMITTED_ARITY = {"R100": 3, "D": 2, "M": 2, "A": 2}
ONE_PATH = frozenset("ADMTUXB")
TWO_PATHS = frozenset("RC")


def format_row(row: tuple) -> str:
    return "\t".join(row)


def parse_staged(raw: bytes) -> frozenset:
    fields = raw.split(b"\0")
    if fields[-1] != b"":
        raise ValueError("staged output does not end with NUL")
    fields = fields[:-1]
    rows, i = [], 0
    while i < len(fields):
        status = fields[i].decode("ascii", "strict")
        if status in ONE_PATH:
            width = 1
        elif status[:1] in TWO_PATHS and status[1:].isdigit():
            width = 2
        else:
            raise ValueError(f"unknown staged status {status!r}")
        paths = fields[i + 1:i + 1 + width]
        if len(paths) != width or not all(paths):
            raise ValueError(f"truncated staged record {status!r}")
        rows.append((status, *(p.decode("utf-8", "strict") for p in paths)))
        i += 1 + width
    return frozenset(rows)


def parse_admitted(text: str) -> frozenset:
    rows, seen = set(), set()
    for n, line in enumerate(text.split("\n"), 1):
        if not line:
            continue
        row = tuple(line.split("\t"))
        if row[0] not in ADMITTED_ARITY:
            raise ValueError(f"admitted line {n}: status {row[0]!r} is not R100, D, M or A")
        if len(row) != ADMITTED_ARITY[row[0]]:
            raise ValueError(f"admitted line {n}: {row[0]} needs {ADMITTED_ARITY[row[0]] - 1} path(s)")
        if not all(row[1:]):
            raise ValueError(f"admitted line {n}: empty path")
        if row in rows:
            raise ValueError(f"admitted line {n}: duplicate row {format_row(row)!r}")
        for path in row[1:]:
            if path in seen:
                raise ValueError(f"admitted line {n}: path {path!r} is in two rows")
            seen.add(path)
        rows.add(row)
    return frozenset(rows)


def compare(admitted: frozenset, staged: frozenset) -> tuple:
    return sorted(admitted - staged), sorted(staged - admitted)


def git_env() -> dict:
    # GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE override -C, so an inherited one would read another index.
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def run(repo: str, admitted_text: str) -> dict:
    admitted = parse_admitted(admitted_text)
    proc = subprocess.run(["git", "-C", repo, "diff", "--cached", "--name-status", "-M", "-z"],
                          env=git_env(), capture_output=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"git diff --cached exited {proc.returncode}: {proc.stderr.decode(errors='replace').strip()}")
    missing, extra = compare(admitted, parse_staged(proc.stdout))
    return {"ok": not missing and not extra,
            "missing": [format_row(r) for r in missing],
            "extra": [format_row(r) for r in extra]}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--admitted", required=True, metavar="FILE")
    args = ap.parse_args(argv)
    with open(args.admitted, encoding="utf-8") as f:
        text = f.read()
    try:
        result = run(args.repo, text)
    except (ValueError, RuntimeError) as exc:
        print(f"stage_check: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=1))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
