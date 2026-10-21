"""Compare checkpoint/live notebook bytes and render their digest rows (T382).

Input: notebook paths as labels and JSON bytes; None means no live notebook.
Output: one pair row and ordered checkpoint cell rows, or UTF-8 TSV bytes.
Pure: no filesystem, process, clock, environment or random reads; no notebook
execution. Malformed input raises fdsafe.Refusal naming its path or TSV field.
"""
from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence

from ops.migrate import fdsafe
from ops.migrate.unit_manifest import canonical

PAIR_FIELDS = ("checkpoint", "live", "status", "checkpoint_sha256", "live_sha256",
               "checkpoint_cells", "live_cells", "unique_cells")
CELL_FIELDS = ("checkpoint", "index", "cell_type", "cell_sha256", "source_sha256", "in_live")


def _parse(path: str, data: bytes) -> list[dict]:
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                return fdsafe.Refusal(path, f"duplicate key {key!r}")
            result[key] = value
        return result

    def constant(token):
        return fdsafe.Refusal(path, f"invalid JSON constant {token}")

    def check(value, location):
        # Hooks run bottom-up; defer raising until the cell index is known.
        if isinstance(value, fdsafe.Refusal):
            raise fdsafe.Refusal(path, f"{location}: {value}")
        if isinstance(value, dict):
            for key, item in value.items():
                check(item, f"{location}.{key}")
        elif isinstance(value, list):
            for index, item in enumerate(value):
                check(item, f"{location}[{index}]")

    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=pairs, parse_constant=constant)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise fdsafe.Refusal(path, str(exc)) from exc
    check(value, "notebook")
    if not isinstance(value, dict) or not isinstance(value.get("cells"), list):
        raise fdsafe.Refusal(path, "expected an object with a cells list")
    cells = []
    for index, cell in enumerate(value["cells"]):
        where = f"cells[{index}]"
        if not isinstance(cell, dict):
            raise fdsafe.Refusal(path, f"{where}: expected an object")
        if cell.get("cell_type") not in ("code", "markdown", "raw"):
            raise fdsafe.Refusal(path, f"{where}: invalid cell_type")
        source = cell.get("source")
        if not (isinstance(source, str) or
                isinstance(source, list) and all(isinstance(item, str) for item in source)):
            raise fdsafe.Refusal(path, f"{where}: source must be a string or list of strings")
        try:
            source_sha = _sha("".join(source).encode("utf-8"))
            cell_sha = _sha(canonical(cell))
        except UnicodeEncodeError as exc:
            raise fdsafe.Refusal(path, f"{where}: {exc}") from exc
        cells.append({"cell_type": cell["cell_type"], "source_sha256": source_sha,
                      "cell_sha256": cell_sha})
    return cells


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compare(checkpoint_path: str, checkpoint: bytes, live_path: str,
            live: bytes | None) -> tuple[dict[str, str], list[dict[str, str]]]:
    checkpoint_cells = _parse(checkpoint_path, checkpoint)
    live_cells = [] if live is None else _parse(live_path, live)
    live_sources = {cell["source_sha256"] for cell in live_cells}
    cells = []
    for index, cell in enumerate(checkpoint_cells):
        source_sha = cell["source_sha256"]
        cells.append({"checkpoint": checkpoint_path, "index": str(index),
                      "cell_type": cell["cell_type"], "cell_sha256": cell["cell_sha256"],
                      "source_sha256": source_sha,
                      "in_live": "yes" if source_sha in live_sources else "no"})
    pair = {"checkpoint": checkpoint_path, "live": live_path,
            "status": "unmatched" if live is None else "exact" if live == checkpoint else "differing",
            "checkpoint_sha256": _sha(checkpoint),
            "live_sha256": "" if live is None else _sha(live),
            "checkpoint_cells": str(len(checkpoint_cells)),
            "live_cells": "" if live is None else str(len(live_cells)),
            "unique_cells": str(sum(row["in_live"] == "no" for row in cells))}
    return pair, cells


def _field(field: str, value: str) -> bytes:
    try:
        data = value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise fdsafe.Refusal(field, str(exc)) from exc
    if any(byte in data for byte in b"\t\r\n"):
        raise fdsafe.Refusal(field, "value contains tab, CR or LF")
    return data


def render(fields: Sequence[str], rows: Sequence[Mapping[str, str]]) -> bytes:
    lines = [b"\t".join(_field(field, field) for field in fields)]
    for row in rows:
        for field in fields:
            if field not in row:
                raise fdsafe.Refusal(field, "missing field")
        for field in row:
            if field not in fields:
                raise fdsafe.Refusal(field, "extra field")
        lines.append(b"\t".join(_field(field, row[field]) for field in fields))
    return b"\n".join(lines) + b"\n"
