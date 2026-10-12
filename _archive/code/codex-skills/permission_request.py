#!/usr/bin/env python3
"""Permission-request reviewer notes for Codex."""

from __future__ import annotations

import json
import re
import sys
from typing import Any

PATTERNS = [
    (
        "paid provider",
        re.compile(
            r"\b(ANTHROPIC_API_KEY|OPENAI_API_KEY|mvp-r100|mech-beta|real_anthropic|dashboard-elevate)\b",
            re.I,
        ),
    ),
    (
        "credential movement",
        re.compile(r"\b(keychain|secret|token|credential|auth\.json|\.env)\b", re.I),
    ),
    (
        "destructive git/filesystem",
        re.compile(r"\b(git\s+reset\s+--hard|git\s+checkout\s+--|rm\s+-rf)\b", re.I),
    ),
    (
        "network",
        re.compile(
            r"\b(git\s+push|gh\s+pr|curl|wget|npm\s+install|uv\s+sync|pip\s+install)\b", re.I
        ),
    ),
]


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
hits = [label for label, pattern in PATTERNS if pattern.search(joined)]

if hits:
    print(
        "Codex permission posture: request touches "
        + ", ".join(hits)
        + ". Confirm explicit operator authorization and least scope. "
        "If no HIL/approval surface is available, build to the gate, then run "
        "`just codex-credential-gate --unit ... --gate ... --forward-closed ... --resume ...` "
        "and update Project_Roadmap_v1.md or .harness/roadmap_status.md.",
        file=sys.stderr,
    )

sys.exit(0)
