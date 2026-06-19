# 07 — CP1: GOVERNED, IN-PIPELINE MEMIT WRITE (viability prototype — result)
_Run 2026-06-18 on the pod (RTX 4090). Artifact: `/workspace/experiments/governance/cp1_governed_write.py`; result `/workspace/results/cp1_result.json`; ledger `/workspace/results/cp1_state_ledger.jsonl`; run log `/workspace/logs/cp1_run.log`. Engine UNMODIFIED; all governance is our-own-code wrapping the validated recipe._

## The CP1 question (from 03/06)
We had proven the edit MATH + OFFLINE serving + the decoupled bridge (A1–A5, L-BRIDGE), but NOT a MEMIT
compile running as a **first-class, in-pipeline step** behind a Patch Authorization Gate / Commit Executor
with ledger entries, that **fails cleanly**. The spec wants exactly this (§9.10, §10.2, §11.5); it eliminated
n8n (D70) for not hosting "multi-minute GPU-bound MEMIT compile as a first-class step." Our earlier bridge ran
the compile OUT-OF-BAND — as a production path that is a C16 violation. CP1 closes that gap.

## Scope (operator decision, legible)
**PARAMETRIC-ONLY.** CP1 gates+commits the `.vindex` (parametric) write and proves clean-fail atomicity on
that side. The Commit Executor's defining **dual-medium** property (§9.10 simultaneous Git+engine write; §11.5
D46 Git-first ordering; Transaction Controller; compensation) is represented only as a STRUCTURAL PLACEHOLDER
(`git_prepare` no-op) and is **DEFERRED TO G1**. CP1 must NOT be read as proving dual-medium 2PC.

## Method (what the prototype is)
A single deterministic, non-reasoning pipeline (no LLM in the loop, C-OR2):
`StateLedger` (append-only, hash-chained, §11.15) · `Orchestrator` (single-use Orchestrator-signed tokens,
§10.4 — HMAC stub for the asymmetric key) · `PatchAuthorizationGate` (§10.2 pre-checks + core checks) ·
`RecipeEngine` (loads Qwen3-0.6B once; null-space projector P from CACHED covariances = D20 orthogonal
projection; in-solve AlphaEdit band [4–8]) · `CommitExecutor` (PREPARE → [git placeholder] → **in-step GPU
compile** → package `.vlp` → APPLY+COMPILE on the frozen base `/dev/shm/qwen3.vindex` → post-write probe →
COMMITTED). Five tests, all sharing one model load; negative tests use distinct edits (unique patch_hash).

## Measurement → criterion → verdict (all PASS; `cp1_result.json`)
| Test | Falsifiable criterion (set BEFORE) | Measured | Verdict |
|---|---|---|---|
| **T-POS** | authorized patch → in-step compile → overlay mounted → post-write probe → PREPARED+COMMITTED | COMMITTED; probe `"Berlin."` ✓ (expect Berlin); compile **1.1s**; **15360** down-overrides; overlay_hash `d364a337…` | **PASS** |
| **T-GATE** | bad-sig / tampered-hash / out-of-scope / replay / expired → HARD reject, NO compile, NO COMMITTED | 5/5 rejected: `TOKEN_SIGNATURE_INVALID`, `INTEGRITY_HASH_MISMATCH`, `SCOPE_RELATION_FORBIDDEN`, `TOKEN_REPLAY`, `TOKEN_EXPIRED`; none committed | **PASS** |
| **T-ATOM** | compile throws mid-step → PREPARED stays, NO COMMITTED, frozen base bytes unchanged | mid_compile + mid_mount: both `FAILED`, PREPARED present, **no** COMMITTED, base checksum unchanged; `WRITE_FAILED` forensic entry | **PASS** |
| **T-DET** | same patch twice → identical overlay hash; no LLM in loop | identical overlay hash within process | **PASS** (governance sense; see caveat) |
| **LEDGER** | hash-chain intact across all events | 19 entries, chain intact (1 KEY_ANCHOR · 5 TOKEN_CONSUMED · 4 PREPARED · 2 COMMITTED · 5 WRITE_REJECTED · 2 WRITE_FAILED) | **PASS** |

## What CP1 PROVES (precise)
- A **deterministic non-reasoning executor hosts the GPU MEMIT compile in-process as a blocking first-class
  step**, emits PREPARED/COMMITTED to a hash-chained ledger, and **fails cleanly** (PREPARED-without-COMMITTED,
  frozen base untouched) when the GPU step throws. This is the **execution-model fit** the spec required and
  n8n (D70) lacked.
- The **Patch Authorization Gate enforces all five §10.2 checks tested** (signature, integrity/patch-hash,
  scope/relation, single-use replay, TTL expiry) as HARD rejections that never reach the engine — closing the
  C16 "out-of-band bridge = security violation" gap by routing the same validated recipe THROUGH the Gate.
- The edit serves correctly post-commit (France→Berlin), consistent with L-BRIDGE.

## CAVEATS / honest scope (do not overclaim)
- **n8n / duration:** execution-MODEL fit proven; the compile here was single-fact ~1s. Multi-minute / batch
  compile DURATION + scale = **G6**, NOT validated here.
- **Determinism:** governance sense (C-OR2: non-reasoning, no LLM, in-process repeatable) HOLDS (T-DET
  bit-identical within a process). **Cross-process overlay bytes are NOT bit-reproducible** (GPU FP; root cause
  = non-deterministic memory-efficient-attention backward inside `compute_z`; confirmed `warn_only` deterministic
  mode does not fix it). This is **not a C-OR2 requirement** — spec compaction (§8.10) is itself a full MEMIT
  re-run verified BEHAVIORALLY (COMPACTION_REGRESSION), not by hash; the ledger `overlay_hash` anchors
  STORED-artifact integrity, not recompile-reproducibility. Eager-attention fix deliberately NOT applied
  (engine-adjacent; solves a non-requirement).
- **Post-write probe:** BEHAVIORAL (L2-class, `larql run`) standing in for the mandatory **L1 SELECT** storage
  read-back (§8.9) — pending **CP2** query-schema capability.
- **Stubs (flagged):** Orchestrator signing = HMAC (symmetric) for the asymmetric key (§10.5 → G2);
  `git_prepare` = no-op (G1); `mid_mount` fault = SYNTHETIC (raises before the subprocess, tests
  exception→no-commit cleanup, not a real partial mount); C16 "Gate is sole path" holds by HARNESS
  CONSTRUCTION, not structural enforcement; `frozen_base_unchanged` = base is a read-only input, NOT a
  2PC-atomicity proof (that is G1).

## Net
CP1 is **PROVEN for its scope**: governed, in-pipeline, parametric MEMIT write with gate-reject and clean-fail
atomicity, deterministic in the governance sense. Dual-medium 2PC, real L1 SELECT probe, asymmetric signing,
and batch-scale duration are explicitly carried forward to G1 / CP2 / G2 / G6.
