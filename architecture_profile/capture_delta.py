#!/usr/bin/env python3
"""
Delta Token-ID Capture — Session 2.5 (Workstream 1)

Purpose:
    Capture revised probe prompts after Section 3 retrospective surfaced
    weak-signal top-1s in 6 critical Stage 1 probes + 2 shared-specificity
    probes. Per D-S25-2 / D-S25-3 / D-S25-4.

Closes:
    - OQ-PROBE-3 (multi-token expected output edge cases) — extends the
      original capture
    - Operator-deferred revisions ratified in this session

Output:
    /workspace/architecture_profile/token-id-capture-results-delta.json
    (Merge with original token-id-capture-results.json downstream)

Wall time: ~1-2 min (model load on warm HF cache + ~10 forward passes).
"""

import json
import os
import sys
from datetime import datetime, timezone

import torch
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "EleutherAI/gpt-j-6B"
MODEL_REVISION = "float16"
OUTPUT_PATH = "/workspace/architecture_profile/token-id-capture-results-delta.json"

# Revised prompts. Multiple candidates per shared-spec slot for empirical
# selection; single candidate per per-fact slot.
REVISED_PROBES = [
    # Shared-specificity (corpus-wide, load-bearing) — multiple candidates
    {"slot": "p-shared-spec-1", "candidate": "A", "prompt": "The capital of France is the city of",        "expected": "Paris"},
    {"slot": "p-shared-spec-1", "candidate": "B", "prompt": "Paris is the capital of",                     "expected": "France"},
    {"slot": "p-shared-spec-1", "candidate": "C", "prompt": "The capital city of France is",               "expected": "Paris"},
    {"slot": "p-shared-spec-2", "candidate": "A", "prompt": "The largest planet by mass is",               "expected": "Jupiter"},
    {"slot": "p-shared-spec-2", "candidate": "B", "prompt": "Among the planets in our solar system, the largest is", "expected": "Jupiter"},
    {"slot": "p-shared-spec-2", "candidate": "C", "prompt": "The biggest planet in our solar system is",   "expected": "Jupiter"},

    # Per-fact gen probes (Stage 1 critical) — single candidate each
    {"slot": "p-cfb-001-gen-2", "candidate": "A", "prompt": "Michael Jordan wore jersey number",           "expected": "23"},
    {"slot": "p-cfb-002-gen-2", "candidate": "A", "prompt": "Tom Brady wore jersey number",                "expected": "12"},
    {"slot": "p-cfb-003-gen-2", "candidate": "A", "prompt": "Wayne Gretzky wore jersey number",            "expected": "99"},
    {"slot": "p-cfb-002-gen-3", "candidate": "A", "prompt": "Tom Brady was drafted by the",                "expected": "New"},
    {"slot": "p-cfb-003-gen-3", "candidate": "A", "prompt": "Wayne Gretzky's home country is",             "expected": "Canada"},

    # cfb-004 paired re-captures (same prompts as cfb-002, since both
    # subjects are Tom Brady; results inherit from cfb-002 captures)
    # Logged as alias references, not separate captures
]


def get_top_k(model, tokenizer, prompt, k=5, device="cuda"):
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    final_logits = outputs.logits[0, -1, :]
    probs = torch.softmax(final_logits.float(), dim=-1)
    topk = torch.topk(probs, k=k)
    return {
        "ids":    topk.indices.cpu().tolist(),
        "tokens": [tokenizer.decode([t]) for t in topk.indices.cpu().tolist()],
        "probs":  topk.values.cpu().tolist(),
    }


