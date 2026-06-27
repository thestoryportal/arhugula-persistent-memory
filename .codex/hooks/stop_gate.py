#!/usr/bin/env python3
"""Codex Stop hook — closeout posture (verification + §0.4 obligations) without claiming success."""
from __future__ import annotations
import json, os, subprocess, sys
from pathlib import Path

ROOT = Path(os.environ.get("LLMDB_ROOT", Path(__file__).resolve().parents[2]))

def run(args):
    try: return subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=60).stdout.strip()
    except Exception as e: return f"<{e}>"

guard = ROOT / "tools/codex_context_guard.py"
closeout = run([sys.executable, str(guard), "closeout"]) if guard.exists() else ""
status = run(["git", "status", "--short", "--branch"])

msg = "\n".join([
    "=== Codex STOP posture ===",
    status or "<git status unavailable>",
    closeout,
    "Before claiming completion: report the EXACT verification commands + their results; do NOT claim success without them.",
    "Methodology gates: use experiment-gate for evidence packages; scientific-critical-thinking/premortem before verdicts; debug-mantra-scrutinize on failures; scientific-problem-selection before choosing or reframing a science arc.",
    "For evidence-bearing work: ensure tools/experiment_gate.py bundle <D-ID> exists or explicitly state why the gate is not applicable.",
    "If an experiment ran UNATTENDED (no-HIL autonomy): write the finding to logs/pending_findings/NN_<unit>.md (STAGING) — do NOT author CORPUS/NN or edit the append-only ledger/runbook/checkpoint. The operator folds staged findings into the canonical §0.4 record on review.",
    "If an experiment ran in a SUPERVISED session: complete the full §0.4 close-out (CORPUS/NN + 00/03 + runbook §0.3/§12/§13 + checkpoint + memory). A clean HALT with a diagnostic is SUCCESS.",
])
print(json.dumps({"continue": True, "systemMessage": msg}, separators=(",", ":")))
sys.exit(0)
