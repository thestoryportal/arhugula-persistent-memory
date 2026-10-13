#!/usr/bin/env python3
"""Session-start posture reminder for Codex."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def exists(path: str) -> str:
    return "present" if (ROOT / path).exists() else "missing"


def run_guard() -> str:
    script = ROOT / "tools/codex_context_guard.py"
    if not script.exists():
        raise SystemExit("<codex context guard missing>")
    try:
        proc = subprocess.run(
            ["/usr/bin/python3", str(script), "preflight"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=75,
        )
    except Exception as exc:  # pragma: no cover - hook defensive path
        raise SystemExit(f"<codex context guard unavailable: {exc}>") from exc
    output = (
        proc.stdout.strip() or proc.stderr.strip() or "<codex context guard produced no output>"
    )
    if proc.returncode != 0:
        print(output)
        sys.exit(proc.returncode)
    return output


print("Codex project posture for arhugula-v2:")
print("- Read AGENTS.md first; consult CLAUDE.md only for targeted canonical lineage.")
print(f"- Roadmap status: .harness/roadmap_status.md is {exists('.harness/roadmap_status.md')}.")
print(f"- justfile is {exists('justfile')}; prefer just recipes for repo gates.")
print("- Use isolated worktrees for substantive edits and keep PRs reviewable.")
print("- Do not mix design-substrate edits with implementation without explicit back-flow scope.")
print("- Deterministic context workflow: .codex/notes/deterministic-context-workflow.md.")
print(run_guard())
