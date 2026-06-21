# PROGRESS — the cumulative build toward F1 (the twin of the north star)

> **This file is the equal-and-opposite of the goal.** `DISCIPLINE.md` §0 says *where we are going*
> (F1). This says *how far we have built toward it and what each result enables next*, so every
> loop's work is **additive** — it stands on the proven base and moves one F1 gap closer, never an
> isolated finding and never a re-run of settled ground.
> **Single source of truth = `CORPUS/00`+`03` + runbook §0.3/§12.** This is the distilled, injectable
> head; on any conflict the CORPUS ledger wins. Kept current via the §0.4 additive-update rule (bottom).

## The goal it converges on
**F1 — prove/falsify the "LLM-as-Database" spec is implementable *before* it's built, and deliver the
ready/not-ready-with-conditions determination.** Falsification-first. Everything below is scored by:
*does it move F1 closer?*

## How to read this (the additive contract)
- Each item is a **node F1 requires.** Edges = **"builds on."**
- **Work is valuable only if ADDITIVE:** it builds on a `PROVEN` node and advances a `PARTIAL`/`OPEN`
  F1 criterion. Orthogonal, redundant, or regressive work is drift — the auditor rejects it even if
  internally correct.
- **Do NOT re-run a `PROVEN-FOR-SCOPE` node.** If tempted, cite the Decision-ID that closed it and
  state what *new* F1 gap your run opens. If you can't, it's redundant — skip it.
- Status ∈ `PROVEN-FOR-SCOPE · PARTIAL · OPEN · FALSIFIED/PRUNED`. "FOR-SCOPE" = proven within a named
  scope (model/N/regime); pushing the scope is itself additive work.

---

## ① FOUNDATION — PROVEN-FOR-SCOPE (locked; build ON these, do not re-run)
| Node | What it locks | Scope | Evidence |
|---|---|---|---|
| **Edit mechanics** | in-weight multi-field editing viable | model/size-dependent (GPT-J ✗; Qwen2.5-7B/3B, Qwen3-0.6B ✓) | CORPUS/00 P1, C1 |
| **Recipe** | in-solve AlphaEdit (null-space P, thresh **0.005**) + preserve-sampling + batched-per-record compile | Qwen2.5-3B, N≤100 | CORPUS/00 R-*, D-S243-* |
| **CP1** governed in-pipeline write | parametric MEMIT write under governance | for-scope | CORPUS/07, D-CP1 |
| **CP3** MEMIT compliance | D12 method-class = D20 null-space mandated | C15 layer-band = open divergence | CORPUS/09 |
| **G1** consistency | dual-medium 2PC + State Ledger + Txn Controller + circuit breaker (10/10) | for-scope | CORPUS/10 |
| **G2** security | real Ed25519 verify-cannot-forge + overlay integrity + CAK ceremony (9/9) | for-scope | CORPUS/11 |
| **G3** validation pipeline | deterministic schema validator: violates/undeclared reject + storage-probe split (8/8) | for-scope | CORPUS/12 |
| **A1** batch eliminates corruption | batch/Genesis joint solve → cross-entity corruption GONE (100→100% @N≤100) | resolves G6.1 write-path; 3B N≤100 | CORPUS/14, D-A1 |
| **B3 / G6.2** quantization survival | the A1-clean store survives **real Q4_K_M** (edits 100% vs native 97.4%) | margin-confound characterized | CORPUS/17 |
| **E1 (Claim A)** CPU deployment loop | serves edited store on CPU via **llama.cpp + Q4_K_M** (~8–13 tok/s) | pod-CPU proxy | CORPUS/18, D-E1-1 ⟨D-E1-1@55708623⟩ |

## ② THE ADDITIVE CHAINS (how the proofs stack toward F1)
**CHAIN A — DEPLOYMENT DATA PATH (the spine):**
`recipe` ✅ → `G6.1` exposes cross-entity scale falsifier → **`A1`** eliminates it ✅ → **`B3`** survives
Q4_K_M ✅ → **`E1·A`** serves on CPU ✅ → **`D1` capacity law `[OPEN — REQUIRED for F1]`** → F1 deployment-readiness.

**CHAIN B — GOVERNANCE / CONTRACT SUBSTRATE:**
`CP1` ✅ + `CP3` ✅ + `G1` ✅ + `G2` ✅ + `G3` ✅ → **`CP2` query-schema build-items `[PARTIAL]`** → F1 contract-readiness.

