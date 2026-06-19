#!/usr/bin/env python3
"""Pre-tool boundary checks for Codex.

The hook input shape may evolve, so this script treats stdin as best-effort JSON
and scans all string values for high-confidence boundary violations.
"""

from __future__ import annotations

import json
import re
import sys
from typing import Any

DESIGN_RE = re.compile(
    r"\bdesign-substrate/|Spec_[A-Za-z_]+_v\d|Implementation_Plan_[A-Za-z_]+_v\d|ADR-[FD]\d"
)
IMPL_RE = re.compile(r"\bharness-[a-z]+/(?:src|tests)/|\btests/")
DESTRUCTIVE_RE = re.compile(r"\b(?:git\s+reset\s+--hard|git\s+checkout\s+--|rm\s+-rf)\b")


def strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        out: list[str] = []
        for key, item in value.items():
            out.extend(strings(key))
            out.extend(strings(item))
        return out
    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            out.extend(strings(item))
        return out
    return []


raw = sys.stdin.read()
try:
    payload: Any = json.loads(raw) if raw.strip() else {}
except json.JSONDecodeError:
    payload = raw

joined = "\n".join(strings(payload))

if DESIGN_RE.search(joined) and IMPL_RE.search(joined):
    print(
        "Blocked by Codex project hook: command appears to mix design-substrate/spec/plan "
        "work with implementation/test work. Split the arc or declare an explicit back-flow scope.",
        file=sys.stderr,
    )
    sys.exit(2)

if DESTRUCTIVE_RE.search(joined):
    print(
        "Blocked by Codex project hook: destructive command requires explicit operator direction.",
        file=sys.stderr,
    )
    sys.exit(2)

sys.exit(0)
