"""Compare checkpoint/live notebook pairs through held directories (T383)."""
from __future__ import annotations

import argparse
import contextlib
import errno
import os
import sys

from ops.migrate import fdsafe, notebook_compare_core as core


def _split(path: str) -> tuple[str, str]:
    with fdsafe.fs(path):
        return os.path.split(os.path.abspath(path))


def _pairs(path: str, data: bytes) -> list[tuple[str, str]]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        line = data[:exc.start].count(b"\n") + 1
        raise fdsafe.Refusal(path, f"line {line}: invalid UTF-8") from exc
    if not text.endswith("\n"):
        raise fdsafe.Refusal(path, f"line {text.count(chr(10)) + 1}: missing final newline")
    lines = text[:-1].split("\n")
    if lines[0] != "checkpoint\tlive":
        raise fdsafe.Refusal(path, "line 1: expected checkpoint<TAB>live header")
    rows = []
    seen = set()
    for number, line in enumerate(lines[1:], 2):
        fields = line.split("\t")
        if len(fields) != 2:
            raise fdsafe.Refusal(path, f"line {number}: expected two fields")
        for field in fields:
            if not os.path.isabs(field) or field != os.path.normpath(field):
                raise fdsafe.Refusal(path, f"line {number}: expected absolute normalized paths")
        checkpoint, live = fields
        if checkpoint in seen:
            raise fdsafe.Refusal(path, f"line {number}: repeated checkpoint")
        seen.add(checkpoint)
        rows.append((checkpoint, live))
    if not rows:
        raise fdsafe.Refusal(path, "line 2: expected at least one pair")
    return rows


def run(pairs_path: str, out: str) -> str:
    with contextlib.ExitStack() as stack:
        parents: dict[str, fdsafe.Dir] = {}

        def held(path: str) -> fdsafe.Dir:
            if path not in parents:
                parents[path] = stack.enter_context(fdsafe.hold_root(path))
            return parents[path]

        parent, name = _split(pairs_path)
        rows = _pairs(pairs_path, fdsafe.read_named(held(parent), name))
        pair_rows, cell_rows = [], []
        for checkpoint, live in rows:
            cp_parent, cp_name = os.path.split(checkpoint)
            live_parent, live_name = os.path.split(live)
            checkpoint_bytes = fdsafe.read_named(held(cp_parent), cp_name)
            live_dir = held(live_parent)
            try:
                live_bytes = fdsafe.read_named(live_dir, live_name)
            except fdsafe.Refusal as exc:
                if exc.errno != errno.ENOENT:
                    raise
                live_bytes = None
            pair, cells = core.compare(checkpoint, checkpoint_bytes, live, live_bytes)
            pair_rows.append(pair)
            cell_rows.extend(cells)
        out_parent, out_name = _split(out)
        parent = stack.enter_context(fdsafe.open_out_parent(out_parent))
        roots = list(parents.values())
        parent_live = parent.live()
        for root in roots:
            if fdsafe.inside(root.live(), parent_live):
                raise fdsafe.Refusal(out, f"output parent is inside root {root.path}")
        outdir = stack.enter_context(fdsafe.mkdir(parent, out_name))
        for name, fields, records in (("pairs.tsv", core.PAIR_FIELDS, pair_rows),
                                      ("cells.tsv", core.CELL_FIELDS, cell_rows)):
            fdsafe.create_file(outdir, name, core.render(fields, records), roots)
            kept = f"{os.path.join(outdir.path, name)} (created, left in place)"
            if fdsafe.live_path(outdir.fd, kept) != outdir.path:
                raise fdsafe.Refusal(kept, "output directory moved during the write")
    counts = {status: sum(row["status"] == status for row in pair_rows)
              for status in ("exact", "differing", "unmatched")}
    unique = sum(int(row["unique_cells"]) for row in pair_rows)
    return (f"{len(pair_rows)} pairs: {counts['exact']} exact, {counts['differing']} differing, "
            f"{counts['unmatched']} unmatched; {unique} unique cells")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pairs", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    try:
        summary = run(args.pairs, args.out)
    except fdsafe.Refusal as exc:
        print(exc, file=sys.stderr)
        return 1
    print(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