**CHAIN C — WRITE ROBUSTNESS / SCALE MECHANISM:**
`recipe`+`G6.1`+`C2` mechanism (key-collinearity U-shaped, min **L8-12**) → **`C2-band` `[OPEN, lead]`** &
**`C/G7` multi-token value robustness `[OPEN]`** → feed `D1` & F1 write-robustness.

## ③ THE ADDITIVE FRONTIER (open nodes whose prerequisites are PROVEN — the ONLY work worth doing)
| Open F1 gap | builds on (proven) | the additive step | moves F1 | priority |
|---|---|---|---|---|
| **D1 capacity law** | A1, B3, E1·A | measure N-before-break (corruption + quantization) → the number a ready/not-ready call needs | deployment-readiness **(REQUIRED)** | ★ critical path |
| **D1 — structural** ✅ DONE | G6.1, A1 | drift = per-relation concentration not global edge-count; **REPLICATES on Qwen2.5-7B (model-general, B1/D-B1-2 ⟨D-B1-2@0db8d819⟩)** → §8.7 amendment written | OQ-W1 reconciliation | DONE (D-D1-1 ⟨D-D1-1@0db8d819⟩+D-B1-2) |
| **D1 — numeric threshold** ⚠️ OPEN | D1-structural | set the per-relation WARNING/HARD value | the readiness number | **DONE (D-D1-2 ⟨D-D1-2@e023d8d2⟩): k≤1 conservative (order-cluster-bootstrap + ≥2 held-out seeds + determinism); mixed-load→pair with global-volume bound; cross-model transfer OPEN** |
| **CP2 schema build-items** | CP2, G3 | L1 triple-readback + 5 query families + violates-rejection | contract-readiness | ★ required |
| **C2-band** | G6.1, C2 mechanism | does min-collinearity band [8-12] reduce **sequential** corruption? (falsifier) | scale mechanism → feeds D1 | ◆ lead — ⚠️ **REAL-BUT-UNDERPOWERED, NOT PROMOTED** (CORPUS/21, D-C2band-1 ⟨D-C2band-1@c6fb6103⟩): mechanical PASS (+18.73pp cross-JS) = real redistribution (within-loc FALL + expr 100% exclude under-editing); underpowered (1 seed), within-entity top-1 cost & mechanism unmeasured; de-confounders queued |
| **C/G7 multi-token** | recipe | multi-token value robustness at the write | write-robustness | ◆ |

## ④ FALSIFIED / PRUNED (do NOT pursue — dead ground)
- **E1 Claim B:** LARQL `gguf-to-vindex` serving **Qwen2.5** — drops 108 attn biases (A7 causal ablation) → garbage. Use **Qwen3 family** or **llama.cpp**. [CORPUS/18]
- **relation-keying** — pruned (C2). [CORPUS/20]
- **A2b K_S staleness** — ruled out (large drift, zero benefit) → only revisit via A3/BetaEdit port. [CORPUS/16]
- **sequential incremental `cache_c` path** for deployment — A1 batch supersedes it (D-SCOPE-1). [CORPUS/14]

## ⑤ DISTANCE TO F1 (the readiness scorecard)

<!-- BEGIN GENERATED:f1-scorecard -->
**F1 READINESS SCORECARD (updated 2026-06-21 (B3N close))** — _auto-generated from `docs/program_state.json` — DO NOT edit between the markers; run `python3 tools/render_state.py --write`._

