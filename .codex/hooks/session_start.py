#!/usr/bin/env python3
"""Codex SessionStart hook — load posture from the pod/HEAD (not memory) + drift anchor."""
from __future__ import annotations
import os, subprocess, sys
from pathlib import Path

ROOT = Path(os.environ.get("LLMDB_ROOT", Path(__file__).resolve().parents[2]))
print("=== LLM-as-Database — Codex session posture ===")
print("NORTH STAR (F1): prove/falsify that the LLM-as-Database spec is implementable, and deliver the readiness determination. Everything serves F1; falsification-first (truth, not green checkmarks).")
print("DRIFT CHECK before any non-trivial action: does this advance F1 or a live runbook §0.3 falsifier? If not, stop and say why.")
print("Load `DISCIPLINE.md` (north star + context read-triggers + deep-thinking-on-failure + tool/loop thresholds).")
print("Read order: README → EXPERIMENT_RUNBOOK.md §0.3 → SESSION_CHECKPOINT.md. Codex guide: AGENTS.md.")
print("Methodology skills installed: experiment-gate, methodology-superpowers, scientific-critical-thinking, debug-mantra-scrutinize, premortem-the-fool, scientific-problem-selection.")
print("Use them at the gate points: problem selection before choosing an arc; critical-thinking/premortem before criteria/verdicts; debug-mantra on failures; verification-before-completion before done.")
print("Advisor route for Codex-led science: Claude out-of-family via tools/claude_advisor.sh (claude.ai Max subscription; no API key).")

guard = ROOT / "tools/codex_context_guard.py"
if guard.exists():
    p = subprocess.run([sys.executable, str(guard), "preflight"], cwd=ROOT, capture_output=True, text=True)
    sys.stdout.write(p.stdout)
    if p.returncode != 0:          # NOT-READY (hard finding) propagates as a hook failure
        sys.stderr.write(p.stderr)
        sys.exit(p.returncode)
sys.exit(0)
