#!/usr/bin/env python3
"""Codex PermissionRequest hook — advisory review of sensitive requests (exit 0, prints note)."""
from __future__ import annotations
import json, re, sys
from typing import Any

PATTERNS = [
    ("PAID-PROVIDER call (GATED — needs a pre-authorized key)",
     re.compile(r"\b(PERPLEXITY_API_KEY|OPENAI_API_KEY|ANTHROPIC_API_KEY|perplexity_(ask|search|research|reason))\b", re.I)),
    ("CREDENTIAL / auth move (GATED)",
     re.compile(r"\b(NOTEBOOKLM_AUTH_JSON|HF_TOKEN|\.hf_token|notebooklm\s+login|gh\s+auth|keychain|secret|credential|auth\.json|\.env)\b", re.I)),
    ("DESTRUCTIVE",
     re.compile(r"\b(rm\s+-rf|git\s+reset\s+--hard|git\s+push\s+--force)\b", re.I)),
    ("NETWORK / install",
     re.compile(r"\b(pip\s+install|uv\s+(add|sync|run)|npm\s+i|npx\b|curl|wget|git\s+push|gh\s+pr)\b", re.I)),
    ("MODEL PULL / heavy compute (standing-auth: PRE-APPROVED)",
     re.compile(r"\b(from_pretrained|snapshot_download|hf_hub_download|get_cov|covariance|llama-quantize|gguf)\b", re.I)),
]

def strings(v: Any):
    if isinstance(v, str): return [v]
    if isinstance(v, dict): return [s for k, i in v.items() for s in strings(k) + strings(i)]
    if isinstance(v, list): return [s for i in v for s in strings(i)]
    return []

raw = sys.stdin.read()
try: payload = json.loads(raw) if raw.strip() else {}
except json.JSONDecodeError: payload = raw
hits = [label for label, pat in PATTERNS if pat.search("\n".join(strings(payload)))]

if hits:
    print("Codex permission posture — touches: " + "; ".join(hits) + ".\n"
          "Standing-auth (DISCIPLINE §3 / [[standing-auth-forward-requirements]]): MODEL PULLS + COVARIANCE COMPUTE + DISK/DOWNLOADS are PRE-APPROVED. "
          "PAID-PROVIDER calls and CREDENTIAL/AUTH moves are GATED — they require a key/secret already authorized in the environment. "
          "In no-HIL autonomy: build to the gate, LOG it to logs/autonomy_gates.jsonl, and proceed to the next unit — do NOT block the whole run.",
          file=sys.stderr)
sys.exit(0)