def main():
    print("=" * 70, flush=True)
    print("Delta Token-ID Capture — Session 2.5", flush=True)
    print("=" * 70, flush=True)

    print("\n[1/3] Loading tokenizer + model (warm HF cache)...", flush=True)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, revision=MODEL_REVISION)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        revision=MODEL_REVISION,
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True,
    ).to("cuda")
    model.eval()
    print(f"      GPU memory: {torch.cuda.memory_allocated() / 1e9:.2f} GB", flush=True)

    # ---- Run captures ----
    print("\n[2/3] Capturing revised probe prompts", flush=True)
    print("-" * 70, flush=True)

    results = []
    by_slot = {}
    for r in REVISED_PROBES:
        top5 = get_top_k(model, tokenizer, r["prompt"], k=5)
        record = {
            "slot": r["slot"],
            "candidate": r["candidate"],
            "prompt": r["prompt"],
            "predicted_target": r["expected"],
            "top_1_token": top5["tokens"][0],
            "top_1_token_id": top5["ids"][0],
            "top_1_prob": top5["probs"][0],
            "top_5_tokens": top5["tokens"],
            "top_5_token_ids": top5["ids"],
            "top_5_probs": top5["probs"],
            "expected_match": top5["tokens"][0].strip() == r["expected"],
        }
        results.append(record)
        by_slot.setdefault(r["slot"], []).append(record)
        match_marker = "✓" if record["expected_match"] else "✗"
        print(f"  {r['slot']:<22} ({r['candidate']}) -> '{top5['tokens'][0]}' "
              f"(p={top5['probs'][0]:.4f}) [predicted '{r['expected']}' {match_marker}]",
              flush=True)
        print(f"    top-5: {list(zip(top5['tokens'], [f'{p:.3f}' for p in top5['probs']]))}",
              flush=True)

    # ---- Auto-select best candidate per slot ----
    print("\n[3/3] Auto-selecting strongest candidate per slot", flush=True)
    print("-" * 70, flush=True)

    selections = {}
    for slot, candidates in by_slot.items():
        # Prefer expected_match; among matches pick highest p; if no match
        # pick highest p anyway and flag for operator review
        matches = [c for c in candidates if c["expected_match"]]
        if matches:
            best = max(matches, key=lambda c: c["top_1_prob"])
            selections[slot] = {
                "selected_candidate": best["candidate"],
                "selected_prompt": best["prompt"],
                "top_1_token": best["top_1_token"],
                "top_1_token_id": best["top_1_token_id"],
                "top_1_prob": best["top_1_prob"],
                "top_5": {"tokens": best["top_5_tokens"],
                          "ids": best["top_5_token_ids"],
                          "probs": best["top_5_probs"]},
                "selection_reason": "expected_match + highest_prob_among_matches",
                "operator_review_required": False,
            }
        else:
            best = max(candidates, key=lambda c: c["top_1_prob"])
            selections[slot] = {
                "selected_candidate": best["candidate"],
                "selected_prompt": best["prompt"],
                "top_1_token": best["top_1_token"],
                "top_1_token_id": best["top_1_token_id"],
                "top_1_prob": best["top_1_prob"],
                "top_5": {"tokens": best["top_5_tokens"],
                          "ids": best["top_5_token_ids"],
                          "probs": best["top_5_probs"]},
                "selection_reason": "no_match_fallback_highest_prob",
                "operator_review_required": True,
            }
        print(f"  {slot:<22} -> '{selections[slot]['top_1_token']}' "
              f"(p={selections[slot]['top_1_prob']:.4f}) "
              f"[{selections[slot]['selection_reason']}]", flush=True)

    # ---- Output ----
    output = {
        "capture_version": "1.0-delta",
        "capture_timestamp": datetime.now(timezone.utc).isoformat(),
        "model": MODEL_NAME,
        "model_revision": MODEL_REVISION,
        "supersedes_in_original": list(by_slot.keys()),
        "all_candidates": results,
        "selections": selections,
        "alias_inheritance": {
            "p-cfb-004-gen-2": "p-cfb-002-gen-2 (same prompt 'Tom Brady wore jersey number'; both gen-2 probes share Tom Brady subject)",
            "p-cfb-004-gen-3": "p-cfb-002-gen-3 (same prompt 'Tom Brady was drafted by the'; both gen-3 probes share Tom Brady subject)",
        },
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print("\n" + "=" * 70, flush=True)
    print(f"DELTA CAPTURE COMPLETE", flush=True)
    print("=" * 70, flush=True)
    print(f"  Output: {OUTPUT_PATH}", flush=True)
    needs_review = [s for s, v in selections.items() if v["operator_review_required"]]
    if needs_review:
        print(f"  ⚠ Slots requiring operator review: {needs_review}", flush=True)
    else:
        print(f"  All slots auto-selected with expected match.", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n!!! FATAL: {type(e).__name__}: {e}", file=sys.stderr, flush=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)
