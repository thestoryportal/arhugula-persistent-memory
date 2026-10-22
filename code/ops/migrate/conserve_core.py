"""Pure content conservation for the root switch (Step 413).

compare takes pre/post mappings keyed by normalized relative path. Each row has
the root_manifest fields: source, kind, bytes, sha256, link_text, device, inode,
nlink, mode. Actions are a list/tuple of (relative path, pre hash, post hash)
for done REPLACEs only. The caller selects actions under the moving root.
Return sorted (path, field/reason) findings; malformed input raises Refusal.
Source and nlink are validated but not compared (R413-1).
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
import re

from ops.migrate import fdsafe

Refusal = fdsafe.Refusal


@dataclass(frozen=True)
class Leaf:
    kind: str
    bytes: int
    sha256: str
    link_text: str | None
    device: int
    inode: int
    mode: int


def _path(value, where, absolute=False):
    if not isinstance(value, str) or "\0" in value:
        raise Refusal(where, "expected a normalized path")
    parts = value[1:] if absolute else value
    if value.startswith("/") != absolute or any(p in ("", ".", "..") for p in parts.split("/")):
        raise Refusal(where, "expected a normalized path")
    return value


def _sha(value, where):
    if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{64}", value) is None:
        raise Refusal(where, "expected a lowercase hex sha256")
    return value


def _manifest(value, where) -> dict[str, Leaf]:
    if not isinstance(value, Mapping):
        raise Refusal(where, "expected a manifest mapping")
    result = {}
    for path, row in value.items():
        _path(path, where)
        location = f"{where}[{path!r}]"
        if not isinstance(row, Mapping):
            raise Refusal(location, "expected a leaf mapping")
        for field in ("source", "kind", "bytes", "sha256", "link_text", "device", "inode", "nlink", "mode"):
            if field not in row:
                raise Refusal(location, f"missing {field}")
        _path(row["source"], location, absolute=True)
        kind, link = row["kind"], row["link_text"]
        if kind not in ("file", "symlink", "socket"):
            raise Refusal(location, "unknown leaf kind")
        for field in ("bytes", "device", "inode", "nlink", "mode"):
            number = row[field]
            if type(number) is not int or number < 0:
                raise Refusal(location, f"{field} must be a non-negative integer")
        if row["mode"] > 0o7777:
            raise Refusal(location, "mode must contain permission bits only")
        if kind == "symlink":
            if not isinstance(link, str) or not link or "\0" in link:
                raise Refusal(location, "expected non-empty link text without NUL")
        elif link is not None:
            raise Refusal(location, "non-link has link text")
        # [LAW:parse-dont-validate] Only checked immutable leaves reach comparison.
        result[path] = Leaf(kind, row["bytes"], _sha(row["sha256"], location), link,
                            row["device"], row["inode"], row["mode"])
    return result


def _actions(value) -> dict[str, tuple[str, str]]:
    if not isinstance(value, (list, tuple)):
        raise Refusal("actions", "expected a list or tuple")
    result = {}
    for action in value:
        if not isinstance(action, (list, tuple)) or len(action) != 3:
            raise Refusal("actions", "expected (path, pre sha256, post sha256)")
        path = _path(action[0], "actions")
        if path in result:
            raise Refusal(path, "duplicate REPLACE")
        result[path] = (_sha(action[1], "actions"), _sha(action[2], "actions"))
    return result


def compare(pre: Mapping, post: Mapping, actions: list | tuple) -> tuple[tuple[str, str], ...]:
    """Compare supplied values without reading or changing any external state."""
    before, after, repairs = _manifest(pre, "pre"), _manifest(post, "post"), _actions(actions)
    findings = []
    for path in before.keys() | after.keys() | repairs.keys():
        for manifest, reason in ((before, "missing-pre"), (after, "missing-post")):
            if path not in manifest:
                findings.append((path, reason))
        if path not in before or path not in after:
            continue
        left, right = before[path], after[path]
        fields = ("kind", "bytes", "sha256", "mode", "link_text", "device", "inode")
        if path in repairs:
            if left.kind != "file" or right.kind != "file":
                raise Refusal(path, "REPLACE requires regular files")
            # [LAW:dataflow-not-control-flow] W6 changes the compared fields as data.
            fields = ("kind", "mode", "link_text", "device")
            pre_hash, post_hash = repairs[path]
            for actual, expected, reason in ((left.sha256, pre_hash, "replace-pre-sha256"),
                                              (right.sha256, post_hash, "replace-post-sha256")):
                if actual != expected:
                    findings.append((path, reason))
        for field in fields:
            if getattr(left, field) != getattr(right, field):
                findings.append((path, field))
    return tuple(sorted(findings))