- **Deployment data path:** recipe ✅ → A1 batch-clean ✅ → B3 Q4_K_M-survival ✅ → E1·A CPU-serve ✅ → D1 structural ✅ (model-general) + numeric k≤1 SET on 3B ⚠️ (cross-model transfer OPEN)
- **Governance:** CP1 ✅ · CP3 ✅ · G1 ✅ · G2 ✅ · G3 ✅ · CP2 ⚠️ (query-schema build-items OPEN — critical path)
- **Robustness:** C/G7 multi-token ❌ · C2-band ⚠️ (real-but-underpowered, not promoted)
- **Critical path:** B3 in-weight-necessity + CP2 schema build-items + D1 numeric cross-model transfer → then write F1
- **Verdict:** NOT delivered. Deployment data-path spine PROVEN-FOR-SCOPE (recipe→A1 batch-clean→B3 Q4_K_M→E1·A CPU-serve; 3B / N≤100). B3 architecture decision TAKEN + SPEC-GROUNDED (D-B3N-1): the spec's write model (§8.3/§8.7/§8.10) is a COMPACTION-BOUNDED HYBRID; in-weight viable for it under 3 conditions — (1) concentration-aware §8.7 (our k≤1 amendment); (2) compaction cadence; (3) ⚠ compaction-at-scale cleanliness (N≥2,000 sub-batched) = UNTESTED, the sharpest open falsifier. Side-store only for high-churn-online or if (3) fails. Remaining blocks: compaction-at-scale test (condition 3) + CP2 (contract) + 7B numeric transfer (OQ-W1, condition 1) + the §1.1 open dims.
<!-- END GENERATED:f1-scorecard -->
- **Governance contracts:** CP1 ✅ · CP3 ✅(C15 open) · G1 ✅ · G2 ✅ · G3 ✅ · **CP2 ⚠️ build-items**
- **Deployment data path:** recipe ✅ → A1 ✅ → B3 ✅ → E1·A ✅ · **D1: structural ✅ (§8.7 amendment, model-general — D1+B1) · numeric guardrail ✅ SET (D-D1-2: k≤1 conservative; order/held-out-dominated; mixed-load→needs global-volume bound) · cross-model transfer ⚠️ OPEN (7B via determinism)**
- **Robustness:** C/G7 ❌ · C2-band ⚠️ REAL-BUT-UNDERPOWERED (CORPUS/21: mechanical PASS = real redistribution, not promoted — 1 seed + cost/mechanism unmeasured) ❌(lead)
- **CRITICAL PATH to a defensible determination:** **B3 in-weight-vs-side-store decision** (highest-stakes, graph-convergence) + **CP2 schema build-items** + **D1 numeric cross-model transfer** (3B guardrail k≤1 DONE; 7B OPEN).
  Everything else is either locked (don't re-run) or feeds these two.

---

## §0.4 ADDITIVE-UPDATE RULE (binding — how a new result enters here)
Every new result MUST attach to this map by declaring, in its CORPUS write **and** its staged finding:
1. **builds-on:** which PROVEN node(s) it stands on (or "new foundation" + why).
2. **advances:** which F1 criterion/chain it moves, and the **status delta** (e.g. `D1: OPEN→PARTIAL`).
3. **evidence:** CORPUS/NN + Decision-ID.
4. **additivity check:** if it neither builds on the proven base nor moves an F1 gap, it is **drift or
   redundancy** — the twin auditor (DISCIPLINE §3.2) rejects it regardless of internal correctness.

Then move the node between ①/③/④ and update ⑤. Re-mirror to memory. A run that does not change this
map's distance-to-F1 produced no F1 progress, however many numbers it generated.


### D-D1-2 — §8.7 numeric-threshold instrument (2026-06-21) [F1 numeric-threshold sub-item CLOSED on 3B; cross-model transfer OPEN]
**D-D1-2** (2026-06-21): §8.7 numeric-threshold instrument → **operational guardrail `k≤1`** (max unanchored per-relation concentration; anchor by k=2; WARNING k=2-3, HARD k=8-10 — REVISED down from k≤2 after the seed-2 across-held-out check). Dual-reviewed (Opus advisor + gpt-5.5 cross-family). k=3-4/k=10-12 = scoped order-dominated observations, NOT portable thresholds; per-relation count = fail-closed SENTINEL not the causal var (edit-set/key-collinearity geometry is). 3B-only (size transfer OPEN), pure-capital anti-conservative, incremental-path-only (deploy=batch/Genesis A1-clean). Instrument: 3B within-process SD=0; ~50pp noise is 7B/across-process; binding 3B uncertainty = edit-ORDER. Artifacts: results/d1_threshold_lowk_3b_s3{,_lowextra}.json, results/d1_instrument_variance_diagnostic_3b_*.json; reviews logs/codex_review_threshold_*OUT.log. **MIXED-LOAD:** pure-capital fails under +12 other-relation load (mixed clean ceiling k=0; driver=other-relation volume) → vindicates the worse-of(global,per-relation) amendment design; pair k≤1 with a global-volume bound + compaction. **SEED-2 (more-toxic held-out):** corrupts at k=1-2 where seed-3 was clean → ceiling k≤2→k≤1; no per-relation count is universally clean (held-out-dependent SENTINEL, not the causal var). +results/d1_mixedload_smoke_3b_s3.json, results/d1_threshold_lowk_3b_s2.json.
