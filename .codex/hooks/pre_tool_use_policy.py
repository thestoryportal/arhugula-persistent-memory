#!/usr/bin/env python3
"""Codex PreToolUse hook — enforce the load-bearing LAWs. Exit 2 = BLOCK; stderr WARN + exit 0 = allow.
Best-effort: stdin is treated as JSON; all string values are scanned."""
from __future__ import annotations
import json, re, sys
from typing import Any

def strings(v: Any):
    if isinstance(v, str): return [v]
    if isinstance(v, dict): return [s for k, i in v.items() for s in strings(k) + strings(i)]
    if isinstance(v, list): return [s for i in v for s in strings(i)]
    return []

raw = sys.stdin.read()
try: payload = json.loads(raw) if raw.strip() else {}
except json.JSONDecodeError: payload = raw
j = "\n".join(strings(payload))

# LAW: the MEMIT engine is UNMODIFIED on the science path
if re.search(r"memit_dry_run/memit/\S+\.(py|json)", j) and re.search(r">|>>|sed -i|\btee\b|\b(apply_patch|Edit|Write)\b", j):
    print("BLOCKED (LAW): memit_dry_run/memit is the UNMODIFIED engine on the science path. A harness-side change requires a LAW#5 inertness proof + one-fix-then-halt — do not edit the engine in-line.", file=sys.stderr)
    sys.exit(2)

# LAW: never overwrite locked evidence / canonical results
if re.search(r"(CORPUS/\S+\.md|results/\S+_result\.json|\S+_state_ledger\.jsonl|reproducibility_manifest\S*\.json)", j) \
   and re.search(r">(?!=)|>>|\brm\b|sed -i|\"(Write|Edit)\"", j):
    print("BLOCKED (LAW): CORPUS/* and results/*_result.json / *_state_ledger.jsonl / reproducibility_manifest* are append-only / never-overwrite. New finding = next CORPUS/NN; namespace new results (RESULT_TAG).", file=sys.stderr)
    sys.exit(2)

# destructive
if re.search(r"\b(rm\s+-rf|git\s+reset\s+--hard|git\s+checkout\s+--|git\s+clean\s+-[a-zA-Z]*f)\b", j):
    print("BLOCKED: destructive command requires explicit operator direction. In no-HIL autonomy: log the intent and skip, do not run.", file=sys.stderr)
    sys.exit(2)

# WARN (allow): un-namespaced result output → artifact-collision trap
if re.search(r"g6_scale_n_\w*result\.json", j) and "RESULT_TAG" not in j and "_qwen7b" not in j and "_bandsearch" not in j:
    print("WARN: a result write without a model/variant namespace can overwrite a canonical artifact (the artifact-collision trap, memory_mirror/durable-artifact-path-collision.md). Set RESULT_TAG.", file=sys.stderr)

# WARN (allow): Edit on big canonical docs on the network FS (silent-revert trap)
if re.search(r"\"(Edit|apply_patch)\"", j) and re.search(r"\b(EXPERIMENT_RUNBOOK|SESSION_CHECKPOINT|DISCIPLINE)\.md", j):
    print("WARN: editing a large canonical doc on the network FS has shown silent reverts — prefer append/rewrite via shell/python and re-read to confirm persistence.", file=sys.stderr)

sys.exit(0)
